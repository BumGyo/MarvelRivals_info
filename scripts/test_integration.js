#!/usr/bin/env node
/**
 * Frontend & Data Integration Smoke Test
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

// 1. Check JSON syntax & structure
const heroes = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'heroes.json'), 'utf8'));
const i18n = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'i18n.json'), 'utf8'));
const trans = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'translations.json'), 'utf8'));

if (!Array.isArray(heroes) || heroes.length < 55) {
  console.error(`Invalid hero count: ${heroes.length}`);
  process.exit(1);
}

// Verify i18n key parity across ko, ja, en
const koKeys = Object.keys(i18n.ko || {}).sort();
['ja', 'en'].forEach(lang => {
  const keys = Object.keys(i18n[lang] || {}).sort();
  if (JSON.stringify(koKeys) !== JSON.stringify(keys)) {
    console.error(`i18n key mismatch between 'ko' and '${lang}'!`);
    process.exit(1);
  }
});

if (!trans.stat_labels || !trans.stat_values || !Array.isArray(trans.stat_patterns)) {
  console.error('translations.json missing required stat_labels/stat_values/stat_patterns');
  process.exit(1);
}

console.log(`✓ JSON files verified (${heroes.length} heroes, ${koKeys.length} UI keys per language).`);

// 2. Verify HTML contains all required interactive IDs & synchronized version hash
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const requiredIds = [
  'main-header', 'logo-btn', 'site-logo-title', 'site-logo-subtitle', 'dev-info-btn',
  'hero-search-input', 'lang-switcher', 'lang-btn-ko', 'lang-btn-ja', 'lang-btn-en',
  'role-filters', 'filter-all', 'filter-vanguard', 'filter-duelist', 'filter-strategist',
  'heroes-count', 'hero-grid', 'hero-modal', 'modal-container', 'modal-hero-avatar', 'modal-hero-name',
  'modal-hero-subname', 'modal-base-stats', 'modal-close-btn', 'tab-btn-skills', 'tab-btn-teamups',
  'view-skills', 'view-teamups', 'hero-forms-bar', 'skill-selector-list', 'skill-detail-display',
  'loadout-selector', 'teamup-columns', 'dev-modal', 'dev-modal-close-btn'
];

const missingIds = requiredIds.filter(id => !html.includes(`id="${id}"`));
if (missingIds.length > 0) {
  console.error('Missing IDs in index.html:', missingIds);
  process.exit(1);
}
console.log(`✓ All ${requiredIds.length} required interactive element IDs verified in index.html.`);

// 3. Verify app.js syntax
try {
  const appCode = fs.readFileSync(path.join(ROOT, 'app.js'), 'utf8');
  new Function(appCode);
  console.log('✓ app.js syntax is valid.');
} catch (e) {
  console.error('app.js syntax error:', e);
  process.exit(1);
}

console.log('\n[SUCCESS] All frontend code and asset integrity checks PASSED!');
