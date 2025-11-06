// Background service worker for RINDA Email extension
chrome.runtime.onInstalled.addListener(() => {
  console.log('RINDA Email extension installed');
});

// Handle messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'FETCH_ACTIONS') {
    // Forward API request to backend
    fetchActionsFromBackend(request.token)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep channel open for async response
  }

  if (request.type === 'GENERATE_DRAFT') {
    // Generate draft from backend
    generateDraft(request.token, request.payload)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
});

async function fetchActionsFromBackend(token) {
  const response = await fetch('http://localhost:8000/api/inbox/analyze', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    throw new Error(`Backend error: ${response.status}`);
  }

  return await response.json();
}

async function generateDraft(token, payload) {
  const response = await fetch('http://localhost:8000/api/drafts/generate', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Backend error: ${response.status}`);
  }

  return await response.json();
}
