from faker import Faker
from odoo import fields, models, api
from odoo.addons.faker.generators.types import get_value_types, get_typed_value
from odoo.addons.faker.generators.constant import clear_constant_fields
from odoo.addons.faker.generators.faker import get_faker_generators, clear_faker_fields, get_faked_value
from odoo.addons.faker.generators.random_record import get_random_record

class GeneratorFields(models.Model):
    _name = 'faker.generator.fields'
    _description = 'Fields of each faker generator'

    generator_id = fields.Many2one('faker.generator', string='Generator', readonly=True)
    model = fields.Char(string='Model', readonly=True)
    field_id = fields.Many2one('ir.model.fields', string='Field', domain="[('model', '=', model), ('store', '=', True)]", ondelete='set null')
    value_type = fields.Selection(get_value_types(), string='Type', required=True)
    faker_generator = fields.Selection(get_faker_generators(), string='Faker generator')
    constant_value = fields.Char(string='Constant value')
    example = fields.Char(compute='get_example', string='Example')

    def generate(self):
        value = None

        if self.value_type == 'constant':
            value = self.constant_value

        if self.value_type == 'faker':
            value = get_faked_value(self)

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

    @api.onchange('generator_id')
    def update_model_on_generator_change(self):
        for record in self:
            self.model = self.generator_id.model_id.model