from flask import Blueprint, request, jsonify, current_app
from .generator import AIGenerator, AIGeneratorError

bp = Blueprint("ai", __name__, url_prefix="/api/v1")

@bp.route("/generate_srs", methods=["POST"])
def generate_srs():
    """Generate a complete SRS document based on project information."""
    if not request.is_json:
        return jsonify({
            "error": "Content-Type must be application/json",
            "missing_fields": ["projectName", "targetUsers", "projectGoals", "projectScope"]
        }), 400

    data = request.get_json(silent=True) or {}
    required_fields = ["projectName", "targetUsers", "projectGoals", "projectScope"]
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400
    
    try:
        generator = AIGenerator()
        srs_sections = generator.generate_srs(data)
        
        return jsonify({
            "status": "success",
            "sections": srs_sections
        })
    except AIGeneratorError as e:
        current_app.logger.error(f"Error generating SRS: {str(e)}")
        return jsonify({
            "error": "Failed to generate SRS document",
            "details": str(e)
        }), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500
