# RINDA Email - AI-Powered Gmail Follow-up Assistant

**Chrome Extension with AI-driven email recommendations**

RINDA Email is a Chrome extension that integrates with Gmail to show a badge with recommended follow-up actions. It uses AI (Claude/GPT-4) to generate personalized email drafts based on your inbox activity.

## 🎯 Features

- **[3] Badge in Gmail**: See at-a-glance how many follow-ups you should send
- **Smart Recommendations**: AI analyzes your inbox to identify important follow-ups
- **Pre-written Drafts**: Click to open Gmail compose with AI-generated email
- **3 Action Types**:
  - 🎯 Follow-ups (no response in 3-7 days)
  - 🤝 Thank you notes (after recent meetings)
  - 💡 Re-engagement (cold leads 7-14 days)
- **Rate Limited**: Max 3 emails/day for MVP testing
- **Privacy-focused**: Only reads email metadata (from, subject, date)

## 🏗️ Tech Stack

### Extension
- Vanilla JavaScript
- InboxSDK (Gmail integration)
- Chrome Manifest V3

### Backend
- FastAPI (Python)
- PostgreSQL (database)
- Redis (rate limiting)
- Google OAuth 2.0 + Gmail API
- Anthropic Claude / OpenAI GPT-4 (draft generation)

## 📋 Prerequisites

- Node.js 18+ (for InboxSDK download)
- Python 3.10+
- PostgreSQL 15+
- Redis 7+
- Google Cloud project with Gmail API enabled
- Anthropic API key or OpenAI API key

## 🚀 Quick Start

### 1. Clone Repository

```bash
cd rinda-email
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your credentials (see Backend Setup below)
```

### 3. Setup Database

```bash
# Create PostgreSQL database
createdb rinda_email

# Run migrations (tables will be auto-created on first run)
python -c "from app.database import init_db; init_db()"
```

### 4. Start Backend

```bash
# Start Redis (in separate terminal)
redis-server

# Start FastAPI server
python run.py

# API will be available at http://localhost:8000
```

### 5. Setup Extension

```bash
cd ../extension

# Download InboxSDK library
curl -o inboxsdk.js https://www.inboxsdk.com/build/inboxsdk.js

# Register for InboxSDK App ID at https://www.inboxsdk.com/register
# Update content.js line 5 with your APP_ID
```

### 6. Load Extension in Chrome

1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `extension/` folder
5. Extension should appear in your extensions list

### 7. Test in Gmail

