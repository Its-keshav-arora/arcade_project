from arcade_tdk import tool, ToolContext
from slack_sdk import WebClient
import os

# Define the tool - using bot token from parameter or environment
@tool()
def announce_pr(context: ToolContext, pr_title: str, pr_url: str, author: str, channel_id: str, slack_bot_token: str = None) -> str:
    """
    Announces a new Pull Request to a specific Slack channel.
    
    Args:
        pr_title: Title of the pull request
        pr_url: URL of the pull request
        author: GitHub username of the PR author
        channel_id: Slack channel ID to send the message to
        slack_bot_token: OAuth token for your Slack bot (optional if set in Arcade environment)
    """
    
    # 1. Get the bot token from parameter or environment variable
    # Priority: parameter > environment variable
    # This allows you to use your specific "Github Bot" token
    slack_token = slack_bot_token or os.environ.get("SLACK_BOT_TOKEN")
    if not slack_token:
        return "Error: SLACK_BOT_TOKEN not provided. Either pass it as a parameter or set it in Arcade's environment variables."
    
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