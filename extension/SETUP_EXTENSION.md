# RINDA Email Extension Setup

## Step 1: Get InboxSDK Library

Download the InboxSDK library:

```bash
cd extension
curl -o inboxsdk.js https://www.inboxsdk.com/build/inboxsdk.js
```

Or download manually from: https://www.inboxsdk.com/build/inboxsdk.js

## Step 2: Register for InboxSDK App ID

1. Visit https://www.inboxsdk.com/register
2. Fill in the form:
   - App Name: RINDA Email
   - App URL: (your website or localhost)
   - Description: AI-powered email follow-up assistant
3. Copy the APP_ID you receive
4. Replace `YOUR_APP_ID_HERE` in `content.js` line 5 with your actual APP_ID

## Step 3: Create Extension Icons

Create simple 16x16, 48x48, and 128x128 PNG icons and save them as:
- `icons/icon16.png`
- `icons/icon48.png`
- `icons/icon128.png`

You can use any online icon generator or create simple colored squares for testing.

**Quick method using placeholder images:**
```bash
# Windows (using PowerShell to create blank PNGs)
# Or just download any PNG and rename it three times
```

For MVP testing, you can use any PNG image temporarily.

## Step 4: Load Extension in Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `extension/` folder
5. The extension should now appear in your extensions list

## Step 5: Test in Gmail

1. Open Gmail (https://mail.google.com)
2. Look for the RINDA Email icon in the toolbar
3. You should see a red [3] badge on the icon
4. Click the icon to see the 3 hardcoded action cards
5. Click "Send" on any card to open Gmail compose with the pre-filled draft

## Troubleshooting

- **InboxSDK not loading**: Check browser console (F12) for errors
- **No badge showing**: The badge is added via CSS, check if styles are injected
- **Compose not opening**: Make sure InboxSDK APP_ID is valid
- **Extension not appearing**: Verify manifest.json has no syntax errors

## Next Steps

Once the extension works with hardcoded data:
1. Set up the FastAPI backend
2. Connect extension to backend for real-time actions
3. Implement authentication flow
