#!/usr/bin/env python3
# Split a big file with multiple mail messages into an MMDF mailbox
#
# Copyright (C) 2023 Daniel Fandrich
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
#
# The input file is just a text file with a bunch of e-mails concatenated,
# with some standard headers at the start of each message. It tries to detect
# forwarded messages and keep them attached to the right message.
#
# The input file is not a standard format, so this script can't always do a
# perfect job. The input file may need to be manually tweaked to provide the
# clues this script needs to split messages correctly.

import re
import sys


MMDFSEP = b'\x01\x01\x01\x01\n'
FIRSTHEADERRE = re.compile(
    rb'(^(Date|To|From|Mime-Version|Subject|Cc|Sender|X-Sender|X-Authentication-Warning'
    rb'|X-Originating-Ip|Resent-Date|Received):)|(^From .)', re.I)
# Supports continuation headers starting with a space, too
HEADERRE = re.compile(rb'^([a-zA-Z][-a-zA-Z0-9]+:)|^(\s+\S)', re.A)
FORWARDRE = re.compile(rb'^-* *Forwarded message')
FORWARDING_LINES_COPIED = 2

DEBUG = False  # True to show debugging logs


def debug(s):
    # Write to the same buffer as the message to avoid different flushing times
    if DEBUG:
        sys.stdout.buffer.write(s.encode() + b'\n')


def main():
    sys.stdout.buffer.write(MMDFSEP)

    with sys.stdin.buffer as intext:
        while True:
            debug('HEADER ^')
            # In headers
            while l := intext.readline():
                sys.stdout.buffer.write(l)
                if not HEADERRE.search(l):
                    break

            if not l:
                debug('EOF')
                break   # end of file

            debug('NOT A HEADER ^')

            # In body
            while l := intext.readline():
                if FORWARDRE.search(l):
                    debug('FORWARD v')
                    # Forwarded messages, including their header lines, should
                    # be treated as the previous message body. Solution:
                    # - Copy next few lines verbatim when forwarding is detected,
                    #   since this will probably end in a header block
                    # - If the next line looks like a header, switch to header
                    #   mode to copy remainder of header verbatim, without
                    #   creating a new message
                    sys.stdout.buffer.write(l)
                    for _ in range(FORWARDING_LINES_COPIED):
                        l = intext.readline()
                        if l:
                            sys.stdout.buffer.write(l)
                    l = intext.readline()
                    if l and HEADERRE.search(l):
                        sys.stdout.buffer.write(l)
                        # Looks like we're in a header block. Switch to header mode
                        # in order to avoid creating a new message
                        break
                    sys.stdout.buffer.write(l)

                if FIRSTHEADERRE.search(l):
                    debug('ACTUAL HEADER v')
                    sys.stdout.buffer.write(MMDFSEP)
                    sys.stdout.buffer.write(MMDFSEP)
                    sys.stdout.buffer.write(l)
                    break
                if HEADERRE.search(l):
                    debug('(ALMOST a header v)')
                sys.stdout.buffer.write(l)

        sys.stdout.buffer.write(MMDFSEP)


if __name__ == '__main__':
    main()
