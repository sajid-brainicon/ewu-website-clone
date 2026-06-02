// Statistics Counter with Intersection Observer
document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('.counter');
    const speed = 200;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                counters.forEach(counter => {
                    const updateCount = () => {
                        const target = +counter.getAttribute('data-target');
                        const count = +counter.innerText;
                        const inc = target / speed;
                        if (count < target) {
                            counter.innerText = Math.ceil(count + inc);
                            setTimeout(updateCount, 10);
                        } else {
                            counter.innerText = target;
                        }
                    };
                    updateCount();
                });
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    const counterSection = document.getElementById('counterSection');
    if (counterSection) observer.observe(counterSection);
});

// Lightbox: set modal image from gallery click
document.addEventListener('click', function(e) {
    if (e.target.closest('.gallery-item')) {
        e.preventDefault();
        const imgSrc = e.target.closest('.gallery-item').getAttribute('data-img');
        document.getElementById('lightboxImage').src = imgSrc;
    }
});

// code from claude
/**
 * EWU Home Page JavaScript
 * File: static/js/home.js
 *
 * Sections:
 *  1. Hero Slider
 *  2. Mobile Nav Toggle
 *  3. Stats Counter (Intersection Observer)
 *  4. Calendar Widget
 *  5. Notice Scroll
 *  6. Achievements Carousel
 *  7. Course Search
 *  8. Hero Search
 *  9. Back-to-Top + Floating Buttons
 * 10. Enquiry Modal
 * 11. Ticker pause on hover (already in CSS, reinforced here)
 * 12. Hit Counter (stub)
 * 13. Init
 */

'use strict';

/* ─────────────────────────────────────────────────────────────
   1. HERO SLIDER
   ───────────────────────────────────────────────────────────── */
const Slider = (() => {
  let current    = 0;
  let total      = 0;
  let autoTimer  = null;
  const INTERVAL = 5000;

  function init() {
    const slides   = document.querySelectorAll('.slide');
    const dotsWrap = document.getElementById('sliderDots');
    const prevBtn  = document.getElementById('sliderPrev');
    const nextBtn  = document.getElementById('sliderNext');

    if (!slides.length) return;
    total = slides.length;

    /* Build dots */
    dotsWrap.innerHTML = '';
    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className   = 'slider-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('role', 'tab');
      dot.setAttribute('aria-label', 'Slide ' + (i + 1));
      dot.addEventListener('click', () => goTo(i));
      dotsWrap.appendChild(dot);
    });

    prevBtn && prevBtn.addEventListener('click', () => move(-1));
    nextBtn && nextBtn.addEventListener('click', () => move(1));

    /* Keyboard navigation */
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft')  move(-1);
      if (e.key === 'ArrowRight') move(1);
    });

    /* Touch / swipe */
    let touchStartX = 0;
    const slider = document.getElementById('heroSlider');
    slider.addEventListener('touchstart', (e) => { touchStartX = e.changedTouches[0].clientX; }, { passive: true });
    slider.addEventListener('touchend',   (e) => {
      const diff = touchStartX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) move(diff > 0 ? 1 : -1);
    }, { passive: true });

    startAuto();
  }

  function goTo(index) {
    const slides = document.querySelectorAll('.slide');
    const dots   = document.querySelectorAll('.slider-dot');
    if (!slides.length) return;

    slides[current].classList.remove('active');
    dots[current] && dots[current].classList.remove('active');

    current = (index + total) % total;

    slides[current].classList.add('active');
    dots[current] && dots[current].classList.add('active');

    resetAuto();
  }

  function move(dir) { goTo(current + dir); }

  function startAuto() {
    clearInterval(autoTimer);
    autoTimer = setInterval(() => move(1), INTERVAL);
  }

  function resetAuto() {
    clearInterval(autoTimer);
    autoTimer = setInterval(() => move(1), INTERVAL);
  }

  return { init };
})();


/* ─────────────────────────────────────────────────────────────
   2. MOBILE NAV TOGGLE
   ───────────────────────────────────────────────────────────── */
const MobileNav = (() => {
  function init() {
    const toggle = document.getElementById('navToggle');
    const links  = document.getElementById('navLinks');
    if (!toggle || !links) return;

    toggle.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });

    /* Close on outside click */
    document.addEventListener('click', (e) => {
      if (!toggle.contains(e.target) && !links.contains(e.target)) {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });

    /* Highlight active link */
    const current = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
      const href = link.getAttribute('href');
      if (href && current.endsWith(href) && href !== '#') {
        link.classList.add('active');
      }
    });
  }
  return { init };
})();


