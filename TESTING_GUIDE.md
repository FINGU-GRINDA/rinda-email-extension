# Testing Guide for RINDA Email

## Manual Testing Workflow

### Phase 1: Extension with Hardcoded Data (Priority)

This is the MVP - get this working first!

#### 1.1 Setup Extension

```bash
# Download InboxSDK
cd extension
curl -o inboxsdk.js https://www.inboxsdk.com/build/inboxsdk.js

# For Windows PowerShell:
# Invoke-WebRequest -Uri https://www.inboxsdk.com/build/inboxsdk.js -OutFile inboxsdk.js
```

#### 1.2 Get InboxSDK App ID

1. Visit https://www.inboxsdk.com/register
2. Fill in the form:
   - **App Name**: RINDA Email
   - **App URL**: http://localhost:8000
   - **Description**: AI-powered Gmail follow-up assistant
3. Submit and copy your APP_ID
4. Open `extension/content.js`
5. Replace line 5: `const INBOXSDK_APP_ID = 'sdk_rinda-email_YOUR_APP_ID_HERE';`
   with your actual APP_ID

#### 1.3 Create Extension Icons

Quick method - create simple colored squares:

1. Go to https://favicon.io/favicon-generator/
2. Create a simple icon (letter "R" or email icon)
3. Download and extract
4. Rename files:
   - Any 16x16 PNG → `extension/icons/icon16.png`
   - Any 48x48 PNG → `extension/icons/icon48.png`
   - Any 128x128 PNG → `extension/icons/icon128.png`

Or use placeholders:
- Just copy any PNG file 3 times with those names
- Icons are not critical for MVP testing

#### 1.4 Load Extension in Chrome

1. Open Chrome
2. Go to `chrome://extensions/`
3. Toggle "Developer mode" (top right)
4. Click "Load unpacked"
5. Navigate to and select the `extension/` folder
6. Extension should appear in your list

#### 1.5 Test in Gmail

1. Open Gmail: https://mail.google.com
2. Wait for page to fully load
3. Look for RINDA Email icon in Gmail toolbar (top right area)
4. You should see a red **[3]** badge on the icon

**Expected Result**: ✅ Icon with [3] badge visible

**If not working**:
- Open DevTools (F12) → Console
- Look for error messages
- Check for "RINDA Email: InboxSDK loaded successfully"
- Verify `inboxsdk.js` is downloaded
- Verify APP_ID is correct (no quotes issues)

#### 1.6 Test Action Panel

1. Click the RINDA Email icon
2. Should see modal/panel open
3. Panel should show:
   - Header: "🎯 Recommended Follow-ups"
   - 3 action cards with:
     - Emoji (🎯, 🤝, 💡)
     - Name (Sarah Chen, Michael Rodriguez, Jennifer Park)
     - Reason text
     - Blue "Send" button

**Expected Result**: ✅ Panel displays with 3 cards

**If not working**:
- Check console for errors
- Look for "RINDA Email: Toolbar button clicked"
- Check if modal CSS is applied

#### 1.7 Test Compose Integration

1. Click "Send" button on first action card
2. Should see Gmail compose window open
3. Compose should have:
   - **To**: sarah@techcorp.com
   - **Subject**: Following up on our conversation
   - **Body**: Pre-filled draft text

4. **DO NOT actually send** (these are test emails!)
5. Close compose window
6. Test other 2 cards similarly

**Expected Result**: ✅ Compose opens with pre-filled content

**If not working**:
- Check console: "RINDA Email: Opening compose for action"
- Verify InboxSDK Compose API is available
- Check if Gmail is in correct view (not settings page)

### Phase 2: Backend Testing

Once extension works with hardcoded data, test backend.

#### 2.1 Setup Backend Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2.2 Setup PostgreSQL

```bash
# Create database
createdb rinda_email

# Verify
psql rinda_email
# Should connect successfully
\q
```

**Windows alternative**:
- Open pgAdmin
- Create database "rinda_email"

#### 2.3 Setup Redis

```bash
# Start Redis server
redis-server

# Test in new terminal
redis-cli ping
# Should return: PONG
```

**Windows**:
- Download Redis from: https://github.com/microsoftarchive/redis/releases
- Extract and run `redis-server.exe`

