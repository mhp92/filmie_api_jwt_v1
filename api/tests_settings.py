from filmie_api.settings import *

MIGRATION_MODULES = {
    'auth': None,
    'contenttypes': None,
    'default': None,
    'sessions': None,

    'core': None,
    'profiles': None,
    'snippets': None,
    'scaffold_templates': None,
}


'''

How to use it?

in Terminal: python manage.py test --settings=api.tests_settings

'''