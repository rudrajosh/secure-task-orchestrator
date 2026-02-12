from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }).data
        response.content_type = "application/json"
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        # Log the error here
        # app.logger.error(f"Unexpected error: {e}")
        response = jsonify({
            "code": 500,
            "name": "Internal Server Error",
            "description": "An unexpected error occurred.",
        })
        response.status_code = 500
        return response
