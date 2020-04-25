# GOES
Python packages to download and process data from GOES-16 and GOES-17.

# Requirements
- [numpy](https://numpy.org/)
- [s3fs](https://s3fs.readthedocs.io/en/latest/install.html)
- [pyproj](https://github.com/pyproj4/pyproj)



# Usage
See the next jupyter notebook examples.

- Download GOES16/GOES17 data from amazon ([example](https://github.com/joaohenry23/GOES/blob/master/examples/ex01.ipynb)).
- Make a plot of ABI's channels with [basemap](https://matplotlib.org/basemap/) ([example](https://github.com/joaohenry23/GOES/blob/master/examples/ex02.ipynb)).
- Make a plot of ABI's channels with [Cartopy](https://scitools.org.uk/cartopy/docs/latest/) ([example](https://github.com/joaohenry23/GOES/blob/master/examples/ex03.ipynb)).



# Installation
You can install GOES on Python 2 or 3 on Linux, Windows or other, using the following commands.
\
\
From PYPI using pip:
```
pip install GOES
```
\
From Github using clone.
```
clone https://github.com/joaohenry23/GOES.git
cd GOES
python setup.py install
```
\
Or also from github downloading **GOES-master.zip** and following the next commands.
```
unzip GOES-master.zip
cd GOES-master
python setup.py install
```
<br>

**Check if package was installed**

```
pip show GOES
```
<br>

**Update to the latest version**

```
pip install --upgrade GOES
```
<br>
<br>

# Support
If you have any questions, do not hesitate to write to:
```
joaohenry23@gmail.com

```
