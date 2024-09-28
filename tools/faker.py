from faker import Faker

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

def clear_faker_fields(record):
    record.faker_generator = None
    record.faker_locale = None

def get_faker(record):
    if record.value_type != 'faker':
        raise Exception('A faked value cannot be created for this {} field'.format(record.value_type))

    if not record.faker_generator:
        return None

    faker = Faker(record.faker_locale)
    generator = getattr(faker, record.faker_generator)
    return generator()