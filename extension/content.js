// RINDA Email - Standalone Mode (No InboxSDK needed)
console.log('🚀 RINDA Email: Content script starting...');

// Hardcoded actions for MVP
const HARDCODED_ACTIONS = [
  {
    id: 1,
    emoji: '🎯',
    name: 'Sarah Chen',
    email: 'sarah@techcorp.com',
    action_type: 'follow_up',
    reason: 'No response to proposal sent 3 days ago',
    draft: `Hi Sarah,\n\nI wanted to follow up on the proposal I sent last week. I believe our solution could significantly improve your team's workflow efficiency.\n\nWould you have 15 minutes this week to discuss the next steps?\n\nBest regards`
  },
  {
    id: 2,
    emoji: '🤝',
    name: 'Michael Rodriguez',
    email: 'michael@startup.io',
    action_type: 'thank_you',
    reason: 'Attended demo call yesterday',
    draft: `Hi Michael,\n\nThank you for taking the time to join our demo yesterday. I really appreciated your insightful questions about the integration capabilities.\n\nI've attached the case study we discussed. Let me know if you'd like to explore a pilot program.\n\nLooking forward to hearing from you!`
  },
  {
    id: 3,
    emoji: '💡',
    name: 'Jennifer Park',
    email: 'jennifer@enterprise.com',
    action_type: 'new_opportunity',
    reason: 'Showed interest in LinkedIn post',
    draft: `Hi Jennifer,\n\nI noticed you engaged with our recent post about AI automation. Given your role at Enterprise Corp, I thought you might be interested in how we've helped similar companies reduce manual work by 40%.\n\nWould you be open to a brief conversation about your current challenges?\n\nBest`
  }
];

// Wait for Gmail to load
function waitForGmail() {
  console.log('⏳ RINDA Email: Waiting for Gmail to load...');

  let attempts = 0;
  const maxAttempts = 30;

  const checkInterval = setInterval(() => {
    attempts++;

    // Check if Gmail is loaded
    const gmailReady = document.querySelector('[role="navigation"]') ||
                      document.querySelector('[role="main"]') ||
                      document.querySelector('.nH') ||
                      document.body.classList.contains('aAU');

    if (gmailReady) {
      console.log('✅ RINDA Email: Gmail detected!');
      clearInterval(checkInterval);
      setTimeout(initializeUI, 1000); // Wait 1 more second for stability
    } else if (attempts >= maxAttempts) {
      console.log('⚠️ RINDA Email: Gmail not detected, initializing anyway...');
      clearInterval(checkInterval);
      initializeUI();
    } else {
      console.log(`⏳ Checking... (${attempts}/${maxAttempts})`);
    }
  }, 500);
}

// Initialize the UI
function initializeUI() {
  console.log('🎨 RINDA Email: Creating UI...');

  // Inject styles first
  injectStyles();

  // Create floating button
  createFloatingButton();

  console.log('✅ RINDA Email: UI loaded successfully!');
}

// Create floating action button
function createFloatingButton() {
  // Remove existing button if any
  const existing = document.getElementById('rinda-fab');
  if (existing) {
    existing.remove();
  }

  const button = document.createElement('div');
  button.id = 'rinda-fab';
  button.className = 'rinda-fab';
  button.innerHTML = `
    <div class="rinda-fab-icon">📧</div>
    <div class="rinda-fab-badge">3</div>
  `;
  button.title = 'RINDA Email - 3 AI Recommendations';

  button.addEventListener('click', () => {
    console.log('👆 RINDA Email: Button clicked');
    togglePanel();
  });

  document.body.appendChild(button);
  console.log('✅ Floating button created');
}

// Toggle panel visibility
function togglePanel() {
  const existingPanel = document.getElementById('rinda-panel');

  if (existingPanel) {
    existingPanel.remove();
    console.log('Panel closed');
  } else {
    showPanel();
  }
}

