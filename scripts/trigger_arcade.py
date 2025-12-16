import os
import sys
import re

try:
    from arcadepy import Arcade
except ImportError:
    print("Error: arcadepy not installed. Installing...")
    os.system(f"{sys.executable} -m pip install arcadepy")
    from arcadepy import Arcade

def extract_repo_info(pr_url):
    """Extract owner and repo from PR URL"""
    # Example: https://github.com/Its-keshav-arora/arcade_project/pull/3
    match = re.search(r'github\.com/([^/]+)/([^/]+)', pr_url)
    if match:
        return match.group(1), match.group(2)
    return None, None

def extract_pr_number(pr_url):
    """Extract PR number from PR URL"""
    match = re.search(r'/pull/(\d+)', pr_url)
    if match:
        return int(match.group(1))
    return None

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
    user_email = "keshav11y@gmail.com" 

    print(f"Processing PR: {pr_title} by {author}")
    print(f"PR URL: {pr_url}")

    # 3. Extract repo info from PR URL (optional - we can use GitHub tool to get more details)
    owner, repo = extract_repo_info(pr_url)
    pr_number = extract_pr_number(pr_url)
    
    # 4. Optionally get more PR details using Arcade's GitHub tool
    pr_details = None
    if owner and repo and pr_number:
        try:
            print(f"Fetching PR details from GitHub using Arcade...")
            pr_details = client.tools.execute(
                tool_name="GitHub.GetPullRequest",
                input={
                    "owner": owner,
                    "repo": repo,
                    "pull_number": pr_number
                },
                user_id=user_email
            )
            print(f"PR details retrieved: {pr_details}")
        except Exception as e:
            print(f"Warning: Could not fetch PR details from GitHub: {e}")
            print("Using basic PR information from GitHub Actions...")
    
    # 5. Format the Slack message
    if pr_details and isinstance(pr_details, dict):
        # Use detailed info from GitHub tool if available
        message_text = f"🚨 *New PR Raised* 🚨\n\n"
        message_text += f"*Title:* {pr_details.get('title', pr_title)}\n"
        message_text += f"*Author:* {pr_details.get('user', {}).get('login', author)}\n"
        message_text += f"*Link:* {pr_url}\n"
        if pr_details.get('body'):
            body_preview = pr_details['body'][:200] + "..." if len(pr_details.get('body', '')) > 200 else pr_details.get('body', '')
            message_text += f"\n*Description:* {body_preview}\n"
        message_text += f"\nPlease review! :eyes:"
    else:
        # Use basic info from GitHub Actions
        message_text = f"🚨 *New PR Raised by {author}* 🚨\n\n*Title:* {pr_title}\n*Link:* {pr_url}\n\nPlease review! :eyes:"

    # 6. Send message to Slack using Arcade's Slack.SendMessage tool
    try:
        print("Sending message to Slack...")
        result = client.tools.execute(
            tool_name="Slack.SendMessage",
            input={
                "conversation_id": "C0A3XH9RZJ6",  # Your Slack channel ID
                "text": message_text
            },
            user_id=user_email
        )
        print("Success! Message sent to Slack:")
        print(result)
        
    except Exception as e:
        print(f"Error calling Arcade Slack.SendMessage: {e}")
        import traceback
        traceback.print_exc()
        # Build fail ensures you see the red 'X' in GitHub if it fails
        exit(1) 

if __name__ == "__main__":
    main()