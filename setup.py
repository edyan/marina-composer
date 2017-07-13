from setuptools import setup

setup(
    name='MarinaComposer',
    version='1.0',
    packages=['composer'],
    entry_points='''
        [marina.plugins]
        composer=composer.core:composer
    '''
)
