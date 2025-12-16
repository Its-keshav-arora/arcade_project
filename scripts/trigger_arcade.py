import os
from arcadepy import Arcade

def main():
    # 1. Connect to Arcade
    client = Arcade(api_key=os.environ.get("ARCADE_API_KEY"))
    
    # 2. Gather Data from Environment (passed from the YAML file)
    pr_title = os.environ.get("PR_TITLE")
    pr_url = os.environ.get("PR_URL")
    author = os.environ.get("PR_AUTHOR")
    
    # YOUR EMAIL HERE: This determines which Slack account sends the message
    user_email = "keshav11y@gmail.com" 

    print(f"Triggering Arcade for PR: {pr_title} by {author}...")

    # 3. Call the MCP Tool
    # Ensure 'tool_name' matches exactly what you defined in your MCP server code
    try:
        result = client.tools.execute(
            tool_name="announce_pr", 
            input={
                "pr_title": pr_title,
                "pr_url": pr_url,
                "author": author,
                "channel_id": "C0A3XH9RZJ6" # Replace with your Slack Channel ID
            },
            user_id=user_email
        )
        print("Success! Response from MCP Server:")
        print(result)
        
    except Exception as e:
        print(f"Error calling Arcade: {e}")
        # Build fail ensures you see the red 'X' in GitHub if it fails
        exit(1) 

if __name__ == "__main__":
    main()