
from flask import Flask, request, jsonify
import boto3
import uuid
from datetime import datetime, timezone

app = Flask(__name__)

# Connect to existing DynamoDB table using EC2 IAM Role
dynamodb = boto3.resource(
    "dynamodb",
    region_name="eu-north-1"
)

table = dynamodb.Table("SupportTickets")


# Home endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Support Ticket EC2 Backend is running",
        "status": "healthy"
    })


# Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    }), 200


# Create a new support ticket
@app.route("/tickets", methods=["POST"])
def create_ticket():
    try:
        data = request.get_json(silent=True) or {}

        required = ["name", "email", "subject", "description"]

        for field in required:
            if not str(data.get(field, "")).strip():
                return jsonify({
                    "message": f"{field} is required"
                }), 400

        if len(data["description"].strip()) < 10:
            return jsonify({
                "message": "Description must contain at least 10 characters"
            }), 400

        ticket_id = "EC2-" + uuid.uuid4().hex[:10].upper()

        current_time = datetime.now(timezone.utc).isoformat()

        ticket = {
            "ticketId": ticket_id,
            "name": data["name"].strip()[:80],
            "email": data["email"].strip()[:120],
            "subject": data["subject"].strip()[:120],
            "description": data["description"].strip()[:3000],
            "status": "OPEN",
            "createdAt": current_time,
            "updatedAt": current_time
        }

        table.put_item(Item=ticket)

        return jsonify({
            "message": "Ticket created successfully through EC2 backend",
            "ticketId": ticket_id,
            "status": "OPEN"
        }), 201

    except Exception:
        app.logger.exception("Ticket creation failed")

        return jsonify({
            "message": "Unable to create ticket"
        }), 500


# List all tickets
@app.route("/tickets", methods=["GET"])
def list_tickets():
    try:
        result = table.scan()

        return jsonify({
            "count": result.get("Count", 0),
            "tickets": result.get("Items", [])
        }), 200

    except Exception:
        app.logger.exception("Ticket listing failed")

        return jsonify({
            "message": "Unable to retrieve tickets"
        }), 500


# Get individual ticket by ID
@app.route("/tickets/<ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    try:
        result = table.get_item(
            Key={"ticketId": ticket_id}
        )

        ticket = result.get("Item")

        if not ticket:
            return jsonify({
                "message": "Ticket not found"
            }), 404

        return jsonify(ticket), 200

    except Exception:
        app.logger.exception("Ticket retrieval failed")

        return jsonify({
            "message": "Unable to retrieve ticket"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
