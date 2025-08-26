// Register service worker for PWA support
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').then(reg => {
      // Show a subtle toast when offline/online status changes
      function showToast(message, type = 'info') {
        let toast = document.createElement('div');
        toast.className = `cb-toast cb-toast-${type}`;
        toast.innerHTML = `<i class="bi bi-wifi${type === 'danger' ? '-off' : ''} me-2"></i>${message}`;
        document.body.appendChild(toast);
        setTimeout(() => {
          toast.classList.add('cb-toast-show');
        }, 10);
        setTimeout(() => {
          toast.classList.remove('cb-toast-show');
          setTimeout(() => document.body.removeChild(toast), 400);
        }, 2500);
      }

      window.addEventListener('offline', () => showToast('You are offline', 'danger'));
      window.addEventListener('online', () => showToast('Back online', 'success'));
    });
  });
}

// Responsive navbar toggle animation
document.addEventListener('DOMContentLoaded', function () {
  const toggler = document.querySelector('.navbar-toggler');
  if (toggler) {
    toggler.addEventListener('click', function () {
      const nav = document.getElementById('navbarNav');
      if (nav) {
        nav.classList.toggle('show');
        nav.classList.add('cb-navbar-anim');
        setTimeout(() => nav.classList.remove('cb-navbar-anim'), 350);
      }
    });
  }
});

// Animate cards on scroll (for .card elements)
function animateOnScroll() {
  const cards = document.querySelectorAll('.card');
  const trigger = window.innerHeight * 0.92;
  cards.forEach(card => {
    const rect = card.getBoundingClientRect();
    if (rect.top < trigger) {
      card.classList.add('cb-card-animate');
    }
  });
}
window.addEventListener('scroll', animateOnScroll);
window.addEventListener('DOMContentLoaded', animateOnScroll);

// Add minimal CSS for toasts and animations
(function injectUICSS() {
  const style = document.createElement('style');
  style.innerHTML = `
    .cb-toast {
      position: fixed;
      left: 50%;
      bottom: 2.5rem;
      transform: translateX(-50%) translateY(40px);
      background: #fff;
      color: #222;
      border-radius: 1.5rem;
      box-shadow: 0 4px 24px rgba(0,0,0,0.08);
      padding: 0.75rem 1.5rem;
      font-size: 1.05rem;
      opacity: 0;
      z-index: 9999;
      transition: all 0.4s cubic-bezier(.4,1.4,.6,1);
      pointer-events: none;
      display: flex;
      align-items: center;
      border: 1px solid #e3e3e3;
    }
    .cb-toast-show { opacity: 1; transform: translateX(-50%) translateY(0); }
    .cb-toast-success { border-color: #198754; color: #198754; }
    .cb-toast-danger { border-color: #dc3545; color: #dc3545; }
    .cb-toast-info { border-color: #0d6efd; color: #0d6efd; }
    .cb-navbar-anim { animation: cb-navbarFade 0.35s; }
    @keyframes cb-navbarFade {
      from { opacity: 0; transform: translateY(-10px);}
      to { opacity: 1; transform: translateY(0);}
    }
    .cb-card-animate {
      animation: cb-cardIn 0.7s cubic-bezier(.4,1.4,.6,1) both;
    }
    @keyframes cb-cardIn {
      from { opacity: 0; transform: translateY(40px) scale(0.97);}
      to { opacity: 1; transform: translateY(0) scale(1);}
    }
  `;
  document.head.appendChild(style);
})();