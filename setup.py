import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yzw_spider",
    version="0.0.1",
    author="Hthing",
    author_email="hxcnly@gmail.com",
    description="A web spider for Chinese graduate student examination catalogue.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hthing/yzw/tree/master/",
    license = "MIT Licence",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)