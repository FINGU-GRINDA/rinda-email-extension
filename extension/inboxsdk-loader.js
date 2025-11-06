// InboxSDK Loader - Properly inject into page context for Manifest V3
console.log('🔧 RINDA Email: InboxSDK Loader starting...');

(function() {
  'use strict';

  // For Manifest V3, we need to inject into the page's main world
  // Content scripts run in an isolated world, so we inject a script element

  const cdnSources = [
    'https://www.inboxsdk.com/build/inboxsdk.js',
    'https://unpkg.com/@inboxsdk/core@2.0.0/pageWorld.js',
    'https://cdn.jsdelivr.net/npm/@inboxsdk/core@2.0.0/pageWorld.js'
  ];

  let currentSourceIndex = 0;

  function injectInboxSDK() {
    if (currentSourceIndex >= cdnSources.length) {
      console.error('❌ RINDA Email: All InboxSDK CDN sources failed!');
      console.log('📝 This usually means:');
      console.log('  1. Network/firewall is blocking CDN access');
      console.log('  2. You need to bundle InboxSDK locally');

      // Notify content script that loading failed
      window.postMessage({ type: 'INBOXSDK_LOAD_FAILED' }, '*');
      return;
    }

    const source = cdnSources[currentSourceIndex];
    console.log(`⏳ Loading InboxSDK from: ${source}`);

    const script = document.createElement('script');
    script.src = source;
    script.async = false;

    script.onload = function() {
      console.log(`✅ InboxSDK loaded successfully from: ${source}`);
      // Check if InboxSDK is actually available
      setTimeout(() => {
        if (typeof InboxSDK !== 'undefined') {
          console.log('✨ InboxSDK is available in page context!');
          window.postMessage({ type: 'INBOXSDK_LOADED' }, '*');
        } else {
          console.warn('⚠️ InboxSDK loaded but not available, trying next source...');
          currentSourceIndex++;
          setTimeout(injectInboxSDK, 500);
        }
      }, 100);
    };

    script.onerror = function() {
      console.warn(`⚠️ Failed to load from: ${source}`);
      currentSourceIndex++;
      setTimeout(injectInboxSDK, 500);
    };

    // Inject into page head
    const target = document.head || document.documentElement;
    target.appendChild(script);
  }

  // Start injection when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectInboxSDK);
  } else {
    injectInboxSDK();
  }

})();

console.log('✅ RINDA Email: Loader script initialized');
