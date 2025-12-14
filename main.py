from fastmcp import FastMCP
import logging
from typing import Dict, Any, List
from datetime import datetime

# Import email analysis functions
from email_analyzer import (
    extract_sender_info,
    extract_recipient_info,
    analyze_email_content
)

# Import spreadsheet analysis functions
from spreadsheet_analyzer import (
    validate_spreadsheet_structure,
    analyze_numeric_column,
    detect_patterns,
    filter_data,
    aggregate_data
)

app = FastMCP("Business Analytics MCP Server")


# ========== EMAIL ANALYSIS TOOLS ==========

@app.tool()
async def analyze_business_email(
    email_from: str,
    email_to: str,
    email_subject: str,
    email_body: str,
    email_cc: str = "",
    email_bcc: str = ""
) -> Dict[str, Any]:
    """
    Comprehensive analysis of a business email including sender, recipients, and content analysis.
    
    Args:
        email_from: Sender information (e.g., "John Doe <john@company.com>")
        email_to: Recipients (e.g., "jane@company.com, Bob Smith <bob@company.com>")
        email_subject: Subject line of the email
        email_body: Body content of the email
        email_cc: CC recipients (optional)
        email_bcc: BCC recipients (optional)
        
    Returns:
        Comprehensive analysis dict with sender, recipients, and content insights
    """
    email_data = {
        'from': email_from,
        'to': email_to,
        'cc': email_cc,
        'bcc': email_bcc,
        'subject': email_subject,
        'body': email_body
    }
    
    return {
        'sender': extract_sender_info(email_data),
        'recipients': extract_recipient_info(email_data),
        'content_analysis': analyze_email_content(email_data),
        'timestamp': datetime.now().isoformat()
    }


@app.tool()
async def extract_sender_details(email_from: str) -> Dict[str, str]:
    """
    Extract and analyze sender information.
    
    Args:
        email_from: Sender information (e.g., "John Doe <john@company.com>")
        
    Returns:
        Dictionary with sender name, email, and domain
    """
    return extract_sender_info({'from': email_from})


@app.tool()
async def extract_recipients_details(
    email_to: str,
    email_cc: str = "",
    email_bcc: str = ""
) -> Dict[str, List[Dict[str, str]]]:
    """
    Extract and analyze recipient information.
    
    Args:
        email_to: To recipients
        email_cc: CC recipients (optional)
        email_bcc: BCC recipients (optional)
        
    Returns:
        Dictionary with parsed to, cc, and bcc recipients with their domains
    """
    email_data = {
        'to': email_to,
        'cc': email_cc,
        'bcc': email_bcc
    }
    return extract_recipient_info(email_data)


@app.tool()
async def analyze_email_body(email_subject: str, email_body: str) -> Dict[str, Any]:
    """
    Analyze email content for tone, urgency, key topics, and action items.
    
    Args:
        email_subject: Subject line of the email
        email_body: Body content of the email
        
    Returns:
        Dictionary with content analysis including tone, urgency, topics, and action items
    """
    email_data = {
        'subject': email_subject,
        'body': email_body
    }
    return analyze_email_content(email_data)


# ========== SPREADSHEET ANALYSIS TOOLS ==========

@app.tool()
async def validate_spreadsheet(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate and analyze spreadsheet structure and quality.
    
    Args:
        data: List of row dictionaries from spreadsheet
        
    Returns:
        Dictionary with structure validation results and data quality metrics
    """
    return validate_spreadsheet_structure(data)


@app.tool()
async def analyze_numeric_data(
    data: List[Dict[str, Any]],
    column: str
) -> Dict[str, Any]:
    """
    Perform statistical analysis on numeric column data.
    
    Args:
        data: List of row dictionaries from spreadsheet
        column: Column name to analyze
        
    Returns:
        Dictionary with statistical metrics (sum, mean, median, std_dev, min, max, etc.)
    """
    return analyze_numeric_column(data, column)


@app.tool()
async def detect_column_patterns(
    data: List[Dict[str, Any]],
    column: str
) -> Dict[str, Any]:
    """
    Detect patterns and trends in column data.
    
    Args:
        data: List of row dictionaries from spreadsheet
        column: Column name to analyze
        
    Returns:
        Dictionary with unique values, frequency counts, and duplicates
    """
    return detect_patterns(data, column)


@app.tool()
async def filter_spreadsheet_data(
    data: List[Dict[str, Any]],
    column: str,
    operator: str,
    value: Any
) -> List[Dict[str, Any]]:
    """
    Filter spreadsheet data based on column criteria.
    
    Args:
        data: List of row dictionaries from spreadsheet
        column: Column name to filter on
        operator: Comparison operator ('=', '!=', '>', '<', '>=', '<=', 'contains')
        value: Value to compare against
        
    Returns:
        Filtered list of rows matching the criteria
    """
    return filter_data(data, column, operator, value)


@app.tool()
async def aggregate_spreadsheet_data(
    data: List[Dict[str, Any]],
    group_by: str,
    aggregate_column: str,
    operation: str
) -> List[Dict[str, Any]]:
    """
    Aggregate spreadsheet data by grouping and performing operations.
    
    Args:
        data: List of row dictionaries from spreadsheet
        group_by: Column to group by
        aggregate_column: Column to aggregate
        operation: Operation to perform ('sum', 'avg', 'count', 'min', 'max')
        
    Returns:
        List of aggregated results with group and calculated values
    """
    return aggregate_data(data, group_by, aggregate_column, operation)


# ========== UTILITY TOOL ==========

@app.tool()
async def health_check() -> Dict[str, str]:
    """
    Check if the MCP server is running and responsive.
    
    Returns:
        Dictionary with status and timestamp
    """
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'capabilities': ['email_analysis', 'spreadsheet_analysis']
    }


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="logs/mcpServer.log", level=logging.INFO)
    
    logger.info("Starting Business Analytics MCP Server...")
    app.run(transport="stdio")
