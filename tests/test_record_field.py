# coding: utf-8

import unittest
from cern_snow_client.record import RecordField
from cern_snow_client.common import SnowClientException


class TestRecordBasicAuthentication(unittest.TestCase):

    def test_record_field_str(self):
        rf = RecordField('text')

        self.assertEquals(rf, 'text')
        self.assertEquals(rf, u'text')
        self.assertIsInstance(rf, unicode)
        self.assertEquals(rf + ' text2', u'text text2')

        self.assertEquals(rf.get_value(), 'text')
        self.assertEquals(rf.get_value(), u'text')
        self.assertIs(type(rf.get_value()), unicode)

        self.assertEquals(rf.get_display_value(), 'text')
        self.assertEquals(rf.get_display_value(), u'text')
        self.assertIs(type(rf.get_display_value()), unicode)

        self.assertFalse(rf.is_reference())
        self.assertIsNone(rf.get_referenced_table())

    def test_record_field_unicode(self):
        rf = RecordField(u'text')

        self.assertEquals(rf, 'text')
        self.assertEquals(rf, u'text')
        self.assertIsInstance(rf, unicode)
        self.assertEquals(rf + ' text2', u'text text2')

        self.assertEquals(rf.get_value(), 'text')
        self.assertEquals(rf.get_value(), u'text')
        self.assertIs(type(rf.get_value()), unicode)

        self.assertEquals(rf.get_display_value(), 'text')
        self.assertEquals(rf.get_display_value(), u'text')
        self.assertIs(type(rf.get_display_value()), unicode)

        self.assertFalse(rf.is_reference())
        self.assertIsNone(rf.get_referenced_table())

    def test_record_field_dict_no_link(self):
        rf = RecordField({
            'value': u'some_value',
            'display_value': u'some_display_value',
        })

        self.assertEquals(rf, 'some_value')
        self.assertEquals(rf, u'some_value')
        self.assertIsInstance(rf, unicode)
        self.assertEquals(rf + ' some_value_2', u'some_value some_value_2')

        self.assertEquals(rf.get_value(), 'some_value')
        self.assertEquals(rf.get_value(), u'some_value')
        self.assertIs(type(rf.get_value()), unicode)

        self.assertEquals(rf.get_display_value(), 'some_display_value')
        self.assertEquals(rf.get_display_value(), u'some_display_value')
        self.assertIs(type(rf.get_display_value()), unicode)

        self.assertFalse(rf.is_reference())
        self.assertIsNone(rf.get_referenced_table())

    def test_record_field_dict_with_link(self):
        rf = RecordField({
            "value": "579fb3d90a0a8c08017ac8a1137c8ee6",
            "display_value": "ServiceNow",
            "link": "https://cerntest.service-now.com/api/now/v2/table/"
                    "u_cmdb_ci_functional_services/579fb3d90a0a8c08017ac8a1137c8ee6"
        })

        self.assertEquals(rf, '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(rf, u'579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertIsInstance(rf, unicode)
        self.assertEquals(rf + ' some_value_2', u'579fb3d90a0a8c08017ac8a1137c8ee6 some_value_2')

        self.assertEquals(rf.get_value(), '579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertEquals(rf.get_value(), u'579fb3d90a0a8c08017ac8a1137c8ee6')
        self.assertIs(type(rf.get_value()), unicode)

        self.assertEquals(rf.get_display_value(), 'ServiceNow')
        self.assertEquals(rf.get_display_value(), u'ServiceNow')
        self.assertIs(type(rf.get_display_value()), unicode)

        self.assertTrue(rf.is_reference())
        self.assertEquals(rf.get_referenced_table(), 'u_cmdb_ci_functional_services')

    def test_edge_cases(self):
        rf = RecordField(42)
        self.assertEquals(rf, u'42')
        self.assertEquals(rf.get_value(), u'42')
        self.assertEquals(rf.get_display_value(), u'42')

        rf = RecordField({'value': 42, 'display_value': 84})
        self.assertEquals(rf, u'42')
        self.assertEquals(rf.get_value(), u'42')
        self.assertEquals(rf.get_display_value(), u'84')

        rf = RecordField({'value': 42})
        self.assertEquals(rf, u'42')
        self.assertEquals(rf.get_value(), u'42')
        self.assertEquals(rf.get_display_value(), u'42')

        rf = RecordField({'display_value': 42})
        self.assertEquals(rf, u'42')
        self.assertEquals(rf.get_value(), u'42')
        self.assertEquals(rf.get_display_value(), u'42')

        rf = RecordField({})
        self.assertEquals(rf, '')
        self.assertEquals(rf.get_value(), '')
        self.assertEquals(rf.get_display_value(), '')

        rf = RecordField({'value': u'some_value'})
        self.assertEquals(rf, u'some_value')
        self.assertEquals(rf.get_value(), u'some_value')
        self.assertEquals(rf.get_display_value(), u'some_value')

        rf = RecordField({'display_value': u'some_value'})
        self.assertEquals(rf, u'some_value')
        self.assertEquals(rf.get_value(), u'some_value')
        self.assertEquals(rf.get_display_value(), u'some_value')


if __name__ == '__main__':
    unittest.main()  # for compatibility with Python2.6 unittest
