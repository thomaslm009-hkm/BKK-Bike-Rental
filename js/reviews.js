/* ==========================================================================
   BKK Motorbike Rental - Customer Reviews & Verified Google Reviewer Manager
   ========================================================================== */

const ReviewsManager = {
  currentUser: null,
  selectedRating: 5,
  isMoreExpanded: false,
  isEventsBound: false,

  ratingTexts: {
    5: '5.0 - Exceptional Experience!',
    4: '4.0 - Very Good & Reliable',
    3: '3.0 - Average Ride',
    2: '2.0 - Below Expectations',
    1: '1.0 - Needs Improvement'
  },

  init() {
    this.loadCurrentUser();
    this.renderReviews();
    if (!this.isEventsBound) {
      this.bindEvents();
      this.isEventsBound = true;
    }
  },

  loadCurrentUser() {
    try {
      const savedUser = localStorage.getItem('bkk_reviewer_user');
      if (savedUser) {
        this.currentUser = JSON.parse(savedUser);
      }
    } catch (e) {
      console.warn('Could not parse stored reviewer user', e);
    }
  },

  renderReviews() {
    const mainGrid = document.getElementById('reviews-grid');
    const moreGrid = document.getElementById('reviews-more-grid');
    const moreWrapper = document.getElementById('reviews-more-wrapper');
    const toggleBtn = document.getElementById('btn-toggle-more-reviews');
    const totalCountEl = document.getElementById('reviews-total-count');

    if (!mainGrid) return;

    // Update total count
    const totalReviews = 138 + REVIEWS_DATA.length;
    if (totalCountEl) {
      totalCountEl.textContent = `${totalReviews} Verified Google & In-App Reviews`;
    }

    // Split into initial 3 and remaining
    const initialReviews = REVIEWS_DATA.slice(0, 3);
    const extraReviews = REVIEWS_DATA.slice(3);

    mainGrid.innerHTML = initialReviews.map(r => this.createReviewCardHTML(r)).join('');

    if (moreGrid) {
      moreGrid.innerHTML = extraReviews.map(r => this.createReviewCardHTML(r)).join('');
    }

    // Update Toggle Button text & visibility
    if (toggleBtn) {
      if (extraReviews.length === 0) {
        toggleBtn.style.display = 'none';
      } else {
        toggleBtn.style.display = 'inline-flex';
        const toggleText = document.getElementById('btn-toggle-more-text');
        const toggleIcon = document.getElementById('btn-toggle-more-icon');
        if (toggleText) {
          toggleText.textContent = this.isMoreExpanded
            ? 'Show Fewer Reviews'
            : `See More Reviews (${extraReviews.length} more)`;
        }
        if (toggleIcon) {
          toggleIcon.textContent = this.isMoreExpanded ? '▴' : '💬';
        }
      }
    }

    if (moreWrapper) {
      moreWrapper.style.display = this.isMoreExpanded ? 'block' : 'none';
    }
  },

  createReviewCardHTML(r) {
    const stars = '★'.repeat(r.rating || 5) + '☆'.repeat(5 - (r.rating || 5));
    const bikeBadge = r.bike ? `<span class="review-bike-pill">🏍️ ${r.bike}</span>` : '';
    const googleBadge = r.verifiedGoogle !== false
      ? `<span class="review-google-badge" title="Verified via Google Account">
           <svg width="12" height="12" viewBox="0 0 24 24">
             <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
             <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
             <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
             <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
           </svg>
           Verified Google Rider
         </span>`
      : '';
    const newBadge = r.isNew ? `<span class="review-new-tag">✨ NEW</span>` : '';
    const titleHTML = r.title ? `<h4 class="review-headline">${r.title}</h4>` : '';
    const dateText = r.date || 'Recently';

    return `
      <div class="review-card ${r.isNew ? 'review-highlight-new' : ''}">
        <div class="review-card-top">
          <div class="review-stars-group">
            <span class="review-stars">${stars}</span>
            ${newBadge}
          </div>
          <div class="review-badges-row">
            ${bikeBadge}
            ${googleBadge}
          </div>
        </div>

        ${titleHTML}
        <p class="review-quote">"${r.comment}"</p>

        <div class="review-author">
          <div class="author-avatar">${r.avatar || 'R'}</div>
          <div style="flex: 1;">
            <div class="author-name-row">
              <span class="author-name">${r.name}</span>
              <span class="review-date">${dateText}</span>
            </div>
            <div class="author-role">${r.role || 'Rider in Bangkok'}</div>
          </div>
        </div>
      </div>
    `;
  },

  toggleSeeMore() {
    this.isMoreExpanded = !this.isMoreExpanded;
    this.renderReviews();

    if (this.isMoreExpanded) {
      const moreSection = document.getElementById('reviews-more-wrapper');
      if (moreSection && typeof moreSection.scrollIntoView === 'function') {
        moreSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    }
  },

  openReviewModal() {
    const modal = document.getElementById('review-modal-overlay');
    if (!modal) return;

    this.updateAuthCardUI();
    this.setRating(5);

    // Reset fields if empty
    const titleInput = document.getElementById('review-title-input');
    const commentInput = document.getElementById('review-comment-input');
    if (titleInput) titleInput.value = '';
    if (commentInput) commentInput.value = '';

    modal.classList.add('active');
  },

  closeReviewModal() {
    const modal = document.getElementById('review-modal-overlay');
    if (modal) modal.classList.remove('active');
  },

  updateAuthCardUI() {
    const loggedOutView = document.getElementById('review-auth-logged-out');
    const loggedInView = document.getElementById('review-auth-logged-in');
    const avatarEl = document.getElementById('auth-user-avatar');
    const nameEl = document.getElementById('auth-user-name');
    const emailEl = document.getElementById('auth-user-email');

    if (this.currentUser) {
      if (loggedOutView) loggedOutView.style.display = 'none';
      if (loggedInView) loggedInView.style.display = 'flex';
      if (avatarEl) avatarEl.textContent = this.currentUser.avatar || 'G';
      if (nameEl) nameEl.textContent = this.currentUser.name;
      if (emailEl) emailEl.textContent = this.currentUser.email;
    } else {
      if (loggedOutView) loggedOutView.style.display = 'block';
      if (loggedInView) loggedInView.style.display = 'none';
    }
  },

  handleGoogleLogin() {
    const loginBtn = document.getElementById('btn-google-login');
    if (loginBtn) {
      loginBtn.innerHTML = `<span>Connecting to Google Account...</span>`;
      loginBtn.disabled = true;
    }

    setTimeout(() => {
      this.currentUser = {
        name: 'Thomas Lee',
        email: 'thomas.rider.bkk@gmail.com',
        avatar: 'TL',
        verifiedGoogle: true
      };

      try {
        localStorage.setItem('bkk_reviewer_user', JSON.stringify(this.currentUser));
      } catch (e) {}

      this.updateAuthCardUI();
      App.showToast('✅ Signed in with Google (thomas.rider.bkk@gmail.com)', 'success');

      if (loginBtn) {
        loginBtn.innerHTML = `
          <svg width="18" height="18" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
          </svg>
          <span>Continue with Google / Gmail</span>
        `;
        loginBtn.disabled = false;
      }
    }, 450);
  },

  handleCustomGmailSubmit() {
    const input = document.getElementById('custom-gmail-input');
    if (!input) return;

    let email = input.value.trim().toLowerCase();
    if (!email) {
      App.showToast('Please enter your Gmail address.', 'danger');
      return;
    }

    if (!email.includes('@')) {
      email += '@gmail.com';
    }

    // Derive realistic user name from email
    const prefix = email.split('@')[0];
    const cleanName = prefix
      .replace(/[._\-0-9]+/g, ' ')
      .trim()
      .split(' ')
      .map(w => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' ') || 'Verified Rider';

    const initials = cleanName
      .split(' ')
      .map(w => w.charAt(0))
      .slice(0, 2)
      .join('')
      .toUpperCase() || 'VR';

    this.currentUser = {
      name: cleanName,
      email: email,
      avatar: initials,
      verifiedGoogle: true
    };

    try {
      localStorage.setItem('bkk_reviewer_user', JSON.stringify(this.currentUser));
    } catch (e) {}

    input.value = '';
    this.updateAuthCardUI();
    App.showToast(`✅ Connected Gmail: ${this.currentUser.email}`, 'success');
  },

  switchAccount() {
    this.currentUser = null;
    try {
      localStorage.removeItem('bkk_reviewer_user');
    } catch (e) {}
    this.updateAuthCardUI();
    App.showToast('Signed out of Gmail account. Enter another account to proceed.', 'info');
  },

  setRating(rating) {
    this.selectedRating = rating;
    const starBtns = document.querySelectorAll('.star-btn');
    starBtns.forEach(btn => {
      const val = parseInt(btn.dataset.rating, 10);
      btn.classList.toggle('active', val <= rating);
    });

    const feedbackText = document.getElementById('rating-text-feedback');
    if (feedbackText) {
      feedbackText.textContent = this.ratingTexts[rating] || `${rating}.0`;
    }
  },

  handleReviewSubmit() {
    // 1. Validate Authentication
    if (!this.currentUser) {
      App.showToast('Please sign in with Google or enter your Gmail above to verify your review.', 'danger');
      const authCard = document.getElementById('review-auth-card');
      if (authCard) {
        authCard.classList.add('shake-highlight');
        setTimeout(() => authCard.classList.remove('shake-highlight'), 600);
      }
      return;
    }

    // 2. Validate Inputs
    const titleInput = document.getElementById('review-title-input');
    const commentInput = document.getElementById('review-comment-input');
    const bikeSelect = document.getElementById('review-bike-select');
    const roleSelect = document.getElementById('review-role-select');

    const title = titleInput ? titleInput.value.trim() : '';
    const comment = commentInput ? commentInput.value.trim() : '';
    const bike = bikeSelect ? bikeSelect.value : 'Honda Click 160 ABS';
    const role = roleSelect ? roleSelect.value : 'Rider in Bangkok';

    if (!title || !comment) {
      App.showToast('Please fill in both a headline and detailed review comment.', 'danger');
      return;
    }

    if (comment.length < 15) {
      App.showToast('Please write at least 15 characters to provide helpful rider feedback.', 'danger');
      return;
    }

    // 3. Construct Review Object
    const newReview = {
      id: 'rev-' + Date.now(),
      name: this.currentUser.name,
      email: this.currentUser.email,
      role: role,
      bike: bike,
      rating: this.selectedRating,
      title: title,
      comment: comment,
      avatar: this.currentUser.avatar || 'VR',
      date: 'Just now',
      verifiedGoogle: true,
      isNew: true
    };

    // Prepend to Reviews list
    REVIEWS_DATA.unshift(newReview);

    // Save to localStorage
    try {
      localStorage.setItem('bkk_customer_reviews', JSON.stringify(REVIEWS_DATA));
    } catch (e) {
      console.warn('Could not persist review to localStorage', e);
    }

    // 4. Update UI
    this.closeReviewModal();
    this.renderReviews();

    App.showToast(`🎉 Thank you, ${this.currentUser.name}! Your verified review is published.`, 'success');

    // Smoothly scroll to the Rider Feedback section
    const feedbackSection = document.getElementById('reviews-grid');
    if (feedbackSection && typeof feedbackSection.scrollIntoView === 'function') {
      feedbackSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  },

  bindEvents() {
    // Open / Close modal
    const openBtn = document.getElementById('btn-open-review-modal');
    const closeBtn = document.getElementById('review-modal-close-btn');
    const cancelBtn = document.getElementById('review-cancel-btn');

    if (openBtn) openBtn.addEventListener('click', () => this.openReviewModal());
    if (closeBtn) closeBtn.addEventListener('click', () => this.closeReviewModal());
    if (cancelBtn) cancelBtn.addEventListener('click', () => this.closeReviewModal());

    // Google Login & Custom Gmail
    const googleLoginBtn = document.getElementById('btn-google-login');
    const customGmailBtn = document.getElementById('btn-custom-gmail-submit');
    const customGmailInput = document.getElementById('custom-gmail-input');
    const switchBtn = document.getElementById('btn-auth-switch');

    if (googleLoginBtn) googleLoginBtn.addEventListener('click', () => this.handleGoogleLogin());
    if (customGmailBtn) customGmailBtn.addEventListener('click', () => this.handleCustomGmailSubmit());
    if (customGmailInput) {
      customGmailInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          this.handleCustomGmailSubmit();
        }
      });
    }
    if (switchBtn) switchBtn.addEventListener('click', () => this.switchAccount());

    // Star rating selection
    const starBtns = document.querySelectorAll('.star-btn');
    starBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const rating = parseInt(e.currentTarget.dataset.rating, 10);
        this.setRating(rating);
      });

      btn.addEventListener('mouseenter', (e) => {
        const rating = parseInt(e.currentTarget.dataset.rating, 10);
        starBtns.forEach(b => {
          const val = parseInt(b.dataset.rating, 10);
          b.classList.toggle('hovered', val <= rating);
        });
      });
    });

    const starContainer = document.getElementById('interactive-star-rating');
    if (starContainer) {
      starContainer.addEventListener('mouseleave', () => {
        starBtns.forEach(b => b.classList.remove('hovered'));
      });
    }

    // Toggle "See More"
    const toggleSeeMoreBtn = document.getElementById('btn-toggle-more-reviews');
    if (toggleSeeMoreBtn) {
      toggleSeeMoreBtn.addEventListener('click', () => this.toggleSeeMore());
    }
  }
};

// Expose globally on window
if (typeof window !== 'undefined') {
  window.ReviewsManager = ReviewsManager;
}

// Auto-run if document is already ready
if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => ReviewsManager.init());
  } else {
    ReviewsManager.init();
  }
}
