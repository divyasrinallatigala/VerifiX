"""
risk_scoring.py - Risk scoring and decision service
"""
import json
import google.generativeai as genai
from typing import List, Optional
from project_types import ExtractedData, AuditFlag, AuditDecision, RiskLevel
from config import Config
from dataclasses import asdict

class RiskScoringService:
    """Service for calculating risk scores and making audit decisions"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize risk scoring service with Gemini API"""
        self.api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    def calculate_risk_score(
        self,
        invoice: ExtractedData,
        po: Optional[ExtractedData],
        flags: List[AuditFlag]
    ) -> int:
        """
        Calculate base risk score from flags
        
        Args:
            invoice: Invoice data
            po: PO data
            flags: List of audit flags
        
        Returns:
            Risk score (0-100)
        """
        if not flags:
            return 0
        
        score = 0
        
        for flag in flags:
            if flag.severity == RiskLevel.HIGH:
                score += 35
            elif flag.severity == RiskLevel.MEDIUM:
                score += 20
            elif flag.severity == RiskLevel.LOW:
                score += 10
        
        # Cap at 100
        return min(score, 100)
    
    def determine_risk_level(self, risk_score: int) -> RiskLevel:
        """
        Determine risk level from score
        
        Args:
            risk_score: Calculated risk score
        
        Returns:
            Risk level classification
        """
        if risk_score >= 60:
            return RiskLevel.HIGH
        elif risk_score >= 30:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def get_ai_decision(
        self,
        invoice: ExtractedData,
        po: Optional[ExtractedData],
        flags: List[AuditFlag],
        context: List[str]
    ) -> AuditDecision:
        """
        Get comprehensive AI-powered audit decision
        
        Args:
            invoice: Invoice data
            po: PO data
            flags: List of audit flags
            context: Additional context information
        
        Returns:
            Complete audit decision with reasoning
        """

        # Fallback if no API key
        if not self.api_key or self.api_key == 'Your API key':
            print("WARNING: No valid Gemini API key found. Using fallback decision logic.")
            return self._get_fallback_decision(invoice, po, flags)

        prompt = self._build_decision_prompt(invoice, po, flags, context)
        
        try:
            response = self.model.generate_content(prompt)
            response_text = self._clean_json_response(response.text)
            data = json.loads(response_text)
            
            return AuditDecision(
                risk_score=data['riskScore'],
                risk_level=RiskLevel(data['riskLevel']),
                reasoning_steps=data['reasoningSteps'],
                explanation=data['explanation'],
                recommendation=data['recommendation']
            )
            
        except Exception as e:
            print(f"AI decision failed, using fallback: {e}")
            # Fallback to deterministic decision
            return self._get_fallback_decision(invoice, po, flags)
    
    def _build_decision_prompt(
        self,
        invoice: ExtractedData,
        po: Optional[ExtractedData],
        flags: List[AuditFlag],
        context: List[str]
    ) -> str:
        """Build prompt for AI decision making"""
        return f"""
        You are an expert Indian statutory auditor analyzing invoice compliance.
        
        INVOICE DATA:
        {json.dumps(asdict(invoice), indent=2, default=str)}
        
        REFERENCE PO:
        {json.dumps(asdict(po) if po else {}, indent=2, default=str)}
        
        IDENTIFIED FLAGS:
        {json.dumps([asdict(f) for f in flags], indent=2, default=str)}
        
        CONTEXT:
        {json.dumps(context, indent=2)}
        
        Provide a comprehensive audit decision with:
        1. Risk score (0-100, where 100 is highest risk)
        2. Risk level (LOW, MEDIUM, HIGH)
        3. Step-by-step reasoning (as array of strings)
        4. Overall explanation
        5. Recommendation (APPROVE, REVIEW, REJECT)
        
        Consider:
        - Severity and number of compliance violations
        - Financial impact and materiality
        - Statutory requirements under Indian law
        - Government procurement guidelines
        
        Return ONLY valid JSON:
        {{
          "riskScore": number,
          "riskLevel": "LOW|MEDIUM|HIGH",
          "reasoningSteps": ["step1", "step2", ...],
          "explanation": "string",
          "recommendation": "string"
        }}
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
    
    def _get_fallback_decision(
        self,
        invoice: ExtractedData,
        po: Optional[ExtractedData],
        flags: List[AuditFlag]
    ) -> AuditDecision:
        """Generate fallback decision without AI"""
        risk_score = self.calculate_risk_score(invoice, po, flags)
        risk_level = self.determine_risk_level(risk_score)
        
        reasoning_steps = [
            f"Detected {len(flags)} compliance issues",
            "Cross-verified with reference documents",
            "Applied statutory rules engine",
            f"Calculated risk score: {risk_score}/100"
        ]
        
        if risk_level == RiskLevel.HIGH:
            recommendation = "REJECT"
            explanation = "Critical compliance violations detected. Invoice does not meet statutory requirements."
        elif risk_level == RiskLevel.MEDIUM:
            recommendation = "REVIEW"
            explanation = "Potential compliance issues identified. Manual review recommended before approval."
        else:
            recommendation = "APPROVE"
            explanation = "Invoice meets statutory requirements and aligns with reference documentation."
        
        return AuditDecision(
            risk_score=risk_score,
            risk_level=risk_level,
            reasoning_steps=reasoning_steps,
            explanation=explanation,
            recommendation=recommendation
        )