// Show the panel
function showPanel() {
  const panel = document.createElement('div');
  panel.id = 'rinda-panel';
  panel.className = 'rinda-panel';

  panel.innerHTML = `
    <div class="rinda-panel-header">
      <div class="rinda-panel-title">
        <span class="rinda-title-icon">⚡</span>
        <span class="rinda-title-text">RINDA Email</span>
      </div>
      <button class="rinda-close-btn" onclick="document.getElementById('rinda-panel').remove()">✕</button>
    </div>
    <div class="rinda-panel-subtitle">AI-Recommended Actions</div>
    <div class="rinda-panel-content">
      ${HARDCODED_ACTIONS.map(action => createActionCard(action)).join('')}
    </div>
  `;

  // Add event listeners for buttons
  panel.addEventListener('click', (e) => {
    // Handle compose button
    if (e.target.classList.contains('rinda-compose-btn')) {
      const actionId = parseInt(e.target.dataset.actionId);
      handleCompose(actionId);
    }

    // Handle preview button
    if (e.target.classList.contains('rinda-preview-btn')) {
      const card = e.target.closest('.rinda-card');
      const preview = card.querySelector('.rinda-draft-preview');
      const button = e.target;

      if (preview.style.display === 'none' || !preview.style.display) {
        preview.style.display = 'block';
        button.textContent = '▲ Hide';
      } else {
        preview.style.display = 'none';
        button.textContent = '▼ Preview';
      }
    }
  });

  document.body.appendChild(panel);
  console.log('✅ Panel opened');
}

// Create action card HTML
function createActionCard(action) {
  const badgeColors = {
    follow_up: '#ea8600',
    thank_you: '#1e8e3e',
    new_opportunity: '#1a73e8'
  };

  const badgeLabels = {
    follow_up: 'Follow-up',
    thank_you: 'Thank You',
    new_opportunity: 'New Opportunity'
  };

  return `
    <div class="rinda-card">
      <div class="rinda-card-header">
        <div class="rinda-card-emoji">${action.emoji}</div>
        <div class="rinda-card-info">
          <div class="rinda-card-name">${action.name}</div>
          <div class="rinda-card-email">${action.email}</div>
        </div>
      </div>

      <div class="rinda-card-badge" style="background: ${badgeColors[action.action_type]}">
        ${badgeLabels[action.action_type]}
      </div>

      <div class="rinda-card-reason">${action.reason}</div>

      <div class="rinda-draft-preview" style="display: none;">
        <div class="rinda-draft-label">Draft Preview:</div>
        <div class="rinda-draft-text">${action.draft.replace(/\n/g, '<br>')}</div>
      </div>

      <div class="rinda-card-actions">
        <button class="rinda-preview-btn">▼ Preview</button>
        <button class="rinda-compose-btn" data-action-id="${action.id}">✉️ Compose</button>
      </div>
    </div>
  `;
}

// Handle compose action
function handleCompose(actionId) {
  const action = HARDCODED_ACTIONS.find(a => a.id === actionId);
  if (!action) return;

  console.log('📧 Composing email to:', action.name);

  // Generate subject
  const subjects = {
    follow_up: `Following up: ${action.name}`,
    thank_you: `Thank you for your time`,
    new_opportunity: `Quick question about your workflow`
  };
  const subject = subjects[action.action_type];

  // Create Gmail compose URL
  const url = new URL('https://mail.google.com/mail/');
  url.searchParams.set('view', 'cm');
  url.searchParams.set('fs', '1');
  url.searchParams.set('to', action.email);
  url.searchParams.set('su', subject);
  url.searchParams.set('body', action.draft);

  // Open compose window
  window.open(url.toString(), '_blank', 'width=800,height=600');

  // Show feedback
  const button = document.querySelector(`[data-action-id="${actionId}"]`);
  if (button) {
    const originalText = button.innerHTML;
    button.innerHTML = '✓ Opened!';
    button.style.background = '#1e8e3e';
    setTimeout(() => {
      button.innerHTML = originalText;
      button.style.background = '';
    }, 2000);
  }
}

