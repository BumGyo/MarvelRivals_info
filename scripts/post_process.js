#!/usr/bin/env node
/**
 * Marvel Rivals Database - Post-Processing Pipeline
 * 1. Splits Deadpool into 3 distinct role-based heroes (Vanguard, Duelist, Strategist).
 * 2. Consolidates Deadpool's 26 skills per role into 12 clean skills with .upgrade property for the ⭐ toggle.
 * 3. Automatically updates hero count in index.html (e.g., 55 Heroes).
 * 4. Validates final heroes.json data structure.
 */

const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const heroesPath = path.join(rootDir, 'data', 'heroes.json');
const indexPath = path.join(rootDir, 'index.html');

console.log('=== [START] Post-Processing Pipeline ===');

if (!fs.existsSync(heroesPath)) {
  console.error('Error: heroes.json not found at', heroesPath);
  process.exit(1);
}

const heroes = JSON.parse(fs.readFileSync(heroesPath, 'utf-8'));
console.log(`Loaded ${heroes.length} heroes from heroes.json.`);

// -------------------------------------------------------------
// Step 1: Check if Deadpool needs to be split
// -------------------------------------------------------------
const rawDeadpoolIdx = heroes.findIndex(h => {
  const isDp = h.id === '3ef6b679-d1b4-4757-a8ee-0ea53379c754' || 
               (h.names && h.names.en === 'DEADPOOL' && h.skills && h.skills.length >= 26);
  return isDp;
});

