# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------------------
'''
Description: Creates python custom colors palette
Author: Joao Henry Huaman Chinchay
E-mail: joaohenry23@gmail.com
Created date: Mon, Sep 09, 2019
'''
#-----------------------------------------------------------------------------------------------------------------------------------
import numpy as np
#import math
import warnings
warnings.filterwarnings('ignore')
#-----------------------------------------------------------------------------------------------------------------------------------
def get_lonlat(X, Y, SatLon, SatHeight, Req, Rpol, fmt=np.float32):

   """
   Calculates the longitude and latitude of the center of the pixels of the satellite image, from the fixed
   grid East/West and North/South scanning angle in radians.
   This function is based on the equations from pages 21-22 of https://www.goes-r.gov/users/docs/PUG-L1b-vol3.pdf


   Parameters
   ----------
      X    : array_like
             A scalar 1-D array with the fixed grid East/West scanning angle in radians.

      Y    : array_like
             A scalar 1-D array with the fixed grid North/South scanning angle in radians.

      SatLon : float
               Longitude of satellite in the nadir.

      SatHeight : float
                  Height of satellite in meters.

      Req : float
            Semi major axis of earth.

      Rpol : float
            Semi minor axis of earth.

      fmt : dtype (optional)
            Format (dtype) of returns. Default value is np.float32


   Returns
   -------
      Lons : array_like
             A scalar 2-D array with the longitude of the center of the pixels of the satellite image.

      Lats : array_like
             A scalar 2-D array with the latitude of the center of the pixels of the satellite image.

   """

   H = SatHeight + Req
   X, Y = np.meshgrid(X[:], Y[:])
   lambda0 = (SatLon*np.pi)/180.0

   a = (np.sin(Y)**2.0) + (np.cos(Y)**2.0)*((np.cos(X)**2.0) + ((Req**2.0)/(Rpol**2.0))*(np.sin(X)**2.0))
   b = -2.0*H*np.cos(X)*np.cos(Y)
   c = (H**2.0)-(Req**2.0)
   rs = (-b-np.sqrt((b**2.0)-4.0*a*c))/(2.0*a)
   sx = rs*np.cos(X)*np.cos(Y)
   sy = -rs*np.sin(X)
   sz = rs*np.cos(X)*np.sin(Y)

   Lats = np.arctan(((Req**2.0)/(Rpol**2.0))*(sz/(np.sqrt(((H-sx)**2.0) + (sy**2.0)))))*(180.0/np.pi)
   Lons = (lambda0 - np.arctan(sy/(H-sx)))*(180.0/np.pi)

   Mask = np.where((Lons.mask==True)&(Lats.mask==True), True, False)
   Lons = np.array(np.where((Mask==True), -999.99, Lons), dtype=fmt)
   Lats = np.array(np.where((Mask==True), -999.99, Lats), dtype=fmt)

   return Lons, Lats;

#-----------------------------------------------------------------------------------------------------------------------------------
def midpoint_in_x(Field):

   Field = np.column_stack((Field, np.full([Field.shape[0],1],-999.99)))
   right = np.column_stack((Field[:,1:], np.full([Field.shape[0],1],-999.99)))
   left = np.column_stack((np.full([Field.shape[0],1],-999.99), Field[:,:-1]))
   left2 = np.column_stack((np.full([Field.shape[0],2],-999.99), Field[:,:-2]))

   midpoint = np.where((Field>-400.0)&(left<-400.0),Field-(right-Field)/2.0,-999.99)
   midpoint = np.where((Field>-400.0)&(left>-400.0),(left+Field)/2.0,midpoint)
   midpoint = np.where((Field<-400.0)&(left>-400.0),left+(left-left2)/2.0,midpoint)
   return midpoint;


def midpoint_in_y(Field):

   Field = np.vstack((Field, np.full([1,Field.shape[1]],-999.99)))
   lower = np.vstack((Field[1:,:], np.full([1,Field.shape[1]],-999.99)))
   upper = np.vstack((np.full([1,Field.shape[1]],-999.99), Field[:-1,:]))
   upper2 = np.vstack((np.full([2,Field.shape[1]],-999.99), Field[:-2,:]))

   midpoint = np.where((Field>-400.0)&(upper<-400.0),Field-(lower-Field)/2.0,-999.99)
   midpoint = np.where((Field>-400.0)&(upper>-400.0),(upper+Field)/2.0,midpoint)
   midpoint = np.where((Field<-400.0)&(upper>-400.0),upper+(upper-upper2)/2.0,midpoint)
   return midpoint;

