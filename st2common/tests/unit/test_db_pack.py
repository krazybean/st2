# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the 'License'); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from st2common.models.db.pack import PackDB
from st2common.persistence.pack import Pack

from st2tests import DbTestCase

from tests.unit.base import BaseDBModelCRUDTestCase


class PackDBModelCRUDTestCase(BaseDBModelCRUDTestCase, DbTestCase):
    model_class = PackDB
    persistance_class = Pack
    model_class_kwargs = {
        'name': 'Yolo CI',
        'ref': 'yolo_ci',
        'description': 'YOLO CI pack',
        'version': '0.1.0',
        'author': 'Volkswagen',
        'path': '/opt/stackstorm/packs/yolo_ci/'
    }
    update_attribute_name = 'author'

    def test_path_none(self):
        PackDBModelCRUDTestCase.model_class_kwargs = {
            'name': 'Yolo CI',
            'ref': 'yolo_ci',
            'description': 'YOLO CI pack',
            'version': '0.1.0',
            'author': 'Volkswagen'
        }
        super(PackDBModelCRUDTestCase, self).test_crud_operations()
