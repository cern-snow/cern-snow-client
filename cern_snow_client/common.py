# coding: utf-8


class SnowClientException(Exception):
    pass


class TableClassMapping(object):
    __table_class_mapping = None

    @classmethod
    def get(cls):
        if not cls.__table_class_mapping:
            from task import Task
            from incident import Incident

            cls.__table_class_mapping = {
                'task': {'class': Task, 'can_be_inserted': False},
                'incident': {'class': Incident, 'can_be_inserted': True}
            }

        return cls.__table_class_mapping