/* ─────────────────────────────────────────────────────────────
   3. STATS COUNTER  (Intersection Observer)
   ───────────────────────────────────────────────────────────── */
const StatsCounter = (() => {
  function animateCounter(el) {
    const target  = parseInt(el.dataset.target, 10);
    const suffix  = el.dataset.suffix || '';
    const display = el.dataset.display || null;   /* e.g. "10k+" */
    const duration = 1800;                         /* ms */
    const start    = performance.now();

    if (display) { /* Static display value, no animation needed */
      el.textContent = display;
      return;
    }

    function step(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      /* Ease-out cubic */
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = Math.floor(eased * target);
      el.textContent = value + suffix;
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = target + suffix;
    }

    requestAnimationFrame(step);
  }

  function init() {
    const counters = document.querySelectorAll('.stat-counter');
    if (!counters.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          counters.forEach(c => {
            if (!c.dataset.animated) {
              c.dataset.animated = 'true';
              animateCounter(c);
            }
          });
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });

    const section = document.getElementById('statsRow');
    if (section) observer.observe(section);
  }

  return { init };
})();


/* ─────────────────────────────────────────────────────────────
   4. CALENDAR WIDGET
   ───────────────────────────────────────────────────────────── */
const Calendar = (() => {
  const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun',
                  'Jul','Aug','Sep','Oct','Nov','Dec'];

  let viewYear  = new Date().getFullYear();
  let viewMonth = new Date().getMonth(); // 0-based

  // month is 0-based (0 = January)
  const events = [
    { year: 2026, month: 5,  day: 17, title: 'Spring in the Air 2026' },
    { year: 2025, month: 10, day: 15, title: 'EWU Job Fair 2025' },
    { year: 2024, month: 8,  day:  1, title: 'Seminar on Stress Management' },
    { year: 2024, month: 7,  day: 13, title: 'Counseling Session on Stress Management' },
  ];

  function getEventDays(year, month) {
    return events
      .filter(e => e.year === year && e.month === month)
      .map(e => e.day);
  }

  function getEventTitle(year, month, day) {
    const ev = events.find(e => e.year === year && e.month === month && e.day === day);
    return ev ? ev.title : '';
  }

  function render() {
    const grid    = document.getElementById('calGrid');
    const yearEl  = document.getElementById('calYear');
    const monthEl = document.getElementById('calMonth');
    if (!grid) return;

    yearEl.textContent  = viewYear;
    monthEl.textContent = MONTHS[viewMonth];

    const today     = new Date();
    const firstDay  = new Date(viewYear, viewMonth, 1).getDay(); // 0 = Sun
    const lastDate  = new Date(viewYear, viewMonth + 1, 0).getDate();
    const prevLast  = new Date(viewYear, viewMonth, 0).getDate();
    const eventDays = getEventDays(viewYear, viewMonth);

    let html = '';

    // ── Day-of-week headers ──
    ['SUN','MON','TUE','WED','THU','FRI','SAT'].forEach((d, i) => {
      html += `<div class="cal-dow${i === 0 ? ' sun' : ''}">${d}</div>`;
    });

    // ── Prev month tail ──
    for (let i = 0; i < firstDay; i++) {
      const d     = prevLast - firstDay + i + 1;
      const isSun = i === 0;
      html += `<div class="cal-day other${isSun ? ' sun-col' : ''}">
                 <span>${String(d).padStart(2,'0')}</span>
               </div>`;
    }

    // ── Current month ──
    for (let d = 1; d <= lastDate; d++) {
      const colIndex = (firstDay + d - 1) % 7;
      const isSun    = colIndex === 0;
      const isToday  = d === today.getDate() &&
                       viewMonth === today.getMonth() &&
                       viewYear  === today.getFullYear();
      const hasEv    = eventDays.includes(d);

      let cls = 'cal-day';
      if (isSun)   cls += ' sun-col';
      if (isToday) cls += ' today';
      if (hasEv)   cls += ' has-event';

      const attrs = hasEv
        ? ` title="${getEventTitle(viewYear, viewMonth, d)}"
            onclick="Calendar.highlightEvent(${d})"` : '';

      html += `<div class="${cls}"${attrs}>
                 <span>${String(d).padStart(2,'0')}</span>
               </div>`;
    }

    // ── Next month fill ──
    const cells     = firstDay + lastDate;
    const remaining = cells % 7 === 0 ? 0 : 7 - (cells % 7);
    for (let d = 1; d <= remaining; d++) {
      const colIndex = (cells + d - 1) % 7;
      const isSun    = colIndex === 0;
      html += `<div class="cal-day other${isSun ? ' sun-col' : ''}">
                 <span>${String(d).padStart(2,'0')}</span>
               </div>`;
    }

    grid.innerHTML = html;
  }

  function highlightEvent(day) {
    document.querySelectorAll('.event-item')
      .forEach(el => el.classList.remove('event-item--highlight'));
    const dayStr = String(day).padStart(2, '0');
    document.querySelectorAll('.event-item').forEach(item => {
      const dayEl = item.querySelector('.ev-day');
      if (dayEl && dayEl.textContent.trim() === dayStr) {
        item.classList.add('event-item--highlight');
        item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        setTimeout(() => item.classList.remove('event-item--highlight'), 2000);
      }
    });
  }

  window.calPrev = () => {
    viewMonth--;
    if (viewMonth < 0) { viewMonth = 11; viewYear--; }
    render();
  };

  window.calNext = () => {
    viewMonth++;
    if (viewMonth > 11) { viewMonth = 0; viewYear++; }
    render();
  };

  document.addEventListener('DOMContentLoaded', render);

  return { init: render, highlightEvent };
})();


