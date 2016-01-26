from setuptools import setup, find_packages

exec(open('react/version.py').read())

setup(
    name='react',
    description='Generate fragments of a molecule using smirks',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/3D-e-Chem/python-modified-tanimoto',
    author='Stefan Verhoeven',
    author_email='s.verhoeven@esciencecenter.nl',
    install_requires=['nose', 'coverage', 'mock'],
    entry_points={
        'console_scripts': [
            'react=react.script:main',
        ],
    },
    license='Apache',
    classifiers=[
        'License :: OSI Approved :: Apache Software License'
    ]
)