#!/usr/bin/env python2


import argparse
from appy.pod.renderer import Renderer



### DEFAULTS
sep=','
players_per_page=3
tmpdir="tmp"
template_file_name='henkkari.ods'
output_file_name='result.pdf'



### PARSE ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("-f", help="Input file")
args = parser.parse_args()

if args.f:
    input_file_name = args.f
else:
    if __name__ == "__main__":
        exit()



### READ FILE
# init player list
players=[]

# read file
with open(input_file_name) as input_file:
    for line in input_file:
        players.append(line.split(sep))

# add empty lines to player list
while len(players)%players_per_page > 0:
        players.append(['','',''])



### CREATE ODS-FILES
page=0
player_num=0
while player_num < len(players):
   page_output_file_name = ''.join(output_file_name.split('.')[:-1]) + '_' + str(page) + '.' + output_file_name.split('.')[-1] 
   renderer = Renderer(template_file_name, globals(), page_output_file_name)
   renderer.run()
   page = page+1
   player_num = page*players_per_page
