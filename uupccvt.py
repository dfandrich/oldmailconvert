#!/usr/bin/python3
# Converts a UUPC/extended mailbox into a standard mbox-style mailbox
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
# TODO:
# turn SYNTHESIZE_FROM into a --sent flag, useful for sent mail
# use better logging

import dateutil.parser
import email
import email.utils
import re
import sys
import time

from typing import MutableSequence, TextIO

# Create a From line to separate messages if one doesn't already exist
# This is typically the case for sent mailboxes
SYNTHESIZE_FROM = True

# Mailbox message separator
SEP = '\x01' * 20
CRLF = '\x0d\x0a'

FROM_RE = re.compile(r'^(From [^ ]+ )(\w+, \d+ \w+ \d+ \d+:\d+:\d+ \w+)(.*)$')


def warning(s: str):
    print(s, file=sys.stderr)


def error(s: str):
    warning(s)
    sys.exit(1)


class UupcMboxConverter:
    """Converts a UUPC/extended mailbox into an mbox-style mailbox."""

    def FromEscape(self, msg: MutableSequence[str]):
        """Escape From lines in place.

        The first line is untouched, as it is a legitimate From line.
        """
        for i, s in enumerate(msg):
            if i and s.startswith('From '):
                warning('Warning: Line needed to be escaped: %s' % s)
                msg[i] = '>' + s

    def WriteMsg(self, msg: MutableSequence[str]):
        fr = msg[0]
        if not fr.startswith('From '):
            if not SYNTHESIZE_FROM:
                error('Unexpected first line on #%d: %s' % (self.msgs, fr))
            # No From line found; create one
            self.frm += 1
            eml = email.message_from_string('\n'.join(msg))
            t = dateutil.parser.parse(eml['date'])
            (human, addr) = email.utils.parseaddr(eml['from'])
            fr = 'From %s %s' % (addr, time.asctime(t.utctimetuple()))
            msg.insert(0, fr)
        else:
            m = FROM_RE.match(fr)
            if m:
                # UUPC/extended versions up to (at least) 1.11z wrote a deprecated
                # date format that modern mailers don't necessarily support.
                t = dateutil.parser.parse(m.group(2))
                fr = m.group(1) + time.asctime(t.utctimetuple()) + m.group(3)
                self.cvt += 1
            msg[0] = fr
        self.FromEscape(msg)
        self.msgs += 1
        self.outfile.write('\n'.join(msg) + '\n\n')

    def ConvertMbox(self, infile: TextIO, outfile: TextIO):
        self.outfile = outfile
        self.msgs = 0
        self.cvt = 0
        self.frm = 0
        found_first = False
        msg = []

        for l in infile:
            l = l.rstrip(CRLF)
            if l == SEP:
                found_first = True
                if msg:
                    self.WriteMsg(msg)
                msg = []
                continue
            if not found_first:
                error('File does not appear to be a UUPC/extended mailbox')
            msg.append(l)
        if msg:
            self.WriteMsg(msg)

        print('Messages copied:  %d' % self.msgs, file=sys.stderr)
        print('Dates converted:  %d' % self.cvt, file=sys.stderr)
        print('From lines added: %d' % self.frm, file=sys.stderr)


def main():
    # Use the iso-8859-1 encoding in order to pass 8-bit clean data
    sys.stdin.reconfigure(encoding='iso-8859-1')   # pytype: disable=attribute-error
    sys.stdout.reconfigure(encoding='iso-8859-1')  # pytype: disable=attribute-error
    c = UupcMboxConverter()
    c.ConvertMbox(sys.stdin, sys.stdout)


if __name__ == '__main__':
    main()
