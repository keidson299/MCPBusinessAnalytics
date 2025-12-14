from fastmcp import FastMCP
import logging
import re
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime

app = FastMCP("Business Email Analysis MCP Server")

@dataclass
class EmailMessage:
    """Represents an email message with metadata and content"""
    sender: str
    recipients: List[str]
    cc: List[str]
    bcc: List[str]
    subject: str
    body: str
    date: Optional[str] = None
    message_id: Optional[str] = None


def extract_sender_info(email_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract sender information from email data.
    
    Args:
        email_data: Dictionary containing email metadata with 'from' or 'sender' field
        
    Returns:
        Dictionary with sender name, email, and domain
    """
    sender = email_data.get('from') or email_data.get('sender', '')
    
    # Parse sender format: "John Doe <john.doe@company.com>"
    name_match = re.match(r'^([^<]+)<([^>]+)>$', sender.strip())
    
    if name_match:
        sender_name = name_match.group(1).strip()
        sender_email = name_match.group(2).strip()
    else:
        sender_name = ''
        sender_email = sender.strip()
    
    # Extract domain from email
    domain = sender_email.split('@')[1] if '@' in sender_email else 'unknown'
    
    return {
        'name': sender_name,
        'email': sender_email,
        'domain': domain
    }


def extract_recipient_info(email_data: Dict[str, Any]) -> Dict[str, List[Dict[str, str]]]:
    """
    Extract recipient information from email data.
    
    Args:
        email_data: Dictionary containing email metadata with 'to', 'cc', 'bcc' fields
        
    Returns:
        Dictionary with parsed to, cc, and bcc recipients
    """
    def parse_recipients(recipient_string: str) -> List[Dict[str, str]]:
        """Parse recipient string into list of dicts with name and email"""
        if not recipient_string:
            return []
        
        recipients = []
        # Split by comma, but be careful with commas inside angle brackets
        email_pattern = r'([^<,]*)<([^>]+)>|([^,]+)'
        
        for match in re.finditer(email_pattern, recipient_string):
            if match.group(1) or match.group(2):  # Format: "Name <email>"
                name = match.group(1).strip() if match.group(1) else ''
                email = match.group(2).strip()
            else:  # Format: just email
                name = ''
                email = match.group(3).strip() if match.group(3) else ''
            
            if email:
                recipients.append({
                    'name': name,
                    'email': email,
                    'domain': email.split('@')[1] if '@' in email else 'unknown'
                })
        
        return recipients
    
    return {
        'to': parse_recipients(email_data.get('to', '')),
        'cc': parse_recipients(email_data.get('cc', '')),
        'bcc': parse_recipients(email_data.get('bcc', ''))
    }


def analyze_email_content(email_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the content and metadata of an email.
    
    Args:
        email_data: Dictionary containing email message with subject, body, and optional metadata
        
    Returns:
        Dictionary with content analysis including tone, key topics, urgency, and word count
    """
    subject = email_data.get('subject', '')
    body = email_data.get('body', '')
    full_text = f"{subject} {body}".lower()
    
    # Calculate word count
    word_count = len(body.split())
    
    # Detect urgency indicators
    urgency_keywords = ['urgent', 'asap', 'critical', 'emergency', 'immediately', 'deadline', 'priority', 'rush']
    has_urgency = any(keyword in full_text for keyword in urgency_keywords)
    
    # Detect tone
    tone_indicators = {
        'formal': ['dear', 'sincerely', 'regards', 'professional', 'meeting', 'proposal'],
        'casual': ['hi', 'hey', 'thanks', 'cheers', 'lol', 'cool'],
        'negative': ['problem', 'issue', 'error', 'failed', 'disappointed', 'concern', 'complaint'],
        'positive': ['great', 'excellent', 'success', 'happy', 'appreciate', 'thank you']
    }
    
    detected_tone = []
    for tone, keywords in tone_indicators.items():
        if any(kw in full_text for kw in keywords):
            detected_tone.append(tone)
    
    # Extract key topics (words appearing 3+ times, excluding common words)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'be', 'that', 'this', 'it', 'from'}
    words = [w for w in body.lower().split() if w.isalnum() and w not in stop_words and len(w) > 3]
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    key_topics = [word for word, count in sorted(word_freq.items(), key=lambda x: x[1], reverse=True) if count >= 2][:5]
    
    # Detect questions
    question_count = body.count('?')
    
    # Detect action items (lines with common action words)
    action_keywords = ['please', 'need', 'can you', 'could you', 'will you', 'would you', 'should', 'must', 'required']
    action_items = [line.strip() for line in body.split('\n') if any(kw in line.lower() for kw in action_keywords)]
    
    return {
        'word_count': word_count,
        'character_count': len(body),
        'question_count': question_count,
        'has_urgency': has_urgency,
        'detected_tone': detected_tone if detected_tone else ['neutral'],
        'key_topics': key_topics,
        'estimated_read_time_seconds': max(10, word_count // 200 * 60),
        'action_item_count': len(action_items),
        'action_items': action_items[:3]  # First 3 action items
    }


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


@app.tool()
async def analyze_file():
    print("Test log message to console")

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    logging.basicConfig(filename="logs/mcpServer.log", level=logging.INFO)

    logger.info("Starting MCP server...")
    app.run(transport="stdio")