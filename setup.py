from setuptools import setup, find_packages

setup(
    name='parse_trisigma',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "camelot-py",
        "opencv-python",
        "ghostscript",
        "pandas",
        "numpy",
        "geopandas",
        "shapely",
        "matplotlib"
    ],
)