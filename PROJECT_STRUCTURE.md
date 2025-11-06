# RINDA Email - Project Structure

```
rinda-email/
│
├── extension/                          # Chrome Extension (Frontend)
│   ├── manifest.json                   # Extension manifest (V3)
│   ├── background.js                   # Service worker for API calls
│   ├── content.js                      # InboxSDK integration + UI logic
│   ├── styles.css                      # CSS styles (reference)
│   ├── inboxsdk.js                     # InboxSDK library (download from web)
│   ├── icons/                          # Extension icons
│   │   ├── README.md                   # Instructions for creating icons
│   │   ├── icon16.png                  # 16x16 icon (create)
│   │   ├── icon48.png                  # 48x48 icon (create)
│   │   └── icon128.png                 # 128x128 icon (create)
│   └── SETUP_EXTENSION.md              # Extension setup instructions
│
├── backend/                            # FastAPI Backend (API)
│   ├── app/
│   │   ├── __init__.py                 # App package init
│   │   ├── main.py                     # FastAPI application entry point
│   │   ├── config.py                   # Configuration management
│   │   ├── database.py                 # Database connection setup
│   │   ├── schemas.py                  # Pydantic schemas (request/response)
│   │   │
│   │   ├── models/                     # Database models (SQLAlchemy)
│   │   │   ├── __init__.py
│   │   │   ├── user.py                 # User model
│   │   │   └── email_action.py         # EmailAction model
│   │   │
│   │   ├── api/                        # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                 # Authentication endpoints
│   │   │   ├── inbox.py                # Inbox analysis endpoints
│   │   │   └── drafts.py               # Draft generation endpoints
│   │   │
│   │   └── services/                   # Business logic services
│   │       ├── __init__.py
│   │       ├── auth.py                 # JWT authentication
│   │       ├── google_oauth.py         # Google OAuth 2.0 flow
│   │       ├── gmail_api.py            # Gmail API integration
│   │       ├── llm.py                  # AI draft generation
│   │       └── rate_limiter.py         # Redis rate limiting
│   │
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Environment variables template
│   ├── .env                            # Environment variables (create from .env.example)
│   └── run.py                          # Development server runner
│
├── .gitignore                          # Git ignore rules
├── README.md                           # Main documentation
├── QUICK_START.md                      # 30-minute MVP guide
├── DEVELOPMENT.md                      # Detailed development guide
├── TESTING_GUIDE.md                    # Testing workflows
└── PROJECT_STRUCTURE.md                # This file

```

## File Descriptions

### Extension Files

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `manifest.json` | Chrome extension configuration | 30 | ✅ Ready |
| `background.js` | Background service worker, handles API requests | 50 | ✅ Ready |
| `content.js` | Main logic: InboxSDK integration, UI, compose | 250 | ✅ Ready |
| `styles.css` | CSS for action cards and panel | 100 | ✅ Ready |
| `inboxsdk.js` | InboxSDK library | - | ⚠️ Download |

### Backend Files

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `main.py` | FastAPI app initialization | 60 | ✅ Ready |
| `config.py` | Environment configuration | 40 | ✅ Ready |
| `database.py` | Database session management | 30 | ✅ Ready |
| `schemas.py` | Request/response schemas | 80 | ✅ Ready |
| **Models** |
| `models/user.py` | User database model | 25 | ✅ Ready |
| `models/email_action.py` | EmailAction database model | 35 | ✅ Ready |
| **API Endpoints** |
| `api/auth.py` | OAuth & JWT endpoints | 100 | ✅ Ready |
| `api/inbox.py` | Inbox analysis endpoints | 120 | ✅ Ready |
| `api/drafts.py` | Draft generation endpoints | 80 | ✅ Ready |
| **Services** |
| `services/auth.py` | Authentication logic | 80 | ✅ Ready |
| `services/google_oauth.py` | Google OAuth flow | 90 | ✅ Ready |
| `services/gmail_api.py` | Gmail API integration | 200 | ✅ Ready |
| `services/llm.py` | AI draft generation | 150 | ✅ Ready |
| `services/rate_limiter.py` | Redis rate limiting | 70 | ✅ Ready |

### Documentation Files

