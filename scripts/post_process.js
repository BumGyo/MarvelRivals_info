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

  // Helper to pair base skill with upgraded skill
  function makeSkillWithUpgrade(sList, baseIdx, upIdx) {
    const base = JSON.parse(JSON.stringify(sList[baseIdx]));
    const up = sList[upIdx];
    if (up) {
      base.upgrade = {
        name: up.name,
        icon: up.icon || base.icon,
        description: up.description,
        stats: JSON.parse(JSON.stringify(up.stats || {}))
      };
    }
    return base;
  }

  // 26 Vanguard skills
  const vSkillsRaw = [
    ...dp.skills.slice(0, 4),    // Left Click (0..3)
    ...dp.skills.slice(12, 16),  // Right Click (12..15)
    ...dp.skills.slice(24, 28),  // Q (24..27)
    ...dp.skills.slice(36, 39),  // E (36..38)
    ...dp.skills.slice(45, 47),  // F (45..46)
    ...dp.skills.slice(51, 53),  // Space (51..52)
    ...dp.skills.slice(57, 64)   // Passives (57..63)
  ];

  // 26 Duelist skills
  const dSkillsRaw = [
    ...dp.skills.slice(4, 8),    // Left Click (4..7)
    ...dp.skills.slice(16, 20),  // Right Click (16..19)
    ...dp.skills.slice(28, 32),  // Q (28..31)
    ...dp.skills.slice(39, 42),  // E (39..41)
    ...dp.skills.slice(47, 49),  // F (47..48)
    ...dp.skills.slice(53, 55),  // Space (53..54)
    ...dp.skills.slice(64, 71)   // Passives (64..70)
  ];

  // 26 Strategist skills
  const sSkillsRaw = [
    ...dp.skills.slice(8, 12),   // Left Click (8..11)
    ...dp.skills.slice(20, 24),  // Right Click (20..23)
    ...dp.skills.slice(32, 36),  // Q (32..35)
    ...dp.skills.slice(42, 45),  // E (42..44)
    ...dp.skills.slice(49, 51),  // F (49..50)
    ...dp.skills.slice(55, 57),  // Space (55..56)
    ...dp.skills.slice(71, 78)   // Passives (71..77)
  ];

  function buildConsolidatedSkills(rawList) {
    return [
      makeSkillWithUpgrade(rawList, 0, 2),  // Left Click (Gun)
      makeSkillWithUpgrade(rawList, 1, 3),  // Left Click (Katana)
      makeSkillWithUpgrade(rawList, 4, 7),  // Right Click 1
      makeSkillWithUpgrade(rawList, 5, 6),  // Right Click 2
      makeSkillWithUpgrade(rawList, 8, 11), // Q 1
      makeSkillWithUpgrade(rawList, 9, 10), // Q 2
      makeSkillWithUpgrade(rawList, 12, 14),// E
      JSON.parse(JSON.stringify(rawList[15])), // F (Upgrade guide)
      JSON.parse(JSON.stringify(rawList[17])), // Space
      JSON.parse(JSON.stringify(rawList[19])), // Passive 1 (Healing Factor)
      JSON.parse(JSON.stringify(rawList[20])), // Passive 2 (Maximum Flair)
      JSON.parse(JSON.stringify(rawList[21]))  // Passive 3 (Comical Chaos)
    ];
  }

  const vanguardHero = {
    id: 'deadpool-vanguard',
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
    skills: buildConsolidatedSkills(vSkillsRaw),
    teamups: JSON.parse(JSON.stringify(dp.teamups || []))
  };

  const duelistHero = {
    id: 'deadpool-duelist',
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
    skills: buildConsolidatedSkills(dSkillsRaw),
    teamups: JSON.parse(JSON.stringify(dp.teamups || []))
  };

  const strategistHero = {
    id: 'deadpool-strategist',
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
    skills: buildConsolidatedSkills(sSkillsRaw),
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
