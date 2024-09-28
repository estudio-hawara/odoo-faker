import logging
from odoo import fields, models, api

_logger = logging.getLogger(__name__)

class Target(models.Model):
    _name = 'faker.target'

    name = fields.Char(string='Name of the generator')
    model_id = fields.Many2one('ir.model', string='Target model')
    field_ids = fields.One2many('faker.target.fields', 'target_id', string='Fields')

    def generate(self):
        generated = {}

        for field in self.field_ids:
            generated[field.field_id.name] = field.generate()

        return generated

    def generate_and_save(self):
        generated = self.generate()
        self.env[self.model_id.model].create(generated)
        self.env.cr.commit()