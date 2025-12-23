"""
app.py - Flask REST API for Invoice Audit Agent
"""
import os
import sys
# Add parent directory to path to allow importing project_types
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import base64
from typing import Any, Dict
from enum import Enum
from dataclasses import asdict
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from audit_orchestrator import AuditOrchestrator
from repository import StatutoryArchive
from config import Config

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'), static_url_path=None)
CORS(app)

# Serve React App (Moved to end of file)

# Initialize services
archive = StatutoryArchive()
orchestrator = AuditOrchestrator(archive)

# ==================== UTILITY FUNCTIONS ====================

def convert_to_dict(obj: Any) -> Dict:
    """Convert dataclass to dict recursively"""
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, list):
        return [convert_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, '__dict__'):
        result = {}
        for key, value in obj.__dict__.items():
            # Convert snake_case to camelCase
            camel_key = ''.join(
                word.capitalize() if i > 0 else word 
                for i, word in enumerate(key.split('_'))
            )
            result[camel_key] = convert_to_dict(value)
        return result
    else:
        return str(obj)

# ==================== API ENDPOINTS ====================

# Removed redundant / route to allow serve() to handle it

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'VerifiX Invoice Audit Agent',
        'version': '1.0.0',
        'gemini_configured': bool(Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != 'Your API key')
    })

@app.route('/api/audit/sample', methods=['POST'])
def audit_sample():
    """Process sample invoice audit"""
    try:
        result = orchestrator.process_sample()
        return jsonify(convert_to_dict(result))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/audit/upload', methods=['POST'])
def upload_file():
    """Handle invoice upload and auditing"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Retrieve optional PO file
    po_file = request.files.get('po_file')
    po_data = None
    po_mime_type = None

    if po_file and po_file.filename != '':
        po_data = base64.b64encode(po_file.read()).decode('utf-8')
        po_mime_type = po_file.mimetype

    try:
        # Read file as base64
        file_content = file.read()
        base64_data = base64.b64encode(file_content).decode('utf-8')
        mime_type = file.mimetype

        # Process document with optional PO
        result = orchestrator.process_document(
            base64_data, 
            mime_type,
            po_data=po_data,
            po_mime_type=po_mime_type
        )
        
        # Convert to dictionary using dataclasses.asdict
        # We need to handle nested dataclasses properly if simple dict conversion fails
        # But dataclasses.asdict handles recursion well
        return jsonify(asdict(result))

    except Exception as e:
        print(f"Error processing upload: {str(e)}")
        # Return 500 with error message
        return jsonify({'error': str(e)}), 500

@app.route('/api/archive', methods=['GET'])
def get_archive():
    """Get statutory archive contents"""
    return jsonify({
        'userUploadedInvoice': [convert_to_dict(inv) for inv in archive.get_all_invoices()],
        'referenceDocuments': {k: convert_to_dict(v) for k, v in archive.get_all_pos().items()}
    })

@app.route('/api/archive/invoices', methods=['GET'])
def get_invoices():
    """Get all uploaded invoices"""
    return jsonify([convert_to_dict(inv) for inv in archive.get_all_invoices()])

@app.route('/api/archive/pos', methods=['GET'])
def get_pos():
    """Get all reference POs"""
    return jsonify({k: convert_to_dict(v) for k, v in archive.get_all_pos().items()})

@app.route('/api/rules/list', methods=['GET'])
def list_rules():
    """List all validation rules"""
    return jsonify({
        'rules': [
            {
                'id': 'R-SEM-001',
                'name': 'Vendor Mismatch',
                'description': 'Check vendor name matches PO',
                'severity': 'HIGH'
            },
            {
                'id': 'R-GST-002',
                'name': 'Amount Exceeds PO',
                'description': 'Check invoice amount doesn\'t exceed PO',
                'severity': 'HIGH'
            },
            {
                'id': 'R-GST-003',
                'name': 'Invalid GST Number',
                'description': 'Check GST number is present and valid',
                'severity': 'MEDIUM'
            },
            {
                'id': 'R-FIN-004',
                'name': 'Tax Calculation Error',
                'description': 'Check tax calculation is correct',
                'severity': 'MEDIUM'
            },
            {
                'id': 'R-PO-005',
                'name': 'Missing PO Reference',
                'description': 'Check PO reference exists',
                'severity': 'HIGH'
            },
            {
                'id': 'R-DATE-006',
                'name': 'Invalid Date Sequence',
                'description': 'Check invoice date is after PO date',
                'severity': 'MEDIUM'
            },
            {
                'id': 'R-ITEM-007',
                'name': 'Line Items Mismatch',
                'description': 'Check line items match PO',
                'severity': 'MEDIUM'
            }
        ]
    })

# ==================== FRONTEND SERVING ====================

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Check if the requested path exists as a static file
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # Otherwise, serve index.html for React routing
    return send_from_directory(app.static_folder, 'index.html')

# ==================== MAIN ====================

if __name__ == '__main__':
    print("=" * 60)
    print("Starting VerifiX Invoice Audit Agent")
    print("=" * 60)
    print(f"Gemini API Key configured: {bool(Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != 'Your API key')}")
    print(f"Server: http://{Config.HOST}:{Config.PORT}")
    print("=" * 60)
    print("\nAvailable Endpoints:")
    print("  GET  /api/health          - Health check")
    print("  POST /api/audit/sample    - Process sample invoice")
    print("  POST /api/audit/upload    - Upload and audit invoice")
    print("  GET  /api/archive         - Get all archived documents")
    print("  GET  /api/archive/invoices - Get all invoices")
    print("  GET  /api/archive/pos     - Get all POs")
    print("  GET  /api/rules/list      - List all validation rules")
    print("=" * 60)
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
