## Database – Amazon DynamoDB

- Service: Amazon DynamoDB
- Region: ap-south-1 (Mumbai)
- Table Name: SupportTickets
- Partition Key: ticketId
- Data Type: String
- Capacity Mode: On-demand

The DynamoDB table stores support ticket
information including customer details,
issue description, ticket status and timestamps.



## Messaging Services

### Amazon SQS
- Main Queue: support-ticket-queue
- Dead Letter Queue: support-ticket-dlq
- Queue Type: Standard
- Maximum Receives: 3

### Amazon SNS
- Topic: support-ticket-notifications
- Protocol: Email
- Region: ap-south-1
- Subscription Status: Confirmed

GitHub webhook integration tested successfully.
GitHub webhook integration tested successfully.
5.
