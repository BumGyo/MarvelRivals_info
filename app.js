/**
 * MARVEL RIVALS SKILL & TEAM-UP DATABASE - APP LOGIC
 * Lightweight, zero-dependency vanilla JS application.
 * Supports Korean (KO), Japanese (JA), and English (EN).
 */

(function () {
  'use strict';

  // Application State
  let heroesData = [];
  let i18nData = {};
  let currentLang = normalizeLang(localStorage.getItem('mr_db_lang') || 'ko');
  let currentRole = 'ALL';
  let searchQuery = '';
  let selectedHero = null;
  let currentFormIndex = 0;
  let selectedSkillIndex = 0;
  let selectedSkillIsUpgraded = false;
  let selectedLoadout = 1;
  let lastFocusedElement = null;
  let isSyncingFromUrl = false;

  // Pre-indexed Translation Caches (O(1) lookups & pre-compiled RegExps)
  let statLabelsExact = Object.create(null);
  let statLabelsLower = new Map();
  let statValuesExact = Object.create(null);
  let statValuesLower = new Map();
  let compiledStatPatterns = [];
  const labelMemo = { ko: new Map(), ja: new Map() };
  const valueMemo = { ko: new Map(), ja: new Map() };

  // DOM Elements
  const logoBtn = document.getElementById('logo-btn');
  const siteLogoSubtitle = document.getElementById('site-logo-subtitle');
  const heroGrid = document.getElementById('hero-grid');
  const heroSearchInput = document.getElementById('hero-search-input');
  const heroesCountEl = document.getElementById('heroes-count');
  const langBtns = document.querySelectorAll('.lang-btn');
  const roleBtns = document.querySelectorAll('.role-btn');

  // Hero Modal Elements
  const modalOverlay = document.getElementById('hero-modal');
  const modalContainer = document.getElementById('modal-container');
  const modalCloseBtn = document.getElementById('modal-close-btn');
  const modalHeroAvatar = document.getElementById('modal-hero-avatar');
  const modalHeroName = document.getElementById('modal-hero-name');
  const modalHeroSubname = document.getElementById('modal-hero-subname');
  const modalBaseStats = document.getElementById('modal-base-stats');
  const tabBtnSkills = document.getElementById('tab-btn-skills');
  const tabBtnTeamups = document.getElementById('tab-btn-teamups');
  const viewSkills = document.getElementById('view-skills');
  const viewTeamups = document.getElementById('view-teamups');
  const heroFormsBar = document.getElementById('hero-forms-bar');
  const skillSelectorList = document.getElementById('skill-selector-list');
  const skillDetailDisplay = document.getElementById('skill-detail-display');
  const loadoutSelector = document.getElementById('loadout-selector');
  const teamupColumns = document.getElementById('teamup-columns');

  // Developer Info Modal Elements
  const devInfoBtn = document.getElementById('dev-info-btn');
  const devModal = document.getElementById('dev-modal');
  const devModalCloseBtn = document.getElementById('dev-modal-close-btn');

  const KEY_ORDER = {
    'Left Click': 1,
    'Right Click': 2,
    'Q': 3,
    'SHIFT': 4,
    'Shift': 4,
    'E': 5,
    'F': 6,
    'C': 7,
    'Space': 8,
    'SPACE': 8,
    'V': 9,
    'X': 10,
    'Z': 11,
    'Passive': 20,
    'PASSIVE': 20
  };

  const KEY_FALLBACK_TRANS = {
    'Left Click': { ko: '마우스 좌클릭', ja: '左クリック' },
    'Right Click': { ko: '마우스 우클릭', ja: '右クリック' },
    'Q': { ko: 'Q (궁극기)', ja: 'Q (アルティメット)' },
    'SHIFT': { ko: 'Shift', ja: 'Shift' },
    'Shift': { ko: 'Shift', ja: 'Shift' },
    'SPACE': { ko: 'Space', ja: 'Space' },
    'Space': { ko: 'Space', ja: 'Space' },
    'Passive': { ko: '패시브', ja: 'パッシブ' },
    'PASSIVE': { ko: '패시브', ja: 'パッシブ' },
    'None': { ko: '패시브', ja: 'パッシブ' }
  };

  function normalizeLang(lang) {
    if (lang === 'jp') return 'ja';
    if (lang === 'kr') return 'ko';
    return (lang === 'ko' || lang === 'ja' || lang === 'en') ? lang : 'ko';
  }

  function getUiText() {
    return i18nData[currentLang] || i18nData.en || {};
  }

  function getStatHighlightClass(rawKey) {
    const lower = rawKey.toLowerCase();
    if (lower === 'damage' || lower.endsWith(' damage')) return 'highlight-damage';
    if (lower === 'cooldown' || lower === 'cd' || lower === 'cooldowns') return 'highlight-cooldown';
    if (lower === 'healing' || lower === 'healing amount' || lower.endsWith(' range') || lower === 'range') return 'highlight-range';
    if (lower === 'projectile speed' || lower === 'fire rate' || lower === 'attack interval') return 'highlight-speed';
    if (lower === 'ammo' || lower === 'ammo consumption') return 'highlight-ammo';
    return '';
  }

  function getStatEntries(stats) {
    if (!stats) return [];
    if (Array.isArray(stats)) return stats;
    return Object.entries(stats);
  }

  function translateKeyName(rawKey, keyTransObj, lang) {
    if (!rawKey) return '';
    if (lang === 'en') return rawKey === 'None' ? 'Passive' : rawKey;
    if (keyTransObj && keyTransObj[lang] && keyTransObj[lang] !== rawKey) {
      return keyTransObj[lang];
    }
    return KEY_FALLBACK_TRANS[rawKey]?.[lang] || rawKey;
  }

  /**
   * Build fast O(1) lookup tables and pre-compiled RegExps
   */
  function indexTranslations(trans) {
    if (!trans || typeof trans !== 'object') return;

    statLabelsExact = trans.stat_labels || Object.create(null);
    statLabelsLower = new Map();
    for (const [k, v] of Object.entries(statLabelsExact)) {
      const lk = k.trim().toLowerCase();
      if (!statLabelsLower.has(lk) || (v.ko && v.ko.toLowerCase() !== lk)) {
        statLabelsLower.set(lk, v);
      }
    }

    statValuesExact = trans.stat_values || Object.create(null);
    statValuesLower = new Map();
    for (const [k, v] of Object.entries(statValuesExact)) {
      statValuesLower.set(k.trim().toLowerCase(), v);
    }

    compiledStatPatterns = [];
    for (const p of (trans.stat_patterns || [])) {
      try {
        compiledStatPatterns.push({
          regex: new RegExp(p.regex, 'i'),
          ko: p.ko || '',
          ja: p.ja || p.ko || ''
        });
      } catch (_) {
        // Ignore malformed pattern safely
      }
    }
  }

  /**
   * Pre-sort skills and build a unified search string per hero
   */
  function prepareHeroesData(heroes) {
    const sortSkills = list => {
      if (Array.isArray(list)) {
        list.sort((a, b) => (KEY_ORDER[a.key] || 15) - (KEY_ORDER[b.key] || 15));
      }
    };

    heroes.forEach(hero => {
      sortSkills(hero.skills);
      if (Array.isArray(hero.forms)) {
        hero.forms.forEach(f => sortSkills(f.skills));
      }

      const tokens = [
        hero.id,
        hero.name,
        hero.names?.en,
        hero.names?.ko,
        hero.names?.ja,
        hero.role,
        hero.role_name?.ko,
        hero.role_name?.ja
      ];

      const collectSkillTokens = s => {
        if (!s) return;
        tokens.push(s.name, s.key, s.description_trans?.ko, s.description_trans?.ja);
        if (s.upgrade) tokens.push(s.upgrade.name);
      };

      (hero.skills || []).forEach(collectSkillTokens);
      (hero.forms || []).forEach(f => {
        tokens.push(f.name, f.names?.en, f.names?.ko, f.names?.ja);
        (f.skills || []).forEach(collectSkillTokens);
      });
      (hero.teamups || []).forEach(tu => {
        tokens.push(
          tu.name,
          tu.loadout_name,
          tu.partner_name?.en,
          tu.partner_name?.ko,
          tu.partner_name?.ja
        );
      });

      hero._searchBlob = tokens.filter(Boolean).join(' ').toLowerCase();
    });
  }

  /**
   * Initialize Application
   */
  async function init() {
    const scriptEl = document.querySelector('script[data-version]');
    const version = scriptEl?.getAttribute('data-version') || '1';
    const qs = `?v=${encodeURIComponent(version)}`;

    try {
      const [heroesRes, i18nRes, transRes] = await Promise.all([
        fetch(`data/heroes.json${qs}`),
        fetch(`data/i18n.json${qs}`),
        fetch(`data/translations.json${qs}`).catch(() => null)
      ]);

      if (!heroesRes.ok || !i18nRes.ok) {
        throw new Error(`HTTP ${heroesRes.status || i18nRes.status}`);
      }

      heroesData = await heroesRes.json();
      i18nData = await i18nRes.json();

      if (!Array.isArray(heroesData) || heroesData.length === 0) {
        throw new Error('Hero data is empty or invalid');
      }

      if (transRes && transRes.ok) {
        try {
          indexTranslations(await transRes.json());
        } catch (e) {
          console.warn('Could not parse translations.json:', e);
        }
      }

      prepareHeroesData(heroesData);
      setupEventListeners();
      applyLanguage(currentLang);
      renderHeroGrid();
      syncModalWithHash();
    } catch (err) {
      console.error('Initialization error:', err);
      const t = getUiText();
      heroesCountEl.textContent = '—';
      heroGrid.innerHTML = `
        <div class="empty-state error-state">
          <h3>⚠️ ${escapeHtml(t.loadErrorTitle || '데이터를 불러오는 데 실패했습니다.')}</h3>
          <p>${escapeHtml(err.message)}</p>
        </div>
      `;
    }
  }

  /**
   * Setup Delegated & Global Event Listeners
   */
  function setupEventListeners() {
    // Logo Reset
    if (logoBtn) {
      logoBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (searchQuery || currentRole !== 'ALL') {
          searchQuery = '';
          heroSearchInput.value = '';
          setRoleFilter('ALL');
        }
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }

    // Language Switcher
    langBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const lang = normalizeLang(btn.getAttribute('data-lang'));
        if (lang !== currentLang) {
          currentLang = lang;
          localStorage.setItem('mr_db_lang', currentLang);
          applyLanguage(currentLang);
          renderHeroGrid();
          if (selectedHero) {
            updateModalContent();
          }
        }
      });
    });

    // Role Filter Buttons
    roleBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        setRoleFilter(btn.getAttribute('data-role') || 'ALL');
      });
    });

    // Real-time Search
    heroSearchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim().toLowerCase();
      renderHeroGrid();
    });

    // Delegated Hero Card Click & Keydown
    heroGrid.addEventListener('click', (e) => {
      const card = e.target.closest('.hero-card');
      if (card) {
        openHeroModal(card.getAttribute('data-id'), card);
      }
    });
    heroGrid.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        const card = e.target.closest('.hero-card');
        if (card) {
          e.preventDefault();
          openHeroModal(card.getAttribute('data-id'), card);
        }
      }
    });

    // Delegated Form Switcher Click
    if (heroFormsBar) {
      heroFormsBar.addEventListener('click', (e) => {
        const btn = e.target.closest('.hero-form-btn');
        if (!btn) return;
        const idx = parseInt(btn.getAttribute('data-form-idx'), 10);
        if (!Number.isNaN(idx) && currentFormIndex !== idx) {
          currentFormIndex = idx;
          selectedSkillIndex = 0;
          selectedSkillIsUpgraded = false;
          updateModalContent();
        }
      });
    }

    // Delegated Skill Selector Click
    skillSelectorList.addEventListener('click', (e) => {
      const item = e.target.closest('.skill-select-item');
      if (!item) return;
      const idx = parseInt(item.getAttribute('data-index'), 10);
      if (!Number.isNaN(idx) && selectedSkillIndex !== idx) {
        selectedSkillIndex = idx;
        selectedSkillIsUpgraded = false;
        renderSkillSelectorList();
        renderSkillDetailDisplay();
      }
    });

    // Delegated Skill Upgrade Toggle Click
    skillDetailDisplay.addEventListener('click', (e) => {
      if (e.target.closest('#skill-upgrade-star-btn')) {
        selectedSkillIsUpgraded = !selectedSkillIsUpgraded;
        renderSkillDetailDisplay();
      }
    });

    // Delegated Team-Up Loadout Switcher Click
    loadoutSelector.addEventListener('click', (e) => {
      const btn = e.target.closest('.loadout-btn');
      if (!btn) return;
      const num = parseInt(btn.getAttribute('data-loadout'), 10);
      if (!Number.isNaN(num) && selectedLoadout !== num) {
        selectedLoadout = num;
        renderTeamupTab();
      }
    });

    // Keyboard Shortcuts & Modal Focus Trap
    window.addEventListener('keydown', (e) => {
      const isDevModalOpen = devModal && devModal.classList.contains('open');
      const isHeroModalOpen = modalOverlay && modalOverlay.classList.contains('open');

      if (e.key === '/' && document.activeElement !== heroSearchInput && !isHeroModalOpen && !isDevModalOpen) {
        e.preventDefault();
        heroSearchInput.focus();
        return;
      }

      if (e.key === 'Escape') {
        if (isDevModalOpen) {
          closeDevModal();
        } else if (isHeroModalOpen) {
          closeModal();
        }
        return;
      }

      if (e.key === 'Tab' && (isDevModalOpen || isHeroModalOpen)) {
        trapFocus(e, isDevModalOpen ? devModal : modalContainer);
      }
    });

    // URL Hash Navigation (Back button closes modal on mobile/desktop)
    window.addEventListener('hashchange', syncModalWithHash);

    // Developer Modal
    if (devInfoBtn) {
      devInfoBtn.addEventListener('click', (e) => {
        e.preventDefault();
        openDevModal(devInfoBtn);
      });
    }
    if (devModalCloseBtn) {
      devModalCloseBtn.addEventListener('click', closeDevModal);
    }
    if (devModal) {
      devModal.addEventListener('click', (e) => {
        if (e.target === devModal) closeDevModal();
      });
    }

    // Hero Modal Close & Tabs
    modalCloseBtn.addEventListener('click', () => closeModal());
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeModal();
    });
    tabBtnSkills.addEventListener('click', () => switchModalTab('skills'));
    tabBtnTeamups.addEventListener('click', () => switchModalTab('teamups'));
  }

  function setRoleFilter(role) {
    currentRole = role;
    roleBtns.forEach(b => {
      const active = (b.getAttribute('data-role') || 'ALL') === role;
      b.classList.toggle('active', active);
      b.setAttribute('aria-selected', active ? 'true' : 'false');
    });
    renderHeroGrid();
  }

  function trapFocus(e, container) {
    if (!container) return;
    const focusable = container.querySelectorAll(
      'a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    if (focusable.length === 0) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  /**
   * Sync Hero Modal with URL Hash (#hero=<id or slug>)
   */
  function syncModalWithHash() {
    const hash = window.location.hash || '';
    const match = hash.match(/^#hero=(.+)$/i);
    if (match) {
      const target = decodeURIComponent(match[1]).trim().toLowerCase();
      const hero = heroesData.find(
        h => h.id.toLowerCase() === target || (h.names?.en || h.name || '').toLowerCase() === target
      );
      if (hero && (!selectedHero || selectedHero.id !== hero.id)) {
        isSyncingFromUrl = true;
        openHeroModal(hero.id, null);
        isSyncingFromUrl = false;
      }
    } else if (selectedHero) {
      isSyncingFromUrl = true;
      closeModal();
      isSyncingFromUrl = false;
    }
  }

  /**
   * Apply UI Translations based on selected language
   */
  function applyLanguage(lang) {
    const norm = normalizeLang(lang);
    const t = i18nData[norm] || i18nData.en || {};

    document.documentElement.lang = norm;

    langBtns.forEach(btn => {
      btn.classList.toggle('active', normalizeLang(btn.getAttribute('data-lang')) === norm);
    });

    if (siteLogoSubtitle) {
      siteLogoSubtitle.textContent = t.siteSubtitle || 'SKILL & TEAM-UP DATABASE';
    }
    heroSearchInput.placeholder = t.searchPlaceholder || 'Search hero, form, or skill...';

    document.getElementById('label-all').textContent = t.allRoles || 'All';
    document.getElementById('label-vanguard').textContent = t.vanguard || 'Vanguard';
    document.getElementById('label-duelist').textContent = t.duelist || 'Duelist';
    document.getElementById('label-strategist').textContent = t.strategist || 'Strategist';

    document.getElementById('tab-text-skills').textContent = t.skillsTab || 'Abilities';
    document.getElementById('tab-text-teamups').textContent = t.teamUpTab || 'Team-Up';

    if (modalCloseBtn && t.closeModalLabel) {
      modalCloseBtn.setAttribute('aria-label', t.closeModalLabel);
    }
    if (devInfoBtn && t.devBtnLabel) {
      devInfoBtn.setAttribute('aria-label', t.devBtnLabel);
      devInfoBtn.setAttribute('title', t.devBtnLabel);
    }

    const devBadgeText = document.getElementById('dev-badge-text');
    if (devBadgeText) devBadgeText.textContent = t.devBadge || 'CREATOR INFO';
    const devRoleText = document.getElementById('dev-role-text');
    if (devRoleText) devRoleText.textContent = t.devRole || 'Marvel Rivals Player & Programmer';
    const devSnsHeading = document.getElementById('dev-sns-heading');
    if (devSnsHeading) devSnsHeading.textContent = t.devSnsHeading || 'OFFICIAL CHANNELS & SNS';
  }

  function formatHealth(val, lang, isShort = false) {
    if (!val) return 'N/A';
    let str = String(val).trim();
    if (/regenerative shield/i.test(str)) {
      if (lang === 'ko') {
        str = str.replace(/\s*\bHealth\b/gi, '');
        return str.replace(/regenerative shield/i, isShort ? '보호막' : '재생 보호막').trim();
      }
      if (lang === 'ja') {
        str = str.replace(/\s*\bHealth\b/gi, '');
        return str.replace(/regenerative shield/i, isShort ? 'シールド' : '再生シールド').trim();
      }
      return isShort ? str.replace(/regenerative shield/i, 'Shield') : str;
    }
    if (lang === 'ko') str = str.replace(/\bHealth\b/gi, '체력');
    if (lang === 'ja') str = str.replace(/\bHealth\b/gi, '体力');
    return str;
  }

  function formatSpeed(val) {
    if (!val) return 'N/A';
    const str = String(val).trim();
    const numMatch = str.match(/^(\d+(?:\.\d+)?)$/);
    if (numMatch) {
      let num = parseFloat(numMatch[1]);
      if (num >= 100) num /= 100;
      return `${num} m/s`;
    }
    const msMatch = str.match(/^(\d+(?:\.\d+)?)\s*m\/s$/i);
    if (msMatch) {
      return `${parseFloat(msMatch[1])} m/s`;
    }
    return str;
  }

  function getFilteredHeroes() {
    return heroesData.filter(hero => {
      if (currentRole !== 'ALL') {
        const roles = hero.roles || [hero.role];
        if (!roles.includes(currentRole)) return false;
      }
      if (searchQuery && !hero._searchBlob.includes(searchQuery)) {
        return false;
      }
      return true;
    });
  }

  function renderHeroGrid() {
    const heroes = getFilteredHeroes();
    const t = getUiText();
    const countText = heroes.length === 1
      ? (t.heroCountSingle || '1 Hero')
      : (t.heroCountPlural || '{n} Heroes').replace('{n}', String(heroes.length));
    heroesCountEl.textContent = countText;

    if (heroes.length === 0) {
      heroGrid.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">🔍</div>
          <h3>${escapeHtml(t.noResultsTitle || 'No matching heroes found')}</h3>
          <p>${escapeHtml(t.noResultsDesc || 'Try a different keyword or role filter.')}</p>
        </div>
      `;
      return;
    }

    heroGrid.innerHTML = heroes.map(hero => {
      const displayName = hero.names?.[currentLang] || hero.names?.en || hero.name;
      const subName = currentLang !== 'en' ? (hero.names?.en || hero.name) : '';
      const health = formatHealth(hero.base_stats?.Health, currentLang, true);
      const speed = formatSpeed(hero.base_stats?.['Movement Speed']);
      const roleLower = hero.role.toLowerCase();

      return `
        <article class="hero-card role-${roleLower}" data-id="${escapeHtml(hero.id)}" tabindex="0" role="button" aria-label="${escapeHtml(displayName)}">
          <div class="hero-avatar-wrapper">
            <img src="${escapeHtml(hero.avatar)}" alt="${escapeHtml(displayName)}" class="hero-avatar" loading="lazy" decoding="async">
            <div class="role-pill ${escapeHtml(hero.role)}" title="${escapeHtml(hero.role)}">
              <img src="assets/icons/role_${escapeHtml(roleLower)}.png" class="role-pill-icon" alt="${escapeHtml(hero.role)}">
            </div>
          </div>
          <div class="hero-info">
            <h3 class="hero-name-primary">${escapeHtml(displayName)}</h3>
            ${subName ? `<div class="hero-name-sub">${escapeHtml(subName)}</div>` : '<div class="hero-name-sub"></div>'}
            <div class="hero-chips">
              <span class="stat-chip">HP <strong>${escapeHtml(health)}</strong></span>
              <span class="stat-chip">SPD <strong>${escapeHtml(speed)}</strong></span>
            </div>
          </div>
        </article>
      `;
    }).join('');
  }

  /**
   * Open & Close Modals
   */
  function openHeroModal(heroId, triggerEl) {
    const hero = heroesData.find(h => h.id === heroId);
    if (!hero) return;

    lastFocusedElement = triggerEl || document.activeElement;
    selectedHero = hero;

    if (hero.forms && hero.forms.length > 0) {
      currentFormIndex = (hero.names?.en?.toUpperCase() === 'HULK' && hero.forms[1]) ? 1 : 0;
    } else {
      currentFormIndex = 0;
    }
    selectedSkillIndex = 0;
    selectedSkillIsUpgraded = false;
    selectedLoadout = 1;

    updateModalContent();
    switchModalTab('skills');

    modalOverlay.classList.add('open');
    modalOverlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';

    if (!isSyncingFromUrl) {
      const targetHash = `#hero=${encodeURIComponent(hero.id)}`;
      if (window.location.hash !== targetHash) {
        history.pushState(null, '', targetHash);
      }
    }

    modalCloseBtn.focus({ preventScroll: true });
  }

  function closeModal() {
    if (!modalOverlay.classList.contains('open')) return;
    modalOverlay.classList.remove('open');
    modalOverlay.setAttribute('aria-hidden', 'true');
    if (!devModal || !devModal.classList.contains('open')) {
      document.body.style.overflow = '';
    }
    selectedHero = null;

    if (!isSyncingFromUrl && window.location.hash.startsWith('#hero=')) {
      history.pushState(null, '', window.location.pathname + window.location.search);
    }

    if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
      lastFocusedElement.focus({ preventScroll: true });
      lastFocusedElement = null;
    }
  }

  function openDevModal(triggerEl) {
    if (!devModal) return;
    lastFocusedElement = triggerEl || document.activeElement;
    devModal.classList.add('open');
    devModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    if (devModalCloseBtn) devModalCloseBtn.focus({ preventScroll: true });
  }

  function closeDevModal() {
    if (!devModal || !devModal.classList.contains('open')) return;
    devModal.classList.remove('open');
    devModal.setAttribute('aria-hidden', 'true');
    if (!modalOverlay || !modalOverlay.classList.contains('open')) {
      document.body.style.overflow = '';
    }
    if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
      lastFocusedElement.focus({ preventScroll: true });
      lastFocusedElement = null;
    }
  }

  function switchModalTab(tab) {
    const isSkills = tab === 'skills';
    tabBtnSkills.classList.toggle('active', isSkills);
    tabBtnSkills.setAttribute('aria-selected', isSkills ? 'true' : 'false');
    tabBtnTeamups.classList.toggle('active', !isSkills);
    tabBtnTeamups.setAttribute('aria-selected', !isSkills ? 'true' : 'false');

    viewSkills.classList.toggle('active', isSkills);
    viewTeamups.classList.toggle('active', !isSkills);
    if (!isSkills) {
      renderTeamupTab();
    }
  }

  function getActiveHeroSkills() {
    if (!selectedHero) return [];
    const activeForm = (selectedHero.forms && selectedHero.forms[currentFormIndex])
      ? selectedHero.forms[currentFormIndex]
      : null;
    return (activeForm && activeForm.skills && activeForm.skills.length > 0)
      ? activeForm.skills
      : (selectedHero.skills || []);
  }

  function updateModalContent() {
    if (!selectedHero) return;

    const hero = selectedHero;
    const activeForm = (hero.forms && hero.forms[currentFormIndex]) ? hero.forms[currentFormIndex] : null;
    const t = getUiText();

    const displayName = hero.names?.[currentLang] || hero.names?.en || hero.name;
    const subName = currentLang !== 'en' ? (hero.names?.en || hero.name) : '';

    modalHeroAvatar.src = (activeForm && activeForm.avatar) ? activeForm.avatar : hero.avatar;
    modalHeroAvatar.alt = displayName;
    modalHeroName.textContent = displayName;

    const roleTrans = hero.role_name?.[currentLang] || hero.role;
    modalHeroSubname.innerHTML = `
      ${subName ? `<span>${escapeHtml(subName)}</span>` : ''}
      <span class="modal-role-badge ${escapeHtml(hero.role)}">
        <img src="assets/icons/role_${escapeHtml(hero.role.toLowerCase())}.png" class="modal-role-icon" alt="${escapeHtml(hero.role)}">
        ${escapeHtml(roleTrans)}
      </span>
    `;

    const baseStats = (activeForm && activeForm.base_stats) ? activeForm.base_stats : hero.base_stats;
    const health = formatHealth(baseStats?.Health, currentLang, false);
    const speed = formatSpeed(baseStats?.['Movement Speed']);
    const rawMode = baseStats?.['Movement Mode'] || 'Ground';
    const modeDisplay = rawMode === 'Flight' ? (t.modeFlight || 'Flight') : (t.modeGround || 'Ground');

    modalBaseStats.innerHTML = `
      <div class="base-stat-badge">❤️ ${escapeHtml(t.health || 'Health')}: <strong>${escapeHtml(health)}</strong></div>
      <div class="base-stat-badge">⚡ ${escapeHtml(t.speed || 'Speed')}: <strong>${escapeHtml(speed)}</strong></div>
      <div class="base-stat-badge">🚀 ${escapeHtml(t.movementMode || 'Movement')}: <strong>${escapeHtml(modeDisplay)}</strong></div>
    `;

    renderHeroFormsBar();
    renderSkillSelectorList();
    renderSkillDetailDisplay();
    if (viewTeamups.classList.contains('active')) {
      renderTeamupTab();
    }
  }

  function renderHeroFormsBar() {
    if (!heroFormsBar) return;
    if (!selectedHero || !selectedHero.forms || selectedHero.forms.length <= 1) {
      heroFormsBar.style.display = 'none';
      heroFormsBar.innerHTML = '';
      return;
    }

    heroFormsBar.style.display = 'flex';
    heroFormsBar.innerHTML = selectedHero.forms.map((f, idx) => {
      const isActive = idx === currentFormIndex;
      const formName = f.names?.[currentLang] || f.name;
      const avatarSrc = f.avatar || selectedHero.avatar;
      return `
        <button type="button" class="hero-form-btn ${isActive ? 'active' : ''}" data-form-idx="${idx}" aria-pressed="${isActive ? 'true' : 'false'}">
          <img src="${escapeHtml(avatarSrc)}" class="hero-form-avatar" alt="">
          <span>${escapeHtml(formName)}</span>
        </button>
      `;
    }).join('');
  }

  function renderSkillSelectorList() {
    if (!selectedHero) return;
    const skills = getActiveHeroSkills();

    skillSelectorList.innerHTML = skills.map((s, idx) => {
      const isActive = idx === selectedSkillIndex;
      const keyTrans = translateKeyName(s.key, s.key_trans, currentLang);
      const iconHtml = s.icon
        ? `<img src="${escapeHtml(s.icon)}" alt="" class="skill-select-icon" loading="lazy">`
        : `<span class="skill-select-icon skill-icon-fallback">${escapeHtml(s.key)}</span>`;

      return `
        <button type="button" class="skill-select-item ${isActive ? 'active' : ''}" data-index="${idx}" aria-pressed="${isActive ? 'true' : 'false'}">
          ${iconHtml}
          <span class="skill-select-details">
            <span class="skill-select-name">${escapeHtml(s.name)}</span>
            <span class="skill-select-key">${escapeHtml(keyTrans)}</span>
          </span>
        </button>
      `;
    }).join('');
  }

  function renderSkillDetailDisplay() {
    const t = getUiText();
    const skills = getActiveHeroSkills();

    if (!selectedHero || !skills[selectedSkillIndex]) {
      skillDetailDisplay.innerHTML = `<p class="muted-notice">${escapeHtml(t.noSkillSelected || 'No ability selected.')}</p>`;
      return;
    }

    const rawSkill = skills[selectedSkillIndex];
    const hasUpgrade = Boolean(rawSkill.upgrade);
    const activeSkill = (hasUpgrade && selectedSkillIsUpgraded) ? rawSkill.upgrade : rawSkill;
    const keyTrans = translateKeyName(rawSkill.key, rawSkill.key_trans, currentLang);

    const activeSkillDesc = getSkillDescription(activeSkill, currentLang);
    const descHtml = activeSkillDesc
      ? `<div class="skill-desc-box">${escapeHtml(activeSkillDesc)}</div>`
      : '';

    const iconHtml = activeSkill.icon
      ? `<img src="${escapeHtml(activeSkill.icon)}" alt="" class="skill-large-icon">`
      : `<div class="skill-large-icon skill-icon-fallback-lg">${escapeHtml(rawSkill.key)}</div>`;

    const upgradeBtnTitle = selectedSkillIsUpgraded
      ? (t.upgradeViewBase || 'Click to view base stats')
      : (t.upgradeViewUpgraded || 'Click to view upgraded stats');

    const upgradeBtnHtml = hasUpgrade ? `
      <button
        type="button"
        class="skill-upgrade-star-btn ${selectedSkillIsUpgraded ? 'active' : ''}"
        id="skill-upgrade-star-btn"
        title="${escapeHtml(upgradeBtnTitle)}"
        aria-pressed="${selectedSkillIsUpgraded ? 'true' : 'false'}"
      >
        <span class="star-icon">${selectedSkillIsUpgraded ? '★' : '☆'}</span>
        <span class="upgrade-star-label">${selectedSkillIsUpgraded ? 'UPGRADED' : 'UPGRADE'}</span>
      </button>
    ` : '';

    const specHeading = selectedSkillIsUpgraded
      ? (t.upgradedSpecTitle || 'UPGRADED SPECIFICATIONS')
      : (t.specTitle || 'SPECIFICATIONS');

    skillDetailDisplay.innerHTML = `
      <div class="skill-header-info">
        ${iconHtml}
        <div class="skill-header-text">
          <div class="skill-title-row">
            <h3>${escapeHtml(activeSkill.name)}</h3>
            ${upgradeBtnHtml}
          </div>
          <div class="skill-tags-row">
            <span class="key-tag">${escapeHtml(keyTrans)}</span>
            ${(hasUpgrade && selectedSkillIsUpgraded) ? '<span class="upgraded-pill-tag">⚡ UPGRADED</span>' : ''}
          </div>
        </div>
      </div>

      ${descHtml}

      <div>
        <div class="stats-grid-title">📊 ${escapeHtml(specHeading)}</div>
        <div class="stats-grid">
          ${renderStatEntries(activeSkill.stats, false)}
        </div>
      </div>
    `;
  }

  function renderTeamupTab() {
    if (!selectedHero) return;
    const t = getUiText();
    const teamups = selectedHero.teamups || [];

    if (teamups.length === 0) {
      loadoutSelector.innerHTML = '';
      teamupColumns.innerHTML = `
        <div class="empty-state">
          <p>${escapeHtml(t.noTeamups || 'No team-up loadouts registered for this hero.')}</p>
        </div>
      `;
      return;
    }

    const l1Items = teamups.filter(tu => tu.loadout_number === 1);
    const l2Items = teamups.filter(tu => tu.loadout_number === 2);
    if (selectedLoadout === 2 && l2Items.length === 0) {
      selectedLoadout = 1;
    }

    const l1Base = l1Items.find(x => x.tier === 'base') || l1Items[0] || {};
    const l1Enhanced = l1Items.find(x => x.tier === 'enhanced') || l1Items[1] || {};
    const l2Base = l2Items.find(x => x.tier === 'base') || l2Items[0] || {};
    const l2Enhanced = l2Items.find(x => x.tier === 'enhanced') || l2Items[1] || {};

    const l1Name = l1Base.name || l1Enhanced.name || 'Loadout 1';
    const l2Name = l2Base.name || l2Enhanced.name || 'Loadout 2';
    const l1Icon = l1Base.icon || l1Enhanced.icon || '';
    const l2Icon = l2Base.icon || l2Enhanced.icon || '';
    const l1PartnerPic = l1Enhanced.partner_avatar || l1Base.partner_avatar || '';
    const l2PartnerPic = l2Enhanced.partner_avatar || l2Base.partner_avatar || '';

    const loadoutLabel1 = (t.loadoutLabel || 'Loadout {n}').replace('{n}', '1');
    const loadoutLabel2 = (t.loadoutLabel || 'Loadout {n}').replace('{n}', '2');

    loadoutSelector.innerHTML = `
      <button type="button" class="loadout-btn ${selectedLoadout === 1 ? 'active' : ''}" data-loadout="1" aria-pressed="${selectedLoadout === 1 ? 'true' : 'false'}">
        ${l1Icon ? `<img src="${escapeHtml(l1Icon)}" alt="" class="loadout-icon">` : '<span class="loadout-icon-fallback">⚡</span>'}
        <span class="loadout-btn-text">
          <strong>${escapeHtml(l1Name)}</strong>
          <span>${escapeHtml(loadoutLabel1)}</span>
        </span>
        ${l1PartnerPic ? `<img src="${escapeHtml(l1PartnerPic)}" alt="" class="loadout-partner-avatar">` : ''}
      </button>

      ${l2Items.length > 0 ? `
      <button type="button" class="loadout-btn ${selectedLoadout === 2 ? 'active' : ''}" data-loadout="2" aria-pressed="${selectedLoadout === 2 ? 'true' : 'false'}">
        ${l2Icon ? `<img src="${escapeHtml(l2Icon)}" alt="" class="loadout-icon">` : '<span class="loadout-icon-fallback">⚡</span>'}
        <span class="loadout-btn-text">
          <strong>${escapeHtml(l2Name)}</strong>
          <span>${escapeHtml(loadoutLabel2)}</span>
        </span>
        ${l2PartnerPic ? `<img src="${escapeHtml(l2PartnerPic)}" alt="" class="loadout-partner-avatar">` : ''}
      </button>
      ` : ''}
    `;

    const activeItems = selectedLoadout === 1 ? l1Items : l2Items;
    const baseItem = activeItems.find(x => x.tier === 'base') || activeItems[0];
    const enhancedItem = activeItems.find(x => x.tier === 'enhanced') || activeItems[1];

    const partnerPic = enhancedItem?.partner_avatar || baseItem?.partner_avatar || '';
    const partnerNameObj = enhancedItem?.partner_name || baseItem?.partner_name || {};
    const partnerNameDisplay = partnerNameObj[currentLang] || partnerNameObj.en || t.synergyPartnerFallback || 'Synergy Partner';

    const partnerBannerHtml = partnerPic ? `
      <div class="partner-highlight-bar">
        <img src="${escapeHtml(partnerPic)}" alt="${escapeHtml(partnerNameDisplay)}" class="partner-avatar-large">
        <div class="partner-info-text">
          <span class="partner-label">${escapeHtml(t.synergyPartnerLabel || '🤝 SYNERGY PARTNER HERO')}</span>
          <span class="partner-hero-name">${escapeHtml(partnerNameDisplay)}</span>
        </div>
      </div>
    ` : '';

    const baseKeyDisplay = translateKeyName(baseItem?.key || 'Passive', baseItem?.key_trans, currentLang);
    const enhancedKeyDisplay = translateKeyName(enhancedItem?.key || 'Passive', enhancedItem?.key_trans, currentLang);
    const baseDesc = getTeamupDescription(baseItem, 'base', currentLang) || t.baseFallbackDesc || '';
    const enhancedDesc = getTeamupDescription(enhancedItem, 'enhanced', currentLang) ||
      (t.enhancedFallbackDesc || '').replace('{partner}', partnerNameDisplay);

    teamupColumns.innerHTML = `
      ${partnerBannerHtml}

      <div class="teamup-card base">
        <div class="teamup-card-header">
          <span class="teamup-tier-badge base">${escapeHtml(t.baseEffectBadge || '⚡ Base Effect')}</span>
          <span class="teamup-key-label base">${escapeHtml(baseKeyDisplay)}</span>
        </div>
        <div class="teamup-card-title-row">
          ${baseItem?.icon ? `<img src="${escapeHtml(baseItem.icon)}" alt="" class="teamup-mini-icon">` : ''}
          <h4>${escapeHtml(baseItem?.name || 'Base Effect')}</h4>
        </div>
        <div class="teamup-card-desc">${escapeHtml(baseDesc)}</div>
        <div>
          <div class="stats-grid-title">${escapeHtml(t.baseStatsTitle || 'Base Stats')}</div>
          <div class="stats-grid compact-stats-grid">
            ${renderStatEntries(baseItem?.stats, true)}
          </div>
        </div>
      </div>

      <div class="teamup-card enhanced">
        <div class="teamup-card-header">
          <span class="teamup-tier-badge enhanced">${escapeHtml(t.enhancedEffectBadge || '🔥 Enhanced Effect')}</span>
          <span class="teamup-key-label enhanced">${escapeHtml(enhancedKeyDisplay)}</span>
        </div>
        <div class="teamup-card-title-row">
          ${enhancedItem?.icon ? `<img src="${escapeHtml(enhancedItem.icon)}" alt="" class="teamup-mini-icon">` : ''}
          <h4>${escapeHtml(enhancedItem?.name || 'Enhanced Effect')}</h4>
        </div>
        <div class="teamup-card-desc">${escapeHtml(enhancedDesc)}</div>
        <div>
          <div class="stats-grid-title">${escapeHtml(t.enhancedStatsTitle || 'Enhanced Stats')}</div>
          <div class="stats-grid compact-stats-grid">
            ${renderStatEntries(enhancedItem?.stats, true)}
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Render Stat Boxes & Sub-Section Headers (Supports Ordered Tuple Arrays & Duplicate Keys)
   */
  function renderStatEntries(stats, compact) {
    const t = getUiText();
    const entries = getStatEntries(stats).filter(([k]) => k && k.toLowerCase() !== 'key');

    if (entries.length === 0) {
      return `<p class="muted-notice full-span">${escapeHtml(t.noSpecData || 'No specification numbers available.')}</p>`;
    }

    return entries.map(([k, v]) => {
      const valStr = v === null || v === undefined ? '' : String(v).trim();

      // Empty value represents an official NetEase sub-section header (e.g. Punch / Kick, Gatling Gun / Missiles)
      if (!valStr) {
        const headerLabel = translateStatLabel(k, currentLang);
        return `<div class="stat-section-header">${escapeHtml(headerLabel)}</div>`;
      }

      const highlightClass = getStatHighlightClass(k);
      const translatedLabel = translateStatLabel(k, currentLang);
      const translatedValue = translateStatValue(valStr, currentLang);

      return `
        <div class="stat-box ${highlightClass} ${compact ? 'stat-box-compact' : ''}">
          <span class="stat-label">${escapeHtml(translatedLabel)}</span>
          <span class="stat-value">${escapeHtml(translatedValue)}</span>
        </div>
      `;
    }).join('');
  }

  function getSkillDescription(skill, lang) {
    if (!skill) return '';
    if (lang === 'en') return skill.description || '';
    return skill.description_trans?.[lang] || skill.description || '';
  }

  function getTeamupDescription(item, tier, lang) {
    if (!item) return '';
    if (lang === 'en') {
      const desc = item.description || '';
      if (/Base Effect\s*:/i.test(desc) || /Enhanced Effect\s*:/i.test(desc)) {
        if (tier === 'base') {
          const m = desc.match(/Base Effect\s*:\s*([\s\S]*?)(?=\n?\s*Enhanced Effect\s*:|$)/i);
          return m ? m[1].trim() : desc;
        }
        const m = desc.match(/Enhanced Effect\s*:\s*([\s\S]*)$/i);
        return m ? m[1].trim() : desc;
      }
      return desc;
    }
    return item.description_trans?.[lang] || item.description || '';
  }

  function translateStatLabel(k, lang) {
    if (!k || lang === 'en') return k;
    const trimmed = String(k).trim();
    const memo = labelMemo[lang];
    if (memo && memo.has(trimmed)) return memo.get(trimmed);

    let result = trimmed;
    const exact = statLabelsExact[trimmed]?.[lang];
    if (exact && exact.toLowerCase() !== trimmed.toLowerCase()) {
      result = exact;
    } else {
      const ci = statLabelsLower.get(trimmed.toLowerCase())?.[lang];
      if (ci) result = ci;
    }

    if (memo) memo.set(trimmed, result);
    return result;
  }

  function translateStatValue(v, lang) {
    if (!v || typeof v !== 'string' || lang === 'en') return v;
    const trimmed = v.trim();
    const memo = valueMemo[lang];
    if (memo && memo.has(trimmed)) return memo.get(trimmed);

    const stripped = trimmed.replace(/\.$/, '');
    const candidates = [trimmed, stripped, `${stripped}.`];

    for (const cand of candidates) {
      const exact = statValuesExact[cand]?.[lang];
      if (exact) {
        if (memo) memo.set(trimmed, exact);
        return exact;
      }
    }

    for (const cand of candidates) {
      const ci = statValuesLower.get(cand.toLowerCase())?.[lang];
      if (ci) {
        if (memo) memo.set(trimmed, ci);
        return ci;
      }
    }

    for (const p of compiledStatPatterns) {
      if (p.regex.test(trimmed)) {
        const repl = p[lang];
        if (repl) {
          const out = trimmed.replace(p.regex, repl);
          if (memo) memo.set(trimmed, out);
          return out;
        }
      }
    }

    if (memo) memo.set(trimmed, v);
    return v;
  }

  function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
