import logging
from odoo import fields, models, api

_logger = logging.getLogger(__name__)

class Generator(models.Model):
    _name = 'faker.generator'
    _description = 'Generators of fake data for each model'

    name = fields.Char(string='Name')
    model_id = fields.Many2one('ir.model', string='Model')
    field_ids = fields.One2many('faker.generator.fields', 'generator_id', string='Fields')

    def generate(self):
        generated = {}

        for field in self.field_ids:
            generated[field.field_id.name] = field.generate()

        return generated

    def generate_and_save(self):
        generated = self.generate()
        self.env[self.model_id.model].create(generated)
        self.env.cr.commit()