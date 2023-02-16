import re

file = open("files/medicina.xml", "r")


def convert_pages(file):
    file_by_pages = []
    current_page = ""
    number_of_pages = 0
    ignoring_lines = 4
    for line in file:
        # Skip XML header
        if ignoring_lines > 0:
            ignoring_lines -= 1
        else:
            page_breaks = re.search('</page>', line)
            if page_breaks:
                file_by_pages.append(current_page)
                current_page = ""
                number_of_pages += 1
            else:
                current_page += line
    print(f"Successfully read {number_of_pages} pages.")
    return file_by_pages


def get_useful_pages(pages):
    new_pages = []
    running = 0
    useful_pages = 0
    for page in pages:
        lower_limit = re.search('<page number="19".*', page)
        max_limit = re.search('<page number="545".*', page)
        if lower_limit and running == 0:
            running = 1
        elif max_limit:
            running = 0
        elif running == 1:
            new_pages.append(page)
            useful_pages += 1
    print(f"There are {useful_pages} useful pages.")
    return new_pages


def remove_header(pages):
    new_pages = []
    for page in pages:
        page = re.sub('\n.*font="17">V.*', '', page)
        page = re.sub('\n.*font="18".*', '', page)
        new_pages.append(page)
    return new_pages


def remove_page_numbers(pages):
    new_pages = []
    for page in pages:
        page = re.sub('\n?.*<page.*', '', page)
        new_pages.append(page)
    return new_pages


def remove_font_spec(pages):
    new_pages = []
    for page in pages:
        page = re.sub('.*fontspec.*', '', page)
        new_pages.append(page)
    return new_pages


def remove_useless_lines(pages):
    new_pages = []
    for page in pages:
        page = re.sub(
            '\n<text top="\d+" left="\d+" width="\d+" height="\d+" font="\d+">(<b>|<i>)*;?\s+(</b>|</i>)*</text>',
            '',
            page)
        page = re.sub(
            '\n<text top="862" left="324" width="15" height="18" font="8">\d+</text>',
            '',
            page
        )
        new_pages.append(page)
    return new_pages


def get_complete_entries(pages):
    total_entries = 0
    for page in pages:
        lines = page.split('\n')
        new_lines = ""
        for line in lines:
            line = re.match('.* font="19">\s*<b>\s*\d+.*', line)
            if line:
                total_entries += 1
    print(f"There are {total_entries} complete entries.")
    return total_entries


def get_remissive_entries(pages):
    total_entries = 0
    for page in pages:
        lines = page.split('\n')
        new_lines = ""
        for line in lines:
            line = re.match('.* font="19">\s*<b>\s*[a-zA-Z]+.*', line)
            if line:
                total_entries += 1
    print(f"There are {total_entries} remissive entries.")
    return total_entries


def remove_italics_and_bolds_and_closing_texts(pages):
    new_pages = []
    for page in pages:
        lines = page.split('\n')
        new_lines = ""
        for line in lines:
            line = re.sub('(<b>|<i>|</i>|</b>|</text>)', '', line)
            new_lines += line + '\n'
        page = new_lines
        new_pages.append(page)
    return new_pages


def clear_lines(pages):
    # TODO
    pages = remove_italics_and_bolds_and_closing_texts(pages)
    new_pages = []
    trolha = False
    for page in pages:
        lines = page.split('\n')
        new_lines = ""
        ac = 1

        for line in lines:
            # fazer cenas com os named groups para capturar indices
            # Nome principal
            # TODO: Rever esta forma de tratar dos erros
            failed_bold = re.match('.* font="8">\d+', line)
            if failed_bold:
                line = re.sub('.* font="8">', '##', line)
                line += re.sub('. font="19">', '', lines[ac])
            else:
                entries = re.match('.* font="19">', line)
                if entries:
                    remissive = re.match('.* font="6">', lines[ac])
                    if remissive:
                        line = re.sub('.* font="19">', '# ', line)
                    else:
                        line = re.sub('.* font="19">', '## ', line)
                # Langs
                line = re.sub('.* font="17">', '@', line)
                # Escritas noutra língua
                line = re.sub('.* font="22">', '-> ', line)
                # Vids
                line = re.sub('.* font="6">', '~', line)
                # Sinónimos
                line = re.sub('.* font="6">\s+SIN.-', '@@', line)
                # Tipo da doença
                line = re.sub('.* font="21">', '*', line)
                # Notas
                line = re.sub('.* font="24">', '>', line)
            new_lines += line + "\n"
            ac += 1
        page = new_lines
        new_pages.append(page)
    return new_pages


pages = convert_pages(file)
pages = get_useful_pages(pages)
pages = remove_header(pages)
pages = remove_page_numbers(pages)
pages = remove_font_spec(pages)
pages = remove_useless_lines(pages)
complete_entries = get_complete_entries(pages)
remissive_entries = get_remissive_entries(pages)
pages = clear_lines(pages)

print(f"There are {complete_entries + remissive_entries} total entries.")

output = open("output.xml", "w")

for page in pages:
    output.write(page)
# for page in pages:
#    print(f"\n NEW PAGE \n {page} \n")
