#!/usr/bin/env python2
# PYTHON_ARGCOMPLETE_OK
'''
Reads text file with rows formatted as:
<Name>;<Team>;<Serie>;<Compensation>
and exports scoresheets in ods/pdf format.

The script is using LibreOffice UNO API. UNO server can be started with
command:
soffice --accept="socket,port=2002;urp;"
If the python interpreter running the script is not UNO-enabled, the path of
UNO-enabled python can be provided with -u argument
'''
import argparse
import csv
import os.path
import sys
import tempfile

import PyPDF2
import appy.pod.renderer
import argcomplete


SEP = ';'
PLAYERS_PER_PAGE = 3
TEMPLATE_FILE_NAME = 'henkkari.ods'
OUTPUT_FILE_NAME = 'result.pdf'
UNO_PATH = '/usr/bin/python3'


def parse_arguments():
    """Parse commandline argumernts.

    :returns: commandline arguments
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-f", "--input", help="Input file", required=True)
    parser.add_argument("-t", "--template", help="Template file",
                        default=TEMPLATE_FILE_NAME)
    parser.add_argument("-o", "--output", help="Output file",
                        default=OUTPUT_FILE_NAME)
    parser.add_argument("-u", "--uno-path",
                        help="Uno path (something like: /usr/bin/python)",
                        default=UNO_PATH)

    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    if not os.path.exists(args.input):
        sys.exit("Input file \"{}\" not found".format(args.input))
    if not os.path.exists(args.template):
        sys.exit("Template file \"{}\" not found".format(args.template))
    if os.path.exists(args.output):
        sys.exit("Output file \"{}\" already exists".format(args.output))

    return args


def read_file(filename):
    """Read file that contains three words per line, separated by comma.

    :param filename: path to the file
    :returns: List rows, where each row is list of words
    """
    # read file
    with open(filename) as input_file:
        reader = csv.reader(input_file, delimiter=';', quotechar='"')
        players = list(reader)

    for player in players:
        if len(player) != 4:
            sys.exit(
                "A record in input file contains wrong number of fields: {}"
                .format(player)
            )

    return players


def merge_pdf(input_files, output_file):
    """Merge list of pdf files into one pdf.

    :param input_files: list of filenames of pdfs to be merged
    :param output_file: filename of merged pdf
    :returns: None
    """
    output_pdf = PyPDF2.PdfFileMerger()

    for input_file in input_files:
        output_pdf.append(input_file)

    with open(output_file, "wb") as output_stream:
        output_pdf.write(output_stream)


def create_pages(players, template, output_basename, uno_path,
                 output_directory='/tmp/'):
    """Create pages as individual files. The file format is decided from the
    output file suffix.

    :param players: list of players
    :param template: template file path
    :param output_basename: base name for output files
    :param output_directory: directory where outfiles are created
    :returns: list of filenames
    """
    page_num = 0
    player_num = 0
    page_list = []
    while player_num < len(players):
        page_output_file_name = ''.join(output_basename.split('.')[:-1]) \
            + '_' + str(page_num) + '.' + output_basename.split('.')[-1]
        page_output_path = os.path.join(output_directory,
                                        page_output_file_name)
        if os.path.exists(page_output_path):
            raise IOError(
                "File \"{}\" already exists".format(page_output_path)
            )
        page_list.append(page_output_path)
        renderer = appy.pod.renderer.Renderer(
            template,
            {'players': players, 'player_num': player_num},
            page_output_path,
            pythonWithUnoPath=uno_path
        )
        try:
            renderer.run()
        except appy.pod.PodError as error:
            if "Couldn't not connect to LibreOffice on port 2002" \
                    in str(error):
                sys.exit(
                    str(error) + '\n\nStart LibreOffice first:'
                    '\n\n    soffice --accept="socket,port=2002;urp;"'
                )

        page_num = page_num+1
        player_num = page_num*PLAYERS_PER_PAGE

    return page_list


def main():
    """Main function"""
    args = parse_arguments()
    filetype = args.output.split('.')[-1]

    players = read_file(args.input)

    # add empty lines to player list if needed
    while len(players) % PLAYERS_PER_PAGE > 0:
        players.append(['', '', '', ''])

    # Write scoresheets one printable page per file. If output file is pdf, the
    # pages will be merged into one document.
    if filetype == 'pdf':
        page_output_directory = tempfile.mkdtemp()
    else:
        page_output_directory = './'
    page_list = create_pages(players, args.template, args.output,
                             args.uno_path, page_output_directory)

    # merge output files into one file if output file type is pdf
    if filetype == 'pdf':
        merge_pdf(page_list, args.output)


if __name__ == "__main__":
    main()
