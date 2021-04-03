#!/usr/bin/python3
# Converts an e-mail from CompuServe into RFC822 format.
#
# Copyright (C) 2021 Daniel Fandrich
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Each e-mail is expected to be in a file of its own, with the contents of the
# headers and mail as would be logged by a terminal emulator while using the
# command-line CompuServe mail reader to read each message.
#
# Sample message:
#
# Date:  11-Mar-93 21:10 EST
# From:  Joe P. Blo [76543,210]
# Subj:  The subject line
#
# Here is the body.

# TODO:
#  Detect the lines:
#  Distribution:
#  To: [12345,678]
# at the end of message and automatically turn that into a To: line in the header

import dateutil.parser
import dateutil.tz
import re
import sys
from typing import List, TextIO

CIS_DOMAIN = 'compuserve.com'

CRLF = '\x0d\x0a'

FROM_RE = re.compile(r'^From: +(.*) +\[(\d+,\d+)\]$')

TIMEZONE_INFO = {
    "EST": dateutil.tz.gettz("America/New_York"),
    "EDT": dateutil.tz.gettz("America/New_York"),
    "CST": dateutil.tz.gettz("America/Chicago"),
    "CDT": dateutil.tz.gettz("America/Chicago"),
    "PST": dateutil.tz.gettz("America/Los_Angeles"),
    "PDT": dateutil.tz.gettz("America/Los_Angeles"),
}


def CisToDomain(cis_addr: str) -> str:
    """Convert a CompuServe numeric address into a domain address."""
    cis_addr = cis_addr.replace(',', '.')
    return '%s@%s' % (cis_addr, CIS_DOMAIN)


def ConvertMessage(infile: TextIO, outfile: TextIO, to_addr: str):
    to_addr = CisToDomain(to_addr)
    headers = True
    got_subj = False
    got_to = False
    for l in infile:
        l = l.rstrip(CRLF)

        if headers:
            if l.startswith('Subj:'):
                l = re.sub('^Subj: *', 'Subject: ', l)
                if got_subj:
                    sys.stderr.write('Warning: two Subject: lines\n')
                got_subj = True

            elif l.startswith('From:'):
                if got_to:
                    sys.stderr.write('Warning: To: line already exists; not adding a new one\n')
                else:
                    # Add a To: line at this point because there isn't one otherwise
                    outfile.write('To: %s\n' % to_addr)
                    got_to = True

                addr = FROM_RE.match(l)
                if addr:
                    cis = CisToDomain(addr.group(2))
                    l = 'From: %s <%s>' % (addr.group(1), cis)
                else:
                    sys.stderr.write('Warning: From: line could not be converted: %s\n' % l)

            elif l.startswith('Date:'):
                d = dateutil.parser.parse(l[6:], tzinfos=TIMEZONE_INFO)
                l = 'Date: %s' % d.strftime("%a, %d %b %Y %H:%M:%S %z")

            elif l.startswith('Reply to: '):
                l = 'Subject: Re: %s' % l[10:]
                if got_subj:
                    sys.stderr.write('Warning: two Subject: lines\n')
                got_subj = True

            elif l.startswith('To: '):
                if got_to:
                    sys.stderr.write('Warning: two To: lines\n')
                got_to = True
                l = re.sub('^To: *internet: *', 'To: ', l, flags=re.I)

            elif l == '':
                headers = False

        outfile.write(l + '\n')


def ConvertCompuserveMail(argv: List[str]):
    # Use the iso-8859-1 encoding in order to pass 8-bit clean data
    sys.stdin.reconfigure(encoding='iso-8859-1')   # pytype: disable=attribute-error
    sys.stdout.reconfigure(encoding='iso-8859-1')  # pytype: disable=attribute-error
    if len(argv) < 3 or argv[1] != '-t':
        sys.stderr.write('Usage: %s -t <CIS address>\n' % argv[0])
        sys.exit(1)
    to_addr = argv[2]
    ConvertMessage(sys.stdin, sys.stdout, to_addr)


def main():
    ConvertCompuserveMail(sys.argv)


if __name__ == '__main__':
    main()
