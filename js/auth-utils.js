/**
 * SmartSpaar Authentication Utilities
 * Provides consistent authentication status checking and contextual greetings
 */

/**
 * Get contextual greeting based on current time
 * @returns {string} Time-based greeting in Portuguese
 */
function getContextualGreeting() {
  const now = new Date();
  const hour = now.getHours();
  
  if (hour >= 5 && hour < 12) {
    return 'Bom dia';
  } else if (hour >= 12 && hour < 18) {
    return 'Boa tarde';
  } else {
    return 'Boa noite';
  }
}

/**
 * Extract display name from clientPrincipal object
 * @param {Object} clientPrincipal - The authentication principal
 * @returns {string} User's first name or email
 */
function getDisplayName(clientPrincipal) {
  if (!clientPrincipal) return '';
  
  // Try to get first name from userDetails
  if (clientPrincipal.userDetails) {
    // Split by space and take first part as first name
    const name = clientPrincipal.userDetails.split(' ')[0];
    if (name && name.length > 0) {
      return name;
    }
  }
  
  // Fallback to email prefix if available
  if (clientPrincipal.userDetails && clientPrincipal.userDetails.includes('@')) {
    return clientPrincipal.userDetails.split('@')[0];
  }
  
  // Final fallback
  return 'Usuário';
}

/**
 * Check authentication status and return user info
 * @returns {Promise<Object>} Authentication status and user info
 */
async function checkAuthenticationStatus() {
  try {
    const response = await fetch('/.auth/me');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    const isAuthenticated = !!(data.clientPrincipal && data.clientPrincipal.userId);
    
    return {
      isAuthenticated,
      user: data.clientPrincipal,
      displayName: isAuthenticated ? getDisplayName(data.clientPrincipal) : '',
      greeting: getContextualGreeting()
    };
  } catch (error) {
    console.warn('Authentication check failed:', error);
    return {
      isAuthenticated: false,
      user: null,
      displayName: '',
      greeting: getContextualGreeting()
    };
  }
}

/**
 * Redirect to login if not authenticated
 * @param {string} redirectUrl - URL to redirect after login
 */
function requireAuthentication(redirectUrl = '/dashboard') {
  checkAuthenticationStatus().then(authInfo => {
    if (!authInfo.isAuthenticated) {
      window.location.href = `/login?redirect=${encodeURIComponent(redirectUrl)}`;
    }
  });
}

/**
 * Update navigation with authentication status and contextual greeting
 * @param {string} buttonElementId - ID of the auth button element
 */
async function updateNavigationAuth(buttonElementId = 'auth-button') {
  const authInfo = await checkAuthenticationStatus();
  const authButton = document.getElementById(buttonElementId);
  
  if (!authButton) return;
  
  if (authInfo.isAuthenticated) {
    // User is authenticated - show personalized greeting and dashboard access
    authButton.innerHTML = `
      <div class="flex items-center space-x-3">
        <span class="text-sm text-gray-600 hidden md:inline">
          ${authInfo.greeting}, ${authInfo.displayName}!
        </span>
        <a href="/dashboard" class="bg-[var(--accent)] hover:bg-[var(--accent-2)] text-white px-4 py-2 rounded-lg text-sm transition-colors">
          Dashboard
        </a>
      </div>
    `;
  } else {
    // User is not authenticated - show login button
    authButton.innerHTML = `
      <a href="/login" class="bg-[var(--primary)] hover:bg-[var(--primary)]/90 text-white px-4 py-2 rounded-lg text-sm transition-colors">
        Login
      </a>
    `;
  }
  
  authButton.classList.remove('hidden');
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    getContextualGreeting,
    getDisplayName,
    checkAuthenticationStatus,
    requireAuthentication,
    updateNavigationAuth
  };
}