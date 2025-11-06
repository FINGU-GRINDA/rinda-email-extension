"""LLM service for generating email drafts"""

from app.config import settings
from typing import Dict


def generate_email_draft(
    recipient_name: str,
    action_type: str,
    context: str = "",
    last_interaction: str = "",
    signal: str = ""
) -> Dict[str, str]:
    """Generate email draft using LLM"""

    # Build prompt
    prompt = build_prompt(recipient_name, action_type, context, last_interaction, signal)

    # Choose provider
    if settings.AI_PROVIDER == "anthropic":
        return generate_with_anthropic(prompt, action_type)
    elif settings.AI_PROVIDER == "openai":
        return generate_with_openai(prompt, action_type)
    else:
        raise ValueError(f"Unsupported AI provider: {settings.AI_PROVIDER}")


def build_prompt(
    recipient_name: str,
    action_type: str,
    context: str,
    last_interaction: str,
    signal: str
) -> str:
    """Build LLM prompt for email generation"""

    action_instructions = {
        "follow_up": "Write a professional follow-up email checking in on a previous conversation",
        "thank_you": "Write a warm thank you email expressing appreciation",
        "new_opportunity": "Write an engaging email introducing a new opportunity or reconnecting"
    }

    instruction = action_instructions.get(action_type, "Write a professional email")

    prompt = f"""You are a sales email assistant helping write brief, effective follow-up emails.

Task: {instruction}

Recipient: {recipient_name}
Context: {context or 'General business relationship'}
Last Interaction: {last_interaction or 'Recent conversation'}
Signal: {signal or 'Time to follow up'}

Requirements:
- Length: 80-120 words
- Tone: Professional yet friendly
- Include: Clear value proposition or question
- End with: Specific call-to-action
- Format: Plain text, no signatures
- Personalize based on context provided

Write ONLY the email body, nothing else."""

    return prompt


def generate_with_anthropic(prompt: str, action_type: str) -> Dict[str, str]:
    """Generate email using Anthropic Claude"""
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        body = message.content[0].text.strip()
        subject = generate_subject(action_type)

        return {
            "subject": subject,
            "body": body
        }

    except Exception as e:
        print(f"Error generating with Anthropic: {e}")
        return get_fallback_draft(action_type)


def generate_with_openai(prompt: str, action_type: str) -> Dict[str, str]:
    """Generate email using OpenAI GPT-4"""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a professional email writing assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        body = response.choices[0].message.content.strip()
        subject = generate_subject(action_type)

        return {
            "subject": subject,
            "body": body
        }

    except Exception as e:
        print(f"Error generating with OpenAI: {e}")
        return get_fallback_draft(action_type)


def generate_subject(action_type: str) -> str:
    """Generate email subject line"""
    subjects = {
        "follow_up": "Following up on our conversation",
        "thank_you": "Thank you for your time",
        "new_opportunity": "Quick question about your workflow"
    }
    return subjects.get(action_type, "Following up")


def get_fallback_draft(action_type: str) -> Dict[str, str]:
    """Fallback email templates if LLM fails"""
    templates = {
        "follow_up": {
            "subject": "Following up",
            "body": "Hi,\n\nI wanted to follow up on our previous conversation. I believe we have a solution that could really benefit your team.\n\nWould you have time for a quick call this week to discuss next steps?\n\nLooking forward to hearing from you."
        },
        "thank_you": {
            "subject": "Thank you",
            "body": "Hi,\n\nThank you for taking the time to connect. I really appreciated our conversation and your insights.\n\nI've put together some additional information that might be helpful. Let me know if you'd like to explore this further.\n\nBest regards."
        },
        "new_opportunity": {
            "subject": "Quick question",
            "body": "Hi,\n\nI noticed you might be interested in improving your team's workflow efficiency. We've helped similar companies achieve significant results.\n\nWould you be open to a brief conversation about your current challenges?\n\nLet me know!"
        }
    }

    return templates.get(action_type, templates["follow_up"])
