"""
matching_service.py - Service for matching invoices with reference PO documents
"""
import json
import google.generativeai as genai
from typing import Optional, Dict
from project_types import ExtractedData, LineItem
from config import Config
from dataclasses import asdict

class MatchingService:
    """Service for finding and generating reference PO documents"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the matching service with Gemini API"""
        self.api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    def find_matching_po(
        self, 
        invoice: ExtractedData, 
        po_repository: Dict[str, ExtractedData]
    ) -> Optional[ExtractedData]:
        """
        Find matching PO from repository
        
        Args:
            invoice: The invoice to match
            po_repository: Dictionary of available POs
        
        Returns:
            Matching PO if found, None otherwise
        """
        if not invoice.po_no:
            return None
        
        return po_repository.get(invoice.po_no)
    
    def generate_reference_po(self, invoice: ExtractedData) -> ExtractedData:
        """
        Generate a realistic reference PO based on invoice context
        
        Args:
            invoice: The invoice to generate a PO for
        
        Returns:
            Generated PO as ExtractedData
        """
        if not self.api_key or self.api_key == 'AQ.Ab8RN6L6Hzm7lAoihlI27KiDCZEAwSmqCeXxRKhjrx_WPbX8Yg':
            print("WARNING: No valid Gemini API key found. Using mock PO generation.")
            return self._get_mock_po(invoice)

        prompt = self._build_po_generation_prompt(invoice)
        
        try:
            response = self.model.generate_content(prompt)
            response_text = self._clean_json_response(response.text)
            data = json.loads(response_text)
            
            return self._convert_to_extracted_data(data)
            
        except Exception as e:
            print(f"Error calling Gemini API for PO: {str(e)}")
            print("Falling back to mock PO due to API error.")
            return self._get_mock_po(invoice)

    def _get_mock_po(self, invoice: ExtractedData) -> ExtractedData:
        """Generate mock PO for testing/demo"""
        import random
        from datetime import datetime
        
        # Determine date (mock: 10 days before invoice)
        try:
            inv_date = datetime.strptime(invoice.date, '%Y-%m-%d')
            import datetime as dt
            po_date = (inv_date - dt.timedelta(days=10)).strftime('%Y-%m-%d')
        except:
            po_date = "2023-01-01"
            
        # Clone line items with slight variations if we want, but for now exact match is fine for successful audit
        mock_line_items = [
            LineItem(
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total=item.total,
                hsn_code=item.hsn_code
            ) for item in invoice.line_items
        ]

        return ExtractedData(
            vendor=invoice.vendor,
            invoice_no=f"REF-{invoice.invoice_no}", # Only for structure, PO doesn't have invoice no really
            date=po_date,
            total_amount=invoice.total_amount, # Exact match for simplified demo
            tax_amount=invoice.tax_amount,
            gst_no="27AABCU9603R1ZN",
            po_no=invoice.po_no or f"PO-{random.randint(10000, 99999)}",
            line_items=mock_line_items
        )
    
    def is_semantically_equivalent(self, name1: str, name2: str) -> bool:
        """
        Check if two names are semantically the same entity using Gemini
        
        Args:
            name1: First name string
            name2: Second name string
            
        Returns:
            True if semantically equivalent, False otherwise
        """
        if not name1 or not name2:
            return False
            
        # Basic check first
        if name1.lower().strip() == name2.lower().strip():
            return True
            
        if not self.api_key or self.api_key == 'AQ.Ab8RN6L6Hzm7lAoihlI27KiDCZEAwSmqCeXxRKhjrx_WPbX8Yg':
            return False

        prompt = f"""
        Determine if these two entity names refer to the same organization/vendor:
        1. "{name1}"
        2. "{name2}"
        
        Consider common abbreviations (Ltd vs Limited), branch names, and minor typos.
        Return ONLY 'True' if they are the same entity, 'False' otherwise.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return 'true' in response.text.lower()
        except:
            return False

    def calculate_match_score(
        self, 
        invoice: ExtractedData, 
        po: ExtractedData
    ) -> float:
        """
        Calculate similarity score between invoice and PO using semantic matching
        
        Args:
            invoice: Invoice data
            po: PO data
        
        Returns:
            Match score between 0.0 and 1.0
        """
        score = 0.0
        total_checks = 0
        
        # Vendor match - check both vendor and seller names semantically
        is_match = self.is_semantically_equivalent(invoice.vendor, po.vendor)
        if not is_match and invoice.seller:
            is_match = self.is_semantically_equivalent(invoice.seller, po.vendor)
            
        if is_match:
            score += 0.3
        total_checks += 0.3
        
        # Amount match within tolerance (weight: 0.3)
        amount_diff = abs(invoice.total_amount - po.total_amount) / po.total_amount if po.total_amount > 0 else 0
        if amount_diff <= Config.PO_AMOUNT_TOLERANCE:
            score += 0.3 * (1 - amount_diff / Config.PO_AMOUNT_TOLERANCE)
        total_checks += 0.3
        
        # GST match (weight: 0.2)
        if invoice.gst_no and po.gst_no and invoice.gst_no == po.gst_no:
            score += 0.2
        total_checks += 0.2
        
        # Line items match (weight: 0.2)
        line_item_score = self._calculate_line_item_similarity(
            invoice.line_items, 
            po.line_items
        )
        score += 0.2 * line_item_score
        total_checks += 0.2
        
        return score / total_checks if total_checks > 0 else 0.0
    
    def _calculate_line_item_similarity(
        self, 
        invoice_items: list, 
        po_items: list
    ) -> float:
        """Calculate similarity between line items"""
        if not invoice_items or not po_items:
            return 0.0
        
        matches = 0
        for inv_item in invoice_items:
            for po_item in po_items:
                if (inv_item.description.lower() in po_item.description.lower() or
                    po_item.description.lower() in inv_item.description.lower()):
                    matches += 1
                    break
        
        return matches / len(invoice_items)
    
    def _build_po_generation_prompt(self, invoice: ExtractedData) -> str:
        """Build prompt for PO generation"""
        return f"""
        You are generating a realistic Indian Government Purchase Order (PO) document.
        
        Based on this invoice:
        - Vendor: {invoice.vendor}
        - Invoice No: {invoice.invoice_no}
        - Total: ₹{invoice.total_amount}
        - Line Items: {json.dumps([asdict(item) for item in invoice.line_items], default=str)}
        
        Generate a corresponding PO that would have authorized this purchase.
        The PO should have:
        - A PO number in format: PO/[MINISTRY]/2024/[NUMBER]
        - Same vendor
        - Same or slightly different amounts (within 10%)
        - Similar line items
        - Date before the invoice date
        
        Return ONLY a valid JSON object with the same structure as the invoice extraction format.
        """
    
    def _clean_json_response(self, response_text: str) -> str:
        """Clean JSON response from markdown formatting"""
        text = response_text.strip()
        
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        
        return text.strip()
    
    def _convert_to_extracted_data(self, data: dict) -> ExtractedData:
        """Convert parsed JSON to ExtractedData object"""
        line_items = [
            LineItem(
                description=item['description'],
                quantity=item['quantity'],
                unit_price=item['unitPrice'],
                total=item['total'],
                hsn_code=item.get('hsnCode')
            )
            for item in data.get('lineItems', [])
        ]
        
        return ExtractedData(
            vendor=data['vendor'],
            invoice_no=data['invoiceNo'],
            date=data['date'],
            total_amount=data['totalAmount'],
            tax_amount=data['taxAmount'],
            gst_no=data.get('gstNo'),
            po_no=data.get('poNo'),
            line_items=line_items
        )