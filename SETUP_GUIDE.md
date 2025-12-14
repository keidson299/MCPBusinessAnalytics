# Setup & Configuration Guide

Complete step-by-step guide to get the Business Analytics MCP server running with Claude Desktop.

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **Claude Desktop**: Latest version
- **Disk Space**: ~50MB for dependencies

## Installation Steps

### Step 1: Prepare Your Environment

1. Open PowerShell or Command Prompt
2. Navigate to the project directory:

   ```powershell
   cd d:\VisualStudio\GitProjects\MCPBusinessAnalytics
   ```

3. Create a Python virtual environment (optional but recommended):

   ```powershell
   python -m venv venv
   ```

4. Activate the virtual environment:

   ```powershell
   # Windows
   .\venv\Scripts\Activate.ps1

   # macOS/Linux
   source venv/bin/activate
   ```

### Step 2: Install Dependencies

Install the required Python package:

```powershell
pip install fastmcp
```

Verify installation:

```powershell
pip show fastmcp
```

## Starting the MCP Server

### Method 1: Direct Execution (for testing)

```powershell
cd d:\VisualStudio\GitProjects\MCPBusinessAnalytics
python main.py
```

**Expected Output:**

```
Starting Business Analytics MCP Server...
```

The server is now running and ready to receive connections. Leave this terminal open.

### Method 2: Background Execution (for production)

Use Windows Task Scheduler or a background process manager to run the server automatically.

## Connecting to Claude Desktop

### Step 1: Locate the Configuration File

Find your Claude Desktop configuration file:

**Windows:**

- Path: `C:\Users\[YourUsername]\AppData\Roaming\Claude\claude_desktop_config.json`
- Quick access: Press `Win + R`, type `%APPDATA%\Claude\`, press Enter

**macOS:**

- Path: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Linux:**

- Path: `~/.config/Claude/claude_desktop_config.json`

### Step 2: Edit the Configuration File

Open `claude_desktop_config.json` in a text editor (VS Code, Notepad, etc.)

**Current content** (if first time):

```json
{
  "mcpServers": {}
}
```

**Updated content** - Add the business-analytics server:

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

### Step 3: Verify the Configuration

Before restarting Claude, test the path works:

```powershell
python d:\VisualStudio\GitProjects\MCPBusinessAnalytics\main.py
```

It should output: `Starting Business Analytics MCP Server...`

Press `Ctrl + C` to stop it.

### Step 4: Restart Claude Desktop

1. **Close Claude Desktop completely** (not just minimize)

   - Windows: Check Task Manager to ensure all Claude processes are closed
   - macOS: Quit Claude from the menu bar

2. **Wait 10 seconds**

3. **Reopen Claude Desktop**

4. **Verify the connection:**
   - Look for the MCP icon in Claude's interface
   - Try asking: "What MCP tools are available?"
   - Should see: business-analytics server with all analysis tools

## Testing the Connection

### Test 1: Health Check

Ask Claude: "Run a health check on the business analytics server"

Expected response should show:

- Status: healthy
- Timestamp: current date/time
- Capabilities: email_analysis, spreadsheet_analysis

### Test 2: Email Analysis

Ask Claude to analyze an email:

```
Analyze this email:
From: Sarah Chen <sarah@acme.com>
To: team@acme.com
Subject: Q4 Revenue Report - ACTION REQUIRED
Body: Team,
Please submit your Q4 projections by Friday.
This is critical for budget planning.
I need detailed breakdowns by region.
Thanks,
Sarah
```

Expected response should identify:

- Sender: Sarah Chen (sarah@acme.com)
- Urgency: Detected
- Tone: Formal, negative/critical
- Action items: Submit Q4 projections, provide detailed breakdowns

### Test 3: Spreadsheet Analysis

Ask Claude to analyze data:

```
Analyze the sales trends in this data:
[
  {"Quarter": "Q1", "Sales": 45000, "Region": "East"},
  {"Quarter": "Q1", "Sales": 38000, "Region": "West"},
  {"Quarter": "Q2", "Sales": 52000, "Region": "East"},
  {"Quarter": "Q2", "Sales": 41000, "Region": "West"}
]
```

Expected response should show statistics and patterns.

## Troubleshooting

### Issue: "Command not found: python"

**Solution:**

1. Verify Python is installed: `python --version`
2. If not installed, download from python.org
3. During installation, check "Add Python to PATH"
4. Restart your terminal

### Issue: "ModuleNotFoundError: No module named 'fastmcp'"

**Solution:**

```powershell
pip install --upgrade fastmcp
```

Or in virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
pip install fastmcp
```

### Issue: Claude Desktop doesn't show the MCP server

**Solution:**

1. Check config file syntax (use JSON validator)
2. Verify the file path in config is correct
3. Use absolute path with forward slashes or escaped backslashes:
   ```json
   "args": ["d:/VisualStudio/GitProjects/MCPBusinessAnalytics/main.py"]
   ```
4. Test Python path works in terminal
5. Fully close Claude (check Task Manager/Activity Monitor)
6. Restart Claude Desktop
7. Check Claude's logs (if available)

### Issue: Server crashes or hangs

**Solution:**

1. Check logs folder for error messages
2. Run server directly to see error output:
   ```powershell
   python main.py
   ```
3. Check for Python syntax errors:
   ```powershell
   python -m py_compile main.py
   ```

### Issue: Tools not responding

**Solution:**

1. Verify server is still running (check terminal)
2. Check task manager for Python process
3. Restart Claude Desktop
4. Restart the server

## Advanced Configuration

### Custom Server Name

Change the server identifier in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-analytics": {
      // Change "business-analytics" to any name
      "command": "python",
      "args": ["d:\\VisualStudio\\GitProjects\\MCPBusinessAnalytics\\main.py"]
    }
  }
}
```

### Multiple Servers

You can run multiple MCP servers simultaneously:

```json
{
  "mcpServers": {
    "business-analytics": {
      "command": "python",
      "args": ["path/to/business/analytics/main.py"]
    },
    "other-server": {
      "command": "python",
      "args": ["path/to/other/main.py"]
    }
  }
}
```

### Environment Variables

To pass environment variables to the server:

```json
{
  "mcpServers": {
    "business-analytics": {
      "command": "python",
      "args": ["d:\\VisualStudio\\GitProjects\\MCPBusinessAnalytics\\main.py"],
      "env": {
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

## Next Steps

Once connected:

1. **Try different analysis tools** - Practice with various email and spreadsheet formats
2. **Read the main README.md** - Understand all available tools and capabilities
3. **Explore the code** - Check out how analyzers work in the `analyzers/` folder
4. **Customize** - Add new analysis functions as needed

## Support

For issues:

1. Check the logs/ folder for error messages
2. Review README.md for tool documentation
3. Run tests directly: `python main.py`
4. Verify Python installation and dependencies

## Security Notes

- Keep config file path secure
- Don't share API keys or credentials via Claude
- Run server in a trusted environment
- Consider using a virtual environment for isolation