#-----------------------------------------------------------------------------------------------------------------------------------
def get_lonlat_corners(Lons, Lats, fmt=np.float32):

   """
   Calculates corners of pixels of the satellite image, from the longitude and latitude of the center of the pixels.


   Parameters
   ----------
      Lons : array_like
             A scalar 2-D array with the longitude of the center of the pixels of the satellite image.

      Lats : array_like
             A scalar 2-D array with the latitude of the center of the pixels of the satellite image.

      fmt : dtype (optional)
            Format (dtype) of returns. Default value is np.float32


   Returns
   -------
      Lons : array_like
             A scalar 2-D array with the longitude of the corners of the pixels of the satellite image.

      Lats : array_like
             A scalar 2-D array with the latitude of the corners of the pixels of the satellite image.

   """

   Lons = midpoint_in_x(Lons)
   Lats = midpoint_in_y(Lats)

   Lons = np.array(midpoint_in_y(Lons),dtype=fmt)
   Lats = np.array(midpoint_in_x(Lats),dtype=fmt)

   return Lons, Lats;

#-----------------------------------------------------------------------------------------------------------------------------------
def nearest_pixel(Lons, Lats, LonCoord, LatCoord):

   """
   Finds the X and Y index of the pixel closest to the required coordinate.


   Parameters
   ----------

      Lons  : array_like
              A scalar 2-D array with the longitude of the center of the pixels of the satellite image.

      Lats  : array_like
              A scalar 2-D array with the latitude of the center of the pixels of the satellite image.

      LonCoord : float
                 Longitude of the required coordinate.

      LatCoord : float
                 Latitude of the required coordinate.


   Returns
   -------
      xpix : integer
             Index on the X axis of the pixel closest to the required coordinate.

      ypix : integer
             Index on the Y axis of the pixel closest to the required coordinate.

   """

   Dist = np.sqrt( (Lons-LonCoord)**2 + (Lats-LatCoord)**2 )
   ypix, xpix = np.unravel_index( np.argmin(Dist, axis=None ), Dist.shape)

   return xpix, ypix;

#-----------------------------------------------------------------------------------------------------------------------------------

def slice_sat_image(Field, X, Y, SatLon, SatHeight, Req, Rpol, LLLon, URLon, LLLat, URLat, DeltaIndex=4, fmt=np.float32):

   """
   Cuts the field according to the desired area.


   Parameters
   ----------
      Field : array_like
              A scalar 2-D array.

      Lons  : array_like
              A scalar 2-D array with the longitude of the center of the pixels of the satellite image.

      Lats  : array_like
              A scalar 2-D array with the latitude of the center of the pixels of the satellite image.

      LLLon : float
              Lower left longitude of area that wish cut.

      LLLat : float
              Lower left latitude of area that wish cut.

      URLon : float
              Upper right longitude of area that wish cut.

      URLat : float
              Upper right latitude of area that wish cut.

      DeltaIndex : integer
                   Interval between indexes of arrays. This is used to locate more quickly the index
                   of satellite region that will be slice. Default value is 4

      fmt : dtype (optional)
            Format (dtype) of returns. Default value is np.float32


   Returns
   -------
      Field : array_like
              A scalar 2-D array cutted.

      Lons  : array_like
              A scalar 2-D array cutted with longitude of center of the pixels of the satellite image.

      Lats  : array_like
              A scalar 2-D array cutted with latitude of center of the pixels of the satellite image.

   """

   #if DeltaIndex>1 :

   Xlq = X[::DeltaIndex]
   Ylq = Y[::DeltaIndex]
   Lonslq, Latslq = get_lonlat(Xlq, Ylq, SatLon, SatHeight, Req, Rpol, fmt=fmt)

   xpixmax, ypixmin = nearest_pixel(Lonslq, Latslq, URLon, URLat)
   xpixmin, ypixmax = nearest_pixel(Lonslq, Latslq, LLLon, LLLat)

   del Xlq, Ylq, Lonslq, Latslq

   xini = xpixmin*DeltaIndex-DeltaIndex
   xfin = (xpixmax+1)*DeltaIndex+DeltaIndex
   yini = ypixmin*DeltaIndex-DeltaIndex
   yfin = (ypixmax+1)*DeltaIndex+DeltaIndex

   X = X[xini:xfin]
   Y = Y[yini:yfin]
   Field = Field[yini:yfin,xini:xfin]


   Lons, Lats = get_lonlat(X[:], Y[:], SatLon, SatHeight, Req, Rpol, fmt=fmt)

   xpixmax, ypixmin = nearest_pixel(Lons, Lats, URLon, URLat)
   xpixmin, ypixmax = nearest_pixel(Lons, Lats, LLLon, LLLat)


   limits = [xini+xpixmin, xini+xpixmax+1, yini+ypixmin, yini+ypixmax+1]

   Field = np.ascontiguousarray(Field[ypixmin:ypixmax+1,xpixmin:xpixmax+1], dtype=fmt)
   Lons = np.ascontiguousarray(Lons[ypixmin:ypixmax+1,xpixmin:xpixmax+1], dtype=fmt)
   Lats = np.ascontiguousarray(Lats[ypixmin:ypixmax+1,xpixmin:xpixmax+1], dtype=fmt)

   return Field, Lons, Lats, limits;

#-----------------------------------------------------------------------------------------------------------------------------------

