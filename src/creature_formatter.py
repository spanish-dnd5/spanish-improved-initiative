import time
from typing import Dict


def construct_actions(array, subtype):
    result = []
    for element in array:
        name = element['name'].replace('espacio', 'slot')
        description = element['description']
        if subtype in element:
            description += '\n'
            for subelement in element[subtype]:
                description += f"\n• {subelement['name'].replace('espacio', 'slot')}: {subelement['description']}"
        result.append({'Name': name, 'Content': description, 'Usage': ''})
    return result


def format_monster(m: Dict):
    armor_class_notes_array = []
    armor_class_notes = ""

    if 'type' in m['armor_class'][0]:
        armor_class_notes_array.append(m['armor_class'][0]['type'])
    if len(m['armor_class']) > 1:
        for ac in m['armor_class']:
            ac_string = f"{ac['amount']} {ac['condition']}"
            if 'type' in ac:
                ac_string += f" ({ac['type']})"
            armor_class_notes_array.append(ac_string)
        armor_class_notes = f"({', '.join(armor_class_notes_array)})"

    legendary_actions = []
    if 'list' in m['legendary_actions']:
        legendary_actions = m['legendary_actions']['list']

    tags = f" ({', '.join(m['tags'])})" if m['tags'] else ""
    _, link = m['source'].split(':', 1)
    return {
        f"Creatures.{m['index']}": {
            "Id":
            m['index'],
            "Name":
            m['name'],
            "Path":
            "Spanish SDR",
            "Source":
            "http://srd.nosolorol.com/DD5/",
            "Type":
            f"{m['size']} {m['type']}{tags}, {m['alignment']}",
            "HP": {
                "Value": m['hit_points'],
                "Notes": f"({m['hit_dice']})"
            },
            "AC": {
                "Value": m['armor_class'][0]['amount'],
                "Notes": armor_class_notes
            },
            "InitiativeModifier":
            m['initiative'],
            "InitiativeAdvantage":
            False,
            "Speed":
            [f"{type_} {amount}" for type_, amount in m['speed'].items()],
            "Abilities": {
                "Str": m['abilities']['strength'],
                "Dex": m['abilities']['dexterity'],
                "Con": m['abilities']['constitution'],
                "Int": m['abilities']['intelligence'],
                "Wis": m['abilities']['wisdom'],
                "Cha": m['abilities']['charisma']
            },
            "DamageVulnerabilities":
            m['damage_vulnerabilities'],
            "DamageResistances":
            m['damage_resistances'],
            "DamageImmunities":
            m['damage_immunities'],
            "ConditionImmunities":
            m['condition_immunities'],
            "Saves": [{
                "Name": save,
                "Modifier": value
            } for save, value in m['saving_throws'].items()],
            "Skills": [{
                "Name": skill,
                "Modifier": value
            } for skill, value in m['skills'].items()],
            "Senses":
            m['senses'],
            "Languages":
            m['languages'],
            "Challenge":
            m['challenge_rating'],
            "Traits":
            construct_actions(m['special_abilities'], 'spells'),
            "Actions":
            construct_actions(m['actions'], 'extra'),
            "Reactions":
            construct_actions(m['reactions'], 'extra'),
            "LegendaryActions":
            construct_actions(legendary_actions, 'extra'),
            "Description":
            f"{m['description']}\n\n{link}",
            "Player":
            "",
            "Version":
            "2.16.0",
            "ImageURL":
            "",
            "LastUpdateMs":
            int(round(time.time() * 1000))
        }
    }