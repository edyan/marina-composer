from setuptools import setup

setup(
    name='StakkrComposer',
    version='3.2',
    packages=['composer'],
    entry_points='''
        [stakkr.plugins]
        composer=composer.core:composer
    '''
)
