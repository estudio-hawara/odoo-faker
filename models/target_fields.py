from faker import Faker
from odoo import fields, models, api
from odoo.tools import SQL

def get_value_types():
    return [
        ('faker', 'Faker'),
        ('constant', 'Constant'),
        ('random_record', 'Random record'),
    ]

def get_faker_generators():
    return [
        (method, method)
        for method in dir(Faker())
        if not method.startswith("_") and
            not method.startswith("get_") and
            not method.startswith("py") and
            not method.startswith("set_") and
            method not in [
                "add_provider", "binary", "cache_pattern", "del_arguments",
                "enum", "factories", "format", "generator_attrs", "get_formatter",
                "image", "items", "locales", "optional", "paragraphs", "parse",
                "passport_dates", "profile", "provider", "providers", "random",
                "random_choices", "random_letters", "random_sample", "seed",
                "seed_instance", "seed_locale", "sentences", "simple_profile",
                "tar", "texts", "time_series", "unique", "weights", "words",
                "zip"
            ]
        ]

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

    def _clear_faker_fields(self, record):
        if not record.value_type == 'faker':
            record.faker_generator = None
            record.faker_locale = None
            record.example = None

    def _clear_constant_fields(self, record):
        if not record.value_type == 'constant':
            record.constant_value = None
            record.example = None

    def _clear_random_record_fields(self, record):
        if not record.value_type == 'random_record':
            record.example = None

    def _get_faker_example(self, record):
        if not record.value_type == 'faker' or not record.faker_generator:
            return

        faker = Faker(record.faker_locale)
        generator = getattr(faker, record.faker_generator)
        value = generator()

        self._serialize_example(record, value)

    def _get_constant_example(self, record):
        if not record.value_type == 'constant':
            return

        self._serialize_example(record, record.constant_value)

    def _get_random_record_example(self, record):
        if not record.value_type == 'random_record':
            return

        related_table = record.field_id.relation.replace('.', '_')
        query_template = 'select id from %s order by RANDOM() limit 1'
        query = SQL(query_template, SQL.identifier(related_table))
        
        self.env.cr.execute(query)
        result = self.env.cr.fetchone()

        if result == None:
            return

        self._serialize_example(record, result[0])

    def _serialize_example(self, record, value):
        if value == None:
            record.example = None
            return

        if record.field_id.ttype in ('integer', 'many2one'):
            record.example = int(value)
            return

        if record.field_id.ttype == 'boolean':
            if str(value).lower() in ['true', '1']:
                record.example = 'True'
            if str(value).lower() in ['false', '0']:
                record.example = 'False'
            return

        if record.field_id.ttype in ['char', 'text']:
            record.example = value

    @api.onchange('value_type', 'constant_value', 'faker_locale', 'faker_generator')
    def get_example(self):
        for record in self:
            self._clear_faker_fields(record)
            self._clear_constant_fields(record)
            self._clear_random_record_fields(record)
            self._get_faker_example(record)
            self._get_constant_example(record)
            self._get_random_record_example(record)

    @api.onchange('target_id')
    def update_model_on_target_change(self):
        for record in self:
            self.model = self.target_id.model_id.model