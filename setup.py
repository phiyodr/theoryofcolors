import setuptools
from theoryofcolors import __version__

print(setuptools.find_packages())


with open("README.md", "r") as file:
    long_description = file.read()

with open("requirements.txt") as file:
    required = file.read().splitlines()
    
setuptools.setup(
    name="theoryofcolors",
    version=__version__,
    author="Philipp J. Roesch",
    author_email="phiyodr@gmail.com",
    description="Theory Of Colors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phiyodr/theoryofcolors",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.csv", "*.json"]},
    install_requires=[
            "sentence-transformers",
            "scikit-learn",
            "pandas",
            "numpy",
            "string-color",
            "matplotlib"
        ]
    )
