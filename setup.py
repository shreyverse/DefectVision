from setuptools import setup, find_packages

setup(
    name="defectvision",
    version="1.0.0",
    author="Rohit (Computer Vision Project)",
    description="DefectVision: Automated Industrial Surface Defect Detection & Quality Inspection System",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "scikit-image>=0.20.0",
        "matplotlib>=3.7.0",
        "reportlab>=3.6.0"
    ],
    entry_points={
        "console_scripts": [
            "defectvision=src.cli.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
)
