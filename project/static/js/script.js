'use strict';

/* ─────────────────────────────────────────────────────────────
   1. HERO SLIDER
   ───────────────────────────────────────────────────────────── */
const Slider = (() => {
  let current = 0, total = 0, autoTimer = null;
  const INTERVAL = 5000;

  function init() {
    const slides  = document.querySelectorAll('.slide');
    const dotsWrap = document.getElementById('sliderDots');
    const prevBtn  = document.getElementById('sliderPrev');
    const nextBtn  = document.getElementById('sliderNext');
    if (!slides.length) return;
    total = slides.length;

    if (dotsWrap) {
      dotsWrap.innerHTML = '';
      slides.forEach((_, i) => {
        const dot = document.createElement('button');
        dot.className = 'slider-dot' + (i === 0 ? ' active' : '');
        dot.setAttribute('aria-label', 'Slide ' + (i + 1));
        dot.addEventListener('click', () => goTo(i));
        dotsWrap.appendChild(dot);
      });
    }
    prevBtn && prevBtn.addEventListener('click', () => move(-1));
    nextBtn && nextBtn.addEventListener('click', () => move(1));
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
  function startAuto() { clearInterval(autoTimer); autoTimer = setInterval(() => move(1), INTERVAL); }
  function resetAuto() { clearInterval(autoTimer); autoTimer = setInterval(() => move(1), INTERVAL); }
  return { init };
})();

/* ─────────────────────────────────────────────────────────────
   2. MOBILE NAV
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
    document.addEventListener('click', (e) => {
      if (!toggle.contains(e.target) && !links.contains(e.target)) {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
  return { init };
})();

/* ─────────────────────────────────────────────────────────────
   3. STATS COUNTER
   ───────────────────────────────────────────────────────────── */
const StatsCounter = (() => {
  function animateCounter(el) {
    const target  = parseInt(el.dataset.target, 10);
    const suffix  = el.dataset.suffix || '';
    const display = el.dataset.display;
    if (display) { el.textContent = display; return; }
    let cur = 0;
    const step = Math.ceil(target / 60);
    const t = setInterval(() => {
      cur = Math.min(cur + step, target);
      el.textContent = cur + suffix;
      if (cur >= target) clearInterval(t);
    }, 30);
  }
  function init() {
    const counters = document.querySelectorAll('.stat-counter');
    if (!counters.length) return;
    const section = document.getElementById('statsRow');
    if (!section) return;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          counters.forEach(c => {
            if (!c.dataset.animated) { c.dataset.animated = 'true'; animateCounter(c); }
          });
        }
      });
    }, { threshold: 0.3 });
    observer.observe(section);
  }
  return { init };
})();

/* ─────────────────────────────────────────────────────────────
   4. CALENDAR
   ───────────────────────────────────────────────────────────── */
