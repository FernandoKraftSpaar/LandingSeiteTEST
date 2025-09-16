/**
 * Utility functions for authentication and contextual greetings
 */

// Get contextual greeting based on current time
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

// Get user display name from authentication info
function getUserDisplayName(clientPrincipal) {
  if (!clientPrincipal) return '';
  
  // Try different properties that might contain the user's name
  return clientPrincipal.userDetails || 
         clientPrincipal.claims?.find(claim => claim.typ === 'name')?.val ||
         clientPrincipal.claims?.find(claim => claim.typ === 'preferred_username')?.val ||
         clientPrincipal.claims?.find(claim => claim.typ === 'email')?.val ||
         clientPrincipal.userId || 
         'Usuário';
}

// Check authentication status and update navigation
async function checkAuthStatusAndUpdateNav() {
  try {
    const response = await fetch('/.auth/me');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    const { clientPrincipal } = data;
    
    const authButton = document.getElementById('auth-button');
    const userInfo = document.getElementById('userInfo');
    const greeting = getContextualGreeting();
    
    if (clientPrincipal && clientPrincipal.userId) {
      // User is authenticated
      const userName = getUserDisplayName(clientPrincipal);
      const firstName = userName.split(' ')[0]; // Get first name only
      
      if (authButton) {
        authButton.innerHTML = `
          <div class="flex items-center space-x-3">
            <span class="text-sm text-slate-600 hidden md:inline">${greeting}, ${firstName}</span>
            <a href="/dashboard" class="bg-[var(--accent)] hover:bg-[var(--accent-2)] text-white px-4 py-2 rounded-lg text-sm transition-colors flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
              Dashboard
            </a>
            <a href="/.auth/logout" class="text-slate-600 hover:text-slate-800 text-sm">Sair</a>
          </div>
        `;
        authButton.classList.remove('hidden');
      }
      
      if (userInfo) {
        userInfo.textContent = `${greeting}, ${firstName}`;
        userInfo.classList.remove('hidden');
      }
      
      return { isAuthenticated: true, clientPrincipal, userName, greeting };
    } else {
      // User is not authenticated
      if (authButton) {
        authButton.innerHTML = `
          <a href="/login" class="bg-[var(--primary)] hover:bg-[var(--primary)]/90 text-white px-4 py-2 rounded-lg text-sm transition-colors">
            Login
          </a>
        `;
        authButton.classList.remove('hidden');
      }
      
      if (userInfo) {
        userInfo.classList.add('hidden');
      }
      
      return { isAuthenticated: false, clientPrincipal: null, userName: null, greeting };
    }
  } catch (error) {
    console.error('Error checking authentication status:', error);
    
    // Error fetching auth status, show login button
    const authButton = document.getElementById('auth-button');
    if (authButton) {
      authButton.innerHTML = `
        <a href="/login" class="bg-[var(--primary)] hover:bg-[var(--primary)]/90 text-white px-4 py-2 rounded-lg text-sm transition-colors">
          Login
        </a>
      `;
      authButton.classList.remove('hidden');
    }
    
    const userInfo = document.getElementById('userInfo');
    if (userInfo) {
      userInfo.classList.add('hidden');
    }
    
    return { isAuthenticated: false, clientPrincipal: null, userName: null, greeting: getContextualGreeting(), error };
  }
}

// Redirect to login if not authenticated (for protected pages)
async function requireAuthentication(redirectUrl = '/dashboard') {
  const authStatus = await checkAuthStatusAndUpdateNav();
  
  if (!authStatus.isAuthenticated) {
    // Redirect to login with post-login redirect
    window.location.href = `/.auth/login/aad?post_login_redirect_url=${encodeURIComponent(redirectUrl)}`;
    return false;
  }
  
  return true;
}