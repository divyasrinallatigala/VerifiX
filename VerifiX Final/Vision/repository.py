"""
repository.py - Data repository for storing invoices and PO documents
"""
from typing import Dict, List, Optional
from project_types import ExtractedData, LineItem, BoundingBox, FieldCoordinates

class StatutoryArchive:
    """Repository for statutory documents"""
    
    def __init__(self):
        """Initialize the archive with sample data"""
        self.user_uploaded_invoice: List[ExtractedData] = []
        self.reference_documents: Dict[str, ExtractedData] = {
            "PO/MEITY/2024/221": self._create_sample_po()
        }
    
    def _create_sample_po(self) -> ExtractedData:
        """Create sample PO for testing"""
        return ExtractedData(
            vendor="Tech Solutions India Pvt Ltd",
            invoice_no="PO/MEITY/2024/221",
            date="2024-01-15",
            total_amount=500000.0,
            tax_amount=90000.0,
            gst_no="29ABCDE1234F1Z5",
            po_no="PO/MEITY/2024/221",
            line_items=[
                LineItem(
                    description="Enterprise Server Hardware",
                    quantity=10,
                    unit_price=41000.0,
                    total=410000.0,
                    hsn_code="847130"
                )
            ]
        )
    
    def add_invoice(self, invoice: ExtractedData) -> None:
        """Add invoice to archive"""
        self.user_uploaded_invoice.append(invoice)
    
    def add_po(self, po_no: str, po: ExtractedData) -> None:
        """Add PO to archive"""
        self.reference_documents[po_no] = po
    
    def get_po(self, po_no: str) -> Optional[ExtractedData]:
        """Retrieve PO from archive"""
        return self.reference_documents.get(po_no)
    
    def get_all_invoices(self) -> List[ExtractedData]:
        """Get all invoices"""
        return self.user_uploaded_invoice
    
    def get_all_pos(self) -> Dict[str, ExtractedData]:
        """Get all POs"""
        return self.reference_documents


def get_sample_invoice() -> ExtractedData:
    """Get sample invoice for testing"""
    return ExtractedData(
        vendor="Tech Solutions India Pvt Ltd",
        invoice_no="INV-2024-0891",
        date="2024-02-20",
        total_amount=590000.0,
        tax_amount=90000.0,
        gst_no="29ABCDE1234F1Z5",
        po_no="PO/MEITY/2024/221",
        line_items=[
            LineItem(
                description="Enterprise Server Hardware",
                quantity=10,
                unit_price=41000.0,
                total=410000.0,
                hsn_code="847130",
                coords=BoundingBox(x=10, y=45, w=80, h=8)
            ),
            LineItem(
                description="Network Infrastructure Setup",
                quantity=1,
                unit_price=90000.0,
                total=90000.0,
                hsn_code="998314",
                coords=BoundingBox(x=10, y=55, w=80, h=8)
            )
        ],
        field_coords=FieldCoordinates(
            vendor=BoundingBox(x=15, y=12, w=40, h=5),
            invoice_no=BoundingBox(x=70, y=15, w=20, h=4),
            gst_no=BoundingBox(x=15, y=18, w=30, h=3),
            total_amount=BoundingBox(x=65, y=75, w=25, h=6),
            date=BoundingBox(x=70, y=20, w=20, h=3),
            po_no=BoundingBox(x=70, y=24, w=20, h=3)
        )
    )