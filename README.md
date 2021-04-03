# oldmailconvert

This is a set of scripts for converting mail from various historic mail formats
into RFC822-style messages.

These were written to convert some old message archives into an format suitable
for indexing and reading using modern software.

## Programs

### adddate

Adds a Date: line to an existing RFC822 message with the modified time of the
message file. The script takes a file name as an argument and writes the
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

Usage:

  compuservecvt -t 77777,111 <old.txt > new.eml

### mantescvt

Converts MANTES messages. MANTES was a file management system running on an IBM
mainframe under MVS which was used from the 1970s through the 2000s.  The input
to this program is expected to be a terminal log of a single message as
displayed in MANTES with extraneous lines removed.  A single message is passed
in to stdin and the converted messages is written to stdout.

Usage:

  mantescvt old.txt > new.eml

### uupccvt

Converts a message mailbox created by UUPC/extended. This was a uucp package
for MS-DOS systems that used a custom mailbox format somewhat reminiscent of
MMDF.  A single message mailbox is passed in to stdin and an mbox mailbox is
written to stdout.  The normal "From" encoding is performed on the body of
messages when required, as it required by the mbox format.

Usage:

  uupccvt old.mbo > new.mbox

## Installation

The latest source code can be obtained from
https://github.com/dfandrich/oldmailconvert/

The scripts are written in a mix of Python and Bourne shell.

Build and install the latest release of code from Github with:

  pip3 install https://glare.now.sh/dfandrich/oldmailconvert/tar

The regression test suite can be run with the command:

  python3 setup.py test

## Other programs

To convert Fidonet messages, try my program dumpfidomsg
(https://github.com/dfandrich/dumpfidomsg/)

If you're more interested in converting between the contemporary formats mbox,
MMDF, Maildir and MH mail, one simple way is to use the Mutt mailer
(http://mutt.org/), by loading one style of mailbox and mass copying all the
messages into the other style.

## Author

Daniel Fandrich <dan@coneharvesters.com>

This program is Copyright (C) 2021 Daniel Fandrich. It is distributed under the
terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.