// Inject all styles
function injectStyles() {
  const style = document.createElement('style');
  style.id = 'rinda-styles';
  style.textContent = `
    /* Floating Action Button */
    .rinda-fab {
      position: fixed;
      bottom: 30px;
      right: 30px;
      width: 64px;
      height: 64px;
      background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
      border-radius: 50%;
      box-shadow: 0 4px 12px rgba(26, 115, 232, 0.4);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 999999;
      transition: all 0.3s ease;
      animation: fadeInUp 0.5s ease;
    }

    .rinda-fab:hover {
      transform: scale(1.1);
      box-shadow: 0 6px 20px rgba(26, 115, 232, 0.6);
    }

    .rinda-fab-icon {
      font-size: 28px;
      line-height: 1;
    }

    .rinda-fab-badge {
      position: absolute;
      top: -4px;
      right: -4px;
      background: #d93025;
      color: white;
      border-radius: 12px;
      padding: 2px 7px;
      font-size: 12px;
      font-weight: bold;
      font-family: 'Google Sans', Roboto, Arial, sans-serif;
      animation: pulse 2s infinite;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    /* Panel */
    .rinda-panel {
      position: fixed;
      top: 50%;
      right: 40px;
      transform: translateY(-50%);
      width: 420px;
      max-height: 85vh;
      background: white;
      border-radius: 12px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.12);
      z-index: 999998;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      animation: slideInRight 0.3s ease;
      font-family: 'Google Sans', Roboto, Arial, sans-serif;
    }

    .rinda-panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px 24px;
      background: linear-gradient(135deg, #1a73e8 0%, #4285f4 100%);
      color: white;
    }

    .rinda-panel-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 20px;
      font-weight: 500;
    }

    .rinda-title-icon {
      font-size: 24px;
    }

    .rinda-close-btn {
      background: rgba(255,255,255,0.2);
      border: none;
      color: white;
      font-size: 20px;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      cursor: pointer;
      transition: background 0.2s;
    }

    .rinda-close-btn:hover {
      background: rgba(255,255,255,0.3);
    }

    .rinda-panel-subtitle {
      padding: 12px 24px;
      background: #f8f9fa;
      color: #5f6368;
      font-size: 13px;
      border-bottom: 1px solid #e8eaed;
    }

    .rinda-panel-content {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
    }

    /* Action Cards */
    .rinda-card {
      background: white;
      border: 1px solid #e8eaed;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 12px;
      transition: all 0.2s;
    }

    .rinda-card:hover {
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      border-color: #dadce0;
    }

    .rinda-card-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }

    .rinda-card-emoji {
      font-size: 32px;
      line-height: 1;
    }

    .rinda-card-info {
      flex: 1;
    }

    .rinda-card-name {
      font-size: 15px;
      font-weight: 500;
      color: #202124;
      margin-bottom: 2px;
    }

    .rinda-card-email {
      font-size: 13px;
      color: #5f6368;
    }

    .rinda-card-badge {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 500;
      color: white;
      margin-bottom: 12px;
    }

    .rinda-card-reason {
      font-size: 13px;
      color: #5f6368;
      margin-bottom: 12px;
      line-height: 1.4;
    }

    .rinda-draft-preview {
      background: #f8f9fa;
      border-radius: 6px;
      padding: 12px;
      margin-bottom: 12px;
    }

    .rinda-draft-label {
      font-size: 12px;
      color: #5f6368;
      margin-bottom: 8px;
      font-weight: 500;
    }

    .rinda-draft-text {
      font-size: 13px;
      color: #202124;
      line-height: 1.5;
    }

    .rinda-card-actions {
      display: flex;
      gap: 8px;
    }

    .rinda-preview-btn,
    .rinda-compose-btn {
      flex: 1;
      padding: 8px 16px;
      border: 1px solid #dadce0;
      border-radius: 4px;
      background: white;
      color: #1a73e8;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      font-family: 'Google Sans', Roboto, Arial, sans-serif;
    }

    .rinda-preview-btn:hover {
      background: #f8f9fa;
      border-color: #1a73e8;
    }

    .rinda-compose-btn {
      background: #1a73e8;
      color: white;
      border-color: #1a73e8;
    }

    .rinda-compose-btn:hover {
      background: #1765cc;
      box-shadow: 0 1px 3px rgba(26, 115, 232, 0.3);
    }

    /* Animations */
    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes slideInRight {
      from {
        opacity: 0;
        transform: translateY(-50%) translateX(30px);
      }
      to {
        opacity: 1;
        transform: translateY(-50%) translateX(0);
      }
    }

    @keyframes pulse {
      0%, 100% {
        transform: scale(1);
      }
      50% {
        transform: scale(1.1);
      }
    }
  `;

  document.head.appendChild(style);
  console.log('✅ Styles injected');
}

// Start the extension
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', waitForGmail);
} else {
  waitForGmail();
}

console.log('✅ RINDA Email: Script initialized');
