from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Define a catch-all route that handles all paths and common HTTP methods.
# 'defaults={'path': ''}' handles the root path ('/')
# '<path:path>' handles any subpath (e.g., '/api/test')
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def echo_request(path):
    """
    Captures and echoes the incoming HTTP request details (method, path, headers, and body).
    """

    # Extract headers into a standard dictionary (request.headers is a special object)
    headers = {k: v for k, v in request.headers.items()}

    # Extract request body as text. This handles JSON, form data, or raw text payloads.
    try:
        body = request.get_data(as_text=True)
    except Exception as e:
        body = f"Could not decode body: {e}"

    # Construct the response object with all captured details
    response_data = {
        "message": "Request successfully echoed! Details below:",
        "method": request.method,
        "path": f"/{path}",
        "query_parameters": dict(request.args),
        "content_type": request.content_type,
        "headers": headers,
        "body_content": body,
    }

    # Use jsonify to ensure a proper JSON response format
    return jsonify(response_data)

# Run the app, listening on all public IPs (0.0.0.0) which is necessary for Docker
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
