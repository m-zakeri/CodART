"""
CodART setup script

"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codart",  # Replace with your own username
    version="0.2.3dev",
    author="Morteza Zakeri",
    author_email="m-zakeri@live.com",
    description="CodART: Free source code automated refactoring toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/m-zakeri/CodART",

    project_urls={
        "Bug Tracker": "https://github.com/m-zakeri/CodART/issues",
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    package_dir={
        'codart': 'codart',
        'codart.gen': 'codart.gen',
        'codart.metrics': 'codart.metrics',
        'codart.refactoring_design_patterns': 'codart.refactoring_design_patterns',
        'codart.refactorings': 'codart.refactorings',
        'codart.sbse': 'codart.sbse',
        'codart.smells': 'codart.smells',
        'codart.utility': 'codart.utility',
        'codart.visualization': 'codart.visualization',
    },

    packages=setuptools.find_packages(
        include=
        [
            'codart',
            'codart.*'
            'codart.gen',
            'codart.gen.*',
            'codart.metrics',
            'codart.metrics.*',
            'codart.refactoring_design_patterns',
            'codart.refactoring_design_patterns.*',
            'codart.refactorings',
            'codart.refactorings.*',
            'codart.sbse',
            'codart.sbse.*',
            'codart.smells',
            'codart.smells.*',
            'codart.utility',
            'codart.utility.*',
            'codart.visualization',
            'codart.visualization.*',
        ]
    ),

    python_requires=">=3.9",
)
