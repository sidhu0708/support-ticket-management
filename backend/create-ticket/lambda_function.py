
import json
import os
import uuid
import boto3
from datetime import datetime, timezone

# AWS service connections
dynamodb = boto3.resource("dynamodb")
sqs = boto3.client("sqs")

# Environment variables (configure later in AWS Lambda)
table = dynamodb.Table(os.environ["TABLE_NAME"])
queue_url = os.environ["QUEUE_URL"]


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,PATCH,OPTIONS"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    try:
        # Read frontend request
        data = json.loads(event.get("body") or "{}")

        required_fields = ["name", "email", "subject", "description"]

        for field in required_fields:
            if not str(data.get(field, "")).strip():
                return response(400, {
                    "message": f"{field} is required"
                })

        if len(data["description"].strip()) < 10:
            return response(400, {
                "message": "Description must contain at least 10 characters"
            })

        # Generate unique ticket ID
        ticket_id = "TKT-" + uuid.uuid4().hex[:10].upper()

        current_time = datetime.now(timezone.utc).isoformat()

        # Prepare ticket information
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

        # Store ticket in DynamoDB
        table.put_item(Item=ticket)

        # Send ticket event to SQS
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({
                "ticketId": ticket_id,
                "email": ticket["email"],
                "subject": ticket["subject"],
                "createdAt": current_time
            })
        )

        return response(201, {
            "message": "Ticket submitted successfully",
            "ticketId": ticket_id,
            "status": "OPEN"
        })

    except Exception as error:
        print("Error creating ticket:", str(error))

        return response(500, {
            "message": "Unable to create ticket. Please try again."
        })
