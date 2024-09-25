from odoo import fields, models

class Target(models.Model):
    _name = 'faker.target'

    name = fields.Char(string='Name of the generator')
    model_id = fields.Many2one('ir.model', string='Target model')
    field_ids = fields.One2many('faker.target.fields', 'target_id', string='Fields')