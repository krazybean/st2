# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest2
import mock

from st2common.models.db.actionalias import ActionAliasDB
from st2common.util.actionalias_helpstring import generate_helpstring_list


MemoryActionAliasDB = ActionAliasDB


ALIASES = [
    MemoryActionAliasDB(name="kyle_reese", ref="terminator.1",
        pack="the80s", enabled=True,
        formats=["Come with me if you want to live"]
    ),
    MemoryActionAliasDB(name="terminator", ref="terminator.2",
        pack="the80s", enabled=True,
        formats=["I need your {{item}}, your {{item2}}"
            " and your {{vehicle}}"]
    ),
    MemoryActionAliasDB(name="johnny_five_alive", ref="short_circuit.3",
        pack="the80s", enabled=True,
        formats=[{'display': 'Number 5 is {{status}}',
            'representation': ['Number 5 is {{status=alive}}']},
            'Hey, laser lips, your mama was a snow blower.']
    ),
    MemoryActionAliasDB(name="i_feel_alive", ref="short_circuit.4",
        pack="the80s", enabled=True,
        formats=["How do I feel? I feel... {{status}}!"]
    ),
    MemoryActionAliasDB(name='andy', ref='the_goonies.1',
        pack="the80s", enabled=True,
        formats=[{'display': 'Watch this.'}]
    ),
    MemoryActionAliasDB(name='andy', ref='the_goonies.5',
        pack="the80s", enabled=True,
        formats=[{'display': "He's just like his {{relation}}."}]
    ),
    MemoryActionAliasDB(name='data', ref='the_goonies.6',
        pack="the80s", enabled=True,
        formats=[{'representation': "That's okay daddy. You can't hug a {{object}}."}]
    ),
    MemoryActionAliasDB(name='mr_wang', ref='the_goonies.7',
        pack="the80s", enabled=True,
        formats=[{'representation': 'You are my greatest invention.'}]
    ),
    MemoryActionAliasDB(name="Ferris", ref="ferris_buellers_day_off.8",
        pack="the80s", enabled=True,
        formats=["Life moves pretty fast.",
        "If you don't stop and look around once in a while, you could miss it."]
    ),
    MemoryActionAliasDB(name="spengler", ref="ghostbusters.9",
        pack="the80s", enabled=True,
        formats=["{{choice}} cross the {{target}}"]
    )
]


@mock.patch.object(MemoryActionAliasDB, 'get_uid')
class ActionAliasTestCase(unittest2.TestCase):
    '''
    Test scenarios must consist of 80s movie quotes.
    '''
    def test_filtering_no_arg(self, mock):
        result = generate_helpstring_list(ALIASES)
        pack_helpstrings = result.get("the80s")
        self.assertEqual(len(pack_helpstrings), 10)
        self.assertEqual(pack_helpstrings[0].get("display"), "Come with me if you want to live")

    def test_filtering_bad_dataype(self, mock):
        result = 80
        try:
            result = generate_helpstring_list(ALIASES, 44)
        except TypeError:
            pass
        self.assertEqual(result, 80)

    def test_filtering_empty_string(self, mock):
        result = generate_helpstring_list(ALIASES, "")
        pack_helpstrings = result.get("the80s")
        self.assertEqual(len(pack_helpstrings), 10)
        self.assertEqual(pack_helpstrings[0].get("display"), "Come with me if you want to live")

    def test_filtering_no_match(self, mock):
        result = generate_helpstring_list(ALIASES, "xXxXxXx")
        self.assertEqual(result, {})

    def test_filtering_match(self, mock):
        result = generate_helpstring_list(ALIASES, "you")
        pack_helpstrings = result.get("the80s")
        self.assertEqual(len(pack_helpstrings), 4)
        self.assertEqual(pack_helpstrings[0].get("display"), "Come with me if you want to live")

    def test_pack_bad_datatype(self, mock):
        result = generate_helpstring_list(ALIASES, "", {})
        self.assertEqual(result, {})

    def test_pack_empty_string(self, mock):
        result = generate_helpstring_list(ALIASES, "", "")
        pack_helpstrings = result.get("the80s")
        self.assertEqual(len(pack_helpstrings), 10)
        self.assertEqual(pack_helpstrings[0].get("display"), "Come with me if you want to live")

    def test_pack_no_match(self, mock):
        result = generate_helpstring_list(ALIASES, "", "xXxXxXx")
        self.assertEqual(result, {})

    def test_pack_match(self, mock):
        result = generate_helpstring_list(ALIASES, "", "the80s")
        pack_helpstrings = result.get("the80s")
        self.assertEqual(len(pack_helpstrings), 10)
        self.assertEqual(pack_helpstrings[0].get("display"), "Come with me if you want to live")

    def test_limit_bad_datatype(self, mock):
        result = 80
        try:
            result = generate_helpstring_list(ALIASES, "", "the80s", "bad")
        except TypeError:
            pass
        self.assertEqual(result, 80)

    def test_limit_neg_out_of_bounds(self, mock):
        result = generate_helpstring_list(ALIASES, "", "the80s", -3)
        pack_helpstrings = result.get("the80s")
        self.assertEqual(len(pack_helpstrings), 10)
        self.assertEqual(pack_helpstrings[0].get("display"), "Come with me if you want to live")

    def test_limit_pos_out_of_bounds(self, mock):
        result = generate_helpstring_list(ALIASES, "", "the80s", 30)
        pack_helpstrings = result.get("the80s")
        self.assertEqual(len(pack_helpstrings), 10)
        self.assertEqual(pack_helpstrings[0].get("display"), "Come with me if you want to live")

    def test_limit_in_bounds(self, mock):
        result = generate_helpstring_list(ALIASES, "", "the80s", 3)
        pack_helpstrings = result.get("the80s")
        self.assertEqual(len(pack_helpstrings), 3)
        self.assertEqual(pack_helpstrings[0].get("display"), "Come with me if you want to live")

    def test_offset_bad_datatype(self, mock):
        result = 80
        try:
            result = generate_helpstring_list(ALIASES, "", "the80s", 0, "bad")
        except TypeError:
            pass
        self.assertEqual(result, 80)

    def test_offset_neg_out_of_bounds(self, mock):
        result = generate_helpstring_list(ALIASES, "", "the80s", 0, -1)
        pack_helpstrings = result.get("the80s")
        self.assertEqual(len(pack_helpstrings), 10)
        self.assertEqual(pack_helpstrings[0].get("display"), "Come with me if you want to live")

    def test_offset_pos_out_of_bounds(self, mock):
        result = generate_helpstring_list(ALIASES, "", "the80s", 0, 30)
        self.assertEqual(result, {})

    def test_offset_in_bounds(self, mock):
        result = generate_helpstring_list(ALIASES, "", "the80s", 0, 6)
        pack_helpstrings = result.get("the80s")
        self.assertEqual(len(pack_helpstrings), 4)
        self.assertEqual(pack_helpstrings[0].get("display"), "He's just like his {{relation}}.")
