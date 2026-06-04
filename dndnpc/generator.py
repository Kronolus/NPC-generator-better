import json
import random
from .models import NPC
from .names import SmartNameGenerator
from .utils import safe_json_list
from .data import (
    PROFESSIONS, ROLES, GENDERS, SOCIAL_CLASSES, ALIGNMENTS, PERSONALITIES,
    MOTIVATIONS, SECRETS, FEARS, FLAWS, RUMORS, QUEST_HOOKS, USEFUL_INFO,
    COMBAT_ROLES, STAT_HINTS, INVENTORY, VOICES, APPEARANCE,
)

def weighted_choice(items, rng):
    total = sum(max(0, w) for _, w in items)
    if total <= 0:
        return items[0][0]
    roll = rng.random() * total
    upto = 0
    for item, weight in items:
        upto += max(0, weight)
        if upto >= roll:
            return item
    return items[-1][0]

def age_for_race(race_name, rng):
    if race_name == "Elf":
        return rng.randint(80, 650)
    if race_name == "Dwarf":
        return rng.randint(40, 280)
    if race_name == "Goblin":
        return rng.randint(10, 45)
    if race_name == "Kobold":
        return rng.randint(8, 60)
    return rng.randint(16, 90)

def generate_appearance(rng, age):
    mark = rng.choice(APPEARANCE["mark"]) if rng.random() < 0.65 else "bez výrazné jizvy"
    return (
        f"Je kolem {age} let. Má {rng.choice(APPEARANCE['build'])} a je {rng.choice(APPEARANCE['height'])}. "
        f"Má {rng.choice(APPEARANCE['hair_color'])} {rng.choice(APPEARANCE['hair'])}. "
        f"Oči: {rng.choice(APPEARANCE['eyes'])}. "
        f"Nosí {rng.choice(APPEARANCE['clothing'])}. "
        f"Zvláštnost: {mark}."
    )

def make_tags(npc):
    tags = [npc["role"], npc["profession"], npc["social_class"]]
    if "zlo" in npc["alignment"]:
        tags.append("nebezpečný")
    if npc.get("secret"):
        tags.append("má tajemství")
    if npc.get("quest_hook"):
        tags.append("quest")
    return list(dict.fromkeys(tags))

def add_relationships(session, rng, created, chance):
    relation_types = ["přítel", "nepřítel", "dlužník", "věřitel", "sourozenec", "bývalý mentor", "tajný kontakt", "rival"]
    existing = [row.name for row in session.query(NPC).limit(300).all()]
    for npc in created:
        if rng.random() > chance:
            continue
        targets = [n["name"] for n in created if n["name"] != npc["name"]] + existing
        if targets:
            npc["relationships"].append({"type": rng.choice(relation_types), "target": rng.choice(targets)})

def generate_npcs(session, city, races_map, count, seed="", name_style="smart", relation_chance=0.2, allow_dark_secrets=True, full_names=True):
    rng = random.Random(seed or None)
    name_gen = SmartNameGenerator(rng)
    created = []

    try:
        raw_demographics = json.loads(city.demographics or "[]")
    except Exception:
        raw_demographics = []

    demographics = []
    for item in raw_demographics:
        try:
            demographics.append((item.get("race"), float(item.get("weight", 1))))
        except Exception:
            demographics.append((item.get("race"), 1.0))

    if not demographics:
        demographics = [(r.name, 1) for r in races_map.values()]

    for _ in range(count):
        race_name = weighted_choice(demographics, rng)
        race_obj = races_map.get(race_name)
        age = age_for_race(race_name, rng)
        npc = {
            "name": name_gen.generate(race_obj, style=name_style, full_name=full_names),
            "race": race_name,
            "city": city.name,
            "age": age,
            "gender": rng.choice(GENDERS),
            "role": rng.choice(ROLES),
            "profession": rng.choice(PROFESSIONS),
            "social_class": rng.choice(SOCIAL_CLASSES),
            "alignment": rng.choice(ALIGNMENTS),
            "personality": rng.choice(PERSONALITIES),
            "appearance": generate_appearance(rng, age),
            "voice": rng.choice(VOICES),
            "motivation": rng.choice(MOTIVATIONS),
            "secret": rng.choice(SECRETS) if allow_dark_secrets or rng.random() < 0.45 else "",
            "fear": rng.choice(FEARS),
            "flaw": rng.choice(FLAWS),
            "rumor": rng.choice(RUMORS),
            "quest_hook": rng.choice(QUEST_HOOKS) if rng.random() < 0.65 else "",
            "useful_info": rng.choice(USEFUL_INFO),
            "combat_role": rng.choice(COMBAT_ROLES),
            "stat_hint": rng.choice(STAT_HINTS),
            "inventory": rng.choice(INVENTORY),
            "relationships": [],
            "tags": [],
            "dm_notes": "",
            "seed": str(seed) if seed else "",
        }
        npc["tags"] = make_tags(npc)
        created.append(npc)

    add_relationships(session, rng, created, relation_chance)
    return created

def format_profile(npc):
    relationships = npc.get("relationships", [])
    rel_text = "Žádné" if not relationships else "\n".join([f"- {r.get('type')}: {r.get('target')}" for r in relationships])
    tags = ", ".join(npc.get("tags", [])) if isinstance(npc.get("tags"), list) else npc.get("tags", "")
    return f"""# {npc.get('name')}

Základ:
- Rasa: {npc.get('race')}
- Město: {npc.get('city')}
- Věk: {npc.get('age')}
- Pohlaví: {npc.get('gender')}
- Role v příběhu: {npc.get('role')}
- Profese: {npc.get('profession')}
- Společenská vrstva: {npc.get('social_class')}
- Přesvědčení: {npc.get('alignment')}

Vzhled:
{npc.get('appearance')}

Hlas a hraní:
- Hlas: {npc.get('voice')}
- Osobnost: {npc.get('personality')}
- Motivace: {npc.get('motivation')}
- Strach: {npc.get('fear')}
- Slabina: {npc.get('flaw')}

Tajemství a drby:
- Tajemství: {npc.get('secret') or 'Žádné zjevné'}
- Drb: {npc.get('rumor')}
- Užitečná informace: {npc.get('useful_info')}

Quest:
{npc.get('quest_hook') or 'Bez hlavního questu. Může sloužit jako běžné městské NPC.'}

Herní použití:
- Bojová role: {npc.get('combat_role')}
- Stat hint: {npc.get('stat_hint')}
- Inventář: {npc.get('inventory')}
- Tagy: {tags}

Vztahy:
{rel_text}

DM poznámky:
{npc.get('dm_notes') or ''}
"""
