import json

with open("data/heroes.json") as f:
    heroes = json.load(f)

print(f"Total heroes: {len(heroes)}")
assert len(heroes) == 53, "Expected 53 heroes"

for h in heroes:
    assert h["id"], f"Hero missing ID: {h}"
    assert h["name"], f"Hero missing Name: {h}"
    assert "ko" in h["names"] and "ja" in h["names"] and "en" in h["names"], f"Missing translations for {h['name']}"
    valid_roles = ["VANGUARD", "DUELIST", "STRATEGIST", "ALL-ROUNDER"]
    assert h["role"] in valid_roles, f"Invalid role {h['role']} for {h['name']}"
    assert h["base_stats"], f"Missing base_stats for {h['name']}"
    assert h["base_stats"].get("Health") and h["base_stats"]["Health"] != "N/A", f"Missing Health for {h['name']}"
    assert h["base_stats"].get("Movement Speed") and h["base_stats"]["Movement Speed"] != "N/A", f"Missing Movement Speed for {h['name']}"

print("All 53 heroes data schema, base_stats, and multilingual mappings validated successfully!")

# Check specific hero: Iron Man
im = next(h for h in heroes if h["name"] == "IRON MAN")
print("\n--- IRON MAN VERIFICATION ---")
print("KO:", im["names"]["ko"], "| JA:", im["names"]["ja"], "| Role:", im["role"])
print("Skills count:", len(im["skills"]))
print("Sample Skill:", im["skills"][0]["name"], "Key:", im["skills"][0]["key"], "Stats:", im["skills"][0]["stats"])
print("Team-Ups count:", len(im["teamups"]))
for tu in im["teamups"]:
    print(" -> Loadout:", tu["loadout_number"], "| Tier:", tu["tier"], "| Name:", tu["name"], "| Stats:", tu["stats"])

# Check specific hero: Jubilation Lee
jubilee = next(h for h in heroes if h["name"] == "Jubilation Lee")
print("\n--- JUBILATION LEE VERIFICATION ---")
print("KO:", jubilee["names"]["ko"], "| JA:", jubilee["names"]["ja"], "| Role:", jubilee["role"])
print("Team-Ups count:", len(jubilee["teamups"]))
for tu in jubilee["teamups"]:
    print(" -> Loadout:", tu["loadout_number"], "| Tier:", tu["tier"], "| Name:", tu["name"])
