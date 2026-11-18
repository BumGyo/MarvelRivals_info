#!/usr/bin/env node
/**
 * Marvel Rivals Database - Post-Processing Pipeline
 * 1. Splits Deadpool into 3 role-based heroes using live official raw_forms stats.
 * 2. Consolidates Deadpool's skills per role with .upgrade property for the ⭐ toggle.
 * 3. Builds multi-form structures dynamically from live raw_forms (Hulk, Black Cat, Magik, Cloak & Dagger, Gambit, White Fox).
 * 4. Splits combined English Team-Up descriptions into Base / Enhanced per tier & enriches partner metadata.
 * 5. Embeds KR/JP skill & team-up translations (with positional + value numerical patch resilience).
 * 6. Strips redundant raw_forms / duplicate form skills and updates hero counts & cache hash in index.html and README.md.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const rootDir = path.resolve(__dirname, '..');
const heroesPath = path.join(rootDir, 'data', 'heroes.json');
const indexPath = path.join(rootDir, 'index.html');
const readmePath = path.join(rootDir, 'README.md');

console.log('=== [START] Post-Processing Pipeline ===');

function normalizeCardImage(hero) {
  if (!hero || typeof hero.avatar !== 'string') return;
  if (hero.avatar.includes('/card-image')) return;
  if (typeof hero.full_img === 'string' && hero.full_img.includes('/card-image')) {
    hero.avatar = hero.full_img;
  }
}

function getDynamicFormStats(rawForms, idx, fallbackHealth, fallbackSpeed = '6 m/s', fallbackMode = 'Ground') {
  const rf = Array.isArray(rawForms) ? rawForms[idx] : null;
  const st = (rf && rf.stats) ? rf.stats : {};
  return {
    Health: st.Health || fallbackHealth,
    'Movement Speed': st['Movement Speed'] || fallbackSpeed,
    'Movement Mode': st['Movement Mode'] || fallbackMode
  };
}

function getDynamicFormAvatar(rawForms, idx, heroAvatar) {
  const rf = Array.isArray(rawForms) ? rawForms[idx] : null;
  return (rf && rf.avatar) ? rf.avatar : heroAvatar;
}

function splitEnglishTeamupDesc(desc, tier) {
  if (!desc || typeof desc !== 'string') return '';
  const hasBase = /Base Effect\s*:/i.test(desc);
  const hasEnhanced = /Enhanced Effect\s*:/i.test(desc);
  if (!hasBase && !hasEnhanced) return desc.trim();

  if (tier === 'base') {
    const m = desc.match(/Base Effect\s*:\s*([\s\S]*?)(?=\n?\s*Enhanced Effect\s*:|$)/i);
    return m ? m[1].trim() : desc.trim();
  }
  if (tier === 'enhanced') {
    const m = desc.match(/Enhanced Effect\s*:\s*([\s\S]*)$/i);
    return m ? m[1].trim() : desc.trim();
  }
  return desc.trim();
}

if (!fs.existsSync(heroesPath)) {
  console.error('Error: heroes.json not found at', heroesPath);
  process.exit(1);
}

const heroes = JSON.parse(fs.readFileSync(heroesPath, 'utf-8'));
console.log(`Loaded ${heroes.length} heroes from heroes.json.`);
heroes.forEach(normalizeCardImage);

if (!Array.isArray(heroes) || heroes.length < 50) {
  console.error(`[FATAL ERROR] heroes.json has invalid hero count (${heroes ? heroes.length : 0} < 50). Aborting.`);
  process.exit(1);
}

// -------------------------------------------------------------
// Step 1: Split Deadpool into 3 role-specific heroes with live stats
// -------------------------------------------------------------
const rawDeadpoolIdx = heroes.findIndex(h =>
  h.id === '3fwwmrinftem5' ||
  h.id === '3ef6b679-d1b4-4757-a8ee-0ea53379c754' ||
  (h.names && h.names.en === 'DEADPOOL' && h.skills && h.skills.length >= 20)
);

if (rawDeadpoolIdx !== -1) {
  const dp = heroes[rawDeadpoolIdx];
  console.log(`Splitting combined Deadpool (skills: ${dp.skills.length}) into 3 roles...`);

  const clone = obj => JSON.parse(JSON.stringify(obj));

  function buildRoleSkills(dpSkills, startForm) {
    const l1 = dpSkills.filter(s => s.form_index === startForm);
    const l2 = dpSkills.filter(s => s.form_index === startForm + 1);
    const up = dpSkills.filter(s => s.form_index === startForm + 2);

    function pairUpgrade(baseSkill) {
      if (!baseSkill) return null;
      const s = clone(baseSkill);
      const baseClean = baseSkill.name.trim();
      const upSkill =
        up.find(u => u.name.replace(/\s*-\s*UPGRADED$/i, '').replace(/\s+UPGRADED$/i, '').trim() === baseClean) ||
        up.find(u => {
          const uNorm = u.name.replace(/\s*-\s*UPGRADED$/i, '').replace(/\s+UPGRADED$/i, '').trim();
          return u.name.startsWith(baseClean) || baseClean.startsWith(uNorm);
        });

      if (upSkill) {
        s.upgrade = {
          name: upSkill.name,
          icon: upSkill.icon || s.icon,
          description: upSkill.description,
          stats: clone(upSkill.stats || [])
        };
      }
      return s;
    }

    if (l1.length === 0) {
      return dpSkills.slice(startForm * 8, startForm * 8 + 11).map(clone);
    }

    const lc1 = l1.find(s => s.key === 'Left Click');
    const lc2 = l2.find(s => s.key === 'Left Click');
    const rc1 = l1.find(s => s.key === 'Right Click');
    const rc2 = l2.find(s => s.key === 'Right Click');
    const q1 = l1.find(s => s.key === 'Q');
    const q2 = l2.find(s => s.key === 'Q');
    const e = l1.find(s => s.key === 'E') || l2.find(s => s.key === 'E');
    const f = l1.find(s => s.key === 'F');
    const space = l1.find(s => s.key === 'Space') || l2.find(s => s.key === 'Space');
    const p1 = l1.find(s => s.name === 'HEALING FACTOR' || s.key.toLowerCase() === 'passive');
    const p2 = l1.find(s => s.name === 'MAXIMUM FLAIR');

    return [
      pairUpgrade(lc1),
      pairUpgrade(lc2),
      pairUpgrade(rc1),
      pairUpgrade(rc2),
      pairUpgrade(q1),
      pairUpgrade(q2),
      pairUpgrade(e),
      f ? clone(f) : null,
      space ? clone(space) : null,
      p1 ? clone(p1) : null,
      p2 ? clone(p2) : null
    ].filter(Boolean);
  }

  const dpRoles = [
    {
      id: 'deadpool-vanguard',
      en: 'DEADPOOL (VANGUARD)',
      ko: '데드풀 (뱅가드)',
      ja: 'デッドプール (ヴァンガード)',
      role: 'VANGUARD',
      role_name: { en: 'Vanguard', ko: '뱅가드 (돌격)', ja: 'ヴァンガード (タンク)' },
      rawFormIdx: 0,
      fallbackHp: '500',
      startForm: 0
    },
    {
      id: 'deadpool-duelist',
      en: 'DEADPOOL (DUELIST)',
      ko: '데드풀 (듀얼리스트)',
      ja: 'デッドプール (デュエリスト)',
      role: 'DUELIST',
      role_name: { en: 'Duelist', ko: '듀얼리스트 (공격)', ja: 'デュエリスト (DPS)' },
      rawFormIdx: 3,
      fallbackHp: '275',
      startForm: 3
    },
    {
      id: 'deadpool-strategist',
      en: 'DEADPOOL (STRATEGIST)',
      ko: '데드풀 (전략가)',
      ja: 'デッドプール (ストラテジスト)',
      role: 'STRATEGIST',
      role_name: { en: 'Strategist', ko: '전략가 (지원)', ja: 'ストラテジスト (サポート)' },
      rawFormIdx: 6,
      fallbackHp: '275',
      startForm: 6
    }
  ];

  const splitHeroes = dpRoles.map(cfg => ({
    id: cfg.id,
    name: cfg.en,
    avatar: dp.avatar,
    full_img: dp.full_img || dp.avatar,
    names: { en: cfg.en, ko: cfg.ko, ja: cfg.ja },
    role: cfg.role,
    roles: [cfg.role],
    role_name: cfg.role_name,
    base_stats: getDynamicFormStats(dp.raw_forms, cfg.rawFormIdx, cfg.fallbackHp, '6 m/s', 'Ground'),
    skills: buildRoleSkills(dp.skills, cfg.startForm),
    teamups: clone(dp.teamups || [])
  }));

  heroes.splice(rawDeadpoolIdx, 1, ...splitHeroes);
  console.log('✓ Split Deadpool into 3 role-specific entries with live official base_stats.');
}

// -------------------------------------------------------------
// Step 2: Build Multi-Form Heroes Dynamically from raw_forms
// -------------------------------------------------------------
const MULTI_FORM_CONFIGS = {
  HULK: {
    primaryFormIdx: 1,
    forms: [
      { form_id: 0, en: 'Bruce Banner', ko: '브루스 배너', ja: 'ブルース・バナー', fallbackHp: '200', fallbackSpd: '6 m/s' },
      { form_id: 1, en: 'Hero Hulk', ko: '히어로 헐크', ja: 'ヒーロー・ハルク', fallbackHp: '400+300 Regenerative Shield', fallbackSpd: '6.5 m/s' },
      { form_id: 2, en: 'Monster Hulk', ko: '몬스터 헐크', ja: 'モンスター・ハルク', fallbackHp: '1400', fallbackSpd: '6.5 m/s' }
    ]
  },
  'BLACK CAT': {
    primaryFormIdx: 0,
    forms: [
      { form_id: 0, en: 'Claw Stance', ko: '클로 폼 (근접)', ja: 'クローフォーム (近接)', fallbackHp: '150+125 Regenerative Shield', fallbackSpd: '6 m/s' },
      { form_id: 1, en: 'Whip Stance', ko: '채찍 폼 (중거리)', ja: 'ウィップフォーム (中距離)', fallbackHp: '275', fallbackSpd: '6 m/s' },
      { form_id: 2, en: 'Gilded Deal', ko: '내부자 거래 (암시장)', ja: 'インサイダー取引 (闇市)', fallbackHp: '275', fallbackSpd: '6 m/s' }
    ]
  },
  MAGIK: {
    primaryFormIdx: 0,
    forms: [
      { form_id: 0, en: 'Magik', ko: '일반 매직', ja: '通常マジック', fallbackHp: '150+125 Regenerative Shield', fallbackSpd: '6 m/s' },
      { form_id: 1, en: 'Darkchild', ko: '다크차일드 폼', ja: 'ダークチャイルド', fallbackHp: '250', fallbackSpd: '6 m/s' }
    ]
  },
  'CLOAK & DAGGER': {
    primaryFormIdx: 0,
    forms: [
      { form_id: 0, en: 'Cloak', ko: '클록', ja: 'クローク', fallbackHp: '275', fallbackSpd: '6 m/s' },
      { form_id: 1, en: 'Dagger', ko: '대거', ja: 'ダガー', fallbackHp: '275', fallbackSpd: '6 m/s' }
    ]
  },
  GAMBIT: {
    primaryFormIdx: 0,
    forms: [
      { form_id: 0, en: 'Normal Stance', ko: '기본 폼', ja: '通常フォーム', fallbackHp: '250', fallbackSpd: '6 m/s' },
      { form_id: 1, en: 'Charged Cards', ko: '강화 카드 폼', ja: 'チャージカード', fallbackHp: '275', fallbackSpd: '6 m/s' }
    ]
  },
  'WHITE FOX': {
    primaryFormIdx: 0,
    forms: [
      { form_id: 0, en: 'Human Form', ko: '인간 형태', ja: '人間形態', fallbackHp: '275', fallbackSpd: '6 m/s' },
      { form_id: 1, en: 'Kumiho Form', ko: '구미호 폼', ja: '九尾の狐', fallbackHp: '275', fallbackSpd: '6 m/s' }
    ]
  }
};

heroes.forEach(h => {
  const hName = (h.names?.en || h.name || '').toUpperCase();
  const cfg = MULTI_FORM_CONFIGS[hName];
  if (cfg && (!h.forms || h.forms.length === 0)) {
    const rawSkills = h.skills || [];
    h.forms = cfg.forms.map((fc, idx) => ({
      form_id: fc.form_id,
      name: fc.en,
      names: { en: fc.en, ko: fc.ko, ja: fc.ja },
      avatar: getDynamicFormAvatar(h.raw_forms, idx, h.avatar),
      base_stats: getDynamicFormStats(h.raw_forms, idx, fc.fallbackHp, fc.fallbackSpd, 'Ground'),
      skills: rawSkills.filter(s => s.form_index === fc.form_id)
    }));
    // Sync hero card base_stats with primary form so card and modal always match
    if (h.forms[cfg.primaryFormIdx]) {
      h.base_stats = { ...h.forms[cfg.primaryFormIdx].base_stats };
    }
    // Avoid duplicating primary form skills in top-level h.skills
    h.skills = [];
    console.log(`✓ Configured ${hName} forms dynamically from live raw_forms.`);
  }
});

// -------------------------------------------------------------
// Step 3: Apply Translations & Clean Team-Up Descriptions
// -------------------------------------------------------------
const skillsPath = path.join(rootDir, 'data', 'translations', 'skills.json');
const teamupsPath = path.join(rootDir, 'data', 'translations', 'teamups.json');
const statsPath = path.join(rootDir, 'data', 'translations', 'stats.json');

const skillsMap = fs.existsSync(skillsPath) ? JSON.parse(fs.readFileSync(skillsPath, 'utf-8')) : {};
const teamupsMap = fs.existsSync(teamupsPath) ? JSON.parse(fs.readFileSync(teamupsPath, 'utf-8')) : {};

function norm(t) {
  return t ? t.replace(/\s+/g, ' ').trim() : '';
}

const normSkillsMap = new Map();
const numericSkillTemplates = [];

for (const [key, val] of Object.entries(skillsMap)) {
  const nKey = norm(key);
  if (!nKey) continue;
  normSkillsMap.set(nKey, val);

  const nums = nKey.match(/\d+(?:\.\d+)?/g);
  if (nums && nums.length > 0 && val && val.ko && val.ja) {
    numericSkillTemplates.push({
      templateKey: nKey.replace(/\d+(?:\.\d+)?/g, '<NUM>'),
      nums,
      trans: val
    });
  }
}

function substituteNumbers(str, oldNums, newNums) {
  if (!str || !oldNums || !newNums || oldNums.length !== newNums.length) return null;
  const targetStrNums = str.match(/\d+(?:\.\d+)?/g) || [];

  // 1. Positional substitution when translated sentence contains exact same numbers in same order
  if (targetStrNums.length === oldNums.length && targetStrNums.every((n, i) => n === oldNums[i])) {
    let idx = 0;
    return str.replace(/\d+(?:\.\d+)?/g, () => newNums[idx++]);
  }

  // 2. Non-ambiguous value mapping fallback
  const replacements = new Map();
  for (let i = 0; i < oldNums.length; i++) {
    if (replacements.has(oldNums[i]) && replacements.get(oldNums[i]) !== newNums[i]) return null;
    replacements.set(oldNums[i], newNums[i]);
  }
  return str.replace(/\d+(?:\.\d+)?/g, number => replacements.get(number) ?? number);
}

function resolveSkillTranslation(desc) {
  if (!desc) return null;
  const sDesc = norm(desc);
  if (normSkillsMap.has(sDesc)) return normSkillsMap.get(sDesc);
  if (skillsMap[desc]) return skillsMap[desc];

  const targetNums = sDesc.match(/\d+(?:\.\d+)?/g);
  if (targetNums && targetNums.length > 0) {
    const targetTemplate = sDesc.replace(/\d+(?:\.\d+)?/g, '<NUM>');
    for (const item of numericSkillTemplates) {
      if (item.templateKey === targetTemplate && item.nums.length === targetNums.length) {
        const ko = substituteNumbers(item.trans.ko, item.nums, targetNums);
        const ja = substituteNumbers(item.trans.ja, item.nums, targetNums);
        if (ko && ja) return { ko, ja };
      }
    }
  }
  return null;
}

let skillFallbackCount = 0;
let teamupFallbackCount = 0;

function translateSkillList(list) {
  (list || []).forEach(s => {
    delete s.type;
    delete s.form_index;
    const trans = resolveSkillTranslation(s.description);
    if (trans) {
      s.description_trans = trans;
    } else if (s.description && !s.description_trans) {
      s.description_trans = { ko: s.description, ja: s.description };
      skillFallbackCount++;
    }

    if (s.upgrade) {
      const uTrans = resolveSkillTranslation(s.upgrade.description);
      if (uTrans) {
        s.upgrade.description_trans = uTrans;
      } else if (s.upgrade.description && !s.upgrade.description_trans) {
        s.upgrade.description_trans = { ko: s.upgrade.description, ja: s.upgrade.description };
        skillFallbackCount++;
      }
    }
  });
}

// Pre-index numeric teamup templates for balance-patch number resilience
const numericTeamupTemplates = [];
for (const [key, entry] of Object.entries(teamupsMap)) {
  const nKey = norm(key);
  if (!nKey || !entry || (!entry.base && !entry.enhanced)) continue;
  const nums = nKey.match(/\d+(?:\.\d+)?/g);
  if (nums && nums.length > 0) {
    numericTeamupTemplates.push({
      templateKey: nKey.replace(/\d+(?:\.\d+)?/g, '<NUM>'),
      nums,
      entry
    });
  }
}

heroes.forEach(h => {
  delete h.raw_forms;
  translateSkillList(h.skills);
  if (h.forms) {
    h.forms.forEach(f => translateSkillList(f.skills));
  }

  (h.teamups || []).forEach(tu => {
    const rawDesc = tu.description || '';
    const tDesc = norm(rawDesc);
    const hasNumbersInDesc = /\d/.test(tDesc);

    // 1. Exact description match (only fall back to loadout_name if description has NO numbers and matches same hero)
    let entry = teamupsMap[tDesc] || teamupsMap[rawDesc];
    let subNums = null;

    // 2. Dynamic numerical pattern match when numbers in teamup description were patched
    if (!entry && hasNumbersInDesc) {
      const targetNums = tDesc.match(/\d+(?:\.\d+)?/g);
      const targetTemplate = tDesc.replace(/\d+(?:\.\d+)?/g, '<NUM>');
      for (const cand of numericTeamupTemplates) {
        if (cand.templateKey === targetTemplate && cand.nums.length === targetNums.length) {
          entry = cand.entry;
          subNums = { oldNums: cand.nums, newNums: targetNums };
          break;
        }
      }
    }

    if (!entry && !hasNumbersInDesc) {
      const byName = teamupsMap[tu.loadout_name];
      if (byName && (!byName.hero || byName.hero.toUpperCase() === h.name.toUpperCase())) {
        entry = byName;
      }
    }

    if (entry) {
      let transObj = null;
      if (tu.tier === 'base' && entry.base) {
        transObj = entry.base;
      } else if (tu.tier === 'enhanced' && entry.enhanced) {
        transObj = entry.enhanced;
      } else if (entry.full) {
        transObj = entry.full;
      }

      if (transObj && subNums) {
        const ko = substituteNumbers(transObj.ko, subNums.oldNums, subNums.newNums);
        const ja = substituteNumbers(transObj.ja, subNums.oldNums, subNums.newNums);
        if (ko && ja) transObj = { ko, ja };
        else transObj = null;
      }

      if (transObj) {
        tu.description_trans = transObj;
      }

      // Backfill partner_name if missing from description heuristic
      if (entry.partner && (!tu.partner_name || !tu.partner_name.en)) {
        tu.partner_name = { ...entry.partner };
      }
    }

    // Split English combined description into tier-specific text
    tu.description = splitEnglishTeamupDesc(rawDesc, tu.tier);

    if (tu.description && !tu.description_trans) {
      tu.description_trans = { ko: tu.description, ja: tu.description };
      teamupFallbackCount++;
    }
  });
});

console.log(`✓ Applied KR/JP translations (Skill fallbacks: ${skillFallbackCount}, Team-Up fallbacks: ${teamupFallbackCount}).`);

// -------------------------------------------------------------
// Step 4: Report Newly Discovered Stat Labels Without Polluting stats.json
// -------------------------------------------------------------
if (fs.existsSync(statsPath)) {
  const statsData = JSON.parse(fs.readFileSync(statsPath, 'utf-8'));
  const labels = statsData.labels || {};
  const lowerSet = new Set(Object.keys(labels).map(k => k.toLowerCase()));
  const unknownLabels = new Set();

  function inspectStats(s) {
    if (!s || !s.stats) return;
    const entries = Array.isArray(s.stats) ? s.stats : Object.entries(s.stats);
    for (const [key] of entries) {
      if (!key || key.toLowerCase() === 'key') continue;
      const trimmed = key.trim();
      if (!labels[trimmed] && !lowerSet.has(trimmed.toLowerCase())) {
        unknownLabels.add(trimmed);
      }
    }
    if (s.upgrade) inspectStats(s.upgrade);
  }

  heroes.forEach(h => {
    (h.skills || []).forEach(inspectStats);
    (h.forms || []).forEach(f => (f.skills || []).forEach(inspectStats));
    (h.teamups || []).forEach(inspectStats);
  });

  if (unknownLabels.size > 0) {
    console.log(`[Notice] ${unknownLabels.size} untranslated stat label(s) will use runtime English fallback: ${Array.from(unknownLabels).slice(0, 10).join(', ')}`);
  }
}

// Save compact-friendly heroes.json (single-line stat tuples for smaller size & clean 1-line git diffs)
const formattedHeroesJson = JSON.stringify(heroes, null, 2).replace(
  /\[\n\s+("(?:\\.|[^"\\])*"),\n\s+("(?:\\.|[^"\\])*")\n\s+\]/g,
  '[$1, $2]'
);
fs.writeFileSync(heroesPath, formattedHeroesJson, 'utf-8');
const heroesSizeKb = (fs.statSync(heroesPath).size / 1024).toFixed(1);
console.log(`✓ Saved optimized heroes.json (${heroes.length} heroes, ${heroesSizeKb} KB).`);

// -------------------------------------------------------------
// Step 5: Sync Hero Counts & Content Cache Hash in index.html & README.md
// -------------------------------------------------------------
const hash = crypto.createHash('md5');
['data/heroes.json', 'data/i18n.json', 'data/translations/stats.json', 'app.js', 'styles.css'].forEach(rel => {
  const p = path.join(rootDir, rel);
  if (fs.existsSync(p)) hash.update(fs.readFileSync(p));
});
const versionHash = hash.digest('hex').slice(0, 8);

if (fs.existsSync(indexPath)) {
  let html = fs.readFileSync(indexPath, 'utf-8');
  const count = heroes.length;

  html = html.replace(
    /<div class="count-indicator" id="heroes-count">[^<]*<\/div>/g,
    `<div class="count-indicator" id="heroes-count">${count} Heroes</div>`
  );
  html = html.replace(
    /마블 라이벌즈\(Marvel Rivals\) \d+명 전 영웅/g,
    `마블 라이벌즈(Marvel Rivals) ${count}명 전 영웅`
  );
  html = html.replace(/styles\.css\?v=[a-zA-Z0-9_-]+/g, `styles.css?v=${versionHash}`);
  html = html.replace(/app\.js\?v=[a-zA-Z0-9_-]+/g, `app.js?v=${versionHash}`);
  html = html.replace(/data-version="[a-zA-Z0-9_-]*"/g, `data-version="${versionHash}"`);

  fs.writeFileSync(indexPath, html, 'utf-8');
  console.log(`✓ Updated index.html (${count} Heroes, cache version v=${versionHash}).`);
}

if (fs.existsSync(readmePath)) {
  let readme = fs.readFileSync(readmePath, 'utf-8');
  const count = heroes.length;
  readme = readme.replace(/전체 영웅\(\d+명/g, `전체 영웅(${count}명`);
  readme = readme.replace(/# \d+명 전체 영웅의/g, `# ${count}명 전체 영웅의`);
  fs.writeFileSync(readmePath, readme, 'utf-8');
  console.log(`✓ Updated README.md hero count to ${count}.`);
}

console.log('=== [DONE] Post-Processing Completed Successfully! ===\n');