def slice_area(Field, Lons, Lats, LLLon, URLon, LLLat, URLat, fmt=np.float32):

   """
   Cuts the field according to the desired area.


   Parameters
   ----------
      Field : array_like
              A scalar 2-D array.

      Lons  : array_like
              A scalar 2-D array with the longitude of the center of the pixels of the satellite image.

      Lats  : array_like
              A scalar 2-D array with the latitude of the center of the pixels of the satellite image.

      LLLon : float
              Lower left longitude of area that wish cut.

      LLLat : float
              Lower left latitude of area that wish cut.

      URLon : float
              Upper right longitude of area that wish cut.

      URLat : float
              Upper right latitude of area that wish cut.

      fmt : dtype (optional)
            Format (dtype) of returns. Default value is np.float32


   Returns
   -------
      Field : array_like
              A scalar 2-D array cutted.

      Lons  : array_like
              A scalar 2-D array cutted with longitude of center of the pixels of the satellite image.

      Lats  : array_like
              A scalar 2-D array cutted with latitude of center of the pixels of the satellite image.

   """

   xpixmax, ypixmin = nearest_pixel(Lons, Lats, URLon, URLat)
   xpixmin, ypixmax = nearest_pixel(Lons, Lats, LLLon, LLLat)

   limits = [xpixmin, xpixmax+1, ypixmin, ypixmax+1]

   Field = np.ascontiguousarray(Field[ypixmin:ypixmax+1,xpixmin:xpixmax+1], dtype=fmt)
   Lons = np.ascontiguousarray(Lons[ypixmin:ypixmax+1,xpixmin:xpixmax+1], dtype=fmt)
   Lats = np.ascontiguousarray(Lats[ypixmin:ypixmax+1,xpixmin:xpixmax+1], dtype=fmt)

   return Field, Lons, Lats, limits;

#-----------------------------------------------------------------------------------------------------------------------------------
def calc_cos_teta(Lons, Lats, JulDay, Hour, Minute, MinCosTheta=0.3, fmt=np.float32) :

   """
   Calculates the Cosine of theta (zenith angle).


   Parameters
   ----------
      Lons   : array_like
               A scalar 2-D array with longitude in decimal degrees.

      Lats   : array_like
               A scalar 2-D array with latitude in decimal degrees.

      JulDay : string
               Julian day of satellite image.

      Hour   : string
               Hour of satellite image.

      Minute : string
               Minute of satellite image.

      MinCosTheta : float
                    Minimum valid value of the cosine of theta

      fmt : dtype (optional)
            Format (dtype) of returns. Default value is np.float32


   Returns
   -------
      CosTheta : array_like
                 Cosine of theta (zenith angle)

   """

   HourDiff = np.where(Lons>-400.0,0.0,np.nan)
   CenMer = -165.0+15.0*(np.arange(24))
   HourVar = np.arange(-11,13,1)

   for idx in range(CenMer.shape[0]):
      HourDiff = np.where( (Lons>= CenMer[idx]-7.5)&(Lons<CenMer[idx]+7.5),HourVar[idx],0.0) + HourDiff


   Gamma = 2.0*np.pi*(float(JulDay)-1.0)/365.0   # Gamma is in radians
   Delta = 0.006918-0.399912*np.cos(Gamma)+0.070257*np.sin(Gamma)-0.006758*np.cos(2*Gamma)+0.000907*np.sin(2*Gamma)-0.002697*np.cos(3*Gamma)+0.00148*np.sin(3*Gamma)  # Solar decline, is in radians.
   EqTime = 229.18*(0.0000075+0.001868*np.cos(Gamma)-0.032077*np.sin(Gamma)-0.014615*np.cos(2*Gamma)-0.04089*np.sin(2*Gamma)) # Equation of time, is in minutes.

   #hhl = float(Hour)+(float(Minute)/60.0)+HourDiff
   Omega = (np.pi/12.0)*( float(Hour) + (float(Minute)/60.0) + HourDiff -12.0 + ( (Lons-HourDiff*15.0)/15.0 ) + EqTime/60.0 ) # Hour angle, is in radians.
   CosTheta = np.sin(Delta)*np.sin(Lats*np.pi/180.0)+np.cos(Delta)*np.cos(Lats*np.pi/180.0)*np.cos(Omega) # Cosine of theta (zenith angle)
   CosTheta[np.where(CosTheta<MinCosTheta)] = np.nan
   CosTheta = np.array(CosTheta, dtype=fmt)

   return CosTheta;

#-----------------------------------------------------------------------------------------------------------------------------------

def calc_orbital_factor(JulDay):

   """
   Calculates the obital factor from julian day.


   Parameters
   ----------

      JulDay : string
               Julian day of satellite image.


   Returns
   -------
      Fn     : float
               Orbital factor.
   """

   Fn = 1.0+0.033*math.cos(2.0*np.pi*float(JulDay)/(365.0))

   return Fn;

#-----------------------------------------------------------------------------------------------------------------------------------


