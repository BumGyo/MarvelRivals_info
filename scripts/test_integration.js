const fs = require('fs');

// Check JSON syntax
const heroes = JSON.parse(fs.readFileSync('data/heroes.json', 'utf8'));
const i18n = JSON.parse(fs.readFileSync('data/i18n.json', 'utf8'));

console.log('JSON files read successfully.');
console.log(`Heroes count: ${heroes.length}`);
console.log(`i18n keys: ${Object.keys(i18n).join(', ')}`);

// Verify HTML contains required IDs
const html = fs.readFileSync('index.html', 'utf8');
const requiredIds = [
  'main-header', 'hero-search-input', 'lang-switcher', 'lang-btn-ko', 'lang-btn-ja', 'lang-btn-en',
  'role-filters', 'filter-all', 'filter-vanguard', 'filter-duelist', 'filter-strategist',
  'heroes-count', 'hero-grid', 'hero-modal', 'modal-container', 'modal-hero-avatar', 'modal-hero-name',
  'modal-hero-subname', 'modal-base-stats', 'modal-close-btn', 'tab-btn-skills', 'tab-btn-teamups',
  'view-skills', 'view-teamups', 'skill-selector-list', 'skill-detail-display', 'loadout-selector', 'teamup-columns'
];

let missingIds = [];
for (const id of requiredIds) {
  if (!html.includes(`id="${id}"`)) {
    missingIds.push(id);
  }
}

if (missingIds.length > 0) {
  console.error('Missing IDs in HTML:', missingIds);
  process.exit(1);
} else {
  console.log(`All ${requiredIds.length} required interactive element IDs verified in index.html!`);
}

// Verify app.js syntax
try {
  const appCode = fs.readFileSync('app.js', 'utf8');
  new Function(appCode); // Test syntax
  console.log('app.js syntax is valid!');
} catch (e) {
  console.error('app.js syntax error:', e);
  process.exit(1);
}

console.log('\n[SUCCESS] All frontend code and asset integrity checks PASSED!');