#### 2.4 Configure Environment

```bash
# Copy example
cp .env.example .env

# Edit .env with your values
# Minimum required:
DATABASE_URL=postgresql://postgres:password@localhost:5432/rinda_email
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-generate-with-openssl
ANTHROPIC_API_KEY=sk-ant-your-key  # OR OPENAI_API_KEY
```

Generate secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### 2.5 Start Backend

```bash
python run.py
```

**Expected Output**:
```
✅ Database initialized
✅ RINDA Email API running in development mode
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 2.6 Test Health Endpoint

```bash
# New terminal
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "environment": "development",
#   "ai_provider": "anthropic"
# }
```

Or open in browser: http://localhost:8000/health

#### 2.7 Test API Documentation

Open http://localhost:8000/docs

Should see:
- Swagger UI with all endpoints
- Authentication section
- Inbox section
- Drafts section

### Phase 3: Google OAuth Testing

#### 3.1 Setup Google Cloud Project

1. Go to https://console.cloud.google.com
2. Create new project: "RINDA Email"
3. Wait for project creation

#### 3.2 Enable APIs

1. APIs & Services → Library
2. Search "Gmail API" → Enable
3. Search "Google+ API" → Enable

#### 3.3 Create OAuth Credentials

1. APIs & Services → Credentials
2. Click "Create Credentials" → OAuth 2.0 Client ID
3. If prompted, configure consent screen first:
   - User type: External
   - App name: RINDA Email
   - User support email: your-email@gmail.com
   - Developer email: your-email@gmail.com
   - Save and continue through all screens
4. Back to Create Credentials → OAuth 2.0 Client ID
5. Application type: Web application
6. Name: RINDA Email Backend
7. Authorized redirect URIs:
   - Add: `http://localhost:8000/api/auth/google/callback`
8. Create
9. Copy Client ID and Client Secret
10. Add to `backend/.env`:
    ```
    GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
    GOOGLE_CLIENT_SECRET=xxx
    ```

#### 3.4 Test OAuth Flow

```bash
# Get authorization URL
curl http://localhost:8000/api/auth/google
```

Response:
```json
{
  "authorization_url": "https://accounts.google.com/o/oauth2/auth?...",
  "state": "random-state-string"
}
```

Copy `authorization_url` and open in browser:
1. Sign in with Google
2. Grant permissions
3. Should redirect to localhost:8000 with code
4. Should see JSON with `access_token`

**Save this access token for next tests!**

### Phase 4: Gmail API Testing

#### 4.1 Test Inbox Analysis

```bash
# Use access_token from OAuth flow above
curl -X GET http://localhost:8000/api/inbox/analyze \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Expected Response**:
```json
{
  "actions": [
    {
      "id": 1,
      "recipient_email": "someone@example.com",
      "recipient_name": "John Doe",
      "action_type": "follow_up",
      "reason": "No response to message sent 4 days ago",
      "emoji": "🎯",
      "draft_subject": "Following up on our conversation",
      "draft_content": "Hi John,\n\nI wanted to...",
      "priority_score": 84,
      "is_sent": false
    }
    // ... 2 more actions
  ],
  "total_count": 3
}
```

**If no actions returned**:
- Check if you have emails in Gmail from 2-14 days ago
- Try sending yourself test emails
- Check console logs for errors

#### 4.2 Test Draft Generation

```bash
curl -X POST http://localhost:8000/api/drafts/generate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_email": "test@example.com",
    "recipient_name": "Test User",
    "action_type": "follow_up",
    "context": "Previous demo call about AI features",
    "last_interaction": "3 days ago",
    "signal": "No response to proposal"
  }'
```

**Expected Response**:
```json
{
  "subject": "Following up on our conversation",
  "body": "Hi Test User,\n\nI wanted to follow up...",
  "action_type": "follow_up"
}
```

**Test 3 times** to verify rate limiting:
- 1st call: Success
- 2nd call: Success
- 3rd call: Success
- 4th call: Should return 429 (Too Many Requests)

#### 4.3 Test Rate Limit Check

```bash
curl http://localhost:8000/api/drafts/rate-limit \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

