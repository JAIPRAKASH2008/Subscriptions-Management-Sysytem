/**
 * Brightloop Subscription Management System - Core Frontend JavaScript
 * Handles:
 * - Real-time password requirement checklist validation
 * - Demo role selection auto-filler
 * - Dynamic table search & status filtering
 * - Accessible Modal dialog management
 */

document.addEventListener('DOMContentLoaded', () => {
  initPasswordValidator();
  initPasswordToggle();
  initDemoRoleSelector();
  initTableFilters();
  initModals();
});

/**
 * 1. Real-time Password Strength and Criteria Verification
 * Checks:
 * - Minimum 8 characters
 * - At least one uppercase letter [A-Z]
 * - At least one lowercase letter [a-z]
 * - At least one special character [!@#$%^&*(),.?":{}|<>]
 */
function initPasswordValidator() {
  const passwordInput = document.getElementById('regPassword');
  if (!passwordInput) return;

  const criteriaLength = document.getElementById('crit-length');
  const criteriaUpper = document.getElementById('crit-upper');
  const criteriaLower = document.getElementById('crit-lower');
  const criteriaSpecial = document.getElementById('crit-special');
  const submitBtn = document.getElementById('registerSubmitBtn');

  const checkCriteria = () => {
    const val = passwordInput.value;
    const hasLength = val.length >= 8;
    const hasUpper = /[A-Z]/.test(val);
    const hasLower = /[a-z]/.test(val);
    const hasSpecial = /[^A-Za-z0-9]/.test(val);

    updateCriterion(criteriaLength, hasLength);
    updateCriterion(criteriaUpper, hasUpper);
    updateCriterion(criteriaLower, hasLower);
    updateCriterion(criteriaSpecial, hasSpecial);

    const allValid = hasLength && hasUpper && hasLower && hasSpecial;
    if (submitBtn) {
      submitBtn.disabled = !allValid;
      submitBtn.style.opacity = allValid ? '1' : '0.6';
      submitBtn.style.cursor = allValid ? 'pointer' : 'not-allowed';
    }
  };

  const updateCriterion = (el, isValid) => {
    if (!el) return;
    if (isValid) {
      el.classList.add('valid');
      const icon = el.querySelector('.criteria-icon');
      if (icon) icon.innerHTML = '✓';
    } else {
      el.classList.remove('valid');
      const icon = el.querySelector('.criteria-icon');
      if (icon) icon.innerHTML = '•';
    }
  };

  passwordInput.addEventListener('input', checkCriteria);
  // Initial run
  checkCriteria();
}

/**
 * 2. Password Visibility Toggle
 */
function initPasswordToggle() {
  const toggleButtons = document.querySelectorAll('.password-toggle-btn');
  toggleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const input = document.getElementById(targetId);
      if (!input) return;

      if (input.type === 'password') {
        input.type = 'text';
        btn.innerHTML = `
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
            <line x1="1" y1="1" x2="23" y2="23"></line>
          </svg>`;
      } else {
        input.type = 'password';
        btn.innerHTML = `
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>`;
      }
    });
  });
}

/**
 * 3. Demo Role Selector on Login (Admin, Staff, Customer)
 */
function initDemoRoleSelector() {
  const roleChips = document.querySelectorAll('.role-chip');
  const emailInput = document.getElementById('loginEmail');
  const passwordInput = document.getElementById('loginPassword');

  if (!roleChips.length || !emailInput || !passwordInput) return;

  const demoAccounts = {
    admin: { email: 'admin@brightloop.io', pass: 'Admin@1234#' },
    staff: { email: 'sarah.chen@brightloop.io', pass: 'Staff@1234#' },
    customer: { email: 'david.miller@acmecorp.com', pass: 'Customer@1234#' }
  };

  roleChips.forEach(chip => {
    chip.addEventListener('click', () => {
      roleChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');

      const role = chip.getAttribute('data-role');
      if (demoAccounts[role]) {
        emailInput.value = demoAccounts[role].email;
        passwordInput.value = demoAccounts[role].pass;
      }
    });
  });
}

/**
 * 4. Data Table Search and Status Filtering
 */
function initTableFilters() {
  const searchInput = document.getElementById('tableSearchInput');
  const filterPills = document.querySelectorAll('.filter-pill');
  const table = document.querySelector('.data-table');

  if (!table) return;
  const rows = table.querySelectorAll('tbody tr');

  function filterTable() {
    const query = (searchInput ? searchInput.value : '').toLowerCase().trim();
    const activeFilter = document.querySelector('.filter-pill.active')?.getAttribute('data-status')?.toLowerCase() || 'all';

    rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      const statusBadge = row.querySelector('.badge-status');
      const statusText = statusBadge ? statusBadge.textContent.toLowerCase().trim() : '';

      const matchesQuery = !query || text.includes(query);
      const matchesStatus = (activeFilter === 'all') || (statusText.includes(activeFilter));

      if (matchesQuery && matchesStatus) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', filterTable);
  }

  filterPills.forEach(pill => {
    pill.addEventListener('click', () => {
      filterPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      filterTable();
    });
  });
}

/**
 * 5. Modal Dialog Open & Close Handlers
 */
function initModals() {
  const openButtons = document.querySelectorAll('[data-modal-open]');
  const closeButtons = document.querySelectorAll('[data-modal-close]');

  openButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const modalId = btn.getAttribute('data-modal-open');
      const modal = document.getElementById(modalId);
      if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  closeButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const modal = btn.closest('.modal-overlay');
      if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });

  // Close when clicking overlay backdrop
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });
}