| File | Purpose | Target Audience |
|------|---------|-----------------|
| `README.md` | Complete overview, setup, API docs | Everyone |
| `QUICK_START.md` | 30-min MVP with hardcoded data | Beginners |
| `DEVELOPMENT.md` | Detailed dev workflow, debugging | Developers |
| `TESTING_GUIDE.md` | Manual testing procedures | QA/Testers |
| `PROJECT_STRUCTURE.md` | This file - architecture overview | All |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Gmail UI                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  RINDA Email Extension (content.js)                    │  │
│  │  ┌──────────┐  ┌──────────────┐  ┌─────────────────┐  │  │
│  │  │  [3]     │  │ Action Panel │  │ Gmail Compose   │  │  │
│  │  │  Badge   │→ │ 3 Cards      │→ │ Pre-filled      │  │  │
│  │  └──────────┘  └──────────────┘  └─────────────────┘  │  │
│  └─────────────────────────┬──────────────────────────────┘  │
└────────────────────────────┼─────────────────────────────────┘
                             │ InboxSDK API
                             │
                    ┌────────▼─────────┐
                    │ background.js    │ Service Worker
                    │ (API Gateway)    │
                    └────────┬─────────┘
                             │ fetch() with JWT
                             │
              ┌──────────────▼──────────────┐
              │  FastAPI Backend            │
              │  (localhost:8000)           │
              │                             │
              │  ┌────────────────────┐    │
              │  │ API Routes         │    │
              │  │ /api/auth/*        │    │
              │  │ /api/inbox/*       │    │
              │  │ /api/drafts/*      │    │
              │  └─────────┬──────────┘    │
              │            │                │
              │  ┌─────────▼──────────┐    │
              │  │ Services Layer     │    │
              │  │ - Google OAuth     │    │
              │  │ - Gmail API        │    │
              │  │ - LLM (Claude/GPT) │    │
              │  │ - Rate Limiter     │    │
              │  └─────────┬──────────┘    │
              └────────────┼───────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                 │
    ┌─────▼──────┐  ┌─────▼──────┐  ┌──────▼───────┐
    │ PostgreSQL │  │   Redis    │  │ Gmail API    │
    │ (Database) │  │  (Cache)   │  │ Google Cloud │
    └────────────┘  └────────────┘  └──────────────┘
```

## Data Flow

### 1. Extension Load (MVP)
```
User opens Gmail
  → InboxSDK.load() initializes
  → Toolbar button added with [3] badge
  → HARDCODED_ACTIONS ready to display
```

### 2. User Clicks Badge (MVP)
```
Click RINDA icon
  → showActionPanel() called
  → Modal/panel created with 3 cards
  → Cards display: emoji + name + reason + button
```

### 3. User Clicks Send (MVP)
```
Click "Send" button
  → handleSendAction() called
  → sdk.Compose.openNewComposeView()
  → Set recipient, subject, body
  → User reviews and sends via Gmail
```

### 4. Full Flow (With Backend)
```
Extension loads
  → Check JWT token in storage
  → If no token, prompt OAuth
  → User authenticates with Google
  → Backend exchanges code for JWT
  → Extension stores JWT

User clicks badge
  → Extension calls /api/inbox/analyze
  → Backend fetches Gmail emails
  → Backend analyzes interactions
  → Backend generates AI drafts
  → Backend returns top 3 actions
  → Extension displays actions

User clicks Send
  → Extension calls /api/inbox/actions/{id}/mark-sent
  → Backend updates database
  → Extension opens compose with draft
  → User sends via Gmail
  → Backend increments rate limit counter
```

## Tech Stack Details

### Frontend (Extension)
- **Language**: Vanilla JavaScript (ES6+)
- **Framework**: None (pure JS)
- **Gmail SDK**: InboxSDK v2
- **Manifest**: V3 (latest Chrome extension standard)
- **Storage**: chrome.storage.local (for JWT tokens)

### Backend (API)
- **Language**: Python 3.10+
- **Framework**: FastAPI 0.109+
- **ORM**: SQLAlchemy 2.0+
- **Auth**: JWT (python-jose)
- **OAuth**: google-auth-oauthlib
- **AI**: Anthropic Claude / OpenAI GPT-4

### Database
- **Primary**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Schema**: 2 tables (users, email_actions)

### External APIs
- **Gmail API**: Read emails (metadata only)
- **Google OAuth 2.0**: Authentication
- **Anthropic API**: Draft generation (Claude)
- **OpenAI API**: Draft generation (GPT-4) - alternative

## Development Priorities

### Phase 1: MVP (Days 1-2) - PRIORITY ⭐
- [x] Extension with hardcoded data
- [x] Badge shows [3]
- [x] Panel displays 3 actions
- [x] Compose opens with draft
- **Goal**: 10 users can test hardcoded version

### Phase 2: Backend (Days 3-5)
- [x] FastAPI server running
- [x] Database schema created
- [x] OAuth flow working
- [x] Gmail API integration
- [x] AI draft generation
- **Goal**: Backend generates real actions

### Phase 3: Integration (Days 6-7)
- [ ] Extension connects to backend
- [ ] Real actions replace hardcoded
- [ ] Rate limiting enforced
- [ ] Error handling
- **Goal**: 10 users test full version

### Phase 4: Polish (Week 2+)
- [ ] Better action scoring
- [ ] Email thread analysis
- [ ] Sentiment detection
- [ ] Analytics dashboard
- **Goal**: Production-ready

## Key Features

### MVP Features ✅
- [x] Chrome extension loads in Gmail
- [x] Badge shows action count
- [x] Side panel with action cards
- [x] Compose integration
- [x] 3 action types (follow_up, thank_you, new_opportunity)

### Backend Features ✅
- [x] Google OAuth 2.0
- [x] JWT authentication
- [x] Gmail API integration (metadata only)
- [x] AI draft generation (Claude/GPT-4)
- [x] Rate limiting (3 emails/day)
- [x] PostgreSQL storage
- [x] Redis caching

### Future Features 📋
- [ ] Extension OAuth flow
- [ ] Real-time action updates
- [ ] Email thread context
- [ ] Sentiment analysis
- [ ] Custom templates
- [ ] Team features
- [ ] Analytics dashboard
- [ ] Mobile support

## Success Metrics

### MVP Success (Week 1)
- ✅ Extension loads without errors
- ✅ Badge displays correctly
- ✅ Panel shows 3 actions
- ✅ Compose opens with draft
- 🎯 10 users test and provide feedback

### Backend Success (Week 2)
- ✅ Backend handles OAuth
- ✅ Gmail API returns emails
- ✅ AI generates relevant drafts
- ✅ Rate limiting works
- 🎯 Actions are contextually relevant

### Full Success (Week 3)
- [ ] Extension + backend integrated
- [ ] Real actions from user's Gmail
- [ ] AI drafts are high quality
- [ ] 90%+ user satisfaction
- 🎯 Ready for beta launch

## Next Steps

1. **Start with MVP** (QUICK_START.md)
   - Get extension working with hardcoded data
   - Test in Gmail
   - Share with 10 users

2. **Setup Backend** (README.md)
   - Configure environment
   - Start services
   - Test APIs

3. **Integrate** (DEVELOPMENT.md)
   - Connect extension to backend
   - Test full flow
   - Deploy to production

---

**Questions?** See other documentation files for detailed guides.
