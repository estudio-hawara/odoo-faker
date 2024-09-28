from odoo.tools import SQL

def get_random_record(record, cr):
    if not record.value_type == 'random_record':
        raise('A random record cannot be created for this {} field'.format(record.value_type))

    related_table = record.field_id.relation.replace('.', '_')
    query_template = 'select id from %s order by RANDOM() limit 1'
    query = SQL(query_template, SQL.identifier(related_table))
    
    cr.execute(query)
    result = cr.fetchone()

    if result == None:
        return None

    return result[0]