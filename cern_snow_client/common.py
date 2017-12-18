# -*- coding: utf-8 -*-
#
# This file is part of the cern-snow-client library.
# Copyright (c) 2017 CERN
# Authors:
#  - James Clerc <james.clerc@cern.ch> <james.clerc@epitech.eu>
#  - David Martin Clavo <david.martin.clavo@cern.ch>
#
# The cern-snow-client library is free software; you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# The cern-snow-client library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with the cern-snow-client library.  If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


class SnowClientException(Exception):
    pass


class TableClassMapping(object):
    __table_class_mapping = None

    @classmethod
    def get(cls):
        if not cls.__table_class_mapping:
            from task import Task
            from incident import Incident
            from request import Request

            cls.__table_class_mapping = {
                'task': {'class': Task, 'can_be_inserted': False, 'is_base_table': True},
                'incident': {'class': Incident, 'can_be_inserted': True},
                'u_request_fulfillment': {'class': Request, 'can_be_inserted': True}
            }

        return cls.__table_class_mapping
