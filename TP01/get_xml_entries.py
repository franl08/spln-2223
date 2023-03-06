import re

f = open('output.xml', 'r')

for line in f:
    matchobj = re.search(
        '<text top="\d+" left="\d+" width="\d+" height="\d+" font="\d+">', line)
    if matchobj:
        print(line)
