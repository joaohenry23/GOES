import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()

setuptools.setup(
   name="GOES",
   version="3.2",
   author="Joao Henry Huamán Chinchay",
   author_email="joaohenry23@gmail.com",
   description="Python packages to download and manipulate GOES-16/17 data.",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/joaohenry23/GOES",
   license='BSD 3-Clause',
   packages=setuptools.find_packages(),
   classifiers=[
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: BSD License",
      "Operating System :: OS Independent",
   ],
   python_requires='>=2.7',
   install_requires=[
      "numpy",
      "requests",
      "s3fs",
      "pyproj",
      "netCDF4",
   ],
)
