from faker import Faker
from odoo import fields, models, api
from ..tools.types import get_value_types, get_typed_value
from ..tools.constant import clear_constant_fields
from ..tools.faker import get_faker_generators, clear_faker_fields, get_faker
from ..tools.random_record import get_random_record

class TargetFields(models.Model):
    _name = 'faker.target.fields'

    target_id = fields.Many2one('faker.target', string='Target', readonly=True)
    model = fields.Char(string='Model', readonly=True)
    field_id = fields.Many2one('ir.model.fields', string='Field', domain="[('model', '=', model), ('store', '=', True)]", ondelete='set null')
    value_type = fields.Selection(get_value_types(), string='Type', required=True)
    faker_generator = fields.Selection(get_faker_generators(), string='Faker generator')
    faker_locale = fields.Many2one('res.lang', string='Faker locale')
    constant_value = fields.Char(string='Constant value')
    example = fields.Char(compute='get_example', string='Example')

    def generate(self):
        value = None

        if self.value_type == 'constant':
            value = self.constant_value

        if self.value_type == 'faker':
            value = get_faker(self)

        if self.value_type == 'random_record':
            value = get_random_record(self, self.env.cr)

        return get_typed_value(self, value)

    @api.onchange('value_type', 'constant_value', 'faker_locale', 'faker_generator')
    def get_example(self):
        for record in self:
            if record.value_type != 'constant':
                clear_constant_fields(record)

            if record.value_type != 'faker':
                clear_faker_fields(record)

            record.example = record.generate()

    @api.onchange('target_id')
    def update_model_on_target_change(self):
        for record in self:
            self.model = self.target_id.model_id.model