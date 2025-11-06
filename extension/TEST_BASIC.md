# 🧪 Basic Extension Test

If InboxSDK is causing issues, let's first verify your extension CAN load on Gmail.

## Quick Test (1 minute)

### Step 1: Add Test Script

1. Open: `extension/manifest.json`
2. Find the `"js"` array (around line 23)
3. Change it to:
```json
"js": ["simple-test.js", "inboxsdk-loader.js", "content.js"],
```

**Before:**
```json
"js": ["inboxsdk-loader.js", "content.js"],
```

**After:**
```json
"js": ["simple-test.js", "inboxsdk-loader.js", "content.js"],
```

4. **Save** the file

### Step 2: Reload & Test

1. Go to: `chrome://extensions/`
2. Click reload on RINDA Email
3. Go to Gmail (or refresh if already open)

### Step 3: Look for Test Button

**You should see:**
- A blue button in top-right: "✅ RINDA Email is Working!"
- Click it to see confirmation

**If you see this button:**
✅ Extension IS working
✅ Scripts CAN load on Gmail
✅ Problem is with InboxSDK specifically

**If you DON'T see this button:**
❌ Extension isn't loading at all
❌ Check chrome://extensions/ for errors
❌ Verify manifest.json has no syntax errors

---

## Results

**Share with me:**
1. Did you see the test button?
2. What's in the console (F12)?
3. Any errors in chrome://extensions/?

This will help me fix the exact issue!
