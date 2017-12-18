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
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with the cern-snow-client library.  If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

from record import Record
from record import RecordQuery
from task import Task

package_table = 'u_request_fulfillment'


class Request(Task):
    """
        The class Task has all the methods of the Record and Task classes,
        plus some extra methods.

        Args:
            session (SnowRestSession): a cern_snow_client.session.SnowRestSession object, which will be used
                to authenticate and communicate with ServiceNow
            values (:obj:`dict`, optional): initial values for the record

        Examples:

            Inserting a new incident:

            >>> req = Request(s)  # s is a SnowRestSession object
            >>> req.short_description = "New request"
            >>> req.u_business_service = 'e85a3f3b0a0a8c0a006a2912f2f352d1'  # Service Element "ServiceNow"
            >>> req.u_functional_element = '579fb3d90a0a8c08017ac8a1137c8ee6'  # Functional ELement "ServiceNow"
            >>> req.comments = "Initial description"
            >>> req.insert()

            Adding a comment to an incident after getting it:

            >>> req = Request(s)  # s is a SnowRestSession object
            >>> if req.get('c69bd7324fdabac07db7d3ef0310c73b'):
            >>>     req.add_comment('New comment')  # will immediately add a new comment in ServiceNow

            Resolving an Incident for which we know the number:

            >>> req = Request(s)  # s is a SnowRestSession object
            >>> req.resolve('New comment', close_code='Not authorised', key=('number', 'RQF0746626'))
        """

    def __init__(self, session, values=None):
        Record.__init__(self, session, package_table, values=values)


class RequestQuery(RecordQuery):

    def __init__(self, session):
        RecordQuery.__init__(self, session, package_table)