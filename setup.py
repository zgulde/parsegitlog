import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parsegitlog",
    version="0.0.1",
    author="Zach Gulde",
    author_email="zachgulde@gmail.com",
    description="Get a representation of commits in a git repository as JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zgulde/parsegitlog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
