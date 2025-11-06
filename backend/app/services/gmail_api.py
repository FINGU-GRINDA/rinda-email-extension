"""Gmail API service for reading emails"""

from datetime import datetime, timedelta
from typing import List, Dict
from app.services.google_oauth import get_gmail_service
import base64
import email


def get_recent_emails(access_token: str, max_results: int = 50) -> List[Dict]:
    """Fetch recent emails from Gmail (metadata only)"""
    service = get_gmail_service(access_token)

    # Get emails from last 30 days
    query = f'newer_than:30d'

    try:
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])
        emails = []

        for message in messages:
            # Get message details
            msg = service.users().messages().get(
                userId='me',
                id=message['id'],
                format='metadata',
                metadataHeaders=['From', 'To', 'Subject', 'Date']
            ).execute()

            email_data = parse_email_metadata(msg)
            emails.append(email_data)

        return emails

    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []


def parse_email_metadata(msg: dict) -> Dict:
    """Parse email metadata from Gmail API response"""
    headers = {h['name']: h['value'] for h in msg['payload']['headers']}

    return {
        "id": msg['id'],
        "thread_id": msg['threadId'],
        "from": headers.get('From', ''),
        "to": headers.get('To', ''),
        "subject": headers.get('Subject', ''),
        "date": headers.get('Date', ''),
        "snippet": msg.get('snippet', ''),
        "internal_date": datetime.fromtimestamp(int(msg['internalDate']) / 1000)
    }


def get_thread_messages(access_token: str, thread_id: str) -> List[Dict]:
    """Get all messages in a thread"""
    service = get_gmail_service(access_token)

    try:
        thread = service.users().threads().get(
            userId='me',
            id=thread_id,
            format='metadata',
            metadataHeaders=['From', 'To', 'Subject', 'Date']
        ).execute()

        messages = []
        for msg in thread.get('messages', []):
            email_data = parse_email_metadata(msg)
            messages.append(email_data)

        return messages

    except Exception as e:
        print(f"Error fetching thread: {e}")
        return []


def extract_email_address(from_header: str) -> str:
    """Extract email address from 'From' header"""
    # Handle formats like "Name <email@example.com>" or "email@example.com"
    if '<' in from_header and '>' in from_header:
        start = from_header.index('<') + 1
        end = from_header.index('>')
        return from_header[start:end].strip()
    return from_header.strip()


def extract_name(from_header: str) -> str:
    """Extract name from 'From' header"""
    if '<' in from_header:
        return from_header[:from_header.index('<')].strip().strip('"')
    return ""


def analyze_email_interactions(emails: List[Dict]) -> List[Dict]:
    """Analyze emails to identify follow-up opportunities"""
    # Group by sender
    senders = {}

    for email_data in emails:
        from_header = email_data['from']
        email_addr = extract_email_address(from_header)
        name = extract_name(from_header)

        if email_addr not in senders:
            senders[email_addr] = {
                "email": email_addr,
                "name": name or email_addr.split('@')[0],
                "messages": [],
                "last_interaction": None
            }

        senders[email_addr]["messages"].append(email_data)

        # Update last interaction
        msg_date = email_data['internal_date']
        if not senders[email_addr]["last_interaction"] or msg_date > senders[email_addr]["last_interaction"]:
            senders[email_addr]["last_interaction"] = msg_date

    # Identify follow-up opportunities
    opportunities = []
    now = datetime.now()

    for sender_email, data in senders.items():
        last_msg = data["last_interaction"]
        days_since = (now - last_msg).days

        # Skip recent interactions (< 2 days)
        if days_since < 2:
            continue

        # Determine action type and reason
        action = determine_action_type(data, days_since)

        if action:
            opportunities.append({
                "recipient_email": data["email"],
                "recipient_name": data["name"],
                "action_type": action["type"],
                "reason": action["reason"],
                "emoji": action["emoji"],
                "last_interaction": last_msg,
                "thread_id": data["messages"][-1]["thread_id"],
                "message_id": data["messages"][-1]["id"],
                "priority_score": action["priority"]
            })

    # Sort by priority
    opportunities.sort(key=lambda x: x["priority_score"], reverse=True)

    return opportunities[:10]  # Return top 10


def determine_action_type(sender_data: dict, days_since: int) -> dict | None:
    """Determine the type of follow-up action needed"""
    message_count = len(sender_data["messages"])
    latest_msg = sender_data["messages"][-1]

    # Follow-up for no response (3-7 days)
    if 3 <= days_since <= 7:
        return {
            "type": "follow_up",
            "reason": f"No response to message sent {days_since} days ago",
            "emoji": "🎯",
            "priority": 80 + days_since
        }

    # Thank you for recent interaction (2-3 days)
    if 2 <= days_since <= 3 and message_count >= 2:
        return {
            "type": "thank_you",
            "reason": f"Recent conversation {days_since} days ago",
            "emoji": "🤝",
            "priority": 70
        }

    # Re-engage cold lead (7-14 days)
    if 7 <= days_since <= 14:
        return {
            "type": "new_opportunity",
            "reason": f"Last contact {days_since} days ago - re-engagement opportunity",
            "emoji": "💡",
            "priority": 60
        }

    return None
