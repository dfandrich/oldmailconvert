# Tests for adddate
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

import datetime
import os
import subprocess
import tempfile
import unittest


class TestAdddateCvt(unittest.TestCase):

    TEST_TIME = '2020-07-07 12:34:56 -0400'  # Fixed time for testing

    def run_inout_test(self, infn, outfn):
        with tempfile.NamedTemporaryFile(mode='w') as inputfile:
            with open(infn, 'r') as realinput:
                inputfile.write(realinput.read())
            inputfile.flush()
            expected_time = datetime.datetime.strptime(
                self.TEST_TIME, '%Y-%m-%d %H:%M:%S %z').timestamp()
            os.utime(inputfile.name, times=(expected_time, expected_time))
            p = subprocess.run(
                ['./adddate', inputfile.name],
                capture_output=True, text=True, env={'TZ': 'UTC+4'})

            with open(outfn, 'r') as e:
                expecteddata = e.read()
            self.assertEqual(expecteddata, p.stdout)

    def test_message_1(self):
        self.run_inout_test('testdata/adddate.input.1', 'testdata/adddate.expected.1')

    def test_message_2(self):
        self.run_inout_test('testdata/adddate.input.2', 'testdata/adddate.expected.2')


if __name__ == '__main__':
    unittest.main()
