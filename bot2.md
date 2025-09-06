### Enhanced Workflow for Mapping Conversations to REST API Notifications with Jinja2 Templates and Draft Option

This workflow extends the previous approach to use **Jinja2 templates** for formatting notification messages and adds a **draft option** where users can send notifications to themselves for proofreading before broadcasting to the team. The workflow leverages GitHub Copilot (or a similar AI coding assistant) to parse free-format human/bot conversations into structured parameters for a REST API notification service, with the message formatted using a Jinja2 template. The output is a JSON object specifying the `sendNotification` function and its parameters, including the recipient (self for draft or team), the formatted message, and the channel.

#### Assumptions
- The REST API service accepts POST requests at an endpoint like `https://api.rester.example/notify` with a JSON payload containing `recipient`, `message`, and `channel`.
- Jinja2 is used to format messages dynamically based on conversation-derived parameters.
- The draft option sends the notification to the user's email (or ID) for review before sending to the team.
- Copilot is integrated into an IDE (e.g., VS Code) or used via its API/extensions for parsing and code generation.
- The conversation provides context for recipients, message content, and optional draft preference.

#### Workflow Steps
1. **Capture and Preprocess Conversation**:
   - Collect the conversation as a string (e.g., "Human: Notify DevOps about the urgent meeting tomorrow at 10 AM, but send a draft to me first.").
   - Clean irrelevant data (e.g., timestamps) to focus on actionable content.
   - Use Copilot Chat to refine the input interactively if needed.

2. **Prompt Copilot for Intent Extraction and Parameter Mapping**:
   - Feed the conversation into Copilot via a prompt or code comment, instructing it to extract the function (`sendNotification`), parameters, and detect the draft option.
   - Example Prompt:
     ```
     // Parse this conversation to map to a REST API notification call:
     // Conversation: [insert conversation text]
     // Function: sendNotification(recipient, message, channel, is_draft)
     // Use Jinja2 template to format message (e.g., "Urgent: {{ event }} at {{ time }}").
     // If draft requested, set recipient to user_email and is_draft to true.
     // Output as JSON: { "functionName": "sendNotification", "parameters": { "recipient": "user@example.com", "message": "Urgent: Meeting at 10 AM", "channel": "email", "is_draft": true } }
     ```
   - Copilot identifies entities (e.g., team, event, time, draft intent) and suggests a Jinja2 template.

3. **Format Message with Jinja2**:
   - Define a Jinja2 template (e.g., "Urgent: {{ event }} at {{ time }} for {{ team }}") based on conversation context.
   - Render the template with extracted parameters (e.g., `event="Meeting"`, `time="10 AM"`, `team="DevOps"`).
   - Copilot can suggest template variations or refine them based on conversation nuances.

4. **Handle Draft Option**:
   - If the conversation includes phrases like "send a draft" or "to me first," set `is_draft=true` and `recipient=user_email` (e.g., "user@example.com").
   - After user approval (e.g., via a follow-up conversation), re-run with `is_draft=false` and `recipient=team` (e.g., "devops@company.com").

5. **Validate and Send Notification**:
   - Validate the JSON output against the API schema (e.g., valid recipient, non-empty message).
   - Send a POST request to the REST API with the payload.
   - If `is_draft=true`, log the draft sent to the user; otherwise, confirm team notification.

6. **Iterate for Multi-Turn Conversations**:
   - Track state (e.g., draft sent, user approval) using variables or Copilot Studio.
   - Re-run on new messages to update parameters or confirm draft approval.

#### Example Implementation (Python with Jinja2 and REST API)
Below is a Python script that integrates Jinja2 for message formatting, handles the draft option, and sends notifications via a REST API. The script assumes a RESTer-like service and a user email for drafts.

<xaiArtifact artifact_id="6abad62a-9a4f-438d-9ac0-bec86246456a" artifact_version_id="cbca918f-8d75-479e-91ca-5107f2296f15" title="notify_team.py" contentType="text/python">
import json
import requests
from jinja2 import Template

# Predefined function to send notification via REST API
def sendNotification(recipient, message, channel, is_draft=False):
    payload = {
        "recipient": recipient,
        "message": message,
        "channel": channel,
        "is_draft": is_draft
    }
    response = requests.post("https://api.rester.example/notify", json=payload)
    return response.json()

# Jinja2 template for notification message
notification_template = "Urgent: {{ event }} at {{ time }} for {{ team }}"

# Simulated user email for drafts
user_email = "user@example.com"

# Step 1: Conversation input
conversation = """
Human: Notify DevOps about the urgent meeting tomorrow at 10 AM, but send a draft to me first.
"""

# Step 2: Parse conversation (Copilot-generated logic)
def parse_conversation(convo):
    # Simulated Copilot output: parse entities and detect draft intent
    params = {
        "event": "Meeting",
        "time": "10 AM tomorrow",
        "team": "DevOps",
        "draft_requested": "draft to me" in convo.lower()
    }

    # Step 3: Format message with Jinja2
    template = Template(notification_template)
    message = template.render(event=params["event"], time=params["time"], team=params["team"])

    # Step 4: Set recipient based on draft option
    recipient = user_email if params["draft_requested"] else "devops@company.com"
    is_draft = params["draft_requested"]

    return {
        "functionName": "sendNotification",
        "parameters": {
            "recipient": recipient,
            "message": message,
            "channel": "email",
            "is_draft": is_draft
        }
    }

# Step 5: Execute
extracted = parse_conversation(conversation)

# Validate parameters
if not extracted["parameters"]["recipient"] or not extracted["parameters"]["message"]:
    raise ValueError("Invalid parameters")

# Send notification
result = sendNotification(**extracted["parameters"])
print(result)  # Example: {"status": "success", "message": "Notification sent"}
</xaiArtifact>

#### How It Works
- **Conversation Parsing**: The `parse_conversation` function simulates Copilot-generated logic, extracting entities (e.g., `event`, `time`, `team`) and detecting draft requests. In an IDE, Copilot would autocomplete this based on the prompt.
- **Jinja2 Templating**: The `notification_template` is rendered with extracted parameters to create a formatted message (e.g., "Urgent: Meeting at 10 AM tomorrow for DevOps").
- **Draft Option**: If "draft" is detected, the recipient is set to `user_email`, and `is_draft=true`. After user approval (e.g., via a new conversation message like "Approved"), re-run with the team recipient.
- **REST API Call**: The `sendNotification` function sends the payload to the REST API. The API can handle `is_draft` to route the notification appropriately (e.g., to a preview queue for drafts).
- **Extensibility**: Use Copilot Studio for multi-turn dialog management or GitHub Copilot Workspace for collaborative refinement.

#### Benefits and Considerations
- **Flexibility**: Jinja2 templates allow reusable, customizable message formats.
- **Draft Support**: Enables proofreading without spamming the team, improving reliability.
- **Scalability**: Add more templates or channels (e.g., Slack, Teams) by extending the script.
- **Limitations**: Copilot’s parsing accuracy depends on conversation clarity. Test with ambiguous inputs (e.g., "send it to me first" vs. "draft").
- **Security**: Ensure the REST API requires authentication (e.g., API keys) and validate user_email.

If you have specific API details (e.g., endpoint, payload schema), more conversation examples, or additional channels/templates, I can further customize the script. Let me know if you want a JavaScript version or integration with specific platforms like Slack!