const fs = require('fs');
const assert = require('assert');

const heroes = JSON.parse(fs.readFileSync('data/heroes.json', 'utf8'));

const multiFormHeroes = [
  { id: '1011', name: 'Hulk', expectedForms: 3 },
  { id: '1027', name: 'Black Cat', expectedForms: 3 },
  { id: '1029', name: 'Magik', expectedForms: 2 },
  { id: '1046', name: 'Cloak & Dagger', expectedForms: 2 },
  { id: '1047', name: 'Gambit', expectedForms: 2 },
  { id: '1058', name: 'White Fox', expectedForms: 2 }
];

console.log('=== MULTI-FORM VERIFICATION TEST ===\n');

for (const exp of multiFormHeroes) {
  const hero = heroes.find(h => h.id === exp.id || (h.names?.en || '').toUpperCase() === exp.name.toUpperCase());
  assert(hero, `Hero ${exp.name} (${exp.id}) not found!`);
  assert(Array.isArray(hero.forms), `Hero ${exp.name} does not have forms array!`);
  assert.strictEqual(hero.forms.length, exp.expectedForms, `Hero ${exp.name} form count mismatch: got ${hero.forms.length}, expected ${exp.expectedForms}`);

  console.log(`✓ Hero: ${exp.name} (${hero.names.ko} / ${hero.names.ja}) - ${hero.forms.length} forms`);

  hero.forms.forEach((form, idx) => {
    assert(form.names.ko && form.names.en && form.names.ja, `Form ${idx} missing localized names!`);
    assert(form.avatar && form.avatar.startsWith('http'), `Form ${idx} invalid avatar: ${form.avatar}`);
    assert(form.base_stats?.Health, `Form ${idx} missing Health stat!`);
    assert(form.base_stats?.['Movement Speed'], `Form ${idx} missing Movement Speed stat!`);
    assert(Array.isArray(form.skills) && form.skills.length > 0, `Form ${idx} has empty skills!`);

    // Check for duplicate skills within form
    const skillNames = form.skills.map(s => s.name);
    const uniqueSkillNames = new Set(skillNames);
    assert.strictEqual(skillNames.length, uniqueSkillNames.size, `Hero ${exp.name} Form ${form.names.en} contains duplicate skills: ${skillNames.join(', ')}`);

    // Verify translations exist
    for (const skill of form.skills) {
      assert(skill.description_trans?.ko, `Skill ${skill.name} missing KO trans in ${exp.name} form ${form.names.en}`);
      assert(skill.description_trans?.ja, `Skill ${skill.name} missing JA trans in ${exp.name} form ${form.names.en}`);
    }

    console.log(`    Form [${idx}]: "${form.names.ko}" / "${form.names.ja}" (${form.names.en}) | HP: ${form.base_stats.Health} | Speed: ${form.base_stats['Movement Speed']} | Skills: ${form.skills.length} skills (NO duplicates)`);
  });
  console.log('');
}

console.log('🎉 ALL MULTI-FORM HEROES AND FORMS VERIFIED SUCCESSFULLY WITH ZERO DUPLICATES!');
