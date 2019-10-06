import setuptools

with open("README.md", "r") as fh:
   long_description = fh.read()

setuptools.setup(
   name="GOES",
   version="0.0.1.2",
   author="Joao Henry Huamán Chinchay",
   author_email="joaohenry23@gmail.com",
   description="Download and process data from GOES-16 and GOES-17",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://github.com/joaohenry23/",
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
      "s3fs",
   ],
)
