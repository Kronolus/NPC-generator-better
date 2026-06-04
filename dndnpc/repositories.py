import json
from .models import Race, City, NPC, NPCHistory
from .utils import to_json, safe_json_list
from .data import RACE_PRESETS, CITY_PRESETS

def add_race(session, name, description="", traits=None, templates=None, samples=None, rules=None):
    race = Race(
        name=name,
        description=description,
        traits=to_json(traits or []),
        name_templates=to_json(templates or []),
        sample_names=to_json(samples or []),
        name_rules=to_json(rules or {}),
    )
    session.add(race)
    session.commit()
    return race

def add_city(session, name, region="", atmosphere="", danger_level="", notes="", demographics=None):
    city = City(
        name=name,
        region=region,
        atmosphere=atmosphere,
        danger_level=danger_level,
        notes=notes,
        demographics=to_json(demographics or []),
    )
    session.add(city)
    session.commit()
    return city

def ensure_sample_data(session):
    if session.query(Race).count() == 0:
        for name, data in RACE_PRESETS.items():
            add_race(
                session,
                name=name,
                description=data["description"],
                traits=data["traits"],
                templates=data["templates"],
                samples=data["samples"],
                rules=data.get("rules", {}),
            )
    if session.query(City).count() == 0:
        for city in CITY_PRESETS:
            add_city(session, **city)

def npc_to_dict(n):
    return {
        "id": n.id,
        "name": n.name,
        "race": n.race,
        "city": n.city,
        "age": n.age,
        "gender": n.gender,
        "role": n.role,
        "profession": n.profession,
        "social_class": n.social_class,
        "alignment": n.alignment,
        "personality": n.personality,
        "appearance": n.appearance,
        "voice": n.voice,
        "motivation": n.motivation,
        "secret": n.secret,
        "fear": n.fear,
        "flaw": n.flaw,
        "rumor": n.rumor,
        "quest_hook": n.quest_hook,
        "useful_info": n.useful_info,
        "combat_role": n.combat_role,
        "stat_hint": n.stat_hint,
        "inventory": n.inventory,
        "relationships": safe_json_list(n.relationships),
        "tags": safe_json_list(n.tags),
        "dm_notes": n.dm_notes,
        "seed": n.seed,
    }

def save_generated_npcs(session, npc_dicts):
    saved = []
    for d in npc_dicts:
        npc = NPC(
            name=d["name"], race=d.get("race"), city=d.get("city"), age=d.get("age"), gender=d.get("gender"),
            role=d.get("role"), profession=d.get("profession"), social_class=d.get("social_class"), alignment=d.get("alignment"),
            personality=d.get("personality"), appearance=d.get("appearance"), voice=d.get("voice"), motivation=d.get("motivation"),
            secret=d.get("secret"), fear=d.get("fear"), flaw=d.get("flaw"), rumor=d.get("rumor"), quest_hook=d.get("quest_hook"),
            useful_info=d.get("useful_info"), combat_role=d.get("combat_role"), stat_hint=d.get("stat_hint"), inventory=d.get("inventory"),
            relationships=to_json(d.get("relationships", [])), tags=to_json(d.get("tags", [])), dm_notes=d.get("dm_notes", ""), seed=d.get("seed"),
        )
        session.add(npc)
        session.flush()
        snap = npc_to_dict(npc)
        session.add(NPCHistory(npc_id=npc.id, snapshot=json.dumps(snap, ensure_ascii=False)))
        saved.append(npc)
    session.commit()
    return saved
