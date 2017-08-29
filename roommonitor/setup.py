from setuptools import setup

setup(
    name='roommonitor',
    packages=['package_msgraph'],
    include_package_data=True,
    install_requires=[
        'flask',
    ]
)