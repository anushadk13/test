from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# In-memory storage (replace with database in production)
patient_data = []

@app.route('/api/patients', methods=['POST'])
def add_patient():
    """Add new patient data"""
    try:
        data = request.get_json()
        
        # Add timestamp if not provided
        if 'createdAt' not in data:
            data['createdAt'] = datetime.now().isoformat() + 'Z'
        if 'lastUpdate' not in data:
            data['lastUpdate'] = datetime.now().isoformat() + 'Z'
        
        # Add auto-increment ID if not provided
        if 'id' not in data:
            data['id'] = len(patient_data) + 1
        
        patient_data.append(data)
        
        return jsonify({
            'message': 'Patient data added successfully',
            'data': data
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Invalid data format',
            'details': str(e)
        }), 400

@app.route('/api/patients', methods=['GET'])
def get_all_patients():
    """Get all patient data"""
    return jsonify(patient_data)

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    """Get patient by ID"""
    patient = next((p for p in patient_data if p['id'] == patient_id), None)
    
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    return jsonify(patient)

@app.route('/api/patients/request/<request_id>', methods=['GET'])
def get_patient_by_request_id(request_id):
    """Get patient by request ID"""
    patient = next((p for p in patient_data if p.get('requestId') == request_id), None)
    
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    return jsonify(patient)

@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update patient data"""
    try:
        # Find patient index
        patient_index = next((i for i, p in enumerate(patient_data) if p['id'] == patient_id), None)
        
        if patient_index is None:
            return jsonify({'error': 'Patient not found'}), 404
        
        # Update patient data
        update_data = request.get_json()
        patient_data[patient_index].update(update_data)
        patient_data[patient_index]['lastUpdate'] = datetime.now().isoformat() + 'Z'
        
        return jsonify({
            'message': 'Patient data updated successfully',
            'data': patient_data[patient_index]
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Update failed',
            'details': str(e)
        }), 400

@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete patient data"""
    patient_index = next((i for i, p in enumerate(patient_data) if p['id'] == patient_id), None)
    
    if patient_index is None:
        return jsonify({'error': 'Patient not found'}), 404
    
    deleted_patient = patient_data.pop(patient_index)
    
    return jsonify({
        'message': 'Patient data deleted successfully',
        'data': deleted_patient
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'total_patients': len(patient_data)
    })

if __name__ == '__main__':
    print("Starting Patient Data Server...")
    print("Available endpoints:")
    print("POST /api/patients - Add new patient data")
    print("GET /api/patients - Get all patient data")
    print("GET /api/patients/<id> - Get patient by ID")
    print("GET /api/patients/request/<request_id> - Get patient by request ID")
    print("PUT /api/patients/<id> - Update patient data")
    print("DELETE /api/patients/<id> - Delete patient data")
    print("GET /health - Health check")
    print("\nServer running at http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=3000)/home/anusha2323/Prior_auth_/skypoint-prior-authorization/PA/testing/test.py