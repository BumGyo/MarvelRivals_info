#!/usr/bin/env node
/**
 * Marvel Rivals Info - Comprehensive Translation & Data Integrity Validator
 * Validates:
 * 1. Source translation dictionaries (skills.json, teamups.json, stats.json) & runtime bundle (translations.json)
 * 2. Cross-language purity (0 Japanese Kana in KO, 0 Korean Hangul in JA) & 0 placeholder strings
 * 3. Hero skills, Deadpool .upgrade skills, multi-form skills, and Team-Up loadouts (including partner names & stats)
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
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

function getStatEntries(stats) {
  if (!stats) return [];
  return Array.isArray(stats) ? stats : Object.entries(stats);
}

console.log('==================================================');
console.log('   Marvel Rivals Info - Translation Validation    ');
console.log('==================================================');

function checkPurity(obj, currentPath) {
  if (!obj || typeof obj !== 'object') return;
  if (typeof obj.ko === 'string' && JAPANESE_REGEX.test(obj.ko)) {
    reportError(`Japanese Kana in KO at ${currentPath}.ko: "${obj.ko.slice(0, 50)}"`);
  }
  if (typeof obj.ja === 'string' && KOREAN_REGEX.test(obj.ja)) {
    reportError(`Korean Hangul in JA at ${currentPath}.ja: "${obj.ja.slice(0, 50)}"`);
  }
  for (const [k, v] of Object.entries(obj)) {
    if (v && typeof v === 'object') {
      checkPurity(v, `${currentPath}.${k}`);
    }
  }
}

// 1. Validate runtime translations.json & source dictionaries
const transPath = path.join(ROOT, 'data', 'translations.json');
const skillsDictPath = path.join(ROOT, 'data', 'translations', 'skills.json');
const teamupsDictPath = path.join(ROOT, 'data', 'translations', 'teamups.json');

let unified = {};
if (!fs.existsSync(transPath)) {
  reportError(`Runtime translations bundle missing: ${transPath}`);
} else {
  unified = JSON.parse(fs.readFileSync(transPath, 'utf8'));
  ['stat_labels', 'stat_values', 'stat_patterns'].forEach(cat => {
    if (!unified[cat]) reportError(`Missing category '${cat}' in data/translations.json`);
  });
  checkPurity(unified, 'translations.json');
  console.log('✓ Validated runtime data/translations.json');
}

if (fs.existsSync(skillsDictPath)) {
  const skillsDict = JSON.parse(fs.readFileSync(skillsDictPath, 'utf8'));
  checkPurity(skillsDict, 'skills.json');
  for (const [k, v] of Object.entries(skillsDict)) {
    if (v.ko && /의 스킬입니다/.test(v.ko)) {
      reportError(`Placeholder "의 스킬입니다" in skills.json: "${k.slice(0, 40)}"`);
    }
    if (v.ja && /のスキル/.test(v.ja)) {
      reportError(`Placeholder "のスキル" in skills.json: "${k.slice(0, 40)}"`);
    }
  }
  console.log(`✓ Validated data/translations/skills.json (${Object.keys(skillsDict).length} entries)`);
}

if (fs.existsSync(teamupsDictPath)) {
  const teamupsDict = JSON.parse(fs.readFileSync(teamupsDictPath, 'utf8'));
  checkPurity(teamupsDict, 'teamups.json');
  console.log(`✓ Validated data/translations/teamups.json (${Object.keys(teamupsDict).length} entries)`);
}

// 2. Validate data/heroes.json
const heroesPath = path.join(ROOT, 'data', 'heroes.json');
if (!fs.existsSync(heroesPath)) {
  reportError(`Heroes file missing: ${heroesPath}`);
} else {
  const heroes = JSON.parse(fs.readFileSync(heroesPath, 'utf8'));
  console.log(`✓ Loaded data/heroes.json (${heroes.length} heroes)`);

  if (!Array.isArray(heroes) || heroes.length < 50) {
    reportError(`Abnormally low hero count (${heroes.length} < 50)`);
  }

  const statLabelsExact = unified.stat_labels || {};
  const statLabelsLower = new Map(
    Object.entries(statLabelsExact).map(([k, v]) => [k.trim().toLowerCase(), v])
  );
  const statValuesExact = unified.stat_values || {};
  const statValuesLower = new Map(
    Object.entries(statValuesExact).map(([k, v]) => [k.trim().toLowerCase(), v])
  );
  const compiledPatterns = (unified.stat_patterns || []).map(p => ({
    rx: new RegExp(p.regex, 'i'),
    ko: p.ko || '',
    ja: p.ja || p.ko || ''
  }));

  function translateStatVal(v, lang) {
    const trimmed = v.trim();
    const stripped = trimmed.replace(/\.$/, '');
    for (const c of [trimmed, stripped, `${stripped}.`]) {
      if (statValuesExact[c]?.[lang]) return statValuesExact[c][lang];
    }
    for (const c of [trimmed, stripped, `${stripped}.`]) {
      const ci = statValuesLower.get(c.toLowerCase())?.[lang];
      if (ci) return ci;
    }
    for (const p of compiledPatterns) {
      if (p.rx.test(trimmed)) return trimmed.replace(p.rx, p[lang]);
    }
    return v;
  }

  let totalSkills = 0;
  let translatedSkills = 0;
  let fallbackSkills = 0;
  let totalTeamups = 0;
  let translatedTeamups = 0;
  let fallbackTeamups = 0;
  let totalStatLabels = 0;
  let translatedStatLabels = 0;
  let totalStatValues = 0;
  let translatedStatValues = 0;

  heroes.forEach(h => {
    const heroName = h.name || h.names?.en || h.id;

    function checkStats(statsContainer, context) {
      for (const [k, val] of getStatEntries(statsContainer)) {
        if (!k || k.toLowerCase() === 'key') continue;
        const trimmedKey = k.trim();
        totalStatLabels++;

        const tr = statLabelsExact[trimmedKey] || statLabelsLower.get(trimmedKey.toLowerCase());
        if (tr && tr.ko && tr.ja && tr.ko.toLowerCase() !== trimmedKey.toLowerCase()) {
          translatedStatLabels++;
        } else {
          reportWarning(`${heroName} (${context}) stat label '${trimmedKey}' missing KO/JA translation (using English fallback).`);
        }

        const vTrim = val === null || val === undefined ? '' : String(val).trim();
        if (vTrim && !/^[\d\s.,\-+/%°():;x×mMsS]+$/.test(vTrim)) {
          totalStatValues++;
          const koTrans = translateStatVal(vTrim, 'ko');
          const jaTrans = translateStatVal(vTrim, 'ja');
          const okKo = koTrans !== vTrim || !/[a-zA-Z]{3,}/.test(vTrim);
          const okJa = jaTrans !== vTrim || !/[a-zA-Z]{3,}/.test(vTrim);
          if (okKo && okJa) {
            translatedStatValues++;
          } else {
            reportWarning(`${heroName} (${context}) stat value untranslated: "${vTrim.slice(0, 60)}"`);
          }
        }
      }
    }

    function validateSkill(s, context) {
      totalSkills++;
      if (KOREAN_REGEX.test(s.name) || JAPANESE_REGEX.test(s.name)) {
        reportError(`${heroName} (${context}) skill name '${s.name}' must remain in English.`);
      }

      if (s.description) {
        const dt = s.description_trans;
        if (!dt || !dt.ko || !dt.ja) {
          reportWarning(`${heroName} (${context}) skill '${s.name}' missing description_trans.`);
          fallbackSkills++;
        } else {
          if (dt.ko === s.description || dt.ja === s.description) {
            fallbackSkills++;
          } else {
            translatedSkills++;
          }
          if (JAPANESE_REGEX.test(dt.ko)) reportError(`${heroName} skill '${s.name}' KO contains Japanese Kana.`);
          if (KOREAN_REGEX.test(dt.ja)) reportError(`${heroName} skill '${s.name}' JA contains Korean Hangul.`);
        }
      }

      checkStats(s.stats, `skill ${s.name}`);

      // Validate Deadpool skill upgrades properly via s.upgrade
      if (s.upgrade) {
        validateSkill(s.upgrade, `upgrade ${s.upgrade.name}`);
      }
    }

    (h.skills || []).forEach(s => validateSkill(s, 'primary'));
    (h.forms || []).forEach(f => {
      (f.skills || []).forEach(s => validateSkill(s, `form ${f.name}`));
    });

    (h.teamups || []).forEach(tu => {
      totalTeamups++;
      if (KOREAN_REGEX.test(tu.loadout_name) || JAPANESE_REGEX.test(tu.loadout_name)) {
        reportError(`${heroName} teamup '${tu.loadout_name}' name must remain in English.`);
      }
      if (tu.tier === 'enhanced' && (!tu.partner_name || !tu.partner_name.en)) {
        reportWarning(`${heroName} enhanced teamup '${tu.name}' is missing partner_name.en.`);
      }
      if (/Base Effect\s*:/i.test(tu.description || '') && /Enhanced Effect\s*:/i.test(tu.description || '')) {
        reportError(`${heroName} teamup '${tu.name}' (${tu.tier}) has unsplit combined English description.`);
      }

      const dt = tu.description_trans;
      if (dt && dt.ko && dt.ja) {
        if (dt.ko === tu.description || dt.ja === tu.description) {
          fallbackTeamups++;
        } else {
          translatedTeamups++;
        }
        if (JAPANESE_REGEX.test(dt.ko)) reportError(`${heroName} teamup '${tu.name}' KO contains Japanese Kana.`);
        if (KOREAN_REGEX.test(dt.ja)) reportError(`${heroName} teamup '${tu.name}' JA contains Korean Hangul.`);
      } else if (tu.description) {
        reportWarning(`${heroName} teamup '${tu.name}' missing description_trans.`);
        fallbackTeamups++;
      }

      checkStats(tu.stats, `teamup ${tu.name}`);
    });
  });

  console.log(`✓ Skills (incl. upgrades): ${translatedSkills} native + ${fallbackSkills} fallback / ${totalSkills} total (${((translatedSkills / totalSkills) * 100).toFixed(1)}% native)`);
  console.log(`✓ Team-Ups: ${translatedTeamups} native + ${fallbackTeamups} fallback / ${totalTeamups} total (${((translatedTeamups / totalTeamups) * 100).toFixed(1)}% native)`);
  console.log(`✓ Stat Labels (Skills + Team-Ups): ${translatedStatLabels} / ${totalStatLabels} (${((translatedStatLabels / totalStatLabels) * 100).toFixed(1)}%)`);
  console.log(`✓ Stat Values (Skills + Team-Ups): ${translatedStatValues} / ${totalStatValues} (${((translatedStatValues / totalStatValues) * 100).toFixed(1)}%)`);
}

console.log('--------------------------------------------------');
if (errorCount === 0) {
  if (warningCount > 0) {
    console.log(`⚠️ VALIDATION PASSED WITH ${warningCount} WARNING(S).`);
  } else {
    console.log('🎉 ALL VALIDATION CHECKS PASSED PERFECTLY (0 errors, 0 warnings)!');
  }
  process.exit(0);
} else {
  console.error(`❌ VALIDATION FAILED WITH ${errorCount} HARD ERROR(S)!`);
  process.exit(1);
}
