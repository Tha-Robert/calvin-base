# -*- coding: utf-8 -*-

# Copyright (c) 2017 Ericsson AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from calvin.runtime.south.calvinsys import base_calvinsys_object

class MockInput(base_calvinsys_object.BaseCalvinsysObject):
    """
    MockInput - Mocked input device.
    """

    init_schema = {
        "type": "object",
        "properties": {
            "data": {
                "description": "Data to return in read",
                "type": "array"
            }
        }
    }

    can_read_schema = {
        "description": "Returns True if data can be read, otherwise False",
        "type": "boolean"
    }

    read_schema = {
        "description": "Get data"
    }

    def init(self, data, **kwargs):
        self.data = list(data)

    def can_read(self):
        return len(self.data) > 0

    def read(self):
        return self.data.pop()

    def close(self):
        self.data = []
