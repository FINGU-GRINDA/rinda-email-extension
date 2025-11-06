## 🚀 RINDA Email Extension - Quick Install Guide

### Step 1: Create Icons (2 minutes)

1. Open `icons/create_simple_icons.html` in your web browser
2. Click "Download All Icons" button
3. Three PNG files will download to your Downloads folder
4. Move these 3 files to the `extension/icons/` folder:
   - `icon16.png`
   - `icon48.png`
   - `icon128.png`

### Step 2: Get InboxSDK App ID (5 minutes)

1. Visit: https://www.inboxsdk.com/register
2. Fill in the form:
   - **App Name**: RINDA Email
   - **App URL**: http://localhost:8000 (or your website)
   - **Description**: AI-powered email follow-up assistant
3. Submit and copy your APP_ID (looks like `sdk_YourAppName_xxxxx`)
4. Open `extension/content.js` in a text editor
5. Find line 4: `const INBOXSDK_APP_ID = 'sdk_rinda-email_YOUR_APP_ID_HERE';`
6. Replace `YOUR_APP_ID_HERE` with your actual APP_ID
7. Save the file

### Step 3: Load Extension in Chrome (2 minutes)

1. Open Google Chrome
2. Go to: `chrome://extensions/`
3. Enable **"Developer mode"** (toggle in top right corner)
4. Click **"Load unpacked"** button
5. Navigate to and select your `rinda-email/extension/` folder
6. Click "Select Folder"
7. Extension should now appear in your extensions list!

### Step 4: Test in Gmail (1 minute)

1. Open a new tab
2. Go to: https://mail.google.com
3. Wait for Gmail to fully load
4. Look for the RINDA Email icon in the Gmail toolbar (top right area)
5. You should see a pulsing red **[3]** badge on the icon!

### Step 5: Try the Features!

**Click the icon** to see the enhanced UI with:
- ⚡ Modern Gmail-native design
- 🎯 3 recommended follow-up actions
- 👀 Click "Preview" to see email drafts
- ✉️ Click "Compose" to open Gmail compose with pre-filled content
- ⌨️ **Keyboard shortcuts**:
  - `1`, `2`, `3` - Select action
  - `↑` `↓` - Navigate between actions
  - `Enter` - Compose email
  - `Esc` - Close panel

### Troubleshooting

**Extension won't load:**
- Check that all 3 icon files exist in `icons/` folder
- Verify `inboxsdk-loader.js` exists
- Check for errors in `chrome://extensions/`

**No badge in Gmail:**
- Open browser console (F12)
- Look for "RINDA Email: InboxSDK loaded" message
- If not found, check your APP_ID is correct
- Make sure you have internet connection (InboxSDK loads from CDN)

**Badge appears but panel won't open:**
- Check browser console for errors
- Try refreshing Gmail page
- Verify content.js has no syntax errors

**InboxSDK won't load:**
- Check browser console for network errors
- Verify internet connection
- Try reloading the extension in `chrome://extensions/`

### 🎉 Success!

Once you see the badge and can click to open the panel, you're all set!

**What you can do now:**
- Click any action card to expand and see the email preview
- Click "Compose" to open Gmail's compose window with the pre-filled draft
- Edit the draft and send via Gmail's native send button
- Use keyboard shortcuts for faster workflow

### Next Steps

- **Connect to backend**: Follow `README.md` to set up the FastAPI backend
- **Real Gmail data**: Connect to Gmail API for actual inbox analysis
- **AI-generated drafts**: Add Anthropic/OpenAI API for custom drafts
- **Share with team**: Package and share the extension folder

---

**Need help?** Check `README.md` or `TESTING_GUIDE.md` for more details.