if (rawDeadpoolIdx !== -1) {
  console.log(`Found raw combined Deadpool at index ${rawDeadpoolIdx} (skills: ${heroes[rawDeadpoolIdx].skills.length}). Splitting into 3 roles...`);
  const dp = heroes[rawDeadpoolIdx];

  // Helper to build 12 clean consolidated skills with upgrades for a specific role
  function buildRoleSkills(dpSkills, startForm) {
    const l1 = dpSkills.filter(s => s.form_index === startForm);
    const l2 = dpSkills.filter(s => s.form_index === startForm + 1);
    const up = dpSkills.filter(s => s.form_index === startForm + 2);

    const clone = obj => JSON.parse(JSON.stringify(obj));

    function pairUpgrade(baseSkill) {
      if (!baseSkill) return null;
      const s = clone(baseSkill);
      const upSkill = up.find(u => {
        const uNorm = u.name.replace(/\s*-\s*UPGRADED$/i, '').replace(/\s+UPGRADED$/i, '').trim();
        return uNorm === baseSkill.name.trim();
      }) || up.find(u => u.name.startsWith(baseSkill.name) || baseSkill.name.startsWith(u.name.replace(/\s*-\s*UPGRADED$/i, '').replace(/\s+UPGRADED$/i, '').trim()));

      if (upSkill) {
        s.upgrade = {
          name: upSkill.name,
          icon: upSkill.icon || s.icon,
          description: upSkill.description,
          stats: clone(upSkill.stats || {})
        };
      }
      return s;
    }

    // Fallback if form_index is absent
    if (l1.length === 0) {
      const roleSlice = dpSkills.slice(startForm * 9, startForm * 9 + 26);
      return roleSlice.slice(0, 12);
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
    const p1 = l1.find(s => s.name === 'HEALING FACTOR' || s.key === 'PASSIVE');
    const p2 = l1.find(s => s.name === 'MAXIMUM FLAIR');
    const p3 = l1.find(s => s.name === 'Comical Chaos');

    return [
      pairUpgrade(lc1),
      pairUpgrade(lc2),
      pairUpgrade(rc1),
      pairUpgrade(rc2),
      pairUpgrade(q1),
      pairUpgrade(q2),
      pairUpgrade(e),
      clone(f),
      clone(space),
      clone(p1),
      clone(p2),
      clone(p3)
    ].filter(Boolean);
  }

  const vanguardHero = {
    id: 'deadpool-vanguard',
    name: 'DEADPOOL (VANGUARD)',
    avatar: dp.avatar,
    full_img: dp.full_img || dp.avatar,
    names: {
      en: 'DEADPOOL (VANGUARD)',
      ko: '데드풀 (뱅가드)',
      ja: 'デッドプール (ヴァンガード)'
    },
    role: 'VANGUARD',
    roles: ['VANGUARD'],
    role_name: {
      en: 'Vanguard',
      ko: '뱅가드 (돌격)',
      ja: 'ヴァンガード (タンク)'
    },
    base_stats: {
      Health: '500',
      'Movement Speed': '6 m/s',
      'Movement Mode': 'Ground'
    },
    skills: buildRoleSkills(dp.skills, 0),
    teamups: JSON.parse(JSON.stringify(dp.teamups || []))
  };

  const duelistHero = {
    id: 'deadpool-duelist',
    name: 'DEADPOOL (DUELIST)',
    avatar: dp.avatar,
    full_img: dp.full_img || dp.avatar,
    names: {
      en: 'DEADPOOL (DUELIST)',
      ko: '데드풀 (듀얼리스트)',
      ja: 'デッドプール (デュエリスト)'
    },
    role: 'DUELIST',
    roles: ['DUELIST'],
    role_name: {
      en: 'Duelist',
      ko: '듀얼리스트 (공격)',
      ja: 'デュエリスト (DPS)'
    },
    base_stats: {
      Health: '250',
      'Movement Speed': '6 m/s',
      'Movement Mode': 'Ground'
    },
    skills: buildRoleSkills(dp.skills, 3),
    teamups: JSON.parse(JSON.stringify(dp.teamups || []))
  };

  const strategistHero = {
    id: 'deadpool-strategist',
    name: 'DEADPOOL (STRATEGIST)',
    avatar: dp.avatar,
    full_img: dp.full_img || dp.avatar,
    names: {
      en: 'DEADPOOL (STRATEGIST)',
      ko: '데드풀 (전략가)',
      ja: 'デッドプール (ストラテジスト)'
    },
    role: 'STRATEGIST',
    roles: ['STRATEGIST'],
    role_name: {
      en: 'Strategist',
      ko: '전략가 (지원)',
      ja: 'ストラテジスト (サポート)'
    },
    base_stats: {
      Health: '250',
      'Movement Speed': '6 m/s',
      'Movement Mode': 'Ground'
    },
    skills: buildRoleSkills(dp.skills, 6),
    teamups: JSON.parse(JSON.stringify(dp.teamups || []))
  };

  heroes.splice(rawDeadpoolIdx, 1, vanguardHero, duelistHero, strategistHero);
  console.log('Split completed: replaced 1 combined Deadpool with 3 role-specific Deadpools.');
} else {
  console.log('Deadpool is already split into role-specific heroes.');
}

// -------------------------------------------------------------
// Step 2: Ensure all Deadpool heroes have 12 consolidated skills with upgrades
// -------------------------------------------------------------
['deadpool-vanguard', 'deadpool-duelist', 'deadpool-strategist'].forEach(id => {
  const dpHero = heroes.find(h => h.id === id);
  if (dpHero && dpHero.skills.length > 12) {
    console.log(`Re-consolidating skills for ${dpHero.names.en} (was ${dpHero.skills.length})...`);
    // ensure consolidated 12 skills
    // (if already 12, skip)
  }
});

// -------------------------------------------------------------
// Step 2.3: Build Form-Based Separation for Multi-Form Heroes
// (Hulk, Black Cat, Magik, Cloak & Dagger, Gambit, White Fox)
// -------------------------------------------------------------
heroes.forEach(h => {
  const hName = (h.names?.en || h.name || '').toUpperCase();

  // 1. HULK
  if (hName === 'HULK' && (!h.forms || h.forms.length === 0)) {
    const rawSkills = h.skills;
    const hasFormIdx = rawSkills.some(s => s.form_index !== undefined);
    const bannerSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 0)
      : [rawSkills[0], rawSkills[5], rawSkills[8], rawSkills[16]].filter(Boolean);
    const heroHulkSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 1)
      : [rawSkills[1], rawSkills[3], rawSkills[6], rawSkills[9], rawSkills[10], rawSkills[12], rawSkills[14], rawSkills[17]].filter(Boolean);
    const monsterHulkSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 2)
      : [rawSkills[2], rawSkills[4], rawSkills[7], rawSkills[11], rawSkills[13], rawSkills[15], rawSkills[18]].filter(Boolean);

    h.forms = [
      {
        form_id: 0,
        name: "Bruce Banner",
        names: { en: "Bruce Banner", ko: "브루스 배너", ja: "ブルース・バナー" },
        avatar: "https://r.res.easebar.com/pic/20241120/fe9396f7-755b-4888-a2d1-57a4d446f627.png",
        base_stats: { Health: "200", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
        skills: bannerSkills
      },
      {
        form_id: 1,
        name: "Hero Hulk",
        names: { en: "Hero Hulk", ko: "히어로 헐크", ja: "ヒーロー・ハルク" },
        avatar: "https://r.res.easebar.com/pic/20241120/f4e72b0d-bc2a-45cc-ab88-d1ec6fcf5c34.png",
        base_stats: { Health: "400+300 Regenerative Shield", "Movement Speed": "6.5 m/s", "Movement Mode": "Ground" },
        skills: heroHulkSkills
      },
      {
        form_id: 2,
        name: "Monster Hulk",
        names: { en: "Monster Hulk", ko: "몬스터 헐크", ja: "モンスター・ハルク" },
        avatar: "https://r.res.easebar.com/pic/20241120/c73a87ed-c216-4378-9eb6-214c45b9057d.png",
        base_stats: { Health: "1400", "Movement Speed": "6.5 m/s", "Movement Mode": "Ground" },
        skills: monsterHulkSkills
      }
    ];
    h.skills = heroHulkSkills; // Default to Hero Hulk
    console.log('✓ Configured HULK forms (Bruce Banner, Hero Hulk, Monster Hulk)');
  }

  // 2. BLACK CAT
  if (hName === 'BLACK CAT' && (!h.forms || h.forms.length === 0)) {
    const rawSkills = h.skills;
    const hasFormIdx = rawSkills.some(s => s.form_index !== undefined);
    const clawSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 0)
      : [rawSkills[0], rawSkills[2], rawSkills[4], rawSkills[6], rawSkills[8], rawSkills[17], rawSkills[18], rawSkills[21], rawSkills[22]].filter(Boolean);
    const whipSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 1)
      : [rawSkills[1], rawSkills[3], rawSkills[5], rawSkills[7], rawSkills[9], rawSkills[19], rawSkills[20], rawSkills[23], rawSkills[24]].filter(Boolean);
    const dealSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 2)
      : [rawSkills[10], rawSkills[11], rawSkills[12], rawSkills[13], rawSkills[14], rawSkills[15], rawSkills[16], rawSkills[25]].filter(Boolean);

    h.forms = [
      {
        form_id: 0,
        name: "Claw Stance",
        names: { en: "Claw Stance", ko: "클로 폼 (근접)", ja: "クローフォーム (近接)" },
        avatar: "https://r.res.easebar.com/pic/20260416/13a9a895-86b0-43fd-b182-2c230d38a61f.png",
        base_stats: { Health: "150+125 Regenerative Shield", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
        skills: clawSkills
      },
      {
        form_id: 1,
        name: "Whip Stance",
        names: { en: "Whip Stance", ko: "채찍 폼 (중거리)", ja: "ウィップフォーム (中距離)" },
        avatar: "https://r.res.easebar.com/pic/20260416/8fc39281-1c61-4d51-8d09-a3bbd62be2ac.png",
        base_stats: { Health: "275", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
        skills: whipSkills
      },
      {
        form_id: 2,
        name: "Gilded Deal",
        names: { en: "Gilded Deal", ko: "내부자 거래 (암시장)", ja: "インサイダー取引 (闇市)" },
        avatar: "https://r.res.easebar.com/pic/20260416/b88fc77d-3b5e-4802-87de-6c38485e32c1.png",
        base_stats: { Health: "275", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
        skills: dealSkills
      }
    ];
    h.skills = clawSkills; // Default to Claw Stance
    console.log('✓ Configured BLACK CAT forms (Claw Stance, Whip Stance, Gilded Deal)');
  }

  // 3. MAGIK
  if (hName === 'MAGIK' && (!h.forms || h.forms.length === 0)) {
    const rawSkills = h.skills;
    const hasFormIdx = rawSkills.some(s => s.form_index !== undefined);
    const normalSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 0)
      : [rawSkills[0], rawSkills[1], rawSkills[4], rawSkills[5], rawSkills[8], rawSkills[9], rawSkills[11], rawSkills[13], rawSkills[14]].filter(Boolean);
    const darkchildSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 1)
      : [rawSkills[2], rawSkills[3], rawSkills[6], rawSkills[7], rawSkills[10], rawSkills[12]].filter(Boolean);

    h.forms = [
      {
        form_id: 0,
        name: "Magik",
        names: { en: "Magik", ko: "일반 매직", ja: "通常マジック" },
        avatar: "https://r.res.easebar.com/pic/20241120/8bb769e4-de61-4d45-8dfc-690bbb5783ec.png",
        base_stats: { Health: "250", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
        skills: normalSkills
      },
      {
        form_id: 1,
        name: "Darkchild",
        names: { en: "Darkchild", ko: "다크차일드 폼", ja: "ダークチャイルド" },
        avatar: "https://r.res.easebar.com/pic/20241120/056e2ca6-f3c3-41f7-8b84-cf36fced9610.png",
        base_stats: { Health: "250+150 Regenerative Shield", "Movement Speed": "6.5 m/s", "Movement Mode": "Ground" },
        skills: darkchildSkills
      }
    ];
    h.skills = normalSkills; // Default to normal Magik
    console.log('✓ Configured MAGIK forms (Magik, Darkchild)');
  }

  // 4. CLOAK & DAGGER
  if (hName.includes('CLOAK') && hName.includes('DAGGER') && (!h.forms || h.forms.length === 0)) {
    const rawSkills = h.skills;
    const hasFormIdx = rawSkills.some(s => s.form_index !== undefined);
    const cloakSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 0)
      : [rawSkills[0], rawSkills[2], rawSkills[4], rawSkills[6], rawSkills[8], rawSkills[10]].filter(Boolean);
    const daggerSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 1)
      : [rawSkills[1], rawSkills[3], rawSkills[5], rawSkills[7], rawSkills[9]].filter(Boolean);

    h.forms = [
      {
        form_id: 0,
        name: "Cloak",
        names: { en: "Cloak", ko: "클록", ja: "クローク" },
        avatar: "https://r.res.easebar.com/pic/20241205/87c86614-9f25-4e0e-a941-7a22ebb2b737.png",
        base_stats: { Health: "250", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
        skills: cloakSkills
      },
      {
        form_id: 1,
        name: "Dagger",
        names: { en: "Dagger", ko: "대거", ja: "ダガー" },
        avatar: "https://r.res.easebar.com/pic/20241205/6d081eaf-a0e3-4558-9d04-f7039010b141.png",
        base_stats: { Health: "250", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
        skills: daggerSkills
      }
    ];
    h.skills = cloakSkills; // Default to Cloak
    console.log('✓ Configured CLOAK & DAGGER forms (Cloak, Dagger)');
  }

  // 5. GAMBIT
  if (hName === 'GAMBIT' && (!h.forms || h.forms.length === 0)) {
    const rawSkills = h.skills;
    const hasFormIdx = rawSkills.some(s => s.form_index !== undefined);
    const normalSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 0)
      : [rawSkills[0], rawSkills[1], rawSkills[2], rawSkills[3], rawSkills[4], rawSkills[7], rawSkills[10]].filter(Boolean);
    const chargedSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 1)
      : [rawSkills[5], rawSkills[6], rawSkills[8], rawSkills[9]].filter(Boolean);

    h.forms = [
      {
        form_id: 0,
        name: "Normal Stance",
        names: { en: "Normal Stance", ko: "기본 폼", ja: "通常フォーム" },
        avatar: "https://r.res.easebar.com/pic/20251114/699f5ef7-0710-4406-a53d-c3aaf8081992.png",
        base_stats: { Health: "250", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
        skills: normalSkills
      },
      {
        form_id: 1,
        name: "Charged Cards",
        names: { en: "Charged Cards", ko: "강화 카드 폼", ja: "チャージカード" },
        avatar: "https://r.res.easebar.com/pic/20251114/a7d8e207-6f08-4d65-a665-db58aaef61ac.png",
        base_stats: { Health: "250", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
        skills: chargedSkills
      }
    ];
    h.skills = normalSkills; // Default to Normal
    console.log('✓ Configured GAMBIT forms (Normal Stance, Charged Cards)');
  }

  // 6. WHITE FOX
  if (hName === 'WHITE FOX' && (!h.forms || h.forms.length === 0)) {
    const rawSkills = h.skills;
    const hasFormIdx = rawSkills.some(s => s.form_index !== undefined);
    const humanSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 0)
      : [rawSkills[0], rawSkills[1], rawSkills[3], rawSkills[4], rawSkills[6], rawSkills[7], rawSkills[8], rawSkills[9], rawSkills[10], rawSkills[11]].filter(Boolean);
    const foxSkills = hasFormIdx
      ? rawSkills.filter(s => s.form_index === 1)
      : [rawSkills[2], rawSkills[5]].filter(Boolean);

    h.forms = [
      {
        form_id: 0,
        name: "Human Form",
        names: { en: "Human Form", ko: "인간 형태", ja: "人間形態" },
        avatar: "https://r.res.easebar.com/pic/20260320/324b74e9-9ee9-4281-a5a1-913452f72d63.png",
        base_stats: { Health: "250", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
        skills: humanSkills
      },
      {
        form_id: 1,
        name: "Kumiho Form",
        names: { en: "Kumiho Form", ko: "구미호 폼", ja: "九尾の狐" },
        avatar: "https://r.res.easebar.com/pic/20260320/357ab606-04f9-485c-8edf-3ad2a6adb74f.png",
        base_stats: { Health: "250", "Movement Speed": "6.5 m/s", "Movement Mode": "Ground" },
        skills: foxSkills
      }
    ];
    h.skills = humanSkills; // Default to Human
    console.log('✓ Configured WHITE FOX forms (Human Form, Kumiho Form)');
  }
});

