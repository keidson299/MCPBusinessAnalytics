"""Shared utilities for business analytics MCP server"""

import re
from typing import List, Dict, Tuple

# Common stop words for text analysis
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
    'of', 'with', 'is', 'be', 'that', 'this', 'it', 'from', 'by', 'as', 
    'are', 'was', 'were', 'been', 'being', 'have', 'has', 'had', 'do', 
    'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
    'can', 'must', 'shall'
}

# Urgency indicators
URGENCY_KEYWORDS = [
    'urgent', 'asap', 'critical', 'emergency', 'immediately', 'deadline', 
    'priority', 'rush', 'quick', 'fast', 'now', 'today'
]

# Tone indicators
TONE_INDICATORS = {
    'formal': ['dear', 'sincerely', 'regards', 'professional', 'meeting', 'proposal', 'hereby'],
    'casual': ['hi', 'hey', 'thanks', 'cheers', 'lol', 'cool', 'awesome'],
    'negative': ['problem', 'issue', 'error', 'failed', 'disappointed', 'concern', 'complaint'],
    'positive': ['great', 'excellent', 'success', 'happy', 'appreciate', 'thank you', 'wonderful']
}

# Action item keywords
ACTION_KEYWORDS = [
    'please', 'need', 'can you', 'could you', 'will you', 'would you', 
    'should', 'must', 'required', 'action', 'do this', 'implement'
]


def parse_email_address(email_string: str) -> Tuple[str, str]:
    """
    Parse email address from various formats.
    
    Args:
        email_string: Email in format "Name <email>" or just "email"
        
    Returns:
        Tuple of (name, email)
    """
    name_match = re.match(r'^([^<]+)<([^>]+)>$', email_string.strip())
    
    if name_match:
        return (name_match.group(1).strip(), name_match.group(2).strip())
    else:
        return ('', email_string.strip())


def parse_recipients(recipient_string: str) -> List[Dict[str, str]]:
    """
    Parse recipient string into list of dicts with name and email.
    
    Args:
        recipient_string: Comma-separated recipients
        
    Returns:
        List of dicts with name, email, and domain
    """
    if not recipient_string:
        return []
    
    recipients = []
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


def extract_domain(email: str) -> str:
    """Extract domain from email address."""
    return email.split('@')[1] if '@' in email else 'unknown'


def extract_key_topics(text: str, top_n: int = 5) -> List[str]:
    """
    Extract frequently mentioned topics from text.
    
    Args:
        text: Text to analyze
        top_n: Number of top topics to return
        
    Returns:
        List of key topics
    """
    words = [w for w in text.lower().split() if w.isalnum() and w not in STOP_WORDS and len(w) > 3]
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    return [word for word, count in sorted(word_freq.items(), key=lambda x: x[1], reverse=True) if count >= 2][:top_n]


def detect_tone(text: str) -> List[str]:
    """
    Detect tone indicators in text.
    
    Args:
        text: Text to analyze
        
    Returns:
        List of detected tones
    """
    text_lower = text.lower()
    detected = []
    
    for tone, keywords in TONE_INDICATORS.items():
        if any(kw in text_lower for kw in keywords):
            detected.append(tone)
    
    return detected if detected else ['neutral']


def detect_urgency(text: str) -> bool:
    """
    Detect urgency indicators in text.
    
    Args:
        text: Text to analyze
        
    Returns:
        True if urgent language detected
    """
    return any(keyword in text.lower() for keyword in URGENCY_KEYWORDS)


def extract_action_items(text: str, max_items: int = 3) -> List[str]:
    """
    Extract potential action items from text.
    
    Args:
        text: Text to analyze
        max_items: Maximum number of action items to return
        
    Returns:
        List of action items
    """
    action_items = [
        line.strip() for line in text.split('\n') 
        if any(kw in line.lower() for kw in ACTION_KEYWORDS)
    ]
    return action_items[:max_items]
