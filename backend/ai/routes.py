from flask import Blueprint, request, jsonify, current_app, session
from .generator import AIGenerator, AIGeneratorError
from .interactive_agent import InteractiveAgent

bp = Blueprint("ai", __name__, url_prefix="/api/v1")

# Store active agent sessions (in production, use Redis or similar)
agent_sessions = {}


@bp.route("/generate_srs", methods=["POST"])
def generate_srs():
    """Generate a complete SRS document based on project information."""
    if not request.is_json:
        return (
            jsonify(
                {
                    "error": "Content-Type must be application/json",
                    "missing_fields": [
                        "projectName",
                        "targetUsers",
                        "projectGoals",
                        "projectScope",
                    ],
                }
            ),
            400,
        )

    data = request.get_json(silent=True) or {}
    required_fields = ["projectName", "targetUsers", "projectGoals", "projectScope"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return (
            jsonify(
                {"error": "Missing required fields", "missing_fields": missing_fields}
            ),
            400,
        )

    try:
        generator = AIGenerator()
        srs_sections = generator.generate_srs(data)

        return jsonify({"status": "success", "sections": srs_sections})
    except AIGeneratorError as e:
        current_app.logger.error(f"Error generating SRS: {str(e)}")
        return (
            jsonify({"error": "Failed to generate SRS document", "details": str(e)}),
            500,
        )
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )


@bp.route("/interactive/start", methods=["POST"])
def start_interactive_session():
    """Start a new interactive SRS generation session."""
    try:
        agent = InteractiveAgent()
        response = agent.start_conversation()

        # Store agent session
        session_id = str(response["conversation_id"])
        agent_sessions[session_id] = {
            "agent": agent,
            "collected_data": {},
        }

        return jsonify(
            {
                "status": "success",
                "session_id": session_id,
                "message": response["message"],
                "progress": response["progress"],
            }
        )
    except Exception as e:
        current_app.logger.error(f"Error starting interactive session: {str(e)}")
        return (
            jsonify(
                {
                    "error": "Failed to start interactive session",
                    "details": str(e),
                }
            ),
            500,
        )


@bp.route("/interactive/respond", methods=["POST"])
def respond_to_agent():
    """Send a response to the interactive agent."""
    if not request.is_json:
        return (
            jsonify({"error": "Content-Type must be application/json"}),
            400,
        )

    data = request.get_json(silent=True) or {}

    if "session_id" not in data or "message" not in data:
        return (
            jsonify({"error": "Missing required fields: session_id and message"}),
            400,
        )

    session_id = data["session_id"]
    user_message = data["message"]

    # Retrieve session
    if session_id not in agent_sessions:
        return (
            jsonify({"error": "Invalid or expired session_id"}),
            404,
        )

    try:
        session_data = agent_sessions[session_id]
        agent = session_data["agent"]
        collected_data = session_data["collected_data"]

        # Process user input
        response = agent.process_user_input(user_message, collected_data)

        # Update session
        agent_sessions[session_id]["collected_data"] = response.get(
            "collected_data", collected_data
        )

        # If complete, generate the full SRS
        if response.get("complete", False):
            sections = agent.generate_complete_srs(response["collected_data"])
            return jsonify(
                {
                    "status": "complete",
                    "message": response["message"],
                    "sections": sections,
                    "progress": response["progress"],
                }
            )

        return jsonify(
            {
                "status": "in_progress",
                "message": response["message"],
                "progress": response["progress"],
            }
        )

    except Exception as e:
        current_app.logger.error(f"Error processing agent response: {str(e)}")
        return (
            jsonify(
                {
                    "error": "Failed to process response",
                    "details": str(e),
                }
            ),
            500,
        )


@bp.route("/interactive/status/<session_id>", methods=["GET"])
def get_session_status(session_id):
    """Get the status of an interactive session."""
    if session_id not in agent_sessions:
        return (
            jsonify({"error": "Invalid or expired session_id"}),
            404,
        )

    session_data = agent_sessions[session_id]
    agent = session_data["agent"]
    collected_data = session_data["collected_data"]

    progress = agent._calculate_progress(collected_data)

    return jsonify(
        {
            "status": "success",
            "session_id": session_id,
            "progress": progress,
            "collected_data": collected_data,
        }
    )
