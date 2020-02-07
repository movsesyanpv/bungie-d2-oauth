import setuptools
import re

with open('bungied2auth/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bungie-d2-oauth",
    version=version,
    author="Pavel Movsesian",
    author_email="movsesyanpv1995@live.com",
    description="Get your Bungie auth tokens",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/movsesyanpv/bungie-d2-oauth",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Flask==1.0.2',
        'setuptools',
        'requests>=2.20.0'
      ],
    python_requires='>=3.6',
)
