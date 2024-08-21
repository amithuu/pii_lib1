from setuptools import setup, find_packages

# setup()

setup(
    name='pii_library',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['Django >= 5.1'],
    description='A Django app to perform PII_Data security.',
    author='Amith Kulkarni',
    author_email='amith@rhythmflows.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9.11',
)
