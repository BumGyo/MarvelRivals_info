const fs = require('fs');
const path = require('path');

const heroes = JSON.parse(fs.readFileSync('data/heroes.json', 'utf8'));
const translations = JSON.parse(fs.readFileSync('data/translations.json', 'utf8'));

console.log("=== Testing Frontend Translation Functions & Patch Resilience ===");

// Simulate frontend functions from app.js
function translateStatLabel(k, lang) {
  if (!k || lang === 'en') return k;
  if (translations.stat_labels?.[k]?.[lang]) {
    return translations.stat_labels[k][lang];
  }
  return k;
}

function translateStatValue(v, lang) {
  if (!v || typeof v !== 'string' || lang === 'en') return v;
  const trimmed = v.trim();
  if (translations.stat_values?.[trimmed]?.[lang]) {
    return translations.stat_values[trimmed][lang];
  }
  const patterns = translations.stat_patterns || [];
  for (const p of patterns) {
    try {
      const regex = new RegExp(p.regex, 'i');
      if (regex.test(trimmed)) {
        const repl = p[lang] || p.ko || '';
        if (repl) return trimmed.replace(regex, repl);
      }
    } catch (e) {}
  }
  return v;
}

// 1. Test Seasonal Patch Resilience (dynamic numbers changing)
const patchScenarios = [
  { original: "60 damage per round", patched: "75 damage per round", expectedKO: "75 발당 데미지", expectedJA: "75 発あたりのダメージ" },
  { original: "Falloff begins at 20m, decreasing to 60% at 40m", patched: "Falloff begins at 25m, decreasing to 50% at 45m", expectedKO: "25m부터 감쇠 시작, 45m에서 50%로 감소", expectedJA: "25mから減衰開始、45mで50%に低下" },
  { original: "35 / s", patched: "42 / s", expectedKO: "초당 42", expectedJA: "毎秒 42" },
  { original: "0.25", patched: "0.35", expectedKO: "0.35", expectedJA: "0.35" }
];

let patchPassed = 0;
for (const s of patchScenarios) {
  const koRes = translateStatValue(s.patched, 'ko');
  const jaRes = translateStatValue(s.patched, 'ja');
  if (koRes === s.expectedKO && jaRes === s.expectedJA) {
    console.log(`✓ Patch Resilience Test Passed: "${s.patched}" -> KO: "${koRes}", JA: "${jaRes}"`);
    patchPassed++;
  } else {
    console.error(`❌ Mismatch for "${s.patched}": KO="${koRes}" (exp "${s.expectedKO}"), JA="${jaRes}" (exp "${s.expectedJA}")`);
  }
}

// 2. Test English Name Integrity across all 55 heroes
let nameIntegrityErrors = 0;
heroes.forEach(h => {
  h.skills.forEach(s => {
    if (/[\uAC00-\uD7AF\u3040-\u309F\u30A0-\u30FF]/.test(s.name)) {
      console.error(`Non-English skill name found in ${h.name}: ${s.name}`);
      nameIntegrityErrors++;
    }
  });
  (h.teamups || []).forEach(tu => {
    if (/[\uAC00-\uD7AF\u3040-\u309F\u30A0-\u30FF]/.test(tu.loadout_name)) {
      console.error(`Non-English teamup name found in ${h.name}: ${tu.loadout_name}`);
      nameIntegrityErrors++;
    }
  });
});

if (nameIntegrityErrors === 0) {
  console.log(`✓ 100% English integrity confirmed across all skill names and team-up names in all 55 heroes.`);
}

console.log("=== All Tests Completed ===");
