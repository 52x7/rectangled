from setuptools import setup, find_packages

setup(name="Rectangled",
	  packages=find_packages(),
	  install_requres=["pillow", "github3.py"],
	  entry_points={'console_scripts': ['rectangled = rectangled:main']})