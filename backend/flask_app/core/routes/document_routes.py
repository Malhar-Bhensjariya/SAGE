from flask import Blueprint

document_bp = Blueprint('document', __name__)

@document_bp.route('/test', methods=['GET'])
def test_document():
    return {'message': 'Document route working!'}
