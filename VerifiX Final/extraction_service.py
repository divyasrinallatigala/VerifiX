"""
extraction_service.py - Document extraction service using Gemini Vision API
"""
import json
import google.generativeai as genai
from typing import Optional
from project_types import ExtractedData, LineItem
from config import Config

class ExtractionService:
    """Service for extracting structured data from invoice documents"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the extraction service with Gemini API"""
        self.api_key = api_key or Config.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    def extract_from_image(self, base64_data: str, mime_type: str) -> ExtractedData:
        """
        Extract invoice data from image/PDF using Gemini Vision
        
        Args:
            base64_data: Base64 encoded document data
            mime_type: MIME type of the document (e.g., 'image/jpeg', 'application/pdf')
        
        Returns:
            ExtractedData object with parsed invoice information
        """
        # Check if key is missing completely
        if not self.api_key:
            raise ValueError("Gemini API Key is MISSING. Please create a .env file in the 'Verifix new' folder with: GEMINI_API_KEY=your_key")
            
        # Check if key is the dummy default (just in case it's still in the .env)
        if self.api_key == '':
            raise ValueError("Gemini API Key is using the default example value. Please replace it with your real key.")

        prompt = self._build_extraction_prompt()
        
        try:
            # Create image part from base64
            image_part = {
                'mime_type': mime_type,
                'data': base64_data
            }
            
            response = self.model.generate_content([prompt, image_part])
            
            # Clean and parse response
            response_text = self._clean_json_response(response.text)
            data = json.loads(response_text)
            
            # Convert to ExtractedData
            return self._convert_to_extracted_data(data)
            
        except Exception as e:
            print(f"Error calling Gemini API: {str(e)}")
            raise e
    
    def _build_extraction_prompt(self) -> str:
        """Build the prompt for deep data extraction and document audit"""
        return """
        You are an expert Indian statutory auditor and data extractor. 
        Deeply analyze this invoice image and extract the following data with high precision.
        
        REQUIRED FIELDS:
        1. Vendor name (Primary entity)
        2. Seller name (Name of the specific seller/branch if mentioned separately)
        3. Invoice number
        4. Date
        5. GST number (if present, must be 15 chars)
        5. PO number (if present)
        6. Total amount (numeric only)
        7. Tax/GST amount (numeric only)
        8. Line items with: description, quantity, unit price, total, HSN/SAC code
        
        DEEP AUDIT ANALYSIS:
        Also perform a structural audit of the document and identify "anomalies":
        - Mathematical errors: Do line item (qty * price) results match the line totals? Does sum of line totals + tax match the total amount?
        - Visual flags: Are there font mismatches, suspicious stamp overlays, or digitally altered text areas?
        - Compliance flags: Is the GST number valid? (Starts with state code 1-37, followed by PAN, 1, Z, and checksum).
        - Logic flags: Is the date valid? Are there unrealistic amounts?
        
        Return ONLY a valid JSON object with this exact structure:
        {
          "vendor": "string",
          "seller": "string or null",
          "invoiceNo": "string",
          "date": "string",
          "totalAmount": number,
          "taxAmount": number,
          "gstNo": "string or null",
          "poNo": "string or null",
          "anomalies": ["list of strings or empty"],
          "lineItems": [
            {
              "description": "string",
              "quantity": number,
              "unitPrice": number,
              "total": number,
              "hsnCode": "string or null"
            }
          ]
        }
        
        Do not include any markdown formatting or explanation, only the JSON.
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
            seller=data.get('seller'),
            invoice_no=data['invoiceNo'],
            date=data['date'],
            total_amount=data['totalAmount'],
            tax_amount=data['taxAmount'],
            gst_no=data.get('gstNo'),
            po_no=data.get('poNo'),
            anomalies=data.get('anomalies', []),
            line_items=line_items
        )

    def _get_mock_data(self) -> ExtractedData:
        """Generate mock extracted data for testing/demo"""
        import random
        from datetime import datetime, timedelta
        
        vendors = ["ABC Supplies", "Tech Solutions Inc", "Global Logistics", "Office Mart"]
        vendor = random.choice(vendors)
        amount = random.randint(5000, 25000)
        
        return ExtractedData(
            vendor=vendor,
            invoice_no=f"INV-{random.randint(1000, 9999)}",
            date=(datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            total_amount=float(amount),
            tax_amount=float(amount * 0.18),
            gst_no="27AABCU9603R1ZN",
            po_no=f"PO-{random.randint(10000, 99999)}",
            line_items=[
                LineItem(
                    description="Office Supplies",
                    quantity=random.randint(1, 10),
                    unit_price=float(amount),
                    total=float(amount),
                    hsn_code="8471"
                )
            ]
        )