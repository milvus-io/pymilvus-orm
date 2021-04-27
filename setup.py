import pathlib
import setuptools
import io
import re

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

with io.open("pymilvus_orm/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

requirements = []
with open("requirements.txt", 'r') as f:
    for line in f.readlines():
        requirements.append(line.strip())

setuptools.setup(
    name="pymilvus-orm",
    version=version,
    description="Python ORM Sdk for Milvus(>= 2.0)",
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/milvus-io/pymilvus-orm.git',
    license="Apache-2.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.6'
)
