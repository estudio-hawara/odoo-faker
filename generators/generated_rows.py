from faker import Faker

def clear_generated_rows_fields(record):
    record.row_generator_id = None
    record.row_count = None

def get_generated_rows_value(record):
    if record.value_type != 'generated_rows':
        raise Exception('A generated row cannot be created for this {} field'.format(record.value_type))

    if not record.row_generator_id or not record.row_count:
        return None

    rows = []

    for _ in range(0, record.row_count):
        generated = record.row_generator_id.generate()
        rows.append((0, 0, generated))

    return rows