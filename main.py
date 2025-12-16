from arcade_tdk import tool, ToolContext
from arcade_tdk.auth import Slack
from slack_sdk import WebClient

# Define the tool with Arcade's Slack Authorization wrapper
@tool(
    requires_auth=Slack(scopes=["chat:write"])
)
def announce_pr(context: ToolContext, pr_title: str, pr_url: str, author: str, channel_id: str) -> str:
    """
    Announces a new Pull Request to a specific Slack channel.
    """
    
    # 1. Get the auto-managed token from Arcade Context
    slack_token = context.authorization.token
    client = WebClient(token=slack_token)

    # 2. Format the message
    message_text = f"🚨 *New PR Raised by {author}* 🚨\n\n*Title:* {pr_title}\n*Link:* {pr_url}\n\nPlease review! :eyes:"

    # 3. Send to Slack
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=message_text
        )
        return f"Message sent successfully! Ts: {response['ts']}"
    except Exception as e:
        # In MCP, we return errors as strings or structured error types
        return f"Failed to send message: {str(e)}"