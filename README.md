# Business Analytics MCP Server

A Model Context Protocol (MCP) server for analyzing business emails and spreadsheet data. Integrates with Claude Desktop to provide intelligent analysis tools.

## Features

### Email Analysis

- Extract sender information (name, email, domain)
- Parse and categorize recipients (To, CC, BCC)
- Analyze email content for tone, urgency, and key topics
- Extract action items and estimate reading time

### Spreadsheet Analysis

- Validate spreadsheet structure and data quality
- Perform statistical analysis on numeric columns
- Detect patterns and trends in data
- Filter data by various criteria
- Aggregate data with grouping operations

## Quick Start

### Prerequisites

- Python 3.8+
- Claude Desktop (latest version)
- pip package manager

### Installation

1. **Clone or navigate to the project directory:**

   ```bash
   cd d:\VisualStudio\GitProjects\MCPBusinessAnalytics
   ```

2. **Install dependencies:**

   ```bash
   pip install fastmcp
   ```

3. **Verify the installation:**
   ```bash
   python main.py --help
   ```

## Running the MCP Server

### Start the Server

Open PowerShell and run:

```bash
python main.py
```

The server will start with output:

```
Starting Business Analytics MCP Server...
```

The server runs in stdio mode and communicates with Claude Desktop through standard input/output.

## Connecting to Claude Desktop

### Step 1: Locate Claude Desktop Config

The MCP server configuration file is typically located at:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Step 2: Update Claude Desktop Configuration

Edit your Claude Desktop config file and add the MCP server:

```json
{
  "mcpServers": {
    "business-analytics": {
      "command": "python",
      "args": ["Path To Project\\MCPBusinessAnalytics\\main.py"]
    }
  }
}
```

**Note:** Use forward slashes or double backslashes for the path on Windows.

### Step 3: Restart Claude Desktop

After updating the config, fully close and restart Claude Desktop. The MCP server will now be available.

## Using the Server with Claude

Once connected, Claude will have access to the following tools:

### Email Analysis Tools

**1. `analyze_eml_file`**

- Processes .eml email files and runs comprehensive analysis
- Input: file path to .eml file
- Returns: sender info, recipient details, content analysis
- Automatically extracts all email headers and body content

**2. `analyze_business_email` (Comprehensive)**

- Analyzes all aspects of an email
- Input: sender, recipients (to, cc, bcc), subject, body
- Returns: sender info, recipient details, content analysis

**3. `extract_sender_details`**

- Extracts only sender information
- Input: sender email
- Returns: name, email, domain

**4. `extract_recipients_details`**

- Extracts recipient information
- Input: to, cc, bcc recipients
- Returns: parsed recipients with domains

**5. `analyze_email_body`**

- Analyzes email content only
- Input: subject, body
- Returns: tone, urgency, topics, action items, reading time

### Spreadsheet Analysis Tools

**1. `validate_spreadsheet`**

- Checks data structure and quality
- Input: list of row dictionaries
- Returns: validation results, missing values, data types

**2. `analyze_numeric_data`**

- Statistical analysis on a column
- Input: data, column name
- Returns: mean, median, std dev, min, max, quartiles

**3. `detect_column_patterns`**

- Finds patterns in column data
- Input: data, column name
- Returns: unique values, frequency, duplicates

**4. `filter_spreadsheet_data`**

- Filters rows by criteria
- Input: data, column, operator (=, !=, >, <, >=, <=, contains), value
- Returns: filtered rows

**5. `aggregate_spreadsheet_data`**

- Groups and aggregates data
- Input: data, group_by column, aggregate_column, operation (sum, avg, count, min, max)
- Returns: aggregated results

### Utility Tools

**`health_check`**

- Verifies server is running
- Returns: status, timestamp, capabilities

## Example Usage in Claude

### Analyzing an .eml File

Ask Claude: "Analyze this email file for me: \path_to_email_file\email.eml"

Claude will use the `analyze_eml_file` tool to:

- Parse the .eml file
- Extract all headers (from, to, cc, bcc, subject)
- Extract the email body
- Run full content analysis

### Analyzing an Email

Ask Claude: "Analyze this email for me"

```
From: John Smith <john@company.com>
To: jane@company.com, Bob Johnson <bob@company.com>
Subject: URGENT: Project Update Needed ASAP
Body: Hi team,
We need the quarterly report by tomorrow. Can you please prioritize this?
This is critical for our presentation.
Thanks,
John
```

Claude will use the `analyze_business_email` tool to extract:

- Sender: John Smith from company.com
- Recipients: jane@company.com, Bob Johnson from company.com
- Urgency: Detected (URGENT, ASAP, critical)
- Tone: Formal, negative (needs, critical)
- Action Items: "We need the quarterly report by tomorrow"

### Analyzing Spreadsheet Data

Ask Claude: "What are the statistics for the sales column?"

Provide your data as JSON:

```json
[
  { "Month": "January", "Sales": 5000, "Region": "North" },
  { "Month": "February", "Sales": 6200, "Region": "North" },
  { "Month": "March", "Sales": 5800, "Region": "South" }
]
```

Claude will use `analyze_numeric_data` to compute statistics.

## Project Structure

```
MCPBusinessAnalytics/
├── main.py                      # Server entry point
├── core/                        # Core utilities & models
│   ├── __init__.py
│   ├── models.py                # Data classes
│   └── utils.py                 # Shared utilities
├── analyzers/                   # Analysis modules
│   ├── __init__.py
│   ├── email_analyzer.py        # Email analysis functions
│   └── spreadsheet_analyzer.py  # Spreadsheet analysis functions
├── logs/                        # Server logs
├── README.md                    # This file
└── QUICKSTART.md                # Guide for starting the project
```

## Troubleshooting

### Server won't start

- Verify Python is installed: `python --version`
- Check fastmcp is installed: `pip list | findstr fastmcp`
- Ensure you're in the correct directory

### Claude Desktop doesn't recognize the server

- Verify the config file path is correct
- Check the python path in config is accurate
- Use forward slashes: `d:/path/to/main.py`
- Restart Claude Desktop completely (not just close)
- Make sure logs folder exists at %APPDATA%\Local\AnthropicClaude\app-version
- Check logs folder for error messages

### Import errors

- Ensure all Python files are in the correct folders
- Verify `__init__.py` files exist in core/ and analyzers/
- Run from project root directory

## Development

To add new analyzers:

1. Create a new module in `analyzers/` folder
2. Import required utilities from `core.utils`
3. Create analysis functions
4. Register as MCP tools in `main.py` using `@app.tool()` decorator
