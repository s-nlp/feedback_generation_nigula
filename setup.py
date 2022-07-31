from setuptools import setup, find_packages
from setuptools.command.install import install
import os

description = "feedback_generation_nigula: the model for generating feedback comments  " \
              " to the English sentences with pre-defined error-spans."
long_description = description
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

# https://discuss.dizzycoding.com/post-install-script-with-python-setuptools/
def _post_install():
    python3 -m spacy download en_core_web_md

class spacy_loader(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)
setup(
    name='feedback_generation_nigula',
    version='0.0.0',
    license='Apache',
    author="Nikolay babakov",
    author_email='bbkhse@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url='https://github.com/skoltech-nlp/feedback_generation_nigula',
    install_requires=[
          'transformers>=4.13.0', 'torch', 'spacy'
      ],
    cmdclass={'install': spacy_loader},
)