# Development Guide

## Development Workflow

### Day 1-2: Extension Frontend (MVP)

**Goal**: Get hardcoded badge working in Gmail

1. **Setup InboxSDK**:
   ```bash
   cd extension
   curl -o inboxsdk.js https://www.inboxsdk.com/build/inboxsdk.js
   ```

2. **Register for APP_ID**:
   - Visit https://www.inboxsdk.com/register
   - Fill in details
   - Copy APP_ID to `content.js` line 5

3. **Create placeholder icons**:
   - Use https://favicon.io/ or any tool
   - Create 16x16, 48x48, 128x128 PNG files
   - Save to `extension/icons/`

4. **Load extension**:
   - Chrome → `chrome://extensions/`
   - Enable Developer mode
   - Load unpacked → select `extension/` folder

5. **Test in Gmail**:
   - Open Gmail
   - Look for RINDA icon in toolbar
   - Should see [3] badge
   - Click to see 3 hardcoded actions
   - Click "Send" to test compose opening

### Day 3-4: Backend Setup

**Goal**: Get FastAPI running with database

1. **Setup Python environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Setup PostgreSQL**:
   ```bash
   # Install PostgreSQL (if not installed)
   # Windows: Download from https://www.postgresql.org/download/windows/
   # Mac: brew install postgresql
   # Linux: sudo apt-get install postgresql

   # Create database
   createdb rinda_email

   # Or using psql
   psql -U postgres
   CREATE DATABASE rinda_email;
   \q
   ```

3. **Setup Redis**:
   ```bash
   # Install Redis
   # Windows: Download from https://github.com/microsoftarchive/redis/releases
   # Mac: brew install redis
   # Linux: sudo apt-get install redis-server

   # Start Redis
   redis-server

   # Test
   redis-cli ping  # Should return PONG
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

5. **Run backend**:
   ```bash
   python run.py
   ```

6. **Test API**:
   ```bash
   # Health check
   curl http://localhost:8000/health

   # Should return:
   # {"status":"healthy","environment":"development","ai_provider":"anthropic"}
   ```

### Day 5: Google OAuth Setup

**Goal**: Connect Gmail API

1. **Google Cloud Console**:
   - Go to https://console.cloud.google.com
   - Create project "RINDA Email"
   - Enable Gmail API
   - Enable Google+ API

2. **Create OAuth credentials**:
   - APIs & Services → Credentials
   - Create OAuth 2.0 Client ID
   - Type: Web application
   - Name: RINDA Email Backend
   - Authorized redirect URIs:
     - `http://localhost:8000/api/auth/google/callback`
   - Copy Client ID and Secret to `.env`

3. **Configure OAuth consent**:
   - OAuth consent screen
   - External + Create
   - App name: RINDA Email
   - User support email: your-email@gmail.com
   - Add scopes:
     - `https://www.googleapis.com/auth/gmail.readonly`
     - `https://www.googleapis.com/auth/gmail.compose`
     - `https://www.googleapis.com/auth/userinfo.email`
   - Add test users (your email)
   - Save

4. **Test OAuth flow**:
   ```bash
   # Get authorization URL
   curl http://localhost:8000/api/auth/google

   # Copy authorization_url and open in browser
   # Complete OAuth flow
   # You'll be redirected back with a token
   ```

### Day 6: AI Integration

**Goal**: Generate drafts with Claude/GPT-4

1. **Get API key**:
   - Anthropic: https://console.anthropic.com/
   - OpenAI: https://platform.openai.com/

2. **Add to .env**:
   ```bash
   AI_PROVIDER=anthropic  # or openai
   ANTHROPIC_API_KEY=sk-ant-xxx
   # OR
   OPENAI_API_KEY=sk-xxx
   ```

3. **Test draft generation**:
   ```bash
   # First get JWT token from OAuth flow above
   TOKEN="your-jwt-token"

   # Generate draft
   curl -X POST http://localhost:8000/api/drafts/generate \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "recipient_email": "test@example.com",
       "recipient_name": "John Doe",
       "action_type": "follow_up",
       "context": "Previous demo call",
       "last_interaction": "3 days ago",
       "signal": "No response to proposal"
     }'
   ```

### Day 7: Integration Testing

**Goal**: Connect extension to live backend

1. **Update extension to use backend**:
   - Extension already has background.js setup
   - Need to implement JWT token storage
   - Add authentication flow to extension

2. **Test full flow**:
   - Load extension in Chrome
   - Click RINDA icon
   - Should prompt for Google login (future feature)
   - For now, manually set token in console:
     ```javascript
     chrome.storage.local.set({jwt_token: 'your-token'})
     ```
   - Click icon again
   - Should fetch real actions from backend
   - Click "Send" to open compose

## Testing Checklist

### Extension Testing

