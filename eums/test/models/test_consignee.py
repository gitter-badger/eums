from unittest import TestCase

from mock import patch
from django.conf import settings

from eums.models import Consignee
from eums.test.factories.consignee_factory import ConsigneeFactory
from eums.rapid_pro.fake_response import FakeResponse


class ConsigneeTest(TestCase):
    def test_should_have_all_expected_fields(self):
        fields_in_consignee = Consignee()._meta._name_map

        for field in ['name', 'contact_person_id']:
            self.assertIn(field, fields_in_consignee)

    def test_string_representation_of_consignee_is_consignee_name(self):
        test_consignee = 'Test Consignee'
        consignee = Consignee(name=test_consignee)
        self.assertEqual(test_consignee, str(consignee))

    @patch('requests.get')
    def test_should_build_contact_with_details_from_contacts_service(self, mock_get):
        contact_id = '54335c56b3ae9d92f038abb0'
        fake_contact_json = {'firstName': "test", 'lastName': "user1", 'phone': "+256 782 443439",
                             '_id': contact_id}
        fake_response = FakeResponse(fake_contact_json, 200)
        consignee = ConsigneeFactory(contact_person_id=contact_id)
        mock_get.return_value = fake_response

        contact = consignee.build_contact()

        self.assertEqual(contact, fake_contact_json)
        self.assertEqual(consignee.contact, contact)
        mock_get.assert_called_with("%s%s/" % (settings.CONTACTS_SERVICE_URL, contact_id))

    def test_should_log_error_if_contact_error_is_encountered_when_fetching_contact_on_build_contact(self):
        pass

    @patch('requests.get')
    def test_should_not_fetch_contact_from_contacts_service_if_contact_was_already_built(self, mock_get):
        contact_id = '54335c56b3ae9d92f038abb1'
        fake_contact_json = {'firstName': "test", 'lastName': "user1", 'phone': "+256 782 443439",
                             '_id': contact_id}
        fake_response = FakeResponse(fake_contact_json, 200)
        consignee = ConsigneeFactory(contact_person_id=contact_id)
        mock_get.return_value = fake_response

        consignee.build_contact()
        consignee.build_contact()

        mock_get.assert_called_with("%s%s/" % (settings.CONTACTS_SERVICE_URL, contact_id))

    def tearDown(self):
        Consignee.objects.all().delete()
