import base64
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/Nutzerfunktion", methods=["GET"])
def nutzerfunktion():
    principal = request.headers.get("x-ms-client-principal")
    if not principal:
        return jsonify({"roles": [], "error": "No authentication header found"}), 401
    decoded = base64.b64decode(principal)
    user = json.loads(decoded)
    return jsonify({
        "userDetails": user.get("userDetails"),
        "userId": user.get("userId"),
        "identityProvider": user.get("identityProvider"),
        "userRoles": user.get("userRoles", [])
    })