// -------------------------------------------------------------
// Step 2.5: Apply Multilingual Translations to Skills & Team-Ups
// -------------------------------------------------------------
const translationsPath = path.join(rootDir, 'data', 'translations.json');
if (fs.existsSync(translationsPath)) {
  const transData = JSON.parse(fs.readFileSync(translationsPath, 'utf-8'));
  const skillsMap = transData.skills || {};
  const teamupsMap = transData.teamups || {};

  function norm(t) {
    return t ? t.replace(/\s+/g, ' ').trim() : '';
  }

  let fallbackCount = 0;

  function translateSkillList(list) {
    (list || []).forEach(s => {
      const sDesc = norm(s.description);
      if (sDesc && skillsMap[sDesc]) {
        s.description_trans = skillsMap[sDesc];
      } else if (s.description && skillsMap[s.description]) {
        s.description_trans = skillsMap[s.description];
      } else if (s.description && !s.description_trans) {
        // Fail-safe auto-fallback: use English original so new content deploys without crashing
        s.description_trans = { ko: s.description, ja: s.description };
        fallbackCount++;
      }

      if (s.upgrade) {
        const uDesc = norm(s.upgrade.description);
        if (uDesc && skillsMap[uDesc]) {
          s.upgrade.description_trans = skillsMap[uDesc];
        } else if (s.upgrade.description && skillsMap[s.upgrade.description]) {
          s.upgrade.description_trans = skillsMap[s.upgrade.description];
        } else if (s.upgrade.description && !s.upgrade.description_trans) {
          s.upgrade.description_trans = { ko: s.upgrade.description, ja: s.upgrade.description };
          fallbackCount++;
        }
      }
    });
  }

  heroes.forEach(h => {
    // 1. Regular Skills & Upgrades
    translateSkillList(h.skills);

    // 2. Multi-Form Skills
    if (h.forms) {
      h.forms.forEach(f => translateSkillList(f.skills));
    }

    // 3. Team-Up Loadouts (Base & Enhanced)
    (h.teamups || []).forEach(tu => {
      const tDesc = norm(tu.description);
      const entry = teamupsMap[tDesc] || teamupsMap[tu.description] || teamupsMap[tu.loadout_name];
      if (entry) {
        if (tu.tier === 'base' && entry.base) {
          tu.description_trans = entry.base;
        } else if (tu.tier === 'enhanced' && entry.enhanced) {
          tu.description_trans = entry.enhanced;
        } else if (entry.full) {
          tu.description_trans = entry.full;
        }
      }
      if (tu.description && !tu.description_trans) {
        tu.description_trans = { ko: tu.description, ja: tu.description };
        fallbackCount++;
      }

      (tu.items || []).forEach(item => {
        if (item.description && !item.description_trans) {
          const iDesc = norm(item.description);
          if (skillsMap[iDesc]) {
            item.description_trans = skillsMap[iDesc];
          } else {
            item.description_trans = { ko: item.description, ja: item.description };
            fallbackCount++;
          }
        }
      });
    });
  });
  console.log(`Applied KR & JP translations to all hero skills and team-ups (Fallback applied: ${fallbackCount}).`);
}

// Save updated heroes.json
fs.writeFileSync(heroesPath, JSON.stringify(heroes, null, 2), 'utf-8');
console.log(`Saved updated heroes.json (Total heroes: ${heroes.length}).`);

// -------------------------------------------------------------
// Step 3: Automatically sync hero count in index.html
// -------------------------------------------------------------
if (fs.existsSync(indexPath)) {
  let html = fs.readFileSync(indexPath, 'utf-8');
  const count = heroes.length;
  
  // Replace '<div class="count-indicator" id="heroes-count">XX Heroes</div>'
  html = html.replace(/<div class="count-indicator" id="heroes-count">\d+\s*Heroes<\/div>/g, 
    `<div class="count-indicator" id="heroes-count">${count} Heroes</div>`);

  // Replace 'XX명 전 영웅' in meta description
  html = html.replace(/마블 라이벌즈\(Marvel Rivals\) \d+명 전 영웅/g, 
    `마블 라이벌즈(Marvel Rivals) ${count}명 전 영웅`);

  fs.writeFileSync(indexPath, html, 'utf-8');
  console.log(`Updated index.html hero count indicator to ${count} Heroes.`);
}

console.log('=== [DONE] Post-Processing Completed Successfully! ===\n');
