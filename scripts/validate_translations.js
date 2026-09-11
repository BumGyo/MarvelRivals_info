const fs = require('fs');
const path = require('path');

const KOREAN_REGEX = /[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]/;
const JAPANESE_REGEX = /[\u3040-\u309F\u30A0-\u30FF]/;

let errorCount = 0;
let warningCount = 0;

function reportError(msg) {
  console.error(`❌ [ERROR] ${msg}`);
  errorCount++;
}

function reportWarning(msg) {
  console.warn(`⚠️ [WARNING] ${msg}`);
  warningCount++;
}

function reportNotice(msg) {
  console.log(`ℹ️ [NOTICE] ${msg}`);
}

console.log("==================================================");
console.log("   Marvel Rivals Info - Translation Validation   ");
console.log("==================================================");

let unified = {};
const transPath = path.join(__dirname, '../data/translations.json');
if (!fs.existsSync(transPath)) {
  reportError(`Master translations file not found: ${transPath}`);
} else {
  try {
    unified = JSON.parse(fs.readFileSync(transPath, 'utf8'));
    console.log(`✓ Loaded data/translations.json`);

    ['skills', 'teamups', 'stat_labels', 'stat_values', 'stat_patterns'].forEach(cat => {
      if (!unified[cat]) {
        reportError(`Missing category '${cat}' in data/translations.json`);
      }
    });

    // Purity check on unified
    let purityErrors = 0;
    function checkPurity(obj, currentPath) {
      if (!obj || typeof obj !== 'object') return;
      if (obj.ko && typeof obj.ko === 'string') {
        if (JAPANESE_REGEX.test(obj.ko)) {
          reportError(`Japanese character detected in Korean translation at ${currentPath}.ko: "${obj.ko.substring(0, 40)}..."`);
          purityErrors++;
        }
      }
      if (obj.ja && typeof obj.ja === 'string') {
        if (KOREAN_REGEX.test(obj.ja)) {
          reportError(`Korean character detected in Japanese translation at ${currentPath}.ja: "${obj.ja.substring(0, 40)}..."`);
          purityErrors++;
        }
      }
      for (const [k, v] of Object.entries(obj)) {
        if (v && typeof v === 'object') {
          checkPurity(v, `${currentPath}.${k}`);
        }
      }
    }
    checkPurity(unified, 'translations');
    // Check for placeholder text in skills
    let placeholderErrors = 0;
    if (unified.skills) {
      for (const [k, v] of Object.entries(unified.skills)) {
        if (v.ko && /의 스킬입니다/.test(v.ko)) {
          reportError(`Placeholder "의 스킬입니다" found in skills.json for "${k.substring(0, 30)}..."`);
          placeholderErrors++;
        }
        if (v.ja && /のスキル/.test(v.ja)) {
          reportError(`Placeholder "のスキル" found in skills.json for "${k.substring(0, 30)}..."`);
          placeholderErrors++;
        }
      }
    }
    if (placeholderErrors === 0) {
      console.log(`✓ 0 low-quality placeholder translations detected in data/translations.json`);
    }
  } catch (e) {
    reportError(`Failed to parse data/translations.json: ${e.message}`);
  }
}

