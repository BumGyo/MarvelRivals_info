const fs = require('fs');
const path = require('path');

const KOREAN_REGEX = /[\uAC00-\uD7AF\u1100-\u11FF\u3130-\u318F]/;
const JAPANESE_REGEX = /[\u3040-\u309F\u30A0-\u30FF]/;

let errorCount = 0;

function reportError(msg) {
  console.error(`❌ [ERROR] ${msg}`);
  errorCount++;
}

console.log("==================================================");
console.log("   Marvel Rivals Info - Translation Validation   ");
console.log("==================================================");

// 1. Validate data/translations.json and components
const transPath = path.join(__dirname, '../data/translations.json');
if (!fs.existsSync(transPath)) {
  reportError(`Master translations file not found: ${transPath}`);
} else {
  try {
    const unified = JSON.parse(fs.readFileSync(transPath, 'utf8'));
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
    if (purityErrors === 0) {
      console.log(`✓ Purity test passed for data/translations.json (0 cross-language contaminations)`);
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
    let totalTeamups = 0;
    let translatedTeamups = 0;
    let namePurityViolations = 0;

    heroes.forEach(h => {
      // Skills check
      (h.skills || []).forEach(s => {
        totalSkills++;
        // Check skill name is kept English
        if (KOREAN_REGEX.test(s.name) || JAPANESE_REGEX.test(s.name)) {
          reportError(`Hero ${h.name} skill name '${s.name}' contains non-English characters! Must be kept in English.`);
          namePurityViolations++;
        }

        if (s.description) {
          if (!s.description_trans || !s.description_trans.ko || !s.description_trans.ja) {
            reportError(`Hero ${h.name} skill '${s.name}' missing description_trans (ko or ja)!`);
          } else {
            translatedSkills++;
            if (JAPANESE_REGEX.test(s.description_trans.ko)) {
              reportError(`Hero ${h.name} skill '${s.name}' KO contains Japanese characters!`);
            }
            if (KOREAN_REGEX.test(s.description_trans.ja)) {
              reportError(`Hero ${h.name} skill '${s.name}' JA contains Korean characters!`);
            }
          }
        }
      });

      // Upgrades check (e.g. Thor)
      (h.upgrade || []).forEach(s => {
        totalSkills++;
        if (KOREAN_REGEX.test(s.name) || JAPANESE_REGEX.test(s.name)) {
          reportError(`Hero ${h.name} upgrade skill name '${s.name}' contains non-English characters!`);
          namePurityViolations++;
        }
        if (s.description) {
          if (!s.description_trans || !s.description_trans.ko || !s.description_trans.ja) {
            reportError(`Hero ${h.name} upgrade '${s.name}' missing description_trans!`);
          } else {
            translatedSkills++;
          }
        }
      });

      // Team-ups check
      (h.teamups || []).forEach(tu => {
        totalTeamups++;
        if (KOREAN_REGEX.test(tu.loadout_name) || JAPANESE_REGEX.test(tu.loadout_name)) {
          reportError(`Hero ${h.name} teamup name '${tu.loadout_name}' contains non-English characters!`);
          namePurityViolations++;
        }

        if (tu.description_trans) {
          translatedTeamups++;
          if (JAPANESE_REGEX.test(tu.description_trans.ko)) {
            reportError(`Hero ${h.name} teamup '${tu.loadout_name}' KO contains Japanese characters!`);
          }
          if (KOREAN_REGEX.test(tu.description_trans.ja)) {
            reportError(`Hero ${h.name} teamup '${tu.loadout_name}' JA contains Korean characters!`);
          }
        } else {
          reportError(`Hero ${h.name} teamup '${tu.loadout_name}' missing description_trans!`);
        }

        (tu.items || []).forEach(item => {
          if (item.description && (!item.description_trans || !item.description_trans.ko || !item.description_trans.ja)) {
            reportError(`Hero ${h.name} teamup '${tu.loadout_name}' item missing description_trans!`);
          }
        });
      });
    });

    console.log(`✓ Skills translation coverage: ${translatedSkills}/${totalSkills} (${((translatedSkills/totalSkills)*100).toFixed(1)}%)`);
    console.log(`✓ Teamups translation coverage: ${translatedTeamups}/${totalTeamups} (${((translatedTeamups/totalTeamups)*100).toFixed(1)}%)`);
    console.log(`✓ English name integrity: ${namePurityViolations === 0 ? 'Passed (All English)' : 'Failed'}`);

  } catch (e) {
    reportError(`Failed to parse data/heroes.json: ${e.message}`);
  }
}

console.log("--------------------------------------------------");
if (errorCount === 0) {
  console.log("🎉 ALL VALIDATION CHECKS PASSED PERFECTLY (0 errors)!");
  process.exit(0);
} else {
  console.error(`⚠️ VALIDATION FAILED WITH ${errorCount} ERRORS!`);
  process.exit(1);
}
