# Tests for mantescvt
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

import subprocess
import unittest


class TestMantesCvt(unittest.TestCase):

    def run_inout_test(self, infn, outfn):
        with open(infn, 'r') as inputfile:
            p = subprocess.run(
                './mantescvt', input=inputfile.read(), capture_output=True, text=True)

        with open(outfn, 'r') as e:
            expecteddata = e.read()
        self.assertEqual(expecteddata, p.stdout)

    def test_message_1(self):
        self.run_inout_test('testdata/mantes.input.1', 'testdata/mantes.expected.1')


if __name__ == '__main__':
    unittest.main()
