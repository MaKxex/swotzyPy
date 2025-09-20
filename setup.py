from setuptools import setup, find_packages

setup(
    name="swotzy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.24.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
    ],
    author="MaKxex",
    description="A Python wrapper for the Swotzy API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)