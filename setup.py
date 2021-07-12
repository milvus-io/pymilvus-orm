import pathlib
import setuptools
import re

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

requirements = [
        "pymilvus==2.0.0rc2",
        "pandas==1.1.5; python_version<'3.7'",
        "pandas==1.2.4; python_version>'3.6'",
    ]

extras_require={
        'test': [
            'sklearn==0.0',
            'pytest==5.3.4',
            'pytest-cov==2.8.1',
            'pytest-timeout==1.3.4',
        ],
        'dev': [
            'sklearn==0.0',
            'pylint==2.4.4',
        ],
        'doc': [
            'mistune==0.8.4',
            'm2r==0.2.1',
            'Sphinx==2.3.1',
            'sphinx-copybutton==0.3.1',
            'sphinx-rtd-theme==0.4.3',
            'sphinxcontrib-applehelp==1.0.1',
            'sphinxcontrib-devhelp==1.0.1',
            'sphinxcontrib-htmlhelp==1.0.2',
            'sphinxcontrib-jsmath==1.0.1',
            'sphinxcontrib-qthelp==1.0.2',
            'sphinxcontrib-serializinghtml==1.1.3',
            'sphinxcontrib-prettyspecialmethods',
        ]
}

setuptools.setup(
    name="pymilvus-orm",
    author='Milvus Team',
    author_email='milvus-team@zilliz.com',
    setup_requires=['setuptools_scm'],
    use_scm_version={'local_scheme': 'no-local-version'},
    description="Python ORM Sdk for Milvus(>= 2.0)",
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/milvus-io/pymilvus-orm.git',
    license="Apache-2.0",
    packages=setuptools.find_packages(),
    dependency_links=[
        'https://test.pypi.org/simple/pymilvus',
    ],
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.6'
)
