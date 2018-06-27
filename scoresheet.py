#!/usr/bin/env python2
# pylint: disable=invalid-name
'''
Reads text file with rows formatted as:
<Name>,<Team>,<Serie>
and exports scoresheets in ods/pdf format.

The script is using LibreOffice UNO API. UNO server can be started with
command:
soffice --accept="socket,port=2002;urp;"
If the python interpreter running the script is not UNO-enabled, the path of
UNO-enabled python can be provided with -u argument
'''
import argparse
import os.path
from appy.pod.renderer import Renderer
from pyPdf import PdfFileWriter, PdfFileReader



### DEFAULTS
SEP = ','
PLAYERS_PER_PAGE = 3
TEMPLATE_FILE_NAME = 'henkkari.ods'
OUTPUT_FILE_NAME = 'result.pdf'
UNO_PATH = None



### PARSE ARGUMENTS
parser = argparse.ArgumentParser(
    description=__doc__, formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("-f", help="Input file")
parser.add_argument("-t", help="Template file")
parser.add_argument("-o", help="Output file")
parser.add_argument("-u", help="Uno path (something like: /usr/bin/python)")
args = parser.parse_args()

if args.f:
    input_file_name = args.f
else:
    exit('No input file given')

if args.o:
    OUTPUT_FILE_NAME = args.o

if args.t:
    TEMPLATE_FILE_NAME = args.t
else:
    print "Using default template: " + TEMPLATE_FILE_NAME
if not os.path.exists(TEMPLATE_FILE_NAME):
    exit("Templatefile \"{}\" not found".format(TEMPLATE_FILE_NAME))

if args.u:
    UNO_PATH = args.u



### READ FILE
# init player list
players = []

# read file
with open(input_file_name) as input_file:
    for line in input_file:
        if line.isspace():
            continue
        words = line.split(SEP)
        if len(words) == 3:
            players.append(words)
        else:
            exit("Faulty line: " + line)

# add empty lines to player list if needed
while len(players)%PLAYERS_PER_PAGE > 0:
    players.append(['', '', ''])




### CREATE PAGES (pdf, ods or something else)
page_num = 0
player_num = 0
page_list = []
while player_num < len(players):
    page_output_file_name = ''.join(OUTPUT_FILE_NAME.split('.')[:-1]) + '_' \
        + str(page_num) + '.' + OUTPUT_FILE_NAME.split('.')[-1]
    if os.path.exists(page_output_file_name):
        exit("File \"{}\" already exists".format(page_output_file_name))
    page_list.append(page_output_file_name)
    renderer = Renderer(TEMPLATE_FILE_NAME,
                        {'players':players, 'player_num':player_num},
                        page_output_file_name,
                        pythonWithUnoPath=UNO_PATH)
    renderer.run()
    page_num = page_num+1
    player_num = page_num*PLAYERS_PER_PAGE



### MERGE PAGES TO ONE PDF-FILE (if output is pdf)
if OUTPUT_FILE_NAME.split('.')[-1] == 'pdf':
    output_pdf = PdfFileWriter()

    for page in page_list:
        input_pdf = PdfFileReader(file(page))
        output_pdf.addPage(input_pdf.getPage(0))

    output_stream = file(OUTPUT_FILE_NAME, "wb")
    output_pdf.write(output_stream)
    output_stream.close()
