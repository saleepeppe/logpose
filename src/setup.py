from setuptools import setup, find_packages

setup(
    name='logpose',  # Required
    version='0.0.1.dev2',  # Required
    description='A python log library',  # Required
    long_description='Log library for python (suitable for prototyping and jupyter projects in general).\n'+
        'Logpose generates YAML files to track each simulation run.',  # Optional
    url='https://github.com/saleepeppe/logpose',  # Optional
    author='Giuseppe Savino',  # Optional
    author_email='giuseppe.savino@outlook.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='development logging',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    install_requires=['pandas', 'pyyaml'],  # Optional
    # project_urls={  # Optional
    #     'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
    #     'Funding': 'https://donate.pypi.org',
    #     'Say Thanks!': 'http://saythanks.io/to/example',
    #     'Source': 'https://github.com/pypa/sampleproject/',
    # },
)