const Calendar = (() => {
  const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  let calDate = new Date();
  let dbEvents = [];  // filled by initWithData()

  function getEventDays() {
    return dbEvents
      .filter(e => {
        const d = new Date(e.date);
        return d.getFullYear() === calDate.getFullYear() &&
               d.getMonth()    === calDate.getMonth();
      })
      .map(e => new Date(e.date).getDate());
  }

  function renderCal() {
    const yearEl  = document.getElementById('calYear');
    const monthEl = document.getElementById('calMonth');
    const grid    = document.getElementById('calGrid');
    if (!grid) return;

    if (yearEl)  yearEl.textContent  = calDate.getFullYear();
    if (monthEl) monthEl.textContent = MONTHS[calDate.getMonth()];

    grid.innerHTML = '';
    const eventDays = getEventDays();

    ['SUN','MON','TUE','WED','THU','FRI','SAT'].forEach((d, i) => {
      const el = document.createElement('div');
      el.className = 'cal-dow' + (i === 0 ? ' sun' : '');
      el.textContent = d;
      grid.appendChild(el);
    });

    const first    = new Date(calDate.getFullYear(), calDate.getMonth(), 1).getDay();
    const days     = new Date(calDate.getFullYear(), calDate.getMonth() + 1, 0).getDate();
    const prevDays = new Date(calDate.getFullYear(), calDate.getMonth(), 0).getDate();
    const today    = new Date();

    // Prev month tail
    for (let i = first - 1; i >= 0; i--) {
      const el = document.createElement('div');
      el.className = 'cal-day other' + (i === first - 1 ? ' sun-col' : '');
      el.innerHTML = `<span>${String(prevDays - i).padStart(2,'0')}</span>`;
      grid.appendChild(el);
    }

    // Current month
    for (let d = 1; d <= days; d++) {
      const colIndex = (first + d - 1) % 7;
      const isSun    = colIndex === 0;
      const isToday  = d === today.getDate() &&
                       calDate.getMonth()    === today.getMonth() &&
                       calDate.getFullYear() === today.getFullYear();
      const hasEv    = eventDays.includes(d);

      let cls = 'cal-day';
      if (isSun)   cls += ' sun-col';
      if (isToday) cls += ' today';
      if (hasEv)   cls += ' has-event';

      const el = document.createElement('div');
      el.className = cls;
      el.innerHTML = `<span>${String(d).padStart(2,'0')}</span>`;
      if (hasEv) {
        el.style.cursor = 'pointer';
        el.addEventListener('click', () => highlightEvent(d));
      }
      grid.appendChild(el);
    }

    // Next month fill
    const cells     = first + days;
    const remaining = cells % 7 === 0 ? 0 : 7 - (cells % 7);
    for (let d = 1; d <= remaining; d++) {
      const el = document.createElement('div');
      el.className = 'cal-day other';
      el.innerHTML = `<span>${String(d).padStart(2,'0')}</span>`;
      grid.appendChild(el);
    }
  }

  function highlightEvent(day) {
    document.querySelectorAll('.event-item').forEach(el => el.classList.remove('event-item--highlight'));
    const dayStr = String(day).padStart(2,'0');
    document.querySelectorAll('.event-item').forEach(item => {
      const dayEl = item.querySelector('.ev-day');
      if (dayEl && dayEl.textContent.trim() === dayStr) {
        item.classList.add('event-item--highlight');
        item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        setTimeout(() => item.classList.remove('event-item--highlight'), 2000);
      }
    });
  }

  function initWithData(data) {
    dbEvents = data || [];
    renderCal();
  }

  window.calPrev = () => { calDate.setMonth(calDate.getMonth() - 1); renderCal(); };
  window.calNext = () => { calDate.setMonth(calDate.getMonth() + 1); renderCal(); };

  return { init: renderCal, initWithData, highlightEvent };
})();

/* ─────────────────────────────────────────────────────────────
   5. NOTICE SCROLL
   ───────────────────────────────────────────────────────────── */
const NoticeScroll = (() => {
  let pos = 0;
  window.noticeScroll = (dir) => {
    const list = document.getElementById('noticeList');
    if (!list) return;
    pos = Math.max(0, Math.min(pos + dir * 80, list.scrollHeight - list.clientHeight));
    list.scrollTop = pos;
  };
  return { init() {} };
})();

/* ─────────────────────────────────────────────────────────────
   6. ADMISSION COUNTDOWN — FIX: guard against null element
   ───────────────────────────────────────────────────────────── */
function updateAdmissionCountdown() {
  const el = document.getElementById('admissionCountdown');
  if (!el) return;   // ← guard: element may not exist on every page

  const deadline = new Date('2026-08-15T23:59:59');
  const diff     = deadline - new Date();

  if (diff <= 0) { el.innerHTML = 'Open'; return; }

  const days  = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  el.innerHTML = `${days}d ${hours}h`;
}

/* ─────────────────────────────────────────────────────────────
   7. COURSE SEARCH
   ───────────────────────────────────────────────────────────── */
window.searchCourse = () => {
  const keyword = document.getElementById('courseKeyword');
  const faculty  = document.getElementById('courseFaculty');
  const dept     = document.getElementById('courseDept');
  const params   = new URLSearchParams();
  if (keyword && keyword.value.trim()) params.set('q', keyword.value.trim());
  if (faculty && faculty.value)        params.set('faculty', faculty.value);
  if (dept    && dept.value)           params.set('dept', dept.value);
  if (!params.toString()) return;
  window.location.href = '/programs/?' + params.toString();
};

/* ─────────────────────────────────────────────────────────────
   8. HERO SEARCH
   ───────────────────────────────────────────────────────────── */
window.doSearch = () => {
  const input = document.getElementById('heroSearch');
  const q = input ? input.value.trim() : '';
  if (!q) return;
  window.location.href = 'https://www.google.com/search?q=site:ewubd.edu+' + encodeURIComponent(q);
};

/* ─────────────────────────────────────────────────────────────
   9. BACK TO TOP
   ───────────────────────────────────────────────────────────── */
window.scrollToTop = () => window.scrollTo({ top: 0, behavior: 'smooth' });

/* ─────────────────────────────────────────────────────────────
   10. ENQUIRY MODAL
   ───────────────────────────────────────────────────────────── */
