import re
import json


def remove_header_footer(content):
    content = re.sub(r'<text.* font="1">ocabulario.*</text>', r'###', content)
    content = re.sub(r'.*\n###\n.*\n', r'___', content)
    content = re.sub(r'<page.*\n|</page>\n', r'', content)

    return content


def mark_entries(content):
    # Entrada Completa
    content = re.sub(r'<text.* font="3"><b>\s*(\d+)\s+(\w+(?:\s\w+)*)\s+(\w)\s*</b></text>\n?',
                     r'\n###IDENT \1;\2;\3', content)
    # Entrada Completa Multilinha
    content = re.sub(r'<text.* font="3"><b>\s*(\d+)\s+(\w+(?:\s\w+)*)\s*</b></text>\n?',
                     r'\n###IDENT \1;\2; ', content)
    # Se existir, serão apenas os termos restantes e o género da palavra
    content = re.sub(
        r'<text.* font="3"><b>\s*(\w+(?:\s\w+)*)\s+(\w)\s*</b></text>\n?', r'\1;\2;', content)

    # Entrada Remissiva -> Todas as restantes que ainda não tenham sido apanhadas
    content = re.sub(
        r'<text.* font="3><b>\s*(\w+(?: \w+)*)\s+(\w)\s*</b></text>\n?', r'\n###REM \1', content)

    return content


def mark_langs(content):
    # Langs têm font = 0
    content = re.sub(
        r'<text.* font="0">\s*(en|es|pt|la)\s*</text>\n?', r'\n###LANG \1 ', content)

    return content


def treat_areas(areas):
    ans = '\n###AR '
    for elem in areas.groups():
        if elem:
            ans += elem + ';'
    return ans


def mark_area(content):
    content = re.sub(
        r'<text.* font="6"><i>\s*(\w+(?:\s\w+)*)\s*(\w+(?:\s\w+)*)*</i></text>\n?', treat_areas, content)
    return content


def mark_hrefs(content):
    content = re.sub(
        r'<text.* fount="5">\s*Vid\.- (.*)</text>\n?', r'\n###HREF \1', content)
    return content


def mark_SIN_or_VAR(content):
    content = re.sub(
        r'<text.* font="5">\s*(SIN|VAR)\.- (.*)</text>\n?', r'\n###\1 \2', content)
    content = re.sub(
        r'< text.* font="5" >\s*(\s.*)\s*</text>\n?', r'\1', content)
    return content


def mark_translations(content):
    content = re.sub(
        r'<text.* font="7"><i>\s*(\S.*)\s*</i></text>\n?', r'\1', content)
    content = re.sub(r'<text.* font="0">\s*;\s*</text>\n?', r';', content)
    return content


def mark_note(content):
    content = re.sub(
        r'<text.* font="9">\s*Nota\.-\s(.*)</text>\n?', r'\n###NOTE \1', content)
    content = re.sub(r'<text.* font="9">\s*(\S.*)</text>\n?', r'\1', content)
    return content


def clean_file(content):
    content = re.sub(r'<text.*>.*</text>\n', r'', content)
    content = re.sub(
        r'<\?xml version="1.0" encoding="UTF-8"\?>\n', r'', content)
    content = re.sub(
        r'<!DOCTYPE pdf2xml SYSTEM "pdf2xml.dtd">\n', r'', content)
    content = re.sub(r'<fontspec.*/>\n', r'', content)
    content = re.sub(
        r'<pdf2xml producer="poppler" version="23.02.0">\n', r'', content)
    return content


content = open("files/medicina.xml", "r", encoding="utf-8").read()

content = remove_header_footer(content)
content = mark_entries(content)
content = mark_langs(content)
content = mark_area(content)
content = mark_hrefs(content)
content = mark_SIN_or_VAR(content)
content = mark_translations(content)
content = mark_note(content)
content = clean_file(content)

output = open("output.txt", "w")
output.write(content)
