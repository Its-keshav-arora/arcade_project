# GitHub PR to Slack Notification using Arcade MCP
<!-- test commit -->

This project automatically sends Slack notifications to your team whenever a Pull Request (PR) is opened in your GitHub repository. It uses [Arcade.dev](https://arcade.dev) MCP (Model Context Protocol) server to seamlessly integrate GitHub and Slack.

## 🎯 What This Project Does

When someone opens a Pull Request in your GitHub repository, this automation:
- Fetches detailed PR information using Arcade's GitHub integration
- Formats a comprehensive notification message
- Sends it automatically to your designated Slack channel
- Includes PR title, author, description, repository details, and direct link

## 📋 Prerequisites

Before setting up this project, ensure you have:

1. **GitHub Account** - A repository where you want to enable PR notifications
2. **Slack Workspace** - Access to a Slack workspace and channel
3. **Arcade Account** - An account on [arcade.dev](https://arcade.dev)
4. **Python 3.10+** - For running the automation script

## 🔑 Getting Your Arcade API Key

1. Go to [arcade.dev](https://arcade.dev)
2. Create your account (or sign in if you already have one)
3. Navigate to the dashboard: [https://api.arcade.dev/dashboard/](https://api.arcade.dev/dashboard/)
4. Click on **"Get API Key"**
5. Copy your API key - you'll need it in the next step

## 🚀 Setup Instructions

### Step 1: Add Arcade API Key to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Name: `ARCADE_API_KEY`
5. Value: Paste your Arcade API key
6. Click **"Add secret"**

### Step 2: Configure the Script

Open `scripts/trigger_arcade.py` and update the following:

```python
# Line 50: Replace with your email address
user_email = "your-email@example.com"  # This email will be used to send messages in Slack
```

Also update the Slack channel name (line 139):

```python
"channel_name": "your-slack-channel-name",  # Replace with your actual Slack channel name
```

### Step 3: Authorize Arcade Tools

Before the automation can work, you need to authorize the Arcade tools:

1. **GitHub Authorization:**
   - The script will attempt to authorize automatically
   - If authorization is required, visit the URL provided in the logs
   - Complete the authorization in the Arcade dashboard

2. **Slack Authorization:**
   - Similarly, authorize the Slack integration
   - Grant permissions to send messages to your Slack workspace

> **Note:** These authorizations are one-time setup steps. Once completed, the automation will work seamlessly.

### Step 4: Verify Workflow File

Ensure the workflow file exists at `.github/workflows/slack-notify.yml`. The workflow is already configured to:
- Trigger automatically when a PR is opened
- Install dependencies (`arcadepy`)
- Run the trigger script with necessary environment variables

## 🔧 How It Works

### Workflow Overview

1. **GitHub Action Trigger:** When a PR is opened, GitHub Actions automatically runs the workflow
2. **Environment Setup:** The workflow sets up Python and installs `arcadepy`
3. **Script Execution:** Runs `scripts/trigger_arcade.py` with PR details as environment variables
4. **Arcade Integration:** The script uses Arcade's MCP tools to:
   - Fetch PR details from GitHub
   - Send formatted message to Slack

### Arcade Tools Used

This project uses two Arcade MCP tools:

1. **`GitHub.GetPullRequest`**
   - Fetches comprehensive PR details including:
     - PR title and description
     - Author information
     - Repository details
     - PR number and state
     - Base and head branches
     - Full PR metadata

2. **`Slack.SendMessage`**
   - Sends formatted messages to your Slack channel
   - Uses `user_email` to identify the message sender
   - Supports Slack markdown formatting

### Message Format

The Slack notification includes:
- 🚨 Alert emoji for visibility
- PR title and author
- Repository name and PR number
- PR state and branch information
- Direct link to the PR
- PR description (truncated to 200 characters if long)
- Call-to-action for review

## 📁 Project Structure

```
arcade_project/
├── .github/
│   └── workflows/
│       └── slack-notify.yml      # GitHub Actions workflow
├── scripts/
│   └── trigger_arcade.py         # Main automation script
├── main.py                        # (Optional - not used in workflow)
├── pyproject.toml                 # Project dependencies
└── README.md                      # This file
```

## 🧪 Testing

To test the setup:

1. Create a new branch in your repository
2. Make a small change (e.g., update README)
3. Open a Pull Request
4. Check your Slack channel - you should receive a notification automatically!

## 🔍 Troubleshooting

### Issue: "ARCADE_API_KEY environment variable not set"
- **Solution:** Ensure you've added the API key to GitHub Secrets (Step 1)

### Issue: "GitHub authorization required"
- **Solution:** Visit the authorization URL provided in the logs and complete the OAuth flow in Arcade dashboard

### Issue: "Slack authorization required"
- **Solution:** Authorize Slack integration in Arcade dashboard

### Issue: Message not appearing in Slack
- **Solution:** 
  - Verify the channel name is correct (case-sensitive)
  - Ensure the bot/user has permission to post in the channel
  - Check that Slack authorization is completed

### Issue: PR details not fetching
- **Solution:** 
  - Verify GitHub authorization is complete
  - Check that the repository owner and name are correct
  - Ensure the PR number is valid

## 📝 Configuration Variables

| Variable | Description | Where to Set |
|----------|-------------|--------------|
| `ARCADE_API_KEY` | Your Arcade API key | GitHub Secrets |
| `user_email` | Email for Slack message author | `scripts/trigger_arcade.py` (line 50) |
| `channel_name` | Slack channel name | `scripts/trigger_arcade.py` (line 139) |

## 🔐 Security Notes

- Never commit your Arcade API key to the repository
- Always use GitHub Secrets for sensitive information
- The `user_email` should be an email associated with your Arcade account
- Ensure your GitHub Actions have appropriate permissions

## 📚 Additional Resources

- [Arcade.dev Documentation](https://arcade.dev)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Arcade Dashboard](https://api.arcade.dev/dashboard/)

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve this automation!

## 📄 License

This project is open source and available for use in your own repositories.

---

**Do Subscribe to ByteMonk for Awesome Projects like these 🚀**
<br>
**Thanks!**
