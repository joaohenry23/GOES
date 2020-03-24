# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------------------
'''
Description: Download data from amazon
Author: Joao Henry Huaman Chinchay
E-mail: joaohenry23@gmail.com
Created date: Monday, Mar 23, 2020
'''
#-----------------------------------------------------------------------------------------------------------------------------------
import numpy as np
import s3fs
from datetime import *
import requests
#-----------------------------------------------------------------------------------------------------------------------------------
def show_products():

   """
   List products.

   """

   Satellite = ['goes16','goes17']
   print(' ')
   for sat in Satellite:
      print('Products for '+sat+':')
      fs = s3fs.S3FileSystem(anon=True)
      for item in fs.ls('s3://noaa-'+sat+'/'):
         if item.split('/')[-1] == 'index.html':
            print(' ')
         else:
            print('\t'+item.split('/')[-1])

   print('Descriptions of products in the next link: \n\t'+'https://docs.opendata.aws/noaa-goes16/cics-readme.html#about-the-data \n')

#-----------------------------------------------------------------------------------------------------------------------------------
def download_file(URL,NameOut,Path):

   """
   Save data in file.

   Parameters
   ----------
   URL: Link of file.

   NameOut: Name of output file.

   Path: Path of folder where file will be saved.

   """

   StartTime = datetime.now()
   req = requests.get(URL, stream=True)
   total_size = int(req.headers['content-length'])
   size = 0
   with open(Path+NameOut,'wb') as output_file:
      for chunk in req.iter_content(chunk_size=1024):
         if chunk:
            rec_size = output_file.write(chunk)
            size = rec_size + size
            print('\t{}\t{:3.0f}%\t{:.2f} min'.format(NameOut,100.0*size/total_size, (datetime.now()-StartTime).seconds/60.0), end='\r', flush=True)
   print('\b')