**Expected Response**:
```json
{
  "allowed": false,
  "current_count": 3,
  "max_count": 3,
  "remaining": 0,
  "reset_time": "2025-01-08T00:00:00"
}
```

### Phase 5: Full Integration Testing

Once both extension and backend work separately, connect them.

#### 5.1 Update Extension to Use Backend

The extension already has background.js setup to call backend APIs.

**For MVP testing**, manually inject token:

1. Open Gmail
2. Open DevTools (F12)
3. Go to Console
4. Run:
   ```javascript
   chrome.storage.local.set({
     jwt_token: 'YOUR_JWT_TOKEN_HERE'
   }, () => {
     console.log('Token saved');
   });
   ```

#### 5.2 Test Live Actions

1. Reload Gmail page
2. Click RINDA Email icon
3. Should now fetch real actions from backend (not hardcoded)
4. Should see your actual email contacts
5. Should see AI-generated reasons

**If still showing hardcoded data**:
- Extension needs to be modified to fetch from backend
- For MVP, hardcoded data is sufficient
- Backend integration is Phase 2

### Testing Checklist

#### Extension (Hardcoded) - Priority ✅

- [ ] Extension loads in Chrome
- [ ] No console errors
- [ ] Icon appears in Gmail toolbar
- [ ] [3] badge shows on icon
- [ ] Clicking icon opens panel
- [ ] Panel shows 3 hardcoded actions
- [ ] Each action has emoji, name, reason, button
- [ ] Clicking "Send" opens Gmail compose
- [ ] Compose has correct recipient
- [ ] Compose has pre-filled subject
- [ ] Compose has pre-filled body
- [ ] User can edit compose
- [ ] User can send via Gmail's send button

#### Backend - Secondary

- [ ] Server starts without errors
- [ ] Health endpoint returns 200
- [ ] API docs accessible at /docs
- [ ] PostgreSQL connection works
- [ ] Redis connection works
- [ ] OAuth flow completes
- [ ] Can get authorization URL
- [ ] Can exchange code for JWT
- [ ] Gmail API fetches emails
- [ ] Inbox analysis returns actions
- [ ] Drafts endpoint generates email
- [ ] Rate limiting enforces 3/day limit
- [ ] Rate limit resets next day

#### Integration - Future

- [ ] Extension authenticates user
- [ ] Extension fetches actions from backend
- [ ] Extension displays live actions
- [ ] Extension respects rate limits
- [ ] Error messages display properly
- [ ] Loading states work

## Debugging Tips

### Extension Not Loading

1. Check `chrome://extensions/` for errors
2. Verify folder structure:
   ```
   extension/
   ├── manifest.json
   ├── background.js
   ├── content.js
   ├── inboxsdk.js  ← Must exist!
   └── icons/
       ├── icon16.png
       ├── icon48.png
       └── icon128.png
   ```
3. Reload extension after changes

### Badge Not Showing

1. Check InboxSDK loaded: Console should show "InboxSDK loaded successfully"
2. Check APP_ID is valid (no typos)
3. Inspect element on toolbar area - look for custom CSS

### Backend Errors

1. Check all services running:
   ```bash
   # PostgreSQL
   pg_isready

   # Redis
   redis-cli ping

   # Backend
   curl http://localhost:8000/health
   ```

2. Check logs in terminal where `python run.py` is running

3. Verify `.env` file has all required variables

### OAuth Issues

1. Verify redirect URI matches exactly (including trailing slashes)
2. Check test users are added to OAuth consent screen
3. Try incognito browser for fresh OAuth flow
4. Check Google Cloud Console → Credentials for any warnings

## Success Criteria

**MVP Success** = Extension shows [3] badge in Gmail, displays 3 hardcoded actions, opens compose with pre-filled draft

**Full Success** = Above + backend generates real actions from Gmail + AI drafts + rate limiting works

## Next Steps After MVP

1. Add OAuth flow to extension (popup for Google sign-in)
2. Fetch real actions from backend instead of hardcoded
3. Display rate limit counter in extension UI
4. Add error handling and retry logic
5. Improve action ranking algorithm
6. Add thread context to drafts
7. Track which emails were sent
8. Add analytics dashboard

---

**Questions?** Check README.md or DEVELOPMENT.md for more details.
