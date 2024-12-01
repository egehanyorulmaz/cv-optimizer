from setuptools import setup, find_packages

setup(
    name="src",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pdfplumber",
        "pypdf",
        "python-dotenv",
        "openai",
    ],
    python_requires=">=3.11",
)
