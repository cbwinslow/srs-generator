from setuptools import setup, find_packages

setup(
    name="srs-generator",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask>=2.3.3",
        "python-dotenv>=1.0.0",
        "gunicorn>=21.2.0",
        "openai>=1.14.0",
    ],
)