/* ─────────────────────────────────────────────────────────────
   5. NOTICE SCROLL (prev / next)
   ───────────────────────────────────────────────────────────── */
const NoticeScroll = (() => {
  const ITEMS_PER_PAGE = 3;
  let currentPage = 0;

  function init() {
    /* Will work even without JS – already shows all notices in HTML.
       JS hides extras and paginates if there are more than ITEMS_PER_PAGE. */
    const list  = document.getElementById('noticeList');
    if (!list) return;
    const items = list.querySelectorAll('.notice-item');
    if (items.length <= ITEMS_PER_PAGE) return; /* nothing to paginate */

    showPage(items, 0);
  }

  function showPage(items, page) {
    currentPage = page;
    const start = page * ITEMS_PER_PAGE;
    items.forEach((item, i) => {
      item.style.display = (i >= start && i < start + ITEMS_PER_PAGE) ? 'flex' : 'none';
    });
  }

  window.noticeScroll = (dir) => {
    const list  = document.getElementById('noticeList');
    if (!list) return;
    const items = list.querySelectorAll('.notice-item');
    const maxPage = Math.ceil(items.length / ITEMS_PER_PAGE) - 1;
    const next = Math.max(0, Math.min(currentPage + dir, maxPage));
    showPage(items, next);
  };

  return { init };
})();


/* ─────────────────────────────────────────────────────────────
   6. ACHIEVEMENTS CAROUSEL
   ───────────────────────────────────────────────────────────── */
const AchCarousel = (() => {
  let achIndex = 0;

  function init() {
    const track = document.getElementById('achTrack');
    if (!track) return;
    update(track);
  }

  function update(track) {
    const cards    = track.querySelectorAll('.ach-card');
    const visible  = getVisibleCount();
    const maxIndex = Math.max(0, cards.length - visible);
    achIndex = Math.max(0, Math.min(achIndex, maxIndex));

    const cardWidth = cards[0] ? cards[0].offsetWidth + 24 : 0;
    track.style.transform = `translateX(-${achIndex * cardWidth}px)`;
  }

  function getVisibleCount() {
    if (window.innerWidth < 600) return 1;
    if (window.innerWidth < 960) return 2;
    return 3;
  }

  window.achScroll = (dir) => {
    const track = document.getElementById('achTrack');
    if (!track) return;
    achIndex += dir;
    update(track);
  };

  window.addEventListener('resize', () => {
    const track = document.getElementById('achTrack');
    if (track) update(track);
  });

  return { init };
})();


/* ─────────────────────────────────────────────────────────────
   7. COURSE SEARCH
   ───────────────────────────────────────────────────────────── */