// 2. Validate data/heroes.json
const heroesPath = path.join(__dirname, '../data/heroes.json');
if (!fs.existsSync(heroesPath)) {
  reportError(`Heroes data file not found: ${heroesPath}`);
} else {
  try {
    const parsed = JSON.parse(fs.readFileSync(heroesPath, 'utf8'));
    const heroes = Array.isArray(parsed) ? parsed : (parsed.heroes || []);
    console.log(`✓ Loaded data/heroes.json (${heroes.length} heroes)`);

    let totalSkills = 0;
    let translatedSkills = 0;
    let fallbackSkills = 0;
    let totalTeamups = 0;
    let translatedTeamups = 0;
    let fallbackTeamups = 0;
    let namePurityViolations = 0;

    heroes.forEach(h => {
      const heroName = h.name || h.names?.en || h.id || 'Unknown Hero';

      function validateSkill(s, context) {
        totalSkills++;
        // Check skill name is kept English
        if (KOREAN_REGEX.test(s.name) || JAPANESE_REGEX.test(s.name)) {
          reportError(`Hero ${heroName} (${context}) skill name '${s.name}' contains non-English characters! Must be kept in English.`);
          namePurityViolations++;
        }

        if (s.description) {
          if (!s.description_trans || !s.description_trans.ko || !s.description_trans.ja) {
            reportWarning(`Hero ${heroName} (${context}) skill '${s.name}' missing description_trans (ko or ja). Auto-fallback used.`);
            fallbackSkills++;
          } else {
            const isKoFallback = s.description_trans.ko === s.description;
            const isJaFallback = s.description_trans.ja === s.description;
            if (isKoFallback || isJaFallback) {
              fallbackSkills++;
            } else {
              translatedSkills++;
            }

            if (/의 스킬입니다/.test(s.description_trans.ko)) {
              reportError(`Hero ${heroName} (${context}) skill '${s.name}' KO contains placeholder "의 스킬입니다"!`);
            }
            if (/のスキル/.test(s.description_trans.ja)) {
              reportError(`Hero ${heroName} (${context}) skill '${s.name}' JA contains placeholder "のスキル"!`);
            }
            if (JAPANESE_REGEX.test(s.description_trans.ko)) {
              reportError(`Hero ${heroName} (${context}) skill '${s.name}' KO contains Japanese characters!`);
            }
            if (KOREAN_REGEX.test(s.description_trans.ja)) {
              reportError(`Hero ${heroName} (${context}) skill '${s.name}' JA contains Korean characters!`);
            }
          }
        }
      }

      (h.skills || []).forEach(s => validateSkill(s, 'primary'));
      if (h.forms) {
        h.forms.forEach(f => {
          (f.skills || []).forEach(s => validateSkill(s, `form ${f.name}`));
        });
      }

      // Upgrades check (e.g. Thor)
      (h.upgrade || []).forEach(s => {
        totalSkills++;
        if (KOREAN_REGEX.test(s.name) || JAPANESE_REGEX.test(s.name)) {
          reportError(`Hero ${heroName} upgrade skill name '${s.name}' contains non-English characters!`);
          namePurityViolations++;
        }
        if (s.description) {
          if (!s.description_trans || !s.description_trans.ko || !s.description_trans.ja) {
            reportWarning(`Hero ${heroName} upgrade '${s.name}' missing description_trans. Auto-fallback used.`);
            fallbackSkills++;
          } else {
            const isKoFallback = s.description_trans.ko === s.description;
            const isJaFallback = s.description_trans.ja === s.description;
            if (isKoFallback || isJaFallback) {
              fallbackSkills++;
            } else {
              translatedSkills++;
            }
          }
        }
      });

      // Team-ups check
      (h.teamups || []).forEach(tu => {
        totalTeamups++;
        if (KOREAN_REGEX.test(tu.loadout_name) || JAPANESE_REGEX.test(tu.loadout_name)) {
          reportError(`Hero ${heroName} teamup name '${tu.loadout_name}' contains non-English characters!`);
          namePurityViolations++;
        }

        if (tu.description_trans && tu.description_trans.ko && tu.description_trans.ja) {
          const isKoFallback = tu.description_trans.ko === tu.description;
          const isJaFallback = tu.description_trans.ja === tu.description;
          if (isKoFallback || isJaFallback) {
            fallbackTeamups++;
          } else {
            translatedTeamups++;
          }

          if (JAPANESE_REGEX.test(tu.description_trans.ko)) {
            reportError(`Hero ${heroName} teamup '${tu.loadout_name}' KO contains Japanese characters!`);
          }
          if (KOREAN_REGEX.test(tu.description_trans.ja)) {
            reportError(`Hero ${heroName} teamup '${tu.loadout_name}' JA contains Korean characters!`);
          }
        } else {
          reportWarning(`Hero ${heroName} teamup '${tu.loadout_name}' missing description_trans. Auto-fallback used.`);
          fallbackTeamups++;
        }

        (tu.items || []).forEach(item => {
          if (item.description && (!item.description_trans || !item.description_trans.ko || !item.description_trans.ja)) {
            reportWarning(`Hero ${heroName} teamup '${tu.loadout_name}' item missing description_trans.`);
          }
        });
      });
    });

    // Check stat labels coverage across all hero skills
    let totalStatLabels = 0;
    let translatedStatLabels = 0;
    const statLabelsDict = unified.stat_labels || {};

    heroes.forEach(h => {
      function checkStats(s) {
        if (!s || !s.stats) return;
        for (const k of Object.keys(s.stats)) {
          if (k.toLowerCase() === 'key') continue;
          totalStatLabels++;
          const tr = statLabelsDict[k.trim()] || statLabelsDict[k];
          if (tr && tr.ko && tr.ja) {
            translatedStatLabels++;
          } else {
            reportError(`Hero ${h.name} stat label '${k}' is missing KO/JA translation in stat_labels!`);
          }
        }
        if (s.upgrade) checkStats(s.upgrade);
      }
      (h.skills || []).forEach(s => checkStats(s));
      (h.forms || []).forEach(f => (f.skills || []).forEach(s => checkStats(s)));
    });

    console.log(`✓ Skills translation: ${translatedSkills} native + ${fallbackSkills} fallback / ${totalSkills} total (${(((translatedSkills + fallbackSkills)/totalSkills)*100).toFixed(1)}% available)`);
    console.log(`✓ Teamups translation: ${translatedTeamups} native + ${fallbackTeamups} fallback / ${totalTeamups} total (${(((translatedTeamups + fallbackTeamups)/totalTeamups)*100).toFixed(1)}% available)`);
    console.log(`✓ Stat labels (titles) translation: ${translatedStatLabels} / ${totalStatLabels} (${((translatedStatLabels/totalStatLabels)*100).toFixed(1)}% translated)`);
    console.log(`✓ English name integrity: ${namePurityViolations === 0 ? 'Passed (All English)' : 'Failed'}`);

  } catch (e) {
    reportError(`Failed to parse data/heroes.json: ${e.message}`);
  }
}

console.log("--------------------------------------------------");
if (errorCount === 0) {
  if (warningCount > 0) {
    console.log(`⚠️ VALIDATION PASSED WITH ${warningCount} WARNINGS (CI will proceed with fallback data).`);
  } else {
    console.log("🎉 ALL VALIDATION CHECKS PASSED PERFECTLY (0 errors, 0 warnings)!");
  }
  process.exit(0);
} else {
  console.error(`❌ VALIDATION FAILED WITH ${errorCount} HARD ERRORS!`);
  process.exit(1);
}
