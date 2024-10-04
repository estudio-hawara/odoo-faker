from odoo import fields, models

class GeneratorWizard(models.TransientModel):
    _name = 'faker.generator.wizard'
    _description = 'Wizard to run a generation batch'

    def default_generator_id(self):
        context = self._context.copy()

        if 'generator_id' in context:
            return context['generator_id']

    generator_id = fields.Many2one('faker.generator', string='Generator', required=True, default=default_generator_id)
    records = fields.Integer(string='Number of records', required=True, default=100)

    def action_generate_records(self):
        for _ in range(self.records):
            self.generator_id.generate_and_save()
            self.env.cr.commit()