window.searchCourse = () => {
  const keyword = document.getElementById('courseKeyword');
  const faculty = document.getElementById('courseFaculty');
  const dept    = document.getElementById('courseDept');

  const params = new URLSearchParams();
  if (keyword && keyword.value.trim()) params.set('q',        keyword.value.trim());
  if (faculty && faculty.value)        params.set('faculty',  faculty.value);
  if (dept    && dept.value)           params.set('dept',     dept.value);

  if (!params.toString()) {
    /* No input — show gentle feedback */
    if (keyword) {
      keyword.style.outline = '2px solid #e53935';
      keyword.placeholder   = 'Please enter a keyword';
      setTimeout(() => {
        keyword.style.outline = '';
        keyword.placeholder   = 'Keywords';
      }, 2500);
    }
    return;
  }

  /* Redirect to programs page with query params */
  window.location.href = '/programs/?' + params.toString();
};


/* ─────────────────────────────────────────────────────────────
   8. HERO SEARCH
   ───────────────────────────────────────────────────────────── */
window.doSearch = () => {
  const input = document.getElementById('heroSearch');
  const q     = input ? input.value.trim() : '';
  if (!q) return;
  window.location.href = 'https://www.google.com/search?q=site:ewubd.edu+' + encodeURIComponent(q);
};

/* Also trigger on Enter key */
document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('heroSearch');
  if (input) {
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') window.doSearch();
    });
  }
});


/* ─────────────────────────────────────────────────────────────
   9. BACK-TO-TOP + SCROLL-BASED VISIBILITY
   ───────────────────────────────────────────────────────────── */
const ScrollBtns = (() => {
  function init() {
    const topBtn = document.getElementById('backToTop');
    if (!topBtn) return;

    window.addEventListener('scroll', () => {
      if (window.scrollY > 400) topBtn.classList.add('visible');
      else                       topBtn.classList.remove('visible');
    }, { passive: true });
  }

  return { init };
})();

window.scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};


/* ─────────────────────────────────────────────────────────────
   10. ENQUIRY MODAL
   ───────────────────────────────────────────────────────────── */
window.openEnquiry = () => {
  const modal = document.getElementById('enquiryModal');
  if (modal) {
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
};

window.closeEnquiry = () => {
  const modal = document.getElementById('enquiryModal');
  if (modal) {
    modal.classList.remove('open');
    document.body.style.overflow = '';
  }
};

/* Close on overlay click */
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('enquiryModal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) window.closeEnquiry();
    });
  }
});

/* Close on Escape key */
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') window.closeEnquiry();
});

window.submitEnquiry = (e) => {
  e.preventDefault();
  const btn  = e.target.querySelector('.modal-submit');
  const orig = btn.textContent;
  btn.textContent = 'Sending...';
  btn.disabled = true;

  /* Simulate async submit — replace with fetch('/enquiry/', ...) in production */
  setTimeout(() => {
    btn.textContent = '✓ Sent! We will contact you soon.';
    btn.style.background = '#28a745';
    setTimeout(() => {
      window.closeEnquiry();
      e.target.reset();
      btn.textContent  = orig;
      btn.disabled     = false;
      btn.style.background = '';
    }, 2200);
  }, 1200);
};


/* ─────────────────────────────────────────────────────────────
   11. HIT COUNTER STUB
       Replace with real API / Django view as needed
   ───────────────────────────────────────────────────────────── */
const HitCounter = (() => {
  function init() {
    const el = document.getElementById('hitCounter');
    if (!el) return;
    /* Static placeholder matching screenshot */
    el.textContent = '203,899,152 Total view, 31,123,734 Unique view';
  }
  return { init };
})();


/* ─────────────────────────────────────────────────────────────
   12. TICKER PAUSE ON HOVER  (redundant safety: CSS handles it)
   ───────────────────────────────────────────────────────────── */
const Ticker = (() => {
  function init() {
    const ticker = document.getElementById('tickerContent');
    if (!ticker) return;
    ticker.addEventListener('mouseenter', () => ticker.style.animationPlayState = 'paused');
    ticker.addEventListener('mouseleave', () => ticker.style.animationPlayState = 'running');
  }
  return { init };
})();


/* ─────────────────────────────────────────────────────────────
   13. INIT — run everything after DOM is ready
   ───────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  Slider.init();
  MobileNav.init();
  StatsCounter.init();
  Calendar.init();
  NoticeScroll.init();
  AchCarousel.init();
  ScrollBtns.init();
  HitCounter.init();
  Ticker.init();
});