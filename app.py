from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
import json

# Initialize the Flask application
app = Flask(__name__)

# Define a simple JSON schema for validation
schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
    },
    "required": ["message"]
}

# Define a catch-all route that handles all paths and common HTTP methods.
# 'defaults={'path': ''}' handles the root path ('/')
# '<path:path>' handles any subpath (e.g., '/api/test')
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def echo_request(path):
    """
    Captures and echoes the incoming HTTP request details (method, path, headers, and body).
    """
    headers = {k: v for k, v in request.headers.items()}
    body = request.get_data(as_text=True)

    if request.content_type == 'application/json':
        try:
            json_body = json.loads(body)
            validate(instance=json_body, schema=schema)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON format"}), 400
        except ValidationError as e:
            return jsonify({"error": f"JSON validation error: {e.message}"}), 400

    response_data = {
        "message": "Request successfully echoed! Details below:",
        "method": request.method,
        "path": f"/{path}",
        "query_parameters": dict(request.args),
        "content_type": request.content_type,
        "headers": headers,
        "body_content": body,
    }

    return jsonify(response_data)

# Run the app, listening on all public IPs (0.0.0.0) which is necessary for Docker
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
