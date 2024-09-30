from odoo import fields, models, api
from odoo.tools import get_lang

class Generator(models.Model):
    _name = 'faker.generator'
    _description = 'Generators of fake data for each model'

    name = fields.Char(string='Name')
    model_id = fields.Many2one('ir.model', string='Model')
    field_ids = fields.One2many('faker.generator.fields', 'generator_id', string='Fields')

    def _default_faker_locale(self):
        return get_lang(self.env)

    faker_locale = fields.Many2one('res.lang', string='Faker locale', default=_default_faker_locale)

    def generate(self):
        generated = {}
        for field in self.field_ids:
            generated[field.field_id.name] = field.generate()
        return generated

    def generate_and_save(self):
        generated = self.generate()
        self.env[self.model_id.model].create(generated)