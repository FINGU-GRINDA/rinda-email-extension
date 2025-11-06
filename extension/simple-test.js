// Simple test file to verify extension is working
// This creates a visible indicator on Gmail page

console.log('🧪 RINDA Email: Simple test script running');

// Create a test button in Gmail UI
function createTestButton() {
  console.log('🎨 Creating test button...');

  const button = document.createElement('div');
  button.id = 'rinda-test-button';
  button.textContent = '✅ RINDA Email is Working!';
  button.style.cssText = `
    position: fixed;
    top: 70px;
    right: 20px;
    background: #1a73e8;
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    font-family: Arial;
    font-size: 14px;
    font-weight: bold;
    z-index: 999999;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    cursor: pointer;
    animation: slideIn 0.5s ease-out;
  `;

  // Add animation
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
  `;
  document.head.appendChild(style);

  button.onclick = () => {
    alert('🎉 RINDA Email extension is loaded!\n\n' +
          'This test button confirms your extension is working.\n\n' +
          'App ID: sdk_rinda_8a9cf72c15\n' +
          'Location: ' + window.location.href);
  };

  document.body.appendChild(button);

  console.log('✅ Test button added to page');

  // Remove after 10 seconds
  setTimeout(() => {
    button.style.opacity = '0.5';
    button.textContent = '✅ Extension Working (click to close)';
    button.onclick = () => button.remove();
  }, 10000);
}

// Wait for Gmail to load
function waitForGmail() {
  if (document.body && document.querySelector('[role="navigation"]')) {
    console.log('✅ Gmail loaded, creating test button');
    createTestButton();
  } else {
    console.log('⏳ Waiting for Gmail to load...');
    setTimeout(waitForGmail, 500);
  }
}

// Start
waitForGmail();
