from setuptools import setup, find_packages


setup(
    name='wtgui',
    version='0.0.1',
    description='A pure Python GUI app to run subsea pipeline wall thickness calculations',
    author='Ben Randerson',
    author_email='ben.m.randerson@gmail.com',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': [
            'wt=wtgui.main:main'
        ]
    }
)
