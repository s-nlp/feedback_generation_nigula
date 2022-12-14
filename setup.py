from setuptools import setup, find_packages
import os

description = "feedback_generation_nigula: the model for generating feedback comments  " \
              " to the English sentences with pre-defined error-spans."
long_description = description
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
    name='feedback_generation_nigula',
    packages = ['feedback_generation_nigula'],
    version='0.0.8',
    license='Apache',
    author="Nikolay babakov",
    author_email='bbkhse@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/skoltech-nlp/feedback_generation_nigula',
    install_requires=[
          'transformers', 'torch', 'spacy'
      ],
    package_data = {'feedback_generation_nigula':['data/*.txt']}
)