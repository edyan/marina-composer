from setuptools import setup

setup(
    name='StakkrComposer',
    version='1.0',
    packages=['composer'],
    entry_points='''
        [stakkr.plugins]
        composer=composer.core:composer
    '''
)
