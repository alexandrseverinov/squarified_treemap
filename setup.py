from setuptools import setup
import os

base_dir = os.path.dirname(__file__)

about = {}
with open(os.path.join(base_dir, "lib", "__about__.py")) as f:
    exec(f.read(), about)

setup(
    name=about["__title__"],
    version=about["__version__"],
    url=about["__url__"],
    author="Aleksandr Severinov",
    author_email="aleksandr.severinov@phystech.edu",
    description="Python implementation of the squarified treemap layout algorithm",
    packages=['squarified_treemap'],
    package_dir={'squarified_treemap': 'lib'},
    install_requires=[]
)
