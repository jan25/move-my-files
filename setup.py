from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='move-my-files',
    version='0.2.4',
    description='CLI tools to organize files on your computer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jan25/move-my-files',
    author='Abhilash Gnan',
    author_email='abhilashgnan@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(where='.', exclude=['tests']),
    package_dir={'': '.'},
    python_requires='>=3.5, <4',
    install_requires=[
        'watchdog',
        'Click',
        'pyyaml',
    ],
    extras_require={
        'dev': [
            'pytest',
            'tox',
        ]
    },
    entry_points={
        'console_scripts': [
            'mmf=app.cli:mmf',
        ],
    },
)
