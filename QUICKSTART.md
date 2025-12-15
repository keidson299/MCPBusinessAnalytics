# Quick Start (5 Minutes)

## 1. Install Dependencies

```powershell
cd d:\VisualStudio\GitProjects\MCPBusinessAnalytics
pip install fastmcp
```

## 2. Starting the MCP Server

In a PowerShell terminal run the command:

```powershell
python main.py
```

You should see a FastMCP startup text, and no further output as the server communicates through stdin/stdout.

## 3. Update Claude Desktop Config

Edit: `%APPDATA%\Claude\claude_desktop_config.json`

Add this:

```json
{
  "mcpServers": {
    "business-analytics": {
      "command": "python",
      "args": ["d:\\VisualStudio\\GitProjects\\MCPBusinessAnalytics\\main.py"]
    }
  }
}
```

## 4. Restart Claude Desktop

Close Claude completely and reopen it.

## 5. Test in Claude

Ask: **"What tools are available?"**

You should see email and spreadsheet analysis tools listed.

## 6. Try an Analysis

**For .eml File:**

```
Analyze this email file: \path_to_email_file\email.eml
```

Claude will parse the .eml file and provide full analysis including sender, recipients, and content insights.

**For Email:**

```
Analyze this email:
From: boss@company.com
To: me@company.com
Subject: URGENT - Report Due Tomorrow
Body: Need the sales report ASAP. Critical for the board meeting.
```

**For Spreadsheet:**

```
Analyze this data:
[{"Product": "A", "Sales": 1000}, {"Product": "B", "Sales": 1500}]

What are the statistics on the Sales column?
```

## Done! 🎉

Read [README.md](README.md) for detailed documentation on all available tools.

### Troubleshooting

- Server won't start? Check Python is installed: `python --version`
- Claude doesn't see server? Verify config path and restart Claude completely
- Still stuck? See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting
