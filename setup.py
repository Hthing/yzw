import setuptools

setuptools.setup(
    name="yzwspider",
    version="0.0.3",
    author="Hthing",
    author_email="hxcnly@gmail.com",
    description="A web spider for Chinese graduate student examination catalogue.",
    long_description="scrapy实现研招网专业目录爬虫，详见https://github.com/Hthing/yzw/tree/master/",
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
    install_requires = ["xlwt", 'pymysql', 'scrapy'] ,
    package_data = {
        'yzwspider': [ 'scrapy.cfg'],
    },
)