"""Data models for business analytics MCP server"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class EmailMessage:
    """Represents an email message with metadata and content"""
    sender: str
    recipients: List[str]
    subject: str
    body: str
    cc: List[str] = field(default_factory=list)
    bcc: List[str] = field(default_factory=list)
    date: Optional[str] = None
    message_id: Optional[str] = None


@dataclass
class SpreadsheetData:
    """Represents spreadsheet data with metadata"""
    filename: str
    sheets: List[str]
    row_count: int
    column_count: int
    data: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CellAnalysis:
    """Analysis result for a spreadsheet cell or range"""
    location: str
    value: Any
    data_type: str
    analysis: Dict[str, Any] = field(default_factory=dict)