1. Open Gmail (https://mail.google.com)
2. Look for RINDA Email icon in toolbar with [3] badge
3. Click to see 3 recommended actions (hardcoded for now)
4. Click "Send" to open compose with pre-filled draft

## 🔧 Backend Setup Guide

### Google Cloud Console Setup

1. **Create Project**:
   - Go to https://console.cloud.google.com
   - Create new project "RINDA Email"

2. **Enable APIs**:
   - Enable Gmail API
   - Enable Google+ API (for user info)

3. **Create OAuth Credentials**:
   - APIs & Services → Credentials
   - Create OAuth 2.0 Client ID
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/api/auth/google/callback`
   - Copy Client ID and Client Secret

4. **Configure OAuth Consent Screen**:
   - User type: External
   - Add scopes: email, profile, gmail.readonly, gmail.compose
   - Add test users (your email)

### Environment Variables

Edit `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/rinda_email

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT (generate random secret)
SECRET_KEY=your-secret-key-here-use-openssl-rand-hex-32

# Google OAuth (from Google Cloud Console)
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# AI Provider (choose: anthropic or openai)
AI_PROVIDER=anthropic

# Anthropic (get from https://console.anthropic.com)
ANTHROPIC_API_KEY=sk-ant-xxx

# OR OpenAI (get from https://platform.openai.com)
OPENAI_API_KEY=sk-xxx

# Rate Limiting
MAX_EMAILS_PER_DAY=3
```

### Generate Secret Key

```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

## 📡 API Endpoints

### Authentication

- `GET /api/auth/google` - Initiate OAuth flow
- `GET /api/auth/google/callback` - OAuth callback
- `POST /api/auth/token` - Exchange code for JWT
- `GET /api/auth/me` - Get current user

### Inbox Analysis

- `GET /api/inbox/analyze` - Analyze inbox, return top 3 actions
- `GET /api/inbox/actions` - Get saved actions
- `POST /api/inbox/actions/{id}/mark-sent` - Mark action as sent

### Draft Generation

- `POST /api/drafts/generate` - Generate email draft
- `GET /api/drafts/rate-limit` - Check rate limit status

## 🔌 Extension Architecture

```
extension/
├── manifest.json          # Chrome extension manifest
├── background.js          # Service worker for API calls
├── content.js            # InboxSDK integration + UI
├── inboxsdk.js           # InboxSDK library (download)
└── icons/                # Extension icons
```

### Key Components

1. **InboxSDK.load()** - Initializes Gmail integration
2. **ToolbarButtons** - Adds [3] badge to Gmail toolbar
3. **Compose API** - Opens compose with pre-filled draft
4. **Background worker** - Handles backend API calls

## 🎨 Customization

### Change Badge Count

Edit `content.js:83`:
```javascript
const badgeCount = 3; // Change this number
```

### Add More Actions

Edit `content.js:18-50` to add more hardcoded actions:
```javascript
{
  id: 4,
  emoji: '🚀',
  name: 'John Doe',
  email: 'john@example.com',
  action_type: 'custom',
  reason: 'Your reason here',
  draft: 'Your email template...'
}
```

### Modify Email Templates

Edit `backend/app/services/llm.py:30-60` to customize prompts.

## 🐛 Troubleshooting

### Extension Issues

**InboxSDK not loading**:
- Check browser console (F12) for errors
- Verify APP_ID is correct in `content.js`
- Ensure `inboxsdk.js` is downloaded

**Badge not showing**:
- Check if styles are injected (inspect element)
- Look for CSS errors in console

**Compose not opening**:
- Verify InboxSDK version 2 is loaded
- Check `sdk.Compose` API is available

### Backend Issues

**Database connection failed**:
```bash
# Check PostgreSQL is running
pg_isready

# Verify DATABASE_URL in .env
psql $DATABASE_URL
```

**Redis connection failed**:
```bash
# Check Redis is running
redis-cli ping  # Should return PONG
```

**OAuth errors**:
- Verify redirect URI matches exactly
- Check OAuth consent screen is published
- Ensure test users are added

**LLM generation fails**:
- Check API key is valid
- Verify AI_PROVIDER setting
- Check API rate limits

## 📊 Database Schema

### users
```sql
- id: Primary key
- email: User email (unique)
- gmail_token: Encrypted Gmail access token
- refresh_token: Encrypted refresh token
- token_expiry: Token expiration time
- created_at, updated_at, last_login
```

### email_actions
```sql
- id: Primary key
- user_id: Foreign key to users
- recipient_email, recipient_name
- action_type: follow_up | thank_you | new_opportunity
- reason: Why this action is recommended
- emoji: Display emoji
- draft_subject, draft_content: Generated email
- priority_score: For ranking (higher = more important)
- is_sent, sent_at: Tracking
- source_thread_id, source_message_id: Gmail references
- created_at, last_interaction_date
```

## 🔐 Security Notes

- Gmail tokens are stored in database (encrypt in production!)
- JWT tokens expire after 7 days
- Rate limiting prevents abuse (3 emails/day)
- Only email metadata is read (no email bodies)
- OAuth scopes are minimal (readonly + compose)

## 🚢 Production Deployment

### Backend

1. **Use environment variables for secrets**
2. **Enable HTTPS** (required for OAuth)
3. **Use managed PostgreSQL** (AWS RDS, Google Cloud SQL)
4. **Use managed Redis** (AWS ElastiCache, Redis Cloud)
5. **Encrypt tokens** in database
6. **Add rate limiting** per IP
7. **Set up monitoring** (Sentry, Datadog)

### Extension

1. **Publish to Chrome Web Store**
2. **Update API URL** to production
3. **Add proper OAuth redirect** to production URL
4. **Generate production icons**
5. **Add privacy policy** link

## 📈 MVP Success Criteria

- ✅ [3] badge shows in Gmail
- ✅ Side panel displays 3 action cards
- ✅ Clicking "Send" opens compose with draft
- ✅ User can review and send via Gmail
- ✅ Backend connects to Gmail API
- ✅ AI generates relevant email drafts
- ✅ Rate limiting works (3/day)
- 🎯 **Goal**: 10 users testing the MVP

## 🗺️ Roadmap

### Phase 1 (7 Days - MVP) ✅
- Basic extension with hardcoded data
- Backend with Gmail API integration
- AI draft generation
- OAuth authentication

### Phase 2 (Next)
- Real-time inbox analysis
- Better action scoring algorithm
- Email thread analysis
- Sentiment detection

### Phase 3 (Future)
- Pro features (unlimited emails)
- Custom templates
- Team collaboration
- Analytics dashboard

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! Please open an issue first to discuss changes.

## 📧 Support

For issues and questions:
- GitHub Issues: [github.com/your-repo/issues]
- Email: support@rinda.email

---

**Built with ❤️ by the RINDA team**
