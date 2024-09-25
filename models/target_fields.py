from faker import Faker
from odoo import fields, models, api

def get_value_types():
    return [
        ('faker', 'Faker'),
        ('constant', 'Constant'),
        ('random_record', 'Random record'),
    ]

def get_faker_generators():
    return [(method, method) for method in dir(Faker()) if not method.startswith("_")]

class TargetFields(models.Model):
    _name = 'faker.target.fields'

    target_id = fields.Many2one('faker.target', string='Target', readonly=True)
    model = fields.Char(string='Model', readonly=True)
    field_id = fields.Many2one('ir.model.fields', string='Field', required=True, domain="[('model', '=', model), ('store', '=', True)]")
    value_type = fields.Selection(get_value_types(), string='Type', required=True)
    faker_generator = fields.Selection(get_faker_generators(), string='Faker generator')
    faker_locale = fields.Many2one('res.lang', string='Faker locale')
    faker_example = fields.Char(compute='get_faker_example', string='Faker example')

    @api.onchange('value_type', 'faker_locale', 'faker_generator')
    def get_faker_example(self):
        for record in self:
            if not record.value_type == 'faker':
                record.faker_generator = None
                record.faker_locale = None
                record.faker_example = None
                continue
            if not record.faker_generator:
                continue
            faker = Faker(self.faker_locale)
            generator = getattr(faker, record.faker_generator)
            record.faker_example = generator()

    @api.onchange('target_id')
    def update_model_on_target_change(self):
        for record in self:
            self.model = self.target_id.model_id.model