window.openEnquiry = () => {
  const modal = document.getElementById('enquiryModal');
  if (modal) modal.classList.add('open');
};
window.closeEnquiry = () => {
  const modal = document.getElementById('enquiryModal');
  if (modal) modal.classList.remove('open');
};
window.submitEnquiry = (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('.modal-submit');
  const orig = btn.textContent;
  btn.textContent = 'Sending...';
  btn.disabled = true;
  setTimeout(() => {
    btn.textContent = '✓ Sent!';
    btn.style.background = '#28a745';
    setTimeout(() => {
      window.closeEnquiry();
      e.target.reset();
      btn.textContent = orig;
      btn.disabled = false;
      btn.style.background = '';
    }, 2200);
  }, 1200);
};

/* ─────────────────────────────────────────────────────────────
   11. HIT COUNTER
   ───────────────────────────────────────────────────────────── */
const HitCounter = (() => {
  function init() {
    const el = document.getElementById('hitCounter');
    if (el) el.textContent = '203,899,152 Total view, 31,123,734 Unique view';
  }
  return { init };
})();

/* ─────────────────────────────────────────────────────────────
   12. TICKER PAUSE ON HOVER
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
   13. PARTNERS SCROLL
   ───────────────────────────────────────────────────────────── */
const PartnersTicker = (() => {
  function init() {
    const track = document.getElementById('partnersTrack');
    if (!track) return;
    let pos = 0;
    setInterval(() => {
      pos += 1;
      const half = track.scrollWidth / 2;
      if (pos >= half) pos = 0;
      track.style.transform = 'translateX(-' + pos + 'px)';
    }, 20);
  }
  return { init };
})();

/* ─────────────────────────────────────────────────────────────
   14. LIVE CHAT — FIX: all functions defined at module level
                        so onclick="" attributes always work
   ───────────────────────────────────────────────────────────── */
function getCookie(name) {
  let value = null;
  if (document.cookie) {
    document.cookie.split(';').forEach(c => {
      c = c.trim();
      if (c.startsWith(name + '=')) value = decodeURIComponent(c.slice(name.length + 1));
    });
  }
  return value;
}

// ── Exposed as plain window functions so onclick="toggleChat()" works ──

window.toggleChat = function () {
  const chat = document.getElementById('chatWidget');
  if (!chat) return;
  chat.classList.toggle('active');
  if (chat.classList.contains('active')) {
    const input = document.getElementById('chatInput');
    if (input) input.focus();
  }
};

window.sendMessage = function () {
  const input = document.getElementById('chatInput');
  const body  = document.getElementById('chatBody');
  if (!input || !body) return;

  const msg = input.value.trim();
  if (!msg || input.disabled) return;

  // User bubble
  const userBubble = document.createElement('div');
  userBubble.className = 'chat-message user';
  userBubble.textContent = msg;
  body.appendChild(userBubble);
  input.value   = '';
  input.disabled = true;
  body.scrollTop = body.scrollHeight;

  // Typing indicator
  const typingEl = document.createElement('div');
  typingEl.className = 'chat-message bot typing';
  typingEl.innerHTML = '<span></span><span></span><span></span>';
  body.appendChild(typingEl);
  body.scrollTop = body.scrollHeight;

  fetch('/chat/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ message: msg }),
  })
    .then(res => {
      if (!res.ok) throw new Error('Network response was not ok');
      return res.json();
    })
    .then(data => {
      typingEl.remove();
      const botBubble = document.createElement('div');
      botBubble.className = 'chat-message bot';
      botBubble.textContent = data.reply;
      body.appendChild(botBubble);
      body.scrollTop = body.scrollHeight;
      input.disabled = false;
      input.focus();
    })
    .catch(() => {
      typingEl.remove();
      const errBubble = document.createElement('div');
      errBubble.className = 'chat-message bot';
      errBubble.textContent = 'Connection error. Please try again.';
      body.appendChild(errBubble);
      input.disabled = false;
    });
};

const Chat = (() => {
  function init() {
    const input = document.getElementById('chatInput');
    if (input) {
      input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') window.sendMessage();
      });
    }
  }
  return { init };
})();

/* ─────────────────────────────────────────────────────────────
   FINAL INIT
   ───────────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  Slider.init();
  MobileNav.init();
  StatsCounter.init();
  Calendar.init();
  NoticeScroll.init();
  HitCounter.init();
  Ticker.init();
  PartnersTicker.init();
  Chat.init();
  updateAdmissionCountdown();
  setInterval(updateAdmissionCountdown, 60000);
});