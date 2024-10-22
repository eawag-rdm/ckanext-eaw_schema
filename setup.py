from setuptools import setup, find_packages
from pathlib import Path

# Path to the current file
here = Path(__file__).resolve().parent

# Get the long description from the README.md file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='ckanext-eaw_schema',
    version='0.0.1',
    description='Eawag dataset schema. Builds on ckanext-scheming and ckanext-repeating.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/eawag-rdm/ckanext-eaw_schema',

    author='Christian Foerster',
    author_email='Christian.Foerster@eawag.ch',

    license='AGPL-3.0-or-later',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],

    keywords='CKAN Eawag dataset schema custom',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    namespace_packages=['ckanext'],

    python_requires='>=3.7',
    install_requires=[
        # Dependencies should be listed in a `requirements.txt` file.
    ],

    include_package_data=True,
    package_data={},

    data_files=[],

    entry_points={
        'ckan.plugins': [
            'eaw_schema=ckanext.eaw_schema.plugin:EawSchemaPlugin',
        ],
        'babel.extractors': [
            'ckan = ckan.lib.extract:extract_ckan',
        ],
    },

    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    },
)

