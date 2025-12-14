"""Email analysis functions for business analytics MCP server"""

from typing import Dict, Any, List
from core.utils import (
    parse_email_address, parse_recipients, extract_domain,
    extract_key_topics, detect_tone, detect_urgency, extract_action_items
)


def extract_sender_info(email_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract sender information from email data.
    
    Args:
        email_data: Dictionary containing email metadata with 'from' or 'sender' field
        
    Returns:
        Dictionary with sender name, email, and domain
    """
    sender = email_data.get('from') or email_data.get('sender', '')
    sender_name, sender_email = parse_email_address(sender)
    domain = extract_domain(sender_email)
    
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
        Dictionary with content analysis including tone, urgency, topics, and word count
    """
    subject = email_data.get('subject', '')
    body = email_data.get('body', '')
    full_text = f"{subject} {body}"
    
    # Calculate word count
    word_count = len(body.split())
    
    # Detect urgency
    has_urgency = detect_urgency(full_text)
    
    # Detect tone
    detected_tone = detect_tone(full_text)
    
    # Extract key topics
    key_topics = extract_key_topics(body, top_n=5)
    
    # Detect questions
    question_count = body.count('?')
    
    # Extract action items
    action_items = extract_action_items(body, max_items=3)
    
    return {
        'word_count': word_count,
        'character_count': len(body),
        'question_count': question_count,
        'has_urgency': has_urgency,
        'detected_tone': detected_tone,
        'key_topics': key_topics,
        'estimated_read_time_seconds': max(10, word_count // 200 * 60),
        'action_item_count': len(action_items),
        'action_items': action_items
    }
