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
    # Example: https://github.com/<owner-name>/arcade_project/pull/3
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
    
    # 4. Authorize GitHub tool if needed, then get PR details
    pr_details = None
    if owner and repo and pr_number:
        try:
            # Check/authorize GitHub tool
            print("Checking GitHub authorization...")
            github_auth = client.tools.authorize(
                tool_name="GitHub.GetPullRequest",
                user_id=user_email
            )
            if github_auth.status != "completed":
                print(f"Warning: GitHub authorization required. Visit: {github_auth.url}")
                print("Note: Authorization must be completed in Arcade dashboard before automation can work.")
            
            print(f"Fetching PR details from GitHub using Arcade...")
            pr_response = client.tools.execute(
                tool_name="GitHub.GetPullRequest",
                input={
                    "owner": owner,
                    "repo": repo,
                    "pull_number": pr_number
                },
                user_id=user_email
            )
            # Extract the value from the response
            if hasattr(pr_response, 'output') and hasattr(pr_response.output, 'value'):
                pr_details = pr_response.output.value
            elif isinstance(pr_response, dict) and 'output' in pr_response:
                pr_details = pr_response['output'].get('value')
            else:
                pr_details = pr_response
            print(f"PR details retrieved successfully")
        except Exception as e:
            print(f"Warning: Could not fetch PR details from GitHub: {e}")
            print("Using basic PR information from GitHub Actions...")
    
    # 5. Format the Slack message with repository update details
    if pr_details and isinstance(pr_details, dict):
        # Use detailed info from GitHub tool if available
        message_text = f"🚨 *Repository Update: New Pull Request* 🚨\n\n"
        message_text += f"*Title:* {pr_details.get('title', pr_title)}\n"
        message_text += f"*Author:* {pr_details.get('user', author)}\n"
        message_text += f"*Repository:* {owner}/{repo}\n"
        message_text += f"*PR #:* {pr_number}\n"
        message_text += f"*State:* {pr_details.get('state', 'open')}\n"
        message_text += f"*Base Branch:* {pr_details.get('base', 'main')} ← *Head Branch:* {pr_details.get('head', 'unknown')}\n"
        message_text += f"*Link:* {pr_url}\n"
        if pr_details.get('body'):
            body_preview = pr_details['body'][:200] + "..." if len(str(pr_details.get('body', ''))) > 200 else str(pr_details.get('body', ''))
            message_text += f"\n*Description:*\n{body_preview}\n"
        message_text += f"\nPlease review! :eyes:"
    else:
        # Use basic info from GitHub Actions
        message_text = f"🚨 *Repository Update: New Pull Request* 🚨\n\n"
        message_text += f"*Title:* {pr_title}\n"
        message_text += f"*Author:* {author}\n"
        message_text += f"*Link:* {pr_url}\n"
        message_text += f"\nPlease review! :eyes:"

    # 6. Authorize Slack tool if needed
    try:
        print("Checking Slack authorization...")
        auth_response = client.tools.authorize(
            tool_name="Slack.SendMessage",
            user_id=user_email
        )
        if auth_response.status != "completed":
            print(f"Warning: Slack authorization required. Visit: {auth_response.url}")
            print("Note: Authorization must be completed in Arcade dashboard before automation can work.")
            # For automation, we'll try to proceed - authorization should be done beforehand
    except Exception as e:
        print(f"Warning: Could not check authorization: {e}")
        print("Proceeding with execution (assuming authorization is already complete)...")

    # 7. Send message to Slack using Arcade's Slack.SendMessage tool
    try:
        print("Sending message to Slack...")
        result = client.tools.execute(
            tool_name="Slack.SendMessage",
            input={
                "channel_name": "repository-updates",  # Your Slack channel name
                "message": message_text  # Use 'message' not 'text'
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