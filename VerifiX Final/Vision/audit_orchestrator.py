"""
audit_orchestrator.py - Main orchestrator that coordinates all audit services
"""
import hashlib
from datetime import datetime
from typing import List, Optional
from project_types import (
    ExtractedData, AuditResult, AuditStatus, 
    AgentStep, AuditFlag, AuditDecision
)
from extraction_service import ExtractionService
from matching_service import MatchingService
from rules_engine import RulesEngine
from risk_scoring import RiskScoringService
from repository import StatutoryArchive

class AuditOrchestrator:
    """Orchestrates the complete audit pipeline"""
    
    def __init__(self, archive: StatutoryArchive):
        """Initialize orchestrator with all services"""
        self.extraction_service = ExtractionService()
        self.matching_service = MatchingService()
        self.rules_engine = RulesEngine()
        self.risk_scoring = RiskScoringService()
        self.archive = archive
        self.steps: List[AgentStep] = []
    
    def process_document(
        self, 
        base64_data: str, 
        mime_type: str,
        po_data: Optional[str] = None,
        po_mime_type: Optional[str] = None
    ) -> AuditResult:
        """
        Process uploaded document through complete audit pipeline
        
        Args:
            base64_data: Base64 encoded document
            mime_type: Document MIME type
            po_data: Optional Base64 encoded PO document
            po_mime_type: Optional PO MIME type
        """
        self.steps = []
        
        try:
            # Step 1: Extract data
            self._add_step("DOC_INTEL", "Executing OCR + Spatial Frame Annotation...", "info")
            invoice_data = self.extraction_service.extract_from_image(base64_data, mime_type)
            self._add_step("DOC_INTEL", f"Entity Framed: {invoice_data.vendor}", "success")
            
            # Step 2: Find, generate, or process manual PO
            if po_data and po_mime_type:
                self._add_step("REFERENCE_AGENT", "Processing Manually Uploaded Reference PO...", "info")
                po_match = self.extraction_service.extract_from_image(po_data, po_mime_type)
                self._add_step("REFERENCE_AGENT", "Manual Reference PO Extracted.", "success")
            else:
                po_match = self._find_or_generate_po(invoice_data)
            
            # Step 3: Run validation rules
            self._add_step("RULE_ENGINE", "Cross-verifying Upload vs Reference Document...", "info")
            flags = self.rules_engine.validate(invoice_data, po_match, self.matching_service)
            status = "warning" if len(flags) > 0 else "success"
            self._add_step("RULE_ENGINE", f"Audit Check Complete. Identified {len(flags)} deviations.", status)
            
            # Step 4: Get AI decision
            self._add_step("DECISION_AGENT", "Executing multi-step reasoning determination...", "info")
            decision = self.risk_scoring.get_ai_decision(invoice_data, po_match, flags, [])
            self._add_step("DECISION_AGENT", "Autonomous legal determination reached.", "success")
            
            # Step 5: Calculate match score
            match_score = self.matching_service.calculate_match_score(invoice_data, po_match) if po_match else 0.0
            
            # Create audit result
            result = self._create_audit_result(invoice_data, po_match, flags, decision, match_score)
            
            # Store in archive
            self.archive.add_invoice(invoice_data)
            
            return result
            
        except Exception as e:
            self._add_step("SYSTEM", f"Critical Agent Chain Violation: {str(e)}", "error")
            raise
    
    def process_sample(self) -> AuditResult:
        """Process sample invoice for testing"""
        from repository import get_sample_invoice
        
        self.steps = []
        
        self._add_step("DOC_INTEL", "Loading Govt Sample from statutory archive...", "success")
        invoice_data = get_sample_invoice()
        
        po_match = self._find_or_generate_po(invoice_data)
        
        self._add_step("RULE_ENGINE", "Cross-verifying Upload vs Reference Document...", "info")
        flags = self.rules_engine.validate(invoice_data, po_match, self.matching_service)
        status = "warning" if len(flags) > 0 else "success"
        self._add_step("RULE_ENGINE", f"Audit Check Complete. Identified {len(flags)} deviations.", status)
        
        self._add_step("DECISION_AGENT", "Executing multi-step reasoning determination...", "info")
        decision = self.risk_scoring.get_ai_decision(invoice_data, po_match, flags, [])
        self._add_step("DECISION_AGENT", "Autonomous legal determination reached.", "success")
        
        # Calculate match score
        match_score = self.matching_service.calculate_match_score(invoice_data, po_match) if po_match else 0.0
        
        result = self._create_audit_result(invoice_data, po_match, flags, decision, match_score)
        
        return result
    
    def _find_or_generate_po(self, invoice: ExtractedData) -> Optional[ExtractedData]:
        """Find matching PO or generate new one"""
        self._add_step("REFERENCE_AGENT", "Searching /statutory_archive/reference_documents/ for matching PO...", "info")
        
        po_match = self.matching_service.find_matching_po(
            invoice, 
            self.archive.reference_documents
        )
        
        if po_match:
            self._add_step("REFERENCE_AGENT", "Found existing matching reference in archive.", "success")
        else:
            self._add_step("REFERENCE_AGENT", "No PO found. Synthesizing realistic Indian Reference PO...", "info")
            po_match = self.matching_service.generate_reference_po(invoice)
            
            if invoice.po_no:
                self.archive.add_po(invoice.po_no, po_match)
            
            self._add_step("REFERENCE_AGENT", "Reference PO generated and saved to /reference_documents/", "success")
        
        return po_match
    
    def _create_audit_result(
        self,
        invoice: ExtractedData,
        po: Optional[ExtractedData],
        flags: List[AuditFlag],
        decision: AuditDecision,
        match_score: float = 0.0
    ) -> AuditResult:
        """Create complete audit result"""
        audit_id = f"AUDIT-IND-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return AuditResult(
            id=audit_id,
            timestamp=datetime.now().isoformat(),
            status=AuditStatus.COMPLETED,
            doc_type='INVOICE',
            extracted_data=invoice,
            po_match=po,
            risk_score=decision.risk_score,
            risk_level=decision.risk_level,
            flags=flags,
            reasoning=decision.reasoning_steps,
            explanation=decision.explanation,
            recommendation=decision.recommendation,
            match_score=match_score,
            hash=f"SHA256:{hashlib.sha256(audit_id.encode()).hexdigest()[:15]}",
            agent_trace=self.steps.copy()
        )
    
    def _add_step(self, agent: str, action: str, status: str) -> None:
        """Add step to trace"""
        self.steps.append(AgentStep(
            agent=agent,
            action=action,
            status=status,
            timestamp=datetime.now().strftime('%H:%M:%S')
        ))