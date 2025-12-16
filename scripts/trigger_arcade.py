import os
import sys

try:
    from arcadepy import Arcade
except ImportError:
    print("Error: arcadepy not installed. Installing...")
    os.system(f"{sys.executable} -m pip install arcadepy")
    from arcadepy import Arcade

def main():
    # 1. Connect to Arcade
    api_key = os.environ.get("ARCADE_API_KEY")
    if not api_key:
        print("Error: ARCADE_API_KEY environment variable not set")
        exit(1)
    
    client = Arcade(api_key=api_key)
    
    # 2. Gather Data from Environment (passed from the YAML file)
    pr_title = os.environ.get("PR_TITLE")
    pr_url = os.environ.get("PR_URL")
    author = os.environ.get("PR_AUTHOR")
    
    if not all([pr_title, pr_url, author]):
        print("Error: Missing PR information from environment variables")
        print(f"PR_TITLE: {pr_title}")
        print(f"PR_URL: {pr_url}")
        print(f"PR_AUTHOR: {author}")
        exit(1)
    
    
    # YOUR EMAIL HERE: This determines which Slack account sends the message
    user_email = "github_bot" 

    print(f"Triggering Arcade for PR: {pr_title} by {author}...")
    print(f"PR URL: {pr_url}")

    # 3. Get the Slack bot token from environment
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    if not slack_bot_token:
        print("Error: SLACK_BOT_TOKEN environment variable not set")
        exit(1)
    
    # 4. Call the Arcade Tool
    # Ensure 'tool_name' matches exactly what you defined in your tool code (main.py)
    try:
        result = client.tools.execute(
            tool_name="announce_pr", 
            input={
                "pr_title": pr_title,
                "pr_url": pr_url,
                "author": author,
                "channel_id": "C0A3XH9RZJ6", # Replace with your Slack Channel ID if needed
                "slack_bot_token": slack_bot_token  # Pass the bot token to use your "Github Bot"
            },
            user_id=user_email
        )
        print("Success! Response from Arcade:")
        print(result)
        
    except Exception as e:
        print(f"Error calling Arcade: {e}")
        import traceback
        traceback.print_exc()
        # Build fail ensures you see the red 'X' in GitHub if it fails
        exit(1) 

if __name__ == "__main__":
    main()