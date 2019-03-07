import os, subprocess, sys
import requests
from bs4 import BeautifulSoup

# settings
OUTPUT_DIR = "output/"
TEMPLATE_FILE = "template.tex"
TAGS = ['POS', 'ANO', 'ESCOLA', 'NOME', 'PONTOS']

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
    vals.append(new)

# load certificate template
template_file = open(TEMPLATE_FILE, "r")
template = template_file.read()
template_file.close()

# create output dir
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# compile for each user
for line in vals:
    output = template
    for i, t in enumerate(TAGS):
        output = output.replace('@' + t + '@', line[i])
    
    # tempfile
    temp_file = open("temp.tex", "w")
    temp_file.write(output)
    temp_file.close()

    name = line[3]

    # call pdflatex
    subprocess.check_call(['pdflatex', '--jobname', name, '--output-directory', OUTPUT_DIR, 'temp.tex'])
    # clean trash
    os.remove(OUTPUT_DIR + name + '.log')
    os.remove(OUTPUT_DIR + name + '.aux')

# remove temp file
os.remove("temp.tex")