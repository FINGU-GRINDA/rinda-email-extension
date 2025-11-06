"""Rate limiting service using Redis"""

import redis
from datetime import datetime, timedelta
from app.config import settings


class RateLimiter:
    """Rate limiter for email sending"""

    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.max_emails = settings.MAX_EMAILS_PER_DAY

    def check_rate_limit(self, user_id: int) -> dict:
        """Check if user has exceeded rate limit"""
        key = f"email_count:{user_id}:{datetime.now().strftime('%Y-%m-%d')}"

        try:
            count = self.redis_client.get(key)
            current_count = int(count) if count else 0

            return {
                "allowed": current_count < self.max_emails,
                "current_count": current_count,
                "max_count": self.max_emails,
                "remaining": max(0, self.max_emails - current_count)
            }

        except Exception as e:
            print(f"Rate limiter error: {e}")
            # Fail open - allow request if Redis is down
            return {
                "allowed": True,
                "current_count": 0,
                "max_count": self.max_emails,
                "remaining": self.max_emails
            }

    def increment_count(self, user_id: int) -> bool:
        """Increment email count for user"""
        key = f"email_count:{user_id}:{datetime.now().strftime('%Y-%m-%d')}"

        try:
            # Check current count
            rate_limit = self.check_rate_limit(user_id)

            if not rate_limit["allowed"]:
                return False

            # Increment
            pipe = self.redis_client.pipeline()
            pipe.incr(key)
            pipe.expire(key, 86400)  # Expire after 24 hours
            pipe.execute()

            return True

        except Exception as e:
            print(f"Rate limiter error: {e}")
            return True  # Fail open

    def get_reset_time(self, user_id: int) -> datetime:
        """Get time when rate limit resets"""
        tomorrow = datetime.now() + timedelta(days=1)
        return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)


# Singleton instance
rate_limiter = RateLimiter()
