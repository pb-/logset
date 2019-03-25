from setuptools import setup, find_packages

setup(
    name='logset',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'logset = logset.sync:run',
        ],
    },
)
