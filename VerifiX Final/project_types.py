"""
types.py - Data types and models for the Invoice Audit Agent
"""
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class AuditStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class BoundingBox:
    x: float
    y: float
    w: float
    h: float

@dataclass
class AuditFlag:
    id: str
    rule: str
    severity: RiskLevel
    description: str
    field: str
    coords: Optional[BoundingBox] = None

@dataclass
class LineItem:
    description: str
    quantity: int
    unit_price: float
    total: float
    hsn_code: Optional[str] = None
    coords: Optional[BoundingBox] = None

@dataclass
class FieldCoordinates:
    vendor: Optional[BoundingBox] = None
    invoice_no: Optional[BoundingBox] = None
    gst_no: Optional[BoundingBox] = None
    total_amount: Optional[BoundingBox] = None
    date: Optional[BoundingBox] = None
    po_no: Optional[BoundingBox] = None

@dataclass
class ExtractedData:
    vendor: str
    invoice_no: str
    date: str
    total_amount: float
    tax_amount: float
    line_items: List[LineItem]
    seller: Optional[str] = None  # Added for semantic matching
    gst_no: Optional[str] = None
    po_no: Optional[str] = None
    anomalies: Optional[List[str]] = None
    field_coords: Optional[FieldCoordinates] = None
    flags: Optional[List[AuditFlag]] = None # Added for trace

@dataclass
class AgentStep:
    agent: str
    action: str
    status: str
    timestamp: str

@dataclass
class AuditDecision:
    risk_score: int
    risk_level: RiskLevel
    reasoning_steps: List[str]
    explanation: str
    recommendation: str

@dataclass
class AuditResult:
    id: str
    timestamp: str
    status: AuditStatus
    doc_type: str
    extracted_data: ExtractedData
    po_match: Optional[ExtractedData]
    risk_score: int
    risk_level: RiskLevel
    flags: List[AuditFlag]
    reasoning: List[str]
    explanation: str
    recommendation: str
    match_score: float
    hash: str
    agent_trace: List[AgentStep]