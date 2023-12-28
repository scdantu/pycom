
from setuptools import setup, find_packages

with open('pycom/version.txt') as f:
    version = f.read().strip()

extras_require = {
    'flask': ['Flask'],
    'flask-caching': ['Flask-Caching'],
    'flask-parameter-validation': ['Flask-Parameter-Validation'],
    'werkzeug': ['Werkzeug'],
    'requests': ['Requests'],
    'logomaker': ['logomaker']
}

setup(
    name='pycom',
    version=version,
    description='Python library PyCoM for interacting with the database of Coevolution matrices of proteins (PyCoMdb)',
    author='Philipp Bibik, Sarath Chandra Dantu',
    author_email='sarath.dantu@brunel.ac.uk',
    url='https://github.com/scdantu/pycom',
    license_files='LICENSE.txt',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'h5py'
    ],
    extras_require=extras_require,
    python_requires='>=3.8',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Database',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent'
    ]
)
