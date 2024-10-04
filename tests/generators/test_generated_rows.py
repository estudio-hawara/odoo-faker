from faker import Faker
from odoo.tests import TransactionCase, tagged
from odoo.addons.faker.generators.generated_rows import \
    clear_generated_rows_fields, \
    get_generated_rows_value

@tagged('faker')
class TestGeneratedRows(TransactionCase):
    def test_clear_generated_rows_fields(self):
        # Prepare
        field = self.env['faker.generator.fields'].new()
        field.row_generator_id = 1
        field.row_count_min = 1
        field.row_count_max = 2

        # Act
        clear_generated_rows_fields(field)

        # Assert
        assert not field.row_generator_id
        assert not field.row_count_min
        assert not field.row_count_max

    def test_get_generated_rows_value(self):
        pass