#-----------------------------------------------------------------------------------------------------------------------------------
def download(Satellite, Product, DateTimeIni = None, DateTimeFin = None, Domain = None, Channel = None, Rename_fmt = False, PathOut = ''):

   """
   Download data of GOES-16 and GOES-17 from Amazon server.
   This function is based on the code of
   blaylockbk https://gist.github.com/blaylockbk/d60f4fce15a7f0475f975fc57da9104d


   Parameters
   ----------
   Satellite : string
               Indicates serie of GOES, the options are:
               goes16
               goes17


   Product : string
             Indicates the instrument and level of product. The products can be list using:
             GOES.show_products()


   DateTimeIni : string (None)
                 String that indicates the initial datetime, their structure
                 must be yyyymmdd-HHMMSS
                 Example:
                    DateTimeIni='20180520-183000'


   DateTimeFin : string (None)
                 String that indicates the final datetime, their structure
                 must be yyyymmdd-HHMMSS
                 Example:
                    DateTimeFin='20180520-183000'


   Domain : string (None)
            This parameter just is necessary with Mesoescale products.
            The options are:
	            M1 : Mesoscale 1
	            M2 : Mesoscale 2


   Channel : string list (None)
             This parameter just is necessary with ABI-L1b-Rad and ABI-L2-CMIP products.
             String list indicates the channel or channels that will be download.
             The channels can be mentioned individually as elements of the list
             or as a sequence of channels separated by a hyphen ('-').
             Example:
                Channel = ['02','08','09','10','11','13']
                Channel = ['02','08-11','13']


   Rename_fmt : bool (False) or string
                Is an optional parameter and its default value is Rename_fmt=False which
                indicates that the file name is kept. If would you like that the file name
                just keep the start time of scan you have to define the format of datetime.
                See the next link to know about datetime format:
                https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).
                Example:
                   Rename_fmt = '%Y%m%d%H%M%S'
                   Rename_fmt = '%Y%m%d%H%M'
                   Rename_fmt = '%Y%j%H%M'


   PathOut : string
            Optional string that indicates the folder where data will be download.
            The default value is folder where python was open.



   """

   # ---------- Satellite -------------------
   try:
      assert Satellite == 'goes16' or Satellite == 'goes17'
   except AssertionError:
      print('\nSatellite should be goes16 or goes17\n')
      return
   else:
      if Satellite == 'goes16':
         Sat = 'G16'
      elif Satellite == 'goes17':
         Sat = 'G17'

   # ---------- Product and Domain -------------------
   if Product[-1] == 'M':
      try:
         assert Domain == 'M1' or Domain == 'M2'
      except AssertionError:
         print("\nProduct domain is mesoscale so you need define Domain='M1' or Domain='M2'\n")
         return
      else:
         if Domain == 'M1':
            Product2 = Product+'1'
         elif Domain == 'M2':
            Product2 = Product+'2'
   else:
      Product2 = Product

   # ---------- DateTimeIni -------------------
   try:
      assert DateTimeIni != None
   except AssertionError:
      print('\nYou must define initial DateTimeIni\n')
      return
   else:
      DateTimeIni = datetime.strptime(DateTimeIni, '%Y%m%d-%H%M%S')

   # ---------- DateTimeFin -------------------
   if DateTimeFin == None :
      DateTimeFin = DateTimeIni
   else:
      DateTimeFin = datetime.strptime(DateTimeFin, '%Y%m%d-%H%M%S')

   # ---------- Channel -------------------

   if Product[:-1] in ['ABI-L1b-Rad','ABI-L2-CMIP']:

      try:
         assert Channel != None
      except AssertionError:
         print('\nYou must define channel or channels\n')
         return
      else:

         try:
            assert isinstance(Channel, list) == True
         except AssertionError:
            print('\nChannel must be a list\n')
            return
         else:
            ChannelList = []
            for item in Channel:

               try:
                  assert isinstance(item, str) == True
               except AssertionError:
                  print('\nEach elements of channel must have string format\n')
                  return
               else:

                  try:
                     assert len(item) == 2 or len(item) == 5
                  except AssertionError:
                     print('\nElement of Channel must be string with two or five characters\n')
                     return
                  else:
                     if len(item) == 2 :
                        ChannelList.append(item)
                     elif len(item) == 5 :
                        ChIni, ChEnd = item.split('-')
                        for Chn in range(int(ChIni),int(ChEnd)+1):
                           ChannelList.append('{:02d}'.format(Chn))

            print('Channel list:', ChannelList, '\n')


   #"""

   # ---------- Loop -------------------
   while DateTimeIni <= DateTimeFin :

      DateTimeFolder = DateTimeIni.strftime('%Y/%j/%H/')
      DateTimeName = DateTimeIni.strftime('%Y%j%H%M')

      server = 's3://noaa-'+Satellite+'/'+Product+'/'
      print(' ')
      print('Server:', server+DateTimeFolder)
      print('PathOut:', PathOut)

      fs = s3fs.S3FileSystem(anon=True)
      ListFiles = np.array(fs.ls(server+DateTimeFolder))


      for line in ListFiles:
         if Product[:-1] in ['ABI-L1b-Rad','ABI-L2-CMIP']:
            NameFile = line.split('/')[-1]
            ChannelFile = NameFile.split('_')[1][-2:]
            DateTimeFile = datetime.strptime(NameFile[NameFile.find('_s')+2:NameFile.find('_e')-1], '%Y%j%H%M%S')

            if Product2 in NameFile   and   ChannelFile in ChannelList   and   DateTimeIni <= DateTimeFile <= DateTimeFin:

               if Rename_fmt == False:
                  NameOut = NameFile
               else:
                  NameOut = NameFile[:NameFile.find('_s')+2] + DateTimeFile.strftime(Rename_fmt) + '.nc'

               #print(ChannelFile, DateTimeFile, NameOut)
               download_file('https://noaa-'+Satellite+'.s3.amazonaws.com'+line[len('noaa-'+Satellite):], NameOut, PathOut)

         else:
            NameFile = line.split('/')[-1]
            DateTimeFile = datetime.strptime(NameFile[NameFile.find('_s')+2:NameFile.find('_e')-1], '%Y%j%H%M%S')

            if Product2 in NameFile   and   DateTimeIni <= DateTimeFile <= DateTimeFin:

               if Rename_fmt == False:
                  NameOut = NameFile
               else:
                  NameOut = NameFile[:NameFile.find('_s')+2] + DateTimeFile.strftime(Rename_fmt) + '.nc'

               #print(DateTimeFile, NameOut)
               download_file('https://noaa-'+Satellite+'.s3.amazonaws.com'+line[len('noaa-'+Satellite):], NameOut, PathOut)


      DateTimeIni = DateTimeIni + timedelta(minutes=60)

#-----------------------------------------------------------------------------------------------------------------------------------

