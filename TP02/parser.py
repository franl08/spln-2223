import ply.yacc as yacc
from lexer import tokens, literals


def p_dic(p):
    "dic : concepts"


def p_concepts(p):
    "concepts : concept concepts"


def p_concepts_single(p):
    "concepts : concept"


def p_concept(p):
    "concept : ID_CONCEPT '.' SEP areas SEP langs"


def p_areas(p):
    "areas : ID_AREAS name_areas"


def p_name_areas(p):
    "name_areas : SEP '-' WORDS name_areas"


def p_name_areas_single(p):
    "name_areas : SEP '-' WORDS"


def p_langs(p):
    "langs : ID_LANGS type_lang"


def p_type_lang(p):
    "type_lang : SEP '*' ID_LANG terms"


def p_terms(p):
    "terms : SEP2 '-' WORDS qual_term var_country terms"


def p_terms_single(p):
    "terms : SEP2 '-' WORDS qual_term var_country"


def p_terms_only_qual(p):
    "terms : SEP2 '-' WORDS qual_term terms"


def p_terms_only_qual_single(p):
    "terms : SEP2 '-' WORDS qual_term"


def p_terms_only_var(p):
    "terms : SEP2 '-' WORDS var_country terms"


def p_terms_only_var_single(p):
    "terms : SEP2 '-' WORDS var_country"


def p_terms_simple(p):
    "terms : SEP2 '-' WORDS terms"


def p_terms_simple_single(p):
    "terms : SEP2 '-' WORDS"


def p_qual_term(p):
    "qual_term : '(' GENDER '|' TYPE_TERM ')'"


def p_qual_term_only_gender(p):
    "qual_term : '(' GENDER ')'"


def p_var_country(p):
    "var_country : SEP3 '+' ID_COUNTRY"


def p_error(p):
    print(f"Syntax Error: {p}")
    parser.success = False


parser = yacc.yacc()

with open('example.txt', 'r') as f:
    content = f.read()
    parser.success = True
    parser.flag = True
    parser.parse(content)
