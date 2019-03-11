'''
    File name: cert-oni.py
    Author: Guilherme Penedo (@guipenedo)
    Date created: 7/20/2013
    Date last modified: 11/03/2019
    Python Version: 3.7
'''

import os, subprocess, sys
import requests
from bs4 import BeautifulSoup

# settings
OUTPUT_DIR = "output/"
OUTPUT_FILENAME = "@ESCOLA@ @NOME@"
TEMPLATE_FILE = "template.tex"
PASSWD_FILE = "passwd.txt"
TEMP_FILE = "temp.tex"

# load passwd.txt info
extra = {}
entry = []
with open(PASSWD_FILE, "r") as f:
    for line in f:
        if line.strip() is '----------------------':
            extra[entry[1] + ' ' + entry[3].replace('_', ' ')] = entry
            entry = []
    f.close()

vals = []
# load standings
url = input("URL com classificação: ")
res = requests.get(url)
res.encoding = 'utf8'
soup = BeautifulSoup(res.text, "html.parser")
trs = soup.findAll('tr')
for tr in trs:
    tds = tr.findAll('td')
    if not tds:
        continue
    new = []
    new.append(tds[0].text)
    new.append(tds[1].text)
    conc = tds[2].text.replace('\n', '').split(' ')
    new.append(conc[0])
    new.append(' '.join(conc[1:]))
    new.append(tds[-1].text.strip())
    key = new[2] + ' ' + new[3]
    while key not in extra:
        key = input("ERRO: key \"" + key + "\" não encontrada! Nova chave: ").strip()
    entry = extra[key]
    new.append(extra[0])
    new.append(extra[2])
    vals.append(new)

# load certificate template
template_file = open(TEMPLATE_FILE, "r")
template = template_file.read()
template_file.close()

# create output dir
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def replace_tags(output, vals):
    TAGS = ['POS', 'ANO', 'ESCOLA', 'NOME', 'PONTOS', 'ESCOLA_COMP', 'NOME_COMP']
    for i, t in enumerate(TAGS):
        output = output.replace('@' + t + '@', vals[i])
    return output

# compile for each user
for line in vals:
    output = replace_tags(template, line)
    
    # tempfile
    temp_file = open(TEMP_FILE, "w")
    temp_file.write(output)
    temp_file.close()

    name = replace_tags(OUTPUT_FILENAME, line)

    # call pdflatex
    subprocess.check_call(['pdflatex', '--jobname', name, '--output-directory', OUTPUT_DIR, TEMP_FILE])
    # clean trash
    os.remove(OUTPUT_DIR + name + '.log')
    os.remove(OUTPUT_DIR + name + '.aux')

# remove temp file
os.remove(TEMP_FILE)