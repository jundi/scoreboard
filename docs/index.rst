Scoresheet
==========
Create printable PDF scoresheet for kyykkä competition.

Reads text file with rows formatted as:
<Name>;<Team>;<Serie>;<Compensation>
and exports scoresheets in ods/pdf format.

The script is using LibreOffice UNO API. UNO server can be started with
command:
soffice --accept="socket,port=2002;urp;"
If the python interpreter running the script is not UNO-enabled, the path of
UNO-enabled python can be provided with -u argument
