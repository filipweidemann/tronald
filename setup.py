import setuptools

"""
with open("README.md", "r") as readme:
    long_description = readme.read()
"""

setuptools.setup(
    name="tronald",
    version="0.1.2",
    author="Filip Weidemann",
    author_email="filip.weidemann@outlook.de",
    description="CLI for getting remote PostgreSQL dumps out of containers onto your machine.",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/filipweidemann/tronald",
    packages=["tronald"],
    entry_points={"console_scripts": ["tronald = tronald.__main__:cli"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
