#!/usr/bin/env python2
'''
Reads text file with rows formatted as:
<Name>,<Team>,<Serie>
and exports scoresheets in ods/pdf format.
'''
import argparse
import os.path
from appy.pod.renderer import Renderer
from pyPdf import PdfFileWriter, PdfFileReader



### DEFAULTS
sep=','
players_per_page=3
template_file_name='henkkari.ods'
output_file_name='result.pdf'
uno_path=None



### PARSE ARGUMENTS
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
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
    output_file_name = args.o

if args.t:
    template_file_name = args.t
else:
    print("Using default template: " + template_file_name)
if not (os.path.exists(template_file_name)):
    exit("Templatefile \"{}\" not found".format(template_file_name))

if args.u:
    uno_path = args.u



### READ FILE
# init player list
players=[]

# read file
with open(input_file_name) as input_file:
    for line in input_file:
        players.append(line.split(sep))

# add empty lines to player list if needed
while len(players)%players_per_page > 0:
        players.append(['','',''])




### CREATE PAGES (pdf, ods or something else)
page_num = 0
player_num = 0
page_list = []
while player_num < len(players):
   page_output_file_name = ''.join(output_file_name.split('.')[:-1]) + '_' + str(page_num) + '.' + output_file_name.split('.')[-1] 
   if os.path.exists(page_output_file_name):
       exit("File \"{}\" already exists".format(page_output_file_name))
   page_list.append(page_output_file_name)
   renderer = Renderer(template_file_name, {'players':players,'player_num':player_num}, page_output_file_name, pythonWithUnoPath=uno_path)
   renderer.run()
   page_num = page_num+1
   player_num = page_num*players_per_page



### MERGE PAGES TO ONE PDF-FILE (if output is pdf)
if output_file_name.split('.')[-1] == 'pdf':
   output_pdf = PdfFileWriter()
   
   for page in page_list:
       input_pdf = PdfFileReader(file(page))
       output_pdf.addPage(input_pdf.getPage(0))
   
   output_stream = file(output_file_name, "wb")
   output_pdf.write(output_stream)
   output_stream.close()
