from distutils.core import setup

setup(
    name='role',
    version='0.1',
    py_modules=['role'],
    entry_points='''
        [console_scripts]
        role=role.cli:cli
    ''',
)