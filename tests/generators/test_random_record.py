from unittest.mock import MagicMock
from odoo.tests import TransactionCase, tagged
from odoo.addons.faker.generators.random_record import get_random_record

class TestRandomRecord(TransactionCase):
    def test_get_random_record(self):
        # Prepare
        field = self.env['faker.generator.fields'].new()
        field.value_type == 'random_record'
        field.field_id = self.env['faker.generator'].new()
        field.field_id.model = 'ir_model'

        cr = MagicMock()
        cr.execute.return_value = None
        cr.fetchone.return_value = [(1,)]

        # Act
        random_record = get_random_record(field, cr)

        # Assert
        query = SQL('select id from "ir_model" order by RANDOM() limit 1')
        cr.execute.assert_called_with(query)
        cr.fetchone.assert_called_with()
        assert random_record == 1