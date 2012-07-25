"""Build and install the jabr package.

"""
from distutils.core import setup


setup(
    name = 'jabr',
    version = '1.0',
    description = 'Journal abbreviation finder.',
    author = 'Andrew Dawson',
    author_email = 'dawson@atm.ox.ac.uk',
    packages = ['jabr'],
    package_dir = {'jabr':'lib'},
    scripts = ['bin/jabr'],
)

