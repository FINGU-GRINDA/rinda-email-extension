# Quick Start - MVP in 30 Minutes

Get RINDA Email working with hardcoded data in Gmail.

## Prerequisites Checklist

- [ ] Chrome browser installed
- [ ] Gmail account
- [ ] Internet connection

That's it! Backend setup comes later.

## Step 1: Download InboxSDK (2 min)

```bash
cd extension

# Mac/Linux:
curl -o inboxsdk.js https://www.inboxsdk.com/build/inboxsdk.js

# Windows PowerShell:
Invoke-WebRequest -Uri https://www.inboxsdk.com/build/inboxsdk.js -OutFile inboxsdk.js

# Or download manually from browser:
# https://www.inboxsdk.com/build/inboxsdk.js
# Save as: extension/inboxsdk.js
```

## Step 2: Get InboxSDK App ID (5 min)

1. Visit: https://www.inboxsdk.com/register
2. Fill in:
   - **App Name**: RINDA Email
   - **App URL**: http://localhost:8000
   - **Description**: AI-powered Gmail assistant
3. Submit
4. Copy your APP_ID (looks like: `sdk_RindaEmail_abc123`)

## Step 3: Configure Extension (2 min)

Open `extension/content.js` in any text editor:

Find line 5:
```javascript
const INBOXSDK_APP_ID = 'sdk_rinda-email_YOUR_APP_ID_HERE';
```

Replace with your APP_ID:
```javascript
const INBOXSDK_APP_ID = 'sdk_RindaEmail_abc123';  // Your actual ID
```

Save file.

## Step 4: Create Icons (5 min)

**Option A - Use Favicon Generator** (Recommended):
1. Go to: https://favicon.io/favicon-generator/
2. Create icon (letter "R" or any design)
3. Download ZIP
4. Extract and copy any PNG files to:
   - `extension/icons/icon16.png`
   - `extension/icons/icon48.png`
   - `extension/icons/icon128.png`

**Option B - Use Placeholder**:
1. Find any PNG image on your computer
2. Copy it 3 times to `extension/icons/` folder
3. Rename to: `icon16.png`, `icon48.png`, `icon128.png`

Icons don't need to be perfect sizes for MVP testing!

## Step 5: Load Extension in Chrome (3 min)

1. Open Chrome
2. Go to: `chrome://extensions/`
3. Enable **Developer mode** (toggle top right)
4. Click **Load unpacked**
5. Select your `extension/` folder
6. Extension appears in list ✅

**Troubleshooting**:
- If error appears, check that:
  - `inboxsdk.js` exists in extension folder
  - All 3 icon files exist
  - `manifest.json` has no syntax errors

## Step 6: Test in Gmail (5 min)

1. Open new tab: https://mail.google.com
2. Wait for Gmail to fully load
3. Look in toolbar (top right area) for RINDA Email icon
4. Should see red **[3]** badge on icon

**Expected**: ✅ Icon with [3] badge visible

## Step 7: Test Actions Panel (3 min)

1. Click RINDA Email icon
2. Panel opens with header: "🎯 Recommended Follow-ups"
3. See 3 action cards:
   - 🎯 Sarah Chen - "No response to proposal sent 3 days ago"
   - 🤝 Michael Rodriguez - "Attended demo call yesterday"
   - 💡 Jennifer Park - "Showed interest in LinkedIn post"
4. Each has a blue "Send" button

**Expected**: ✅ Panel displays correctly

## Step 8: Test Email Compose (5 min)

1. Click **Send** button on first action (Sarah Chen)
2. Gmail compose window opens
3. Check it has:
   - **To**: sarah@techcorp.com
   - **Subject**: Following up on our conversation
   - **Body**: Pre-filled draft text
4. **Close compose** (don't send - it's a test email!)
5. Test other 2 actions similarly

**Expected**: ✅ Compose opens with pre-filled content

## 🎉 Success!

You now have:
- ✅ Working Chrome extension
- ✅ Badge showing in Gmail
- ✅ Side panel with 3 actions
- ✅ Compose integration working

**Next Steps**:
1. Backend setup (see README.md)
2. Connect to live Gmail data
3. Add AI-generated drafts
4. Invite test users

## Troubleshooting

### Extension won't load
- Check `chrome://extensions/` for error details
- Verify all files exist in `extension/` folder
- Try reloading extension (circular arrow icon)

### Badge not showing
- Open DevTools: F12 → Console
- Look for "RINDA Email: InboxSDK loaded successfully"
- If not found, check APP_ID in content.js

### Panel not opening
- Check Console for errors
- Verify click is registered: "Toolbar button clicked" log
- Try refreshing Gmail page

### Compose not opening
- Make sure you're in inbox view (not settings)
- Check Console: "Opening compose for action"
- Try different Gmail view (compact, default, comfortable)

## FAQ

**Q: Do I need a backend for MVP?**
A: No! Extension works with hardcoded data. Backend comes later.

**Q: Can I customize the 3 actions?**
A: Yes! Edit `HARDCODED_ACTIONS` array in `content.js` (line 18-50).

**Q: Does this actually send emails?**
A: No, it only opens Gmail compose. YOU decide whether to send.

**Q: Is this secure?**
A: For MVP with hardcoded data - yes. Production needs OAuth + encryption.

**Q: Can I test with my team?**
A: Yes! Share the `extension/` folder. They follow same steps.

**Q: How do I update the extension?**
A: Make changes → go to `chrome://extensions/` → click reload icon

---

**Time taken**: 30 minutes
**Difficulty**: Beginner
**Cost**: $0

Need help? See README.md or DEVELOPMENT.md for detailed guides.
