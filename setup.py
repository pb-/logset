from setuptools import setup, find_packages

setup(
    name='logset',
    packages=find_packages(),
    install_requires=[
        'flask',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'logset-sync = logset.sync:run',
        ],
    },
)
