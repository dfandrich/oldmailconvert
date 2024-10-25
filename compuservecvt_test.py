# Tests for compuservecvt.py
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

import io
import unittest
from unittest import mock

import compuservecvt


class TestCompuserveCvt(unittest.TestCase):

    def run_inout_test(self, infn, outfn):
        outputfile = io.TextIOWrapper(io.BytesIO())
        with open(infn, 'r') as inputfile, \
            mock.patch('compuservecvt.sys.stdin', new=inputfile), \
                mock.patch('compuservecvt.sys.stdout', new=outputfile):
            compuservecvt.ConvertCompuserveMail(['.', '-t', '77777.111'])

        with outputfile:
            outputfile.seek(0)
            actualdata = outputfile.read()
        with open(outfn, 'r') as e:
            expecteddata = e.read()

        self.assertEqual(expecteddata, actualdata)

    def test_message_1(self):
        self.run_inout_test('testdata/compuserve.input.1', 'testdata/compuserve.expected.1')

    def test_message_2(self):
        self.run_inout_test('testdata/compuserve.input.2', 'testdata/compuserve.expected.2')


if __name__ == '__main__':
    unittest.main()
