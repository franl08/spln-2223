import re
import json

concepts = {}
concepts["complete_entries"] = []
concepts["remissive_entries"] = []


def getCE_index(header_match):
    if header_match:
        return header_match.split(";")[0]


def getCE_name(header_match):
    if header_match:
        return header_match.split(";")[1]


def getCE_gender(header_match):
    if header_match:
        return header_match.split(";")[2]


def getCE_areas(areas_match):
    if areas_match:
        return areas_match.split(";")[:-1]
    else:
        return []


def getCE_syn(syn_match):
    if syn_match:
        return syn_match.split(";")
    else:
        return []


def getCE_vars(vars_match):
    if vars_match:
        return vars_match.split(";")
    else:
        return []


def getCE_translations(translations_match):
    if translations_match:
        return translations_match.split(";")
    else:
        return []


def getCE_note(note_match):
    return note_match


def fill_struct(content):
    global concepts
    complete_entrie = r'###IDENT (?P<header>.*)\n###AR (?P<areas>.*)\n(?:###SIN (?P<syn>.*)\n)?(?:###VAR (?P<var>.*)\n)?(###LANG es (?P<es>.*)\n)?(###LANG en (?P<en>.*)\n)?(###LANG pt (?P<pt>.*)\n)?(###LANG la (?P<la>.*)\n)?(###NOTE (?P<note>.*)\n)?'
    remissive_entrie = r'###REM (?P<rem>.*)\n###HREF (?P<red>.*)'

    for ec in re.finditer(complete_entrie, content):
        obj_ce = {}

        obj_ce["index"] = getCE_index(ec.groupdict()["header"])
        obj_ce["name"] = getCE_name(ec.groupdict()["header"])
        obj_ce["gender"] = getCE_gender(ec.groupdict()["header"])
        obj_ce["synonym"] = getCE_syn(ec.groupdict()["syn"])
        obj_ce["vars"] = getCE_vars(ec.groupdict()["var"])
        obj_ce["translations"] = {}
        obj_ce["translations"]["es"] = getCE_translations(ec.groupdict()["es"])
        obj_ce["translations"]["en"] = getCE_translations(ec.groupdict()["en"])
        obj_ce["translations"]["pt"] = getCE_translations(ec.groupdict()["pt"])
        obj_ce["translations"]["la"] = getCE_translations(ec.groupdict()["la"])
        obj_ce["note"] = getCE_note(ec.groupdict()["note"])

        concepts["complete_entries"].append(obj_ce)

    for er in re.finditer(remissive_entrie, content):
        er_obj = {}

        er_obj["name"] = er.groupdict()["rem"]
        er_obj["href"] = er.groupdict()["red"]

        concepts["remissive_entries"].append(er_obj)

    return concepts


content = open("output.txt", "r").read()
concepts = fill_struct(content)

with open("output.json", "w") as output_file:
    json.dump(concepts, output_file)
