from setuptools import setup

setup(
    name='StakkrComposer',
    version='3.5',
    packages=['composer'],
    entry_points='''
        [stakkr.plugins]
        composer=composer.core:composer
    '''
)