- [ ] Extension loads without errors
- [ ] Badge shows in Gmail toolbar
- [ ] Badge shows correct count [3]
- [ ] Clicking icon opens side panel
- [ ] Side panel shows 3 action cards
- [ ] Each card has emoji, name, reason
- [ ] Clicking "Send" opens Gmail compose
- [ ] Compose has pre-filled recipient
- [ ] Compose has pre-filled subject
- [ ] Compose has pre-filled body
- [ ] User can edit and send via Gmail

### Backend Testing

- [ ] Server starts without errors
- [ ] Health endpoint returns 200
- [ ] Database tables created
- [ ] OAuth flow works
- [ ] Can get authorization URL
- [ ] Can exchange code for tokens
- [ ] JWT tokens are created
- [ ] Gmail API fetches emails
- [ ] Inbox analysis returns actions
- [ ] LLM generates drafts
- [ ] Rate limiting works (3/day)
- [ ] Rate limit resets at midnight

### Integration Testing

- [ ] Extension can call backend APIs
- [ ] CORS allows extension origin
- [ ] JWT authentication works
- [ ] Extension displays backend actions
- [ ] Rate limit shows in extension
- [ ] Error handling works
- [ ] Loading states display properly

## Common Development Tasks

### Add New Action Type

1. **Update backend** (`backend/app/services/gmail_api.py`):
   ```python
   # Add to determine_action_type()
   if some_condition:
       return {
           "type": "new_action_type",
           "reason": "Why this action",
           "emoji": "🎉",
           "priority": 75
       }
   ```

2. **Update LLM prompts** (`backend/app/services/llm.py`):
   ```python
   action_instructions = {
       # ... existing types
       "new_action_type": "Your instruction for LLM"
   }
   ```

3. **Update extension** (`extension/content.js`):
   ```javascript
   // Add to HARDCODED_ACTIONS for testing
   {
       action_type: 'new_action_type',
       emoji: '🎉',
       // ... rest of fields
   }
   ```

### Modify Email Template

Edit `backend/app/services/llm.py`:

```python
def build_prompt(...):
    prompt = f"""You are a sales email assistant.

YOUR CUSTOM INSTRUCTIONS HERE

Requirements:
- Length: 80-120 words
- YOUR CUSTOM REQUIREMENTS
"""
```

### Change Rate Limit

Edit `backend/.env`:

```bash
MAX_EMAILS_PER_DAY=10  # Change from 3 to 10
```

### Debug Extension

1. **Open DevTools**:
   - Right-click extension icon → Inspect
   - Opens service worker console

2. **Check content script**:
   - Open Gmail → F12
   - Console tab
   - Look for "RINDA Email:" logs

3. **Check network requests**:
   - Network tab
   - Filter: XHR
   - Look for API calls to localhost:8000

### Debug Backend

1. **Add debug logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Use FastAPI interactive docs**:
   - Open http://localhost:8000/docs
   - Try API endpoints directly

3. **Check database**:
   ```bash
   psql rinda_email
   SELECT * FROM users;
   SELECT * FROM email_actions;
   ```

## Performance Optimization

### Backend

1. **Database indexing** (already added):
   - `users.email` (unique index)
   - `email_actions.user_id` (foreign key index)

2. **Caching**:
   - Cache Gmail API responses (future)
   - Cache LLM prompts (future)

3. **Async operations**:
   - Use `asyncio` for parallel API calls
   - Batch database operations

### Extension

1. **Lazy loading**:
   - Only fetch actions when icon clicked
   - Cache actions for 5 minutes

2. **Debounce API calls**:
   - Don't refetch on every click

## Security Best Practices

1. **Environment variables**:
   - Never commit `.env` to git
   - Use separate keys for dev/prod

2. **Token storage**:
   - Encrypt tokens in database (production)
   - Use secure token storage in extension

3. **API rate limiting**:
   - Implement per-IP rate limiting
   - Use API keys for extension

4. **CORS**:
   - Restrict origins in production
   - Use specific extension ID

## Deployment Preparation

### Backend

1. **Use production database**:
   ```bash
   # AWS RDS, Google Cloud SQL, etc.
   DATABASE_URL=postgresql://user:pass@prod-db:5432/rinda
   ```

2. **Use production Redis**:
   ```bash
   # AWS ElastiCache, Redis Cloud, etc.
   REDIS_URL=redis://prod-redis:6379
   ```

3. **Environment variables**:
   ```bash
   ENVIRONMENT=production
   DEBUG=False
   ```

4. **HTTPS required** for OAuth

### Extension

1. **Update API URL**:
   ```javascript
   const BACKEND_URL = 'https://api.rinda.email';
   ```

2. **Submit to Chrome Web Store**:
   - Create developer account
   - Prepare store listing
   - Add privacy policy
   - Submit for review

## Troubleshooting Guide

See README.md for common issues and solutions.
