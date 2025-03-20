# oldmailconvert

This is a set of scripts for converting e-mail from various historic mail
formats into RFC822-style messages.  These were written to convert some old
message archives into an format suitable for indexing and reading using modern
e-mail management software.

The output of each script is one of a number of possible formats, but each is
supported by modern software. The results can later be easily converted into
a consistent format if needed (see the *Other programs* section below).

## Programs

### adddate

Adds a Date: line to an existing RFC822 message using the modification time of
the message file. The script takes a file name as an argument and writes the
modified message to stdout. If the message already has a Date: field, it is
left untouched.

Usage:

  adddate old.eml > new.eml

### compuservecvt

Converts CompuServe messages. These consist of messages as logged in a terminal
as they were displayed while using the remote message viewer.  A single message
is passed in to stdin and the converted messages is written to stdout. One
command-line parameter is mandatory: "-t nnnnn,nnn" which specifies the
CompuServe user ID that received the message. This is so a To: line can be
added to the message, which otherwise would show no indication of the receiver.

CompuServe was an early time-share and information system that began offering
access to the consumer public in 1979, and dominated the field in the 1980s
before competitors like AOL entered and Internet access became publicly
available.

Usage:

  compuservecvt -t 77777,111 < old.txt > new.eml

### maillogcvt

Converts a big file with multiple mail messages into an MMDF mailbox. The file
may have been created by logging a mail reading session on a terminal, by
manually concatenating mail messages into a text file, or through some other ad
hoc means.  This script is likely to need some modification for it to work in
your specific case.

The input file is just a text file with a bunch of e-mails concatenated,
with some standard headers (like To:, From:, Subject:) at the start of each
message. It tries to detect forwarded messages and keep them attached to the
right message, since forwarded with their headers can look like an entirely new
message otherwise.  This is tricky business, and can easily go wrong. You may
need to add some of the headers found in your messages to the script in order
for it to split messages on the correct boundaries.

Everything in the input is assumed to be part of a message and nothing is
thrown out, which can result things that aren't messages in the output file or
lines that aren't really part of an MMDF message (like "From " lines). GIGO.
You may need to iterate a few times on your input files to either tweak the
script or preprocess your input before finding a satisfactory result.

Usage:

  maillogcvt < old.txt > new.mmdf

### mantescvt

Converts MANTES messages.  The input to this program is expected to be a
terminal log of a single message as displayed in MANTES with extraneous lines
removed.  A single message is passed in to stdin and the converted messages is
written to stdout.

MANTES was a file management system running on an IBM mainframe under MVS which
was used from the 1970s through the 2000s. It was developed at the University
of Manitoba and used at a number of universities and companies in Canada and
around the world.

Usage:

  mantescvt old.txt > new.eml

### uupccvt

Converts a message mailbox created by UUPC/extended, which is a custom mailbox
format somewhat reminiscent of MMDF.  A single message mailbox is passed in to
stdin and an mbox mailbox is written to stdout.  The normal "From" encoding is
performed on the body of messages when required, as it required by the mbox
format.

UUPC/extended was a uucp package for MS-DOS systems developed in 1985. It
provided a uucp-style suite of programs for mail, USENET news and file transfer
over dial-up modems that ran on DOS systems.

Usage:

  uupccvt < old.mbo > new.mbox

## Installation

The latest source code can be obtained from
https://github.com/dfandrich/oldmailconvert/

The scripts are written in a mix of Python and Bourne shell. They use some
standard POSIX utilities, but assume some of them have GNU extensions
available.

Build and install the latest release of code from Github with:

  pip3 install https://glare.now.sh/dfandrich/oldmailconvert/tar

The regression test suite can be run with the command:

  pytest

or, if pytest is not installed:

  python3 tests.py

I've found some tests related to dates fail in one Python 3.8.14 environment
because dateutil seems to improperly handle time zones in that version.

## Other programs

To convert Fidonet messages, try my program dumpfidomsg
(https://github.com/dfandrich/dumpfidomsg/)

If you're more interested in converting between the contemporary formats mbox,
MMDF, Maildir and MH mail, one simple way is to use the Mutt mailer
(http://mutt.org/), by reading from one style of mailbox, tagging all the
messages, then mass saving them all into an empty mailbox of the other style.

A simple way of turning a plain RFC822 message into a mailbox is to pipe it to
formail, which is part of procmail (https://www.procmail.org/).

## Author

Daniel Fandrich <dan@coneharvesters.com>

This program is Copyright (C) 2021–2025 Daniel Fandrich. It is distributed under the
terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.
