# Quick Start (5 Minutes)

## 1. Install Dependencies

```powershell
cd d:\VisualStudio\GitProjects\MCPBusinessAnalytics
pip install fastmcp
```

## 2. Update Claude Desktop Config

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

## 3. Restart Claude Desktop

Close Claude completely and reopen it.

## 4. Test in Claude

Ask: **"What tools are available?"**

You should see email and spreadsheet analysis tools listed.

## 5. Try an Analysis

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
