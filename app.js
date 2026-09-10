/**
 * MARVEL RIVALS SKILL & TEAM-UP DATABASE - APP LOGIC
 * High-performance, zero-dependency vanilla JS application.
 * Supports Korean (KO), Japanese (JA), and English (EN).
 */

(function () {
  'use strict';

  // State
  let heroesData = [];
  let i18nData = {};
  let translationsData = {};
  let currentLang = localStorage.getItem('mr_db_lang') || 'ko';
  let currentRole = 'ALL';
  let searchQuery = '';
  let selectedHero = null;
  let selectedSkillIndex = 0;
  let selectedSkillIsUpgraded = false;
  let selectedLoadout = 1;

  // DOM Elements
  const heroGrid = document.getElementById('hero-grid');
  const heroSearchInput = document.getElementById('hero-search-input');
  const heroesCountEl = document.getElementById('heroes-count');
  const langBtns = document.querySelectorAll('.lang-btn');
  const roleBtns = document.querySelectorAll('.role-btn');

  // Modal Elements
  const modalOverlay = document.getElementById('hero-modal');
  const modalCloseBtn = document.getElementById('modal-close-btn');
  const modalHeroAvatar = document.getElementById('modal-hero-avatar');
  const modalHeroName = document.getElementById('modal-hero-name');
  const modalHeroSubname = document.getElementById('modal-hero-subname');
  const modalBaseStats = document.getElementById('modal-base-stats');
  const tabBtnSkills = document.getElementById('tab-btn-skills');
  const tabBtnTeamups = document.getElementById('tab-btn-teamups');
  const viewSkills = document.getElementById('view-skills');
  const viewTeamups = document.getElementById('view-teamups');
  const skillSelectorList = document.getElementById('skill-selector-list');
  const skillDetailDisplay = document.getElementById('skill-detail-display');
  const loadoutSelector = document.getElementById('loadout-selector');
  const teamupColumns = document.getElementById('teamup-columns');

  // Static stat color class mappings
  const STAT_HIGHLIGHT_CLASSES = {
    'damage': 'highlight-damage',
    'healing': 'highlight-range',
    'healing amount': 'highlight-range',
    'cooldown': 'highlight-cooldown',
    'range': 'highlight-range',
    'spell field range': 'highlight-range',
    'field range': 'highlight-range',
    'projectile speed': 'highlight-speed',
    'fire rate': 'highlight-speed',
    'ammo': 'highlight-ammo',
    'ammo consumption': 'highlight-ammo'
  };

  /**
   * Initialize Application
   */
  async function init() {
    try {
      const [heroesRes, i18nRes, transRes] = await Promise.all([
        fetch('data/heroes.json'),
        fetch('data/i18n.json'),
        fetch('data/translations.json').catch(() => null)
      ]);

      if (!heroesRes.ok || !i18nRes.ok) {
        throw new Error('Failed to load JSON data');
      }

      heroesData = await heroesRes.json();
      i18nData = await i18nRes.json();
      if (transRes && transRes.ok) {
        try {
          translationsData = await transRes.json();
        } catch (e) {
          console.warn('Could not parse translations.json:', e);
        }
      }

      setupEventListeners();
      applyLanguage(currentLang);
      renderHeroGrid();
    } catch (err) {
      console.error('Initialization error:', err);
      heroGrid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: #ff4d6d;">
          <h3>⚠️ 데이터를 불러오는 데 실패했습니다.</h3>
          <p style="margin-top: 8px; color: #94a3b8;">${err.message}</p>
        </div>
      `;
    }
  }

  /**
   * Setup Event Listeners
   */
  function setupEventListeners() {
    // Language Switcher
    langBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        let lang = btn.getAttribute('data-lang');
        if (lang === 'jp') lang = 'ja';
        if (lang === 'kr') lang = 'ko';
        if (lang && lang !== currentLang) {
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
        roleBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentRole = btn.getAttribute('data-role') || 'ALL';
        renderHeroGrid();
      });
    });

    // Real-time Search
    heroSearchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim().toLowerCase();
      renderHeroGrid();
    });

    // Keyboard shortcut for search
    window.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== heroSearchInput && !modalOverlay.classList.contains('open')) {
        e.preventDefault();
        heroSearchInput.focus();
      } else if (e.key === 'Escape' && modalOverlay.classList.contains('open')) {
        closeModal();
      }
    });

    // Modal Close
    modalCloseBtn.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeModal();
    });

    // Modal Tabs
    tabBtnSkills.addEventListener('click', () => switchModalTab('skills'));
    tabBtnTeamups.addEventListener('click', () => switchModalTab('teamups'));
  }

  /**
   * Apply UI Translations based on selected language
   */
  function applyLanguage(lang) {
    if (lang === 'jp') lang = 'ja';
    const t = i18nData[lang] || i18nData['en'] || {};

    // Keep website browser tab title in English
    document.title = 'Marvel Rivals Skill & Team-Up DB | Hero Stats & Loadouts';

    // Update active lang button
    langBtns.forEach(btn => {
      const btnLang = btn.getAttribute('data-lang');
      btn.classList.toggle('active', btnLang === lang || (lang === 'ja' && (btnLang === 'ja' || btnLang === 'jp')) || (lang === 'ko' && (btnLang === 'ko' || btnLang === 'kr')));
    });

    // Update document language
    document.documentElement.lang = lang;

    // Header & Search
    document.getElementById('site-logo-subtitle').textContent = (lang === 'ko') 
      ? '스킬 수치 & 팀업 백과사전' 
      : (lang === 'ja' ? 'スキル数値 ＆ チームアップ図鑑' : 'SKILL & TEAM-UP DATABASE');

    heroSearchInput.placeholder = t.searchPlaceholder || 'Search hero name or skill...';

    // Banner Text
    const bannerTitle = document.getElementById('banner-title');
    if (bannerTitle) {
      bannerTitle.innerHTML = `<span>${t.siteTitle || '마블 라이벌즈 영웅 스킬 도감'}</span>`;
    }
    const bannerDesc = document.getElementById('banner-desc');
    if (bannerDesc) {
      bannerDesc.textContent = (lang === 'ko')
        ? '마블 라이벌즈 전 영웅의 상세 스킬 수치 및 팀업 로드아웃 정보입니다.'
        : (lang === 'ja'
          ? 'マーベル・ライバルズ全ヒーローのスキル数値およびチームアップ情報です。'
          : 'Detailed skill statistics and team-up loadout information for all Marvel Rivals heroes.');
    }

    // Role Labels
    document.getElementById('label-all').textContent = (lang === 'ko') ? '전체' : (lang === 'ja' ? 'すべて' : 'All');
    document.getElementById('label-vanguard').textContent = t.vanguard || 'Vanguard';
    document.getElementById('label-duelist').textContent = t.duelist || 'Duelist';
    document.getElementById('label-strategist').textContent = t.strategist || 'Strategist';

    // Modal Tabs
    document.getElementById('tab-text-skills').textContent = t.skillsTab || 'Abilities';
    document.getElementById('tab-text-teamups').textContent = t.teamUpTab || 'Team-Up';
    const noticeEl = document.getElementById('teamup-notice-text');
    if (noticeEl) {
      noticeEl.textContent = t.teamUpNotice || '';
    }
  }

  /**
   * Helper to format health with localized shield text
   */
  function formatHealth(val, lang, isShort = false) {
    if (!val) return 'N/A';
    const str = String(val).trim();
    if (/regenerative shield/i.test(str)) {
      if (isShort) {
        if (lang === 'ko') return str.replace(/regenerative shield/i, '보호막');
        if (lang === 'ja') return str.replace(/regenerative shield/i, 'シールド');
        return str.replace(/regenerative shield/i, 'Shield');
      } else {
        if (lang === 'ko') return str.replace(/regenerative shield/i, '재생 보호막');
        if (lang === 'ja') return str.replace(/regenerative shield/i, '再生シールド');
        return str;
      }
    }
    return str;
  }

  /**
   * Helper to format speed uniformly to 'X m/s'
   */
  function formatSpeed(val) {
    if (!val) return 'N/A';
    const str = String(val).trim();
    const numMatch = str.match(/^(\d+(?:\.\d+)?)$/);
    if (numMatch) {
      let num = parseFloat(numMatch[1]);
      if (num >= 100) num = num / 100;
      return `${num} m/s`;
    }
    const msMatch = str.match(/^(\d+(?:\.\d+)?)\s*m\/s$/i);
    if (msMatch) {
      return `${parseFloat(msMatch[1])} m/s`;
    }
    return str;
  }

  /**
   * Filter and search heroes
   */
  function getFilteredHeroes() {
    return heroesData.filter(hero => {
      // Role filter
      if (currentRole !== 'ALL') {
        const roles = hero.roles || [hero.role];
        if (!roles.includes(currentRole)) {
          return false;
        }
      }

      // Search query filter
      if (searchQuery) {
        const enName = (hero.names.en || '').toLowerCase();
        const koName = (hero.names.ko || '').toLowerCase();
        const jaName = (hero.names.ja || '').toLowerCase();
        const role = (hero.role || '').toLowerCase();

        // Also search in skills
        const skillMatch = hero.skills.some(s => 
          (s.name || '').toLowerCase().includes(searchQuery) ||
          (s.key || '').toLowerCase().includes(searchQuery)
        );

        const teamupMatch = hero.teamups.some(tu =>
          (tu.name || '').toLowerCase().includes(searchQuery) ||
          (tu.loadout_name || '').toLowerCase().includes(searchQuery)
        );

        if (!enName.includes(searchQuery) &&
            !koName.includes(searchQuery) &&
            !jaName.includes(searchQuery) &&
            !role.includes(searchQuery) &&
            !skillMatch &&
            !teamupMatch) {
          return false;
        }
      }

      return true;
    });
  }

  /**
   * Render Hero Cards Grid
   */
  function renderHeroGrid() {
    const heroes = getFilteredHeroes();
    heroesCountEl.textContent = `${heroes.length} ${heroes.length === 1 ? 'Hero' : 'Heroes'}`;

    if (heroes.length === 0) {
      heroGrid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: var(--text-dim);">
          <div style="font-size: 36px; margin-bottom: 12px;">🔍</div>
          <h3 style="color: #fff; font-size: 18px; margin-bottom: 6px;">검색 결과가 없습니다</h3>
          <p>다른 검색어나 역할군 필터를 선택해 보세요.</p>
        </div>
      `;
      return;
    }

    heroGrid.innerHTML = heroes.map(hero => {
      const displayName = hero.names[currentLang] || hero.names.en;
      const subName = (currentLang !== 'en') ? hero.names.en : '';
      const health = formatHealth(hero.base_stats?.Health, currentLang, true);
      const speed = formatSpeed(hero.base_stats?.['Movement Speed']);

      // Preview top 4 skill icons
      const skillIconsHtml = hero.skills.slice(0, 4).map(s => {
        if (!s.icon) return '';
        return `<img src="${s.icon}" alt="${escapeHtml(s.name)}" title="${escapeHtml(s.name)}" class="skill-mini-icon" loading="lazy">`;
      }).join('');

      return `
        <article class="hero-card role-${hero.role.toLowerCase()}" data-id="${hero.id}" tabindex="0" role="button" aria-label="${escapeHtml(displayName)}">
          <div class="hero-avatar-wrapper">
            <img src="${hero.avatar}" alt="${escapeHtml(displayName)}" class="hero-avatar" loading="lazy">
            <div class="role-pill ${hero.role}" title="${hero.role}">
              <img src="assets/icons/role_${hero.role.toLowerCase()}.png" class="role-pill-icon" alt="${hero.role}">
            </div>
          </div>
          <div class="hero-info">
            <h3 class="hero-name-primary">${escapeHtml(displayName)}</h3>
            ${subName ? `<div class="hero-name-sub">${escapeHtml(subName)}</div>` : ''}
            <div class="hero-chips">
              <span class="stat-chip">HP <strong>${escapeHtml(health)}</strong></span>
              <span class="stat-chip">SPD <strong>${escapeHtml(speed)}</strong></span>
            </div>
            <div class="hero-skills-preview">
              ${skillIconsHtml}
            </div>
          </div>
        </article>
      `;
    }).join('');

    // Attach click listeners to cards
    heroGrid.querySelectorAll('.hero-card').forEach(card => {
      card.addEventListener('click', () => {
        const id = card.getAttribute('data-id');
        openHeroModal(id);
      });
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          const id = card.getAttribute('data-id');
          openHeroModal(id);
        }
      });
    });
  }

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

  /**
   * Open Hero Detail Modal
   */
  function openHeroModal(heroId) {
    const hero = heroesData.find(h => h.id === heroId);
    if (!hero) return;

    if (hero.skills && Array.isArray(hero.skills)) {
      hero.skills.sort((a, b) => (KEY_ORDER[a.key] || 15) - (KEY_ORDER[b.key] || 15));
    }

    selectedHero = hero;
    selectedSkillIndex = 0;
    selectedSkillIsUpgraded = false;
    selectedLoadout = 1;

    updateModalContent();

    // Default to skills tab
    switchModalTab('skills');

    modalOverlay.classList.add('open');
    modalOverlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  /**
   * Close Hero Detail Modal
   */
  function closeModal() {
    modalOverlay.classList.remove('open');
    modalOverlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    selectedHero = null;
  }

  /**
   * Switch between Skills and Team-Up tabs in Modal
   */
  function switchModalTab(tab) {
    if (tab === 'skills') {
      tabBtnSkills.classList.add('active');
      tabBtnTeamups.classList.remove('active');
      viewSkills.classList.add('active');
      viewTeamups.classList.remove('active');
    } else {
      tabBtnSkills.classList.remove('active');
      tabBtnTeamups.classList.add('active');
      viewSkills.classList.remove('active');
      viewTeamups.classList.add('active');
      renderTeamupTab();
    }
  }

  /**
   * Update full modal content for selectedHero
   */
  function updateModalContent() {
    if (!selectedHero) return;

    const hero = selectedHero;
    const t = i18nData[currentLang] || {};

    const displayName = hero.names[currentLang] || hero.names.en;
    const subName = (currentLang !== 'en') ? hero.names.en : '';

    modalHeroAvatar.src = hero.avatar;
    modalHeroAvatar.alt = displayName;
    modalHeroName.textContent = displayName;
    
    const roleTrans = hero.role_name?.[currentLang] || hero.role;
    modalHeroSubname.innerHTML = `
      ${subName ? `<span>${escapeHtml(subName)}</span>` : ''}
      <span class="modal-role-badge ${hero.role}">
        <img src="assets/icons/role_${hero.role.toLowerCase()}.png" class="modal-role-icon" alt="${hero.role}">
        ${escapeHtml(roleTrans)}
      </span>
    `;

    // Base Stats Badges
    const health = formatHealth(hero.base_stats?.Health, currentLang, false);
    const speed = formatSpeed(hero.base_stats?.['Movement Speed']);
    const rawMode = hero.base_stats?.['Movement Mode'] || 'Ground';

    const healthLabel = t.health || 'Health';
    const speedLabel = t.speed || 'Speed';
    const modeLabel = (currentLang === 'ko') ? '이동 방식' : (currentLang === 'ja' ? '移動モード' : 'Movement');
    const modeDisplay = (currentLang === 'ko')
      ? (rawMode === 'Flight' ? '비행' : '지상')
      : (currentLang === 'ja'
        ? (rawMode === 'Flight' ? '飛行' : '地上')
        : rawMode);

    modalBaseStats.innerHTML = `
      <div class="base-stat-badge">❤️ ${healthLabel}: <strong>${escapeHtml(health)}</strong></div>
      <div class="base-stat-badge">⚡ ${speedLabel}: <strong>${escapeHtml(speed)}</strong></div>
      <div class="base-stat-badge">🚀 ${modeLabel}: <strong>${escapeHtml(modeDisplay)}</strong></div>
    `;

    renderSkillSelectorList();
    renderSkillDetailDisplay();
    renderTeamupTab();
  }

  /**
   * Render Left Skill Selector List in Modal
   */
  function renderSkillSelectorList() {
    if (!selectedHero) return;

    const skills = selectedHero.skills || [];
    skillSelectorList.innerHTML = skills.map((s, idx) => {
      const isActive = idx === selectedSkillIndex;
      const keyTrans = s.key_trans?.[currentLang] || s.key;
      const iconHtml = s.icon 
        ? `<img src="${s.icon}" alt="" class="skill-select-icon">`
        : `<div class="skill-select-icon" style="display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;">${escapeHtml(s.key)}</div>`;

      return `
        <div class="skill-select-item ${isActive ? 'active' : ''}" data-index="${idx}" tabindex="0" role="button">
          ${iconHtml}
          <div class="skill-select-details">
            <div class="skill-select-name">${escapeHtml(s.name)}</div>
            <div class="skill-select-key">${escapeHtml(keyTrans)}</div>
          </div>
        </div>
      `;
    }).join('');

    // Attach click listeners to list items
    skillSelectorList.querySelectorAll('.skill-select-item').forEach(item => {
      item.addEventListener('click', () => {
        const idx = parseInt(item.getAttribute('data-index'), 10);
        if (selectedSkillIndex !== idx) {
          selectedSkillIndex = idx;
          selectedSkillIsUpgraded = false;
          renderSkillSelectorList();
          renderSkillDetailDisplay();
        }
      });
    });
  }

  /**
   * Render Right Skill Detail Box with Infographic Stats Grid
   */
  function renderSkillDetailDisplay() {
    if (!selectedHero || !selectedHero.skills[selectedSkillIndex]) {
      skillDetailDisplay.innerHTML = `<p style="color: var(--text-dim); text-align: center;">No skill selected.</p>`;
      return;
    }

    const rawSkill = selectedHero.skills[selectedSkillIndex];
    const hasUpgrade = Boolean(rawSkill.upgrade);
    const activeSkill = (hasUpgrade && selectedSkillIsUpgraded) ? rawSkill.upgrade : rawSkill;

    const t = i18nData[currentLang] || {};
    const keyTrans = rawSkill.key_trans?.[currentLang] || rawSkill.key;

    // Stat boxes
    const statsEntries = Object.entries(activeSkill.stats || {}).filter(([k, v]) => k.toLowerCase() !== 'key');
    const statsGridHtml = statsEntries.map(([k, v]) => {
      const lowerKey = k.toLowerCase();
      const highlightClass = STAT_HIGHLIGHT_CLASSES[lowerKey] || '';
      const translatedLabel = translateStatLabel(k, currentLang);
      const translatedValue = translateStatValue(v, currentLang);

      return `
        <div class="stat-box ${highlightClass}">
          <span class="stat-label">${escapeHtml(translatedLabel)}</span>
          <span class="stat-value">${escapeHtml(translatedValue)}</span>
        </div>
      `;
    }).join('');

    const activeSkillDesc = getSkillDescription(activeSkill, currentLang);

    const descHtml = activeSkillDesc ? `
      <div class="skill-desc-box">
        ${escapeHtml(activeSkillDesc)}
      </div>
    ` : '';

    const iconHtml = activeSkill.icon 
      ? `<img src="${activeSkill.icon}" alt="" class="skill-large-icon">`
      : `<div class="skill-large-icon" style="display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700;">${escapeHtml(rawSkill.key)}</div>`;

    const upgradeBtnHtml = hasUpgrade ? `
      <button 
        type="button" 
        class="skill-upgrade-star-btn ${selectedSkillIsUpgraded ? 'active' : ''}" 
        id="skill-upgrade-star-btn" 
        title="${selectedSkillIsUpgraded ? (currentLang === 'ko' ? '기본 효과 보기' : (currentLang === 'ja' ? '基本効果を見る' : 'Click to view base stats')) : (currentLang === 'ko' ? '스킬 업그레이드 효과 보기' : (currentLang === 'ja' ? 'スキル強化効果を見る' : 'Click to view upgraded stats'))}"
        aria-label="Toggle Skill Upgrade"
      >
        <span class="star-icon">${selectedSkillIsUpgraded ? '★' : '☆'}</span>
        <span class="upgrade-star-label">${selectedSkillIsUpgraded ? 'UPGRADED' : 'UPGRADE'}</span>
      </button>
    ` : '';

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
            ${(hasUpgrade && selectedSkillIsUpgraded) ? `<span class="upgraded-pill-tag">⚡ UPGRADED</span>` : ''}
          </div>
        </div>
      </div>

      ${descHtml}

      <div>
        <div class="stats-grid-title" style="margin-bottom: 10px;">
          📊 ${(currentLang === 'ko') ? (selectedSkillIsUpgraded ? '업그레이드 스킬 상세 스펙' : '스킬 수치 상세 스펙') : (currentLang === 'ja' ? (selectedSkillIsUpgraded ? '強化スキル詳細数値スペック' : 'スキル詳細数値スペック') : (selectedSkillIsUpgraded ? 'UPGRADED SPECIFICATIONS' : 'SPECIFICATIONS'))}
        </div>
        <div class="stats-grid">
          ${statsGridHtml || '<p style="color: var(--text-dim); font-size: 13px;">상세 수치 정보가 없습니다.</p>'}
        </div>
      </div>
    `;

    // Attach click listener to star button
    const starBtn = skillDetailDisplay.querySelector('#skill-upgrade-star-btn');
    if (starBtn) {
      starBtn.addEventListener('click', () => {
        selectedSkillIsUpgraded = !selectedSkillIsUpgraded;
        renderSkillDetailDisplay();
      });
    }
  }

  /**
   * Render Team-Up Loadout Tab (Season 9 Revamp)
   */
  function renderTeamupTab() {
    if (!selectedHero) return;

    const teamups = selectedHero.teamups || [];
    if (teamups.length === 0) {
      loadoutSelector.innerHTML = '';
      teamupColumns.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-dim);">
          <p>이 영웅은 현재 등록된 팀업 스킬이 없습니다.</p>
        </div>
      `;
      return;
    }

    // Identify loadout 1 and loadout 2
    const l1Items = teamups.filter(tu => tu.loadout_number === 1);
    const l2Items = teamups.filter(tu => tu.loadout_number === 2);

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

    // Loadout Selector Buttons with Partner Hero Avatar
    loadoutSelector.innerHTML = `
      <button type="button" class="loadout-btn ${selectedLoadout === 1 ? 'active' : ''}" data-loadout="1">
        ${l1Icon ? `<img src="${l1Icon}" alt="" class="loadout-icon">` : '⚡'}
        <div class="loadout-btn-text">
          <strong>${escapeHtml(l1Name)}</strong>
          <span>${(currentLang === 'ko') ? '로드아웃 1' : (currentLang === 'ja' ? 'ロードアウト 1' : 'Loadout 1')}</span>
        </div>
        ${l1PartnerPic ? `<img src="${l1PartnerPic}" alt="Partner" title="Partner" class="loadout-partner-avatar">` : ''}
      </button>

      ${l2Items.length > 0 ? `
      <button type="button" class="loadout-btn ${selectedLoadout === 2 ? 'active' : ''}" data-loadout="2">
        ${l2Icon ? `<img src="${l2Icon}" alt="" class="loadout-icon">` : '⚡'}
        <div class="loadout-btn-text">
          <strong>${escapeHtml(l2Name)}</strong>
          <span>${(currentLang === 'ko') ? '로드아웃 2' : (currentLang === 'ja' ? 'ロードアウト 2' : 'Loadout 2')}</span>
        </div>
        ${l2PartnerPic ? `<img src="${l2PartnerPic}" alt="Partner" title="Partner" class="loadout-partner-avatar">` : ''}
      </button>
      ` : ''}
    `;

    // Attach loadout toggle listeners
    loadoutSelector.querySelectorAll('.loadout-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        selectedLoadout = parseInt(btn.getAttribute('data-loadout'), 10);
        renderTeamupTab();
      });
    });

    // Active loadout items
    const activeItems = (selectedLoadout === 1) ? l1Items : l2Items;
    const baseItem = activeItems.find(x => x.tier === 'base') || activeItems[0];
    const enhancedItem = activeItems.find(x => x.tier === 'enhanced') || activeItems[1];

    const partnerPic = enhancedItem?.partner_avatar || baseItem?.partner_avatar || '';
    const partnerNameObj = enhancedItem?.partner_name || baseItem?.partner_name || {};
    const partnerNameDisplay = partnerNameObj[currentLang] || partnerNameObj.en || (currentLang === 'ko' ? '시너지 파트너' : 'Synergy Partner');

    // Partner Hero Bar
    const partnerBannerHtml = partnerPic ? `
      <div class="partner-highlight-bar" style="grid-column: 1/-1;">
        <img src="${partnerPic}" alt="${escapeHtml(partnerNameDisplay)}" class="partner-avatar-large">
        <div class="partner-info-text">
          <span class="partner-label">${(currentLang === 'ko') ? '🤝 강화 시너지 파트너 영웅' : (currentLang === 'ja' ? '🤝 強化シナジー対象ヒーロー' : '🤝 SYNERGY PARTNER HERO')}</span>
          <span class="partner-hero-name">${escapeHtml(partnerNameDisplay)}</span>
        </div>
      </div>
    ` : '';

    teamupColumns.innerHTML = `
      ${partnerBannerHtml}

      <!-- Base Effect Card -->
      <div class="teamup-card base">
        <div class="teamup-card-header">
          <span class="teamup-tier-badge base">
            ${(currentLang === 'ko') ? '⚡ 기본 효과 (솔로 적용)' : (currentLang === 'ja' ? '⚡ 基本効果 (ソロ常時発動)' : '⚡ Base Effect (Solo)')}
          </span>
          <span style="font-size: 12px; color: var(--accent-gold); font-weight: 700;">
            ${escapeHtml(baseItem?.key || 'Passive')}
          </span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
          ${baseItem?.icon ? `<img src="${baseItem.icon}" alt="" style="width: 28px; height: 28px; border-radius: 6px;">` : ''}
          <h4 style="color: #fff; font-size: 16px; font-weight: 700;">${escapeHtml(baseItem?.name || 'Base Effect')}</h4>
        </div>
        <div class="teamup-card-desc">
          ${escapeHtml(getTeamupDescription(baseItem, 'base', currentLang) || (currentLang === 'ko' ? '아군 조합 없이도 솔로로 상시 발동되는 기본 효과입니다.' : 'Solo passive ability applied without requiring team-up partners.'))}
        </div>
        <div>
          <div class="stats-grid-title" style="margin-bottom: 8px;">
            ${(currentLang === 'ko') ? '기본 효과 수치' : (currentLang === 'ja' ? '基本効果数値' : 'Base Stats')}
          </div>
          <div class="stats-grid" style="grid-template-columns: 1fr 1fr;">
            ${renderStatEntries(baseItem?.stats)}
          </div>
        </div>
      </div>

      <!-- Enhanced Effect Card -->
      <div class="teamup-card enhanced">
        <div class="teamup-card-header">
          <span class="teamup-tier-badge enhanced">
            ${(currentLang === 'ko') ? '🔥 강화 효과 (팀업 발동)' : (currentLang === 'ja' ? '🔥 強化効果 (チームアップ発動)' : '🔥 Enhanced Effect (Team-Up)')}
          </span>
          <span style="font-size: 12px; color: var(--accent-cyan); font-weight: 700;">
            ${escapeHtml(enhancedItem?.key || 'Passive')}
          </span>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
          ${enhancedItem?.icon ? `<img src="${enhancedItem.icon}" alt="" style="width: 28px; height: 28px; border-radius: 6px;">` : ''}
          <h4 style="color: #fff; font-size: 16px; font-weight: 700;">${escapeHtml(enhancedItem?.name || 'Enhanced Effect')}</h4>
        </div>
        <div class="teamup-card-desc">
          ${escapeHtml(getTeamupDescription(enhancedItem, 'enhanced', currentLang) || (currentLang === 'ko' ? `${partnerNameDisplay}와(과) 함께 플레이 시 스킬이 대폭 강화됩니다.` : `Activated when teaming up with ${partnerNameDisplay}.`))}
        </div>
        <div>
          <div class="stats-grid-title" style="margin-bottom: 8px;">
            ${(currentLang === 'ko') ? '팀업 강화 수치' : (currentLang === 'ja' ? 'チームアップ強化数値' : 'Enhanced Stats')}
          </div>
          <div class="stats-grid" style="grid-template-columns: 1fr 1fr;">
            ${renderStatEntries(enhancedItem?.stats)}
          </div>
        </div>
      </div>
    `;
  }

  /**
   * Helper to render stat boxes
   */
  function renderStatEntries(statsObj) {
    if (!statsObj || Object.keys(statsObj).length === 0) {
      return `<p style="color: var(--text-dim); font-size: 12px; grid-column: 1/-1;">수치 데이터 없음</p>`;
    }

    return Object.entries(statsObj)
      .filter(([k, v]) => k.toLowerCase() !== 'key')
      .map(([k, v]) => {
        const lowerKey = k.toLowerCase();
        const highlightClass = STAT_HIGHLIGHT_CLASSES[lowerKey] || '';
        const translatedLabel = translateStatLabel(k, currentLang);
        const translatedValue = translateStatValue(v, currentLang);

        return `
          <div class="stat-box ${highlightClass}" style="padding: 8px 10px;">
            <span class="stat-label" style="font-size: 10px;">${escapeHtml(translatedLabel)}</span>
            <span class="stat-value" style="font-size: 13px;">${escapeHtml(translatedValue)}</span>
          </div>
        `;
      }).join('');
  }

  /**
   * Get translated skill description with fallback
   */
  function getSkillDescription(skill, lang) {
    if (!skill) return '';
    if (lang === 'en') return skill.description || '';
    if (skill.description_trans?.[lang]) return skill.description_trans[lang];
    if (translationsData?.skills) {
      const normKey = skill.description ? skill.description.replace(/\s+/g, ' ').trim() : '';
      if (translationsData.skills[normKey]?.[lang]) return translationsData.skills[normKey][lang];
      if (translationsData.skills[skill.description]?.[lang]) return translationsData.skills[skill.description][lang];
    }
    return skill.description || '';
  }

  /**
   * Get translated teamup description with fallback
   */
  function getTeamupDescription(item, tier, lang) {
    if (!item) return '';
    if (lang === 'en') return item.description || '';
    if (item.description_trans?.[lang]) return item.description_trans[lang];
    if (translationsData?.teamups) {
      const normKey = item.description ? item.description.replace(/\s+/g, ' ').trim() : '';
      const entry = translationsData.teamups[normKey] || translationsData.teamups[item.description] || translationsData.teamups[item.name] || translationsData.teamups[item.loadout_name];
      if (entry?.[tier]?.[lang]) return entry[tier][lang];
      if (entry?.full?.[lang]) return entry.full[lang];
    }
    return item.description || '';
  }

  /**
   * Translate Stat Label / Key
   */
  function translateStatLabel(k, lang) {
    if (!k || lang === 'en') return k;
    if (translationsData?.stat_labels?.[k]?.[lang]) {
      return translationsData.stat_labels[k][lang];
    }
    const t = i18nData[lang] || {};
    if (t.stats?.[k]?.[lang]) {
      return t.stats[k][lang];
    }
    return k;
  }

  /**
   * Translate Stat Value dynamically (Seasonal patch numerical resilience!)
   */
  function translateStatValue(v, lang) {
    if (!v || typeof v !== 'string' || lang === 'en') return v;
    const trimmed = v.trim();

    // 1. Exact value translation
    if (translationsData?.stat_values?.[trimmed]?.[lang]) {
      return translationsData.stat_values[trimmed][lang];
    }

    // 2. Dynamic regex pattern translation (preserves numbers from patches!)
    const patterns = translationsData?.stat_patterns || [];
    for (const p of patterns) {
      try {
        const regex = new RegExp(p.regex, 'i');
        if (regex.test(trimmed)) {
          const repl = p[lang] || p.ko || '';
          if (repl) {
            return trimmed.replace(regex, repl);
          }
        }
      } catch (e) {}
    }

    return v;
  }

  /**
   * HTML Escaping Utility
   */
  function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Start app on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
