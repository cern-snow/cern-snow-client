# coding: utf-8

from record import Record
from record import RecordQuery
from task import Task

package_table = 'incident'


class Incident(Task):

    def __init__(self, session, values={}):
        Record.__init__(self, session, package_table, values=values)


class IncidentQuery(RecordQuery):

    def __init__(self, session):
        RecordQuery.__init__(self, session, package_table)
