# coding: utf-8

from record import Record
from record import RecordQuery

package_table = 'task'


class Task(Record):

    def __init__(self, session, values={}):
        Record.__init__(self, session, package_table, values=values)

    def add_comment(self, comment):
        # TODO: Finish this method
        pass

    def add_work_note(self, work_note):
        # TODO: Finish this method
        pass

    def resolve(self, comment, close_code):
        # TODO: Finish this method
        pass


class TaskQuery(RecordQuery):

    def __init__(self, session):
        RecordQuery.__init__(self, session, package_table)
