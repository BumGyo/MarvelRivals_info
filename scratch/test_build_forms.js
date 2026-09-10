const fs = require('fs');

const heroes = JSON.parse(fs.readFileSync('data/heroes.json', 'utf8'));

// Helper to filter skills by form_index or name patterns
function setupForms() {
  heroes.forEach(h => {
    const hName = (h.names?.en || h.name || '').toUpperCase();

    // 1. HULK
    if (hName === 'HULK') {
      const bannerSkills = h.skills.filter(s => s.form_index === 0 || ['Gamma Ray Gun', 'Puny Banner', 'Gamma Grenade'].includes(s.name) || (s.name === 'Gamma Boost' && s.key === 'Passive'));
      const heroHulkSkills = h.skills.filter(s => s.form_index === 1 || ['HULK SMASH!', 'Indestructible Guard'].includes(s.name));
      const monsterHulkSkills = h.skills.filter(s => s.form_index === 2 || ['World Breaker'].includes(s.name));

      h.forms = [
        {
          form_id: 0,
          name: "Bruce Banner",
          names: { en: "Bruce Banner", ko: "브루스 배너", ja: "ブルース・バナー" },
          avatar: "https://r.res.easebar.com/pic/20241120/fe9396f7-755b-4888-a2d1-57a4d446f627.png",
          base_stats: { Health: "200", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
          skills: bannerSkills.length > 0 ? bannerSkills : h.skills.slice(0, 4)
        },
        {
          form_id: 1,
          name: "Hero Hulk",
          names: { en: "Hero Hulk", ko: "히어로 헐크", ja: "ヒーロー・ハルク" },
          avatar: "https://r.res.easebar.com/pic/20241120/f4e72b0d-bc2a-45cc-ab88-d1ec6fcf5c34.png",
          base_stats: { Health: "400+300 Regenerative Shield", "Movement Speed": "6.5 m/s", "Movement Mode": "Ground" },
          skills: heroHulkSkills.length > 0 ? heroHulkSkills : h.skills.slice(4, 12)
        },
        {
          form_id: 2,
          name: "Monster Hulk",
          names: { en: "Monster Hulk", ko: "몬스터 헐크", ja: "モンスター・ハルク" },
          avatar: "https://r.res.easebar.com/pic/20241120/c73a87ed-c216-4378-9eb6-214c45b9057d.png",
          base_stats: { Health: "1400", "Movement Speed": "6.5 m/s", "Movement Mode": "Ground" },
          skills: monsterHulkSkills.length > 0 ? monsterHulkSkills : h.skills.slice(12, 19)
        }
      ];
      console.log(`✓ Configured HULK forms: ${h.forms.map(f => `${f.name} (${f.skills.length} skills)`).join(', ')}`);
    }

    // 2. BLACK CAT
    if (hName === 'BLACK CAT') {
      const clawSkills = h.skills.filter(s => s.form_index === 0 || ['FELINE FURY', 'TURN OF FORTUNE'].includes(s.name));
      const whipSkills = h.skills.filter(s => s.form_index === 1 || ['CLAW WHIP', 'PHANTOM PURSUIT'].includes(s.name));
      const dealSkills = h.skills.filter(s => s.form_index === 2 || ['GILDED DEAL', 'TABLET OF DESTINIES', 'HELM OF HADES', 'FALTINE FLAME ORB', 'CHERNOBOG\'S CRYSTAL', 'RING OF ZONA', 'MENTO-FISH', 'STICKY PAWS'].includes(s.name));

      h.forms = [
        {
          form_id: 0,
          name: "Claw Stance",
          names: { en: "Claw Stance", ko: "클로 폼 (근접)", ja: "クローフォーム (近接)" },
          avatar: "https://r.res.easebar.com/pic/20260416/13a9a895-86b0-43fd-b182-2c230d38a61f.png",
          base_stats: { Health: "150+125 Regenerative Shield", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
          skills: clawSkills.length > 0 ? clawSkills : h.skills.slice(0, 9)
        },
        {
          form_id: 1,
          name: "Whip Stance",
          names: { en: "Whip Stance", ko: "채찍 폼 (중거리)", ja: "ウィップフォーム (中距離)" },
          avatar: "https://r.res.easebar.com/pic/20260416/8fc39281-1c61-4d51-8d09-a3bbd62be2ac.png",
          base_stats: { Health: "275", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
          skills: whipSkills.length > 0 ? whipSkills : h.skills.slice(9, 18)
        },
        {
          form_id: 2,
          name: "Gilded Deal",
          names: { en: "Gilded Deal", ko: "내부자 거래 (암시장)", ja: "インサイダー取引 (闇市)" },
          avatar: "https://r.res.easebar.com/pic/20260416/b88fc77d-3b5e-4802-87de-6c38485e32c1.png",
          base_stats: { Health: "275", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
          skills: dealSkills.length > 0 ? dealSkills : h.skills.slice(18, 26)
        }
      ];
      console.log(`✓ Configured BLACK CAT forms: ${h.forms.map(f => `${f.name} (${f.skills.length} skills)`).join(', ')}`);
    }

    // 3. MAGIK
    if (hName === 'MAGIK') {
      const normalSkills = h.skills.filter(s => s.form_index === 0 || ['Darkchild', 'Limbo\'s Might', 'CHAIN OF CYTTORAK'].includes(s.name));
      const darkchildSkills = h.skills.filter(s => s.form_index === 1);

      h.forms = [
        {
          form_id: 0,
          name: "Magik",
          names: { en: "Magik", ko: "일반 매직", ja: "通常マジック" },
          avatar: "https://r.res.easebar.com/pic/20241120/8bb769e4-de61-4d45-8dfc-690bbb5783ec.png",
          base_stats: { Health: "250", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
          skills: normalSkills.length > 0 ? normalSkills : h.skills.slice(0, 9)
        },
        {
          form_id: 1,
          name: "Darkchild",
          names: { en: "Darkchild", ko: "다크차일드 폼", ja: "ダークチャイルド" },
          avatar: "https://r.res.easebar.com/pic/20241120/056e2ca6-f3c3-41f7-8b84-cf36fced9610.png",
          base_stats: { Health: "250+150 Regenerative Shield", "Movement Speed": "6.5 m/s", "Movement Mode": "Ground" },
          skills: darkchildSkills.length > 0 ? darkchildSkills : h.skills.slice(9, 15)
        }
      ];
      console.log(`✓ Configured MAGIK forms: ${h.forms.map(f => `${f.name} (${f.skills.length} skills)`).join(', ')}`);
    }

    // 4. CLOAK & DAGGER
    if (hName.includes('CLOAK') && hName.includes('DAGGER')) {
      const cloakSkills = h.skills.filter(s => s.form_index === 0 || ['Darkforce Cloak', 'Terror Cape', 'Dark Teleportation', 'FROM SHADOW TO LIGHT'].includes(s.name));
      const daggerSkills = h.skills.filter(s => s.form_index === 1 || ['Lightforce Dagger', 'Shadow\'s Embrace', 'Veil of Lightforce', 'Dagger Storm'].includes(s.name));

      h.forms = [
        {
          form_id: 0,
          name: "Cloak",
          names: { en: "Cloak", ko: "클록", ja: "クローク" },
          avatar: "https://r.res.easebar.com/pic/20241205/87c86614-9f25-4e0e-a941-7a22ebb2b737.png",
          base_stats: { Health: "250", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
          skills: cloakSkills.length > 0 ? cloakSkills : h.skills.slice(0, 6)
        },
        {
          form_id: 1,
          name: "Dagger",
          names: { en: "Dagger", ko: "대거", ja: "ダガー" },
          avatar: "https://r.res.easebar.com/pic/20241205/6d081eaf-a0e3-4558-9d04-f7039010b141.png",
          base_stats: { Health: "250", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
          skills: daggerSkills.length > 0 ? daggerSkills : h.skills.slice(6, 11)
        }
      ];
      console.log(`✓ Configured CLOAK & DAGGER forms: ${h.forms.map(f => `${f.name} (${f.skills.length} skills)`).join(', ')}`);
    }

    // 5. GAMBIT
    if (hName === 'GAMBIT') {
      const normalSkills = h.skills.filter(s => s.form_index === 0 || ['Kinetic Cards', 'Ragin\' Royal Flush', 'Cajun Charge', 'Healing Hearts', 'Breaking Spades', 'Bayou Bash', 'ACE OF ACES'].includes(s.name));
      const chargedSkills = h.skills.filter(s => s.form_index === 1 || ['Bridge Boost', 'Purifying Pick-Up', 'Explosive Trick', 'Bidding Barrage'].includes(s.name));

      h.forms = [
        {
          form_id: 0,
          name: "Normal Stance",
          names: { en: "Normal Stance", ko: "기본 폼", ja: "通常フォーム" },
          avatar: "https://r.res.easebar.com/pic/20251114/699f5ef7-0710-4406-a53d-c3aaf8081992.png",
          base_stats: { Health: "250", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
          skills: normalSkills.length > 0 ? normalSkills : h.skills.slice(0, 7)
        },
        {
          form_id: 1,
          name: "Charged Cards",
          names: { en: "Charged Cards", ko: "강화 카드 폼", ja: "チャージカード" },
          avatar: "https://r.res.easebar.com/pic/20251114/a7d8e207-6f08-4d65-a665-db58aaef61ac.png",
          base_stats: { Health: "250", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
          skills: chargedSkills.length > 0 ? chargedSkills : h.skills.slice(7, 11)
        }
      ];
      console.log(`✓ Configured GAMBIT forms: ${h.forms.map(f => `${f.name} (${f.skills.length} skills)`).join(', ')}`);
    }

    // 6. WHITE FOX
    if (hName === 'WHITE FOX') {
      const humanSkills = h.skills.filter(s => s.form_index === 0 || ['YEOWOO GUSEUL', 'CLAW STRIKE', 'SPECTRAL SURGE', 'FOX FORM AWAKENING', 'SPIRIT SANCTUARY', 'TAIL SWEEP', 'Predatory Pounce', 'KUMIHO UNLEASHED', 'SPIRIT FOX WARD', 'NINE-TAILED AURA'].includes(s.name));
      const foxSkills = h.skills.filter(s => s.form_index === 1 || ['NINEFOLD SLAM', 'BLESSED BY THE NINE'].includes(s.name));

      h.forms = [
        {
          form_id: 0,
          name: "Human Form",
          names: { en: "Human Form", ko: "인간 형태", ja: "人間形態" },
          avatar: "https://r.res.easebar.com/pic/20260320/324b74e9-9ee9-4281-a5a1-913452f72d63.png",
          base_stats: { Health: "250", "Movement Speed": "6 m/s", "Movement Mode": "Ground" },
          skills: humanSkills.length > 0 ? humanSkills : h.skills.slice(0, 10)
        },
        {
          form_id: 1,
          name: "Kumiho Form",
          names: { en: "Kumiho Form", ko: "구미호 폼", ja: "九尾の狐" },
          avatar: "https://r.res.easebar.com/pic/20260320/357ab606-04f9-485c-8edf-3ad2a6adb74f.png",
          base_stats: { Health: "250", "Movement Speed": "6.5 m/s", "Movement Mode": "Ground" },
          skills: foxSkills.length > 0 ? foxSkills : h.skills.slice(10, 12)
        }
      ];
      console.log(`✓ Configured WHITE FOX forms: ${h.forms.map(f => `${f.name} (${f.skills.length} skills)`).join(', ')}`);
    }
  });
}

setupForms();
