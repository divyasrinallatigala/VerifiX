"""
rules_engine.py - Deterministic rules engine for invoice validation
"""
from typing import List, Optional
from project_types import ExtractedData, AuditFlag, RiskLevel
from config import Config

class RulesEngine:
    """Engine for running deterministic validation rules on invoices"""
    
    def __init__(self):
        """Initialize the rules engine"""
        self.rules = [
            self._check_vendor_mismatch,
            self._check_amount_exceeds_po,
            self._check_missing_gst,
            self._check_tax_calculation,
            self._check_missing_po_reference,
            self._check_date_validity,
            self._check_line_items_match,
            self._check_extracted_anomalies
        ]
    
    def validate(
        self, 
        invoice: ExtractedData, 
        po: Optional[ExtractedData] = None,
        matching_service: Optional['MatchingService'] = None
    ) -> List[AuditFlag]:
        """
        Run all validation rules on the invoice
        
        Args:
            invoice: Invoice to validate
            po: Reference PO (optional)
        
        Returns:
            List of audit flags for violations found
        """
        flags = []
        
        for rule in self.rules:
            if rule == self._check_vendor_mismatch:
                result = rule(invoice, po, matching_service)
            else:
                result = rule(invoice, po)
            if isinstance(result, list):
                flags.extend(result)
            elif result:
                flags.append(result)
        
        return flags
    
    def _check_extracted_anomalies(
        self, 
        invoice: ExtractedData, 
        po: Optional[ExtractedData]
    ) -> List[AuditFlag]:
        """Rule R-STR-008: Incorporate deep-audit structural anomalies found during extraction"""
        if not invoice.anomalies:
            return []
            
        flags = []
        for i, anomaly in enumerate(invoice.anomalies):
            flags.append(AuditFlag(
                id=f"R-STR-008-{i}",
                rule="Structural Anomaly",
                severity=RiskLevel.HIGH if "mathematical" in anomaly.lower() or "suspicious" in anomaly.lower() else RiskLevel.MEDIUM,
                description=anomaly,
                field="document"
            ))
            
        return flags
    
    def _check_vendor_mismatch(
        self, 
        invoice: ExtractedData, 
        po: Optional[ExtractedData],
        matching_service: Optional['MatchingService'] = None
    ) -> Optional[AuditFlag]:
        """Rule R-SEM-001: Check vendor name matches PO"""
        if not po:
            return None
        
        is_match = False
        if matching_service:
            is_match = matching_service.is_semantically_equivalent(invoice.vendor, po.vendor)
            if not is_match and invoice.seller:
                is_match = matching_service.is_semantically_equivalent(invoice.seller, po.vendor)
        else:
            is_match = invoice.vendor.lower().strip() == po.vendor.lower().strip()

        if not is_match:
            return AuditFlag(
                id="R-SEM-001",
                rule="Vendor Mismatch",
                severity=RiskLevel.HIGH,
                description=f"Invoice vendor '{invoice.vendor}' does not match PO vendor '{po.vendor}'",
                field="vendor"
            )
        
        return None
    
    def _check_amount_exceeds_po(
        self, 
        invoice: ExtractedData, 
        po: Optional[ExtractedData]
    ) -> Optional[AuditFlag]:
        """Rule R-GST-002: Check invoice amount doesn't exceed PO"""
        if not po:
            return None
        
        max_allowed = po.total_amount * (1 + Config.PO_AMOUNT_TOLERANCE)
        
        if invoice.total_amount > max_allowed:
            excess_percent = ((invoice.total_amount - po.total_amount) / po.total_amount) * 100
            return AuditFlag(
                id="R-GST-002",
                rule="Amount Exceeds PO",
                severity=RiskLevel.HIGH,
                description=f"Invoice amount ₹{invoice.total_amount:,.2f} exceeds PO amount ₹{po.total_amount:,.2f} by {excess_percent:.1f}%",
                field="totalAmount"
            )
        
        return None
    
    def _check_missing_gst(
        self, 
        invoice: ExtractedData, 
        po: Optional[ExtractedData]
    ) -> Optional[AuditFlag]:
        """Rule R-GST-003: Check GST number is present and valid"""
        if not invoice.gst_no or len(invoice.gst_no) < Config.MIN_GST_LENGTH:
            return AuditFlag(
                id="R-GST-003",
                rule="Invalid GST Number",
                severity=RiskLevel.MEDIUM,
                description="GST number is missing or invalid format (must be 15 characters)",
                field="gstNo"
            )
        
        return None
    
    def _check_tax_calculation(
        self, 
        invoice: ExtractedData, 
        po: Optional[ExtractedData]
    ) -> Optional[AuditFlag]:
        """Rule R-FIN-004: Check tax calculation is correct"""
        taxable_amount = invoice.total_amount - invoice.tax_amount
        expected_tax = taxable_amount * Config.GST_RATE
        
        tax_difference = abs(invoice.tax_amount - expected_tax)
        
        if tax_difference > Config.TAX_CALCULATION_TOLERANCE:
            return AuditFlag(
                id="R-FIN-004",
                rule="Tax Calculation Error",
                severity=RiskLevel.MEDIUM,
                description=f"Tax amount ₹{invoice.tax_amount:,.2f} does not match expected ₹{expected_tax:,.2f} (difference: ₹{tax_difference:,.2f})",
                field="taxAmount"
            )
        
        return None
    
    def _check_missing_po_reference(
        self, 
        invoice: ExtractedData, 
        po: Optional[ExtractedData]
    ) -> Optional[AuditFlag]:
        """Rule R-PO-005: Check PO reference exists"""
        if not invoice.po_no:
            return AuditFlag(
                id="R-PO-005",
                rule="Missing PO Reference",
                severity=RiskLevel.HIGH,
                description="Invoice does not reference any Purchase Order",
                field="poNo"
            )
        
        return None
    
    def _check_date_validity(
        self, 
        invoice: ExtractedData, 
        po: Optional[ExtractedData]
    ) -> Optional[AuditFlag]:
        """Rule R-DATE-006: Check invoice date is after PO date"""
        if not po:
            return None
        
        try:
            from datetime import datetime
            invoice_date = datetime.strptime(invoice.date, '%Y-%m-%d')
            po_date = datetime.strptime(po.date, '%Y-%m-%d')
            
            if invoice_date < po_date:
                return AuditFlag(
                    id="R-DATE-006",
                    rule="Invalid Date Sequence",
                    severity=RiskLevel.MEDIUM,
                    description=f"Invoice date ({invoice.date}) is before PO date ({po.date})",
                    field="date"
                )
        except:
            pass  # Skip if date parsing fails
        
        return None
    
    def _check_line_items_match(
        self, 
        invoice: ExtractedData, 
        po: Optional[ExtractedData]
    ) -> Optional[AuditFlag]:
        """Rule R-ITEM-007: Check line items match PO"""
        if not po or not po.line_items:
            return None
        
        # Check if major line items from invoice exist in PO
        unmatched_items = []
        for inv_item in invoice.line_items:
            matched = False
            for po_item in po.line_items:
                if (inv_item.description.lower() in po_item.description.lower() or
                    po_item.description.lower() in inv_item.description.lower()):
                    matched = True
                    break
            
            if not matched:
                unmatched_items.append(inv_item.description)
        
        if unmatched_items and len(unmatched_items) >= len(invoice.line_items) / 2:
            return AuditFlag(
                id="R-ITEM-007",
                rule="Line Items Mismatch",
                severity=RiskLevel.MEDIUM,
                description=f"Multiple line items not found in PO: {', '.join(unmatched_items[:3])}",
                field="lineItems"
            )
        
        return None