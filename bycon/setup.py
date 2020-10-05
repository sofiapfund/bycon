from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name = 'bycon',
     version = '0.01',
     description = 'a Python-based environment for the Beacon v2 genomics API',
     long_description = readme(),
     license = 'MIT',
     url='https://github.com/progenetix/bycon',
     author = 'baudisgroup',
     author_email = 'bg@progenetix.org',
     classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
        ],
    keywords = 'GA4GH Beacon genomics API',
    packages = ['bycon'],
    install_requires = [
        'pymongo==3.11.0',
        'PyYAML==5.3.1'
        ],
    python_requires = '>=3.6',
    include_package_data = True
)