from setuptools import setup, find_packages

setup(
    name='logpose',  # Required
    version='0.0.1.beta2',  # Required
    description='A python log library for data science',  # Required
    long_description='Logpose is a log library for Data Science, suitable for ML prototyping and jupyter projects in general.\n'+
        'Logpose generates YAML files to track and benchmark parameters in simulations.',  # Optional
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
    install_requires=['pandas', 'pyyaml']  # Optional
)