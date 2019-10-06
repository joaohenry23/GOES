# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------------------
'''
Description: Creates python custom colors palette
Author: Joao Henry Huaman Chinchay
E-mail: joaohenry23@gmail.com
Created date: Sat, Sep 21, 2019
'''
#-----------------------------------------------------------------------------------------------------------------------------------
import numpy as np
import s3fs
from datetime import *
#-----------------------------------------------------------------------------------------------------------------------------------
def show_download_options():

   """
   List option of show_download_options.

   """

   Satellite_code = ['G16','G17']
   Satellite_meaning = ['goes16','goes17']
   print(' \nSatellite:')
   for i in range(len(Satellite_code)):
      print('\t{}: {}'.format(Satellite_code[i], Satellite_meaning[i]))


   Product_code = ['ABI-L1b-Rad','ABI-L2-CMIP','ABI-L2-MCMIP','GLM-L2-LCFA']
   Product_meaning = ['ABI Level 1 in Radiance','ABI Level 2 Single Channel in Temperature','ABI Level 2 Multi Channel in Temperature','GLM Level 2']
   print(' \nProduct:')
   for i in range(len(Product_code)):
      print('\t{}: {}'.format(Product_code[i], Product_meaning[i]))


   Domain_code = ['CN','FD','M1','M2']
   Domain_meaning = ['Conus','Full Disk','Mesoscale 1','Mesoscale 2']
   print(' \nDomain:')
   for i in range(len(Domain_code)):
      print('\t{}: {}'.format(Domain_code[i], Domain_meaning[i]))

   return;

#-----------------------------------------------------------------------------------------------------------------------------------
def download_from_amazon(Satellite, Product, Domain = None, Channel = None, DateTimeIni = None, DateTimeFin = None, Rename = False, PathOut = ''):

   """
   Download data from GOES-16 and GOES-17.
   This function is based on the code of blaylockbk (https://gist.github.com/blaylockbk/d60f4fce15a7f0475f975fc57da9104d).


   Parameters
   ----------
   Satellite : string
               Indicates serie of GOES, the options are:
               G16 : goes16
               G17 : goes17

   Product : string
               Indicates the instrument and level of product. the options are:
	            ABI-L1b-Rad : ABI Level 1 in Radiance
	            ABI-L2-CMIP : ABI Level 2 Single Channel in Temperature
	            ABI-L2-MCMIP: ABI Level 2 Multi Channel in Temperature
	            GLM-L2-LCFA : GLM Level 2

   Domain : string (None)
               Indicates the domain of data. The options are:
	            CN : Conus
	            FD : Full Disk
	            M1 : Mesoscale 1
	            M2 : Mesoscale 2

   Channel : string list (None)
               String list that indicates the channel or channels that will be download.
               The channels can be mentioned individually as elements of the list
               or as a sequence of channels separated by a hyphen ('-').
               Example:
                  channel=['02','08','09','10','11']
                  channel=['02','08-11']

   DateTimeIni : string (None)
               String that indicates the initial datetime, their structure
               must be yyyymmdd-HHMMSS
               Example:
                  DateTimeIni='20180520-1830'


   DateTimeFin : string (None)
               String that indicates the final datetime, their structure
               must be yyyymmdd-HHMMSS
               Example:
                  DateTimeIni='20180520-1830'

   Rename : bool (False)
            Optional boolean that indicates if filename will be rename just with the scan start time.
            The default value is False.

   PathOut : string
            Optional string that indicates the folder where data will be download.
            The default value is folder where python was open.


   """


   # ---------- Satellite -------------------
   if Satellite == 'G16':
      Sat = 'goes16'
   elif Satellite == 'G17':
      Sat = 'goes17'
   else:
      print('You must choose a Satellite')
      exit()


   # ---------- Domain -------------------
   if Domain == 'CN':
      dom1 = 'C'
      dom2 = 'C'
   elif Domain == 'FD':
      dom1 = 'F'
      dom2 = 'F'
   elif Domain == 'M1':
      dom1 = 'M'
      dom2 = 'M1'
   elif Domain == 'M2':
      dom1 = 'M'
      dom2 = 'M2'
   elif Domain == None :
      if Product == 'GLM' :
         dom1 = ''
         dom2 = ''
      else :
         print('You must define Domain')
         exit()
   else:
      print('You must define valid Domain')
      exit()


   # ---------- Product -------------------
   server = ''
   name = ''

   if Product == 'ABI-L1':
      server = 'noaa-'+Sat+'/' + 'ABI-L1b-Rad' + dom1 + '/'
      name = 'OR_ABI-L1b-Rad' + dom2

   elif Product == 'ABI-L2S':
      server = 'noaa-'+Sat+'/' + 'ABI-L2-CMIP' + dom1 + '/'
      name = 'OR_ABI-L2-CMIP' + dom2

   elif Product == 'ABI-L2M':
      server = 'noaa-'+Sat+'/' + 'ABI-L2-MCMIP' + dom1 + '/'
      name = 'OR_ABI-L2-MCMIP' + dom2

   elif Product == 'GLM':
      server = 'noaa-'+Sat+'/' + 'GLM-L2-LCFA/'
      name = 'OR_GLM-L2-LCFA'

   else:
      print('You must choose a Product')
      exit()


   # ---------- DateTimeIni -------------------
   if DateTimeIni == None :
      print('You must define initial DateTime')
      exit()
   else:
      DateTimeIni = datetime.strptime(DateTimeIni, '%Y%m%d-%H%M%S')


   # ---------- DateTimeFin -------------------
   if DateTimeFin == None :
      DateTimeFin = DateTimeIni
   else:
      DateTimeFin = datetime.strptime(DateTimeFin, '%Y%m%d-%H%M%S')


   # ---------- Channel -------------------
   if Channel == None :
      if Product == 'ABI-L1' or Product == 'ABI-L2S' : #or Product == 'ABI-L2M' :
         print('You must define channel or channels')
      else:
         ChannelList = []
   else :
      ChannelList = []
      for item in Channel :
         if isinstance(item, str) == True :

            if len(item) == 2 :
               ChannelList.append(item)
            elif len(item) == 5 :
               ChIni, ChEnd = item.split('-')
               for Chn in range(int(ChIni),int(ChEnd)+1):
                  ChannelList.append('{:02d}'.format(Chn))
            else:
               print('Element of Channel must be string with two or five characters')

         else :
            print('Channel must be a list and each of its elements must have string format')
            exit()

   print('Channel list', ChannelList, '\n')


   # ---------- Loop -------------------
   while DateTimeIni <= DateTimeFin :

      DateTimeFolder = DateTimeIni.strftime('%Y/%j/%H/')
      DateTimeName = DateTimeIni.strftime('%Y%j%H%M')

      print(' ')
      print('Server:', server+DateTimeFolder)
      print('PathOut:', PathOut)

      fs = s3fs.S3FileSystem(anon=True)
      ListFiles = np.array(fs.ls(server+DateTimeFolder))

      for line in ListFiles :
         if Product == 'ABI-L1' or Product == 'ABI-L2S' :

            NameFile = line.split('/')[-1]
            ChannelFile = NameFile.split('_')[1][-2:]
            DateTimeFile = datetime.strptime(NameFile.split('_')[3][-14:-3], '%Y%j%H%M')

            if ChannelFile in ChannelList and DateTimeFile >= DateTimeIni and DateTimeFile <= DateTimeFin :

               if Rename == False :
                  NameOut = NameFile
               elif Rename == True :
                  NameOut = NameFile.split('_')[0] + '_' + NameFile.split('_')[1] + '_' + NameFile.split('_')[2] + '_s' + DateTimeFile.strftime('%Y%m%d%H%M') + '.nc'

               print(ChannelFile, DateTimeFile, NameOut)
               fs.get(line, PathOut+NameOut)


         elif Product == 'ABI-L2M' :

            NameFile = line.split('/')[-1]
            DateTimeFile = datetime.strptime(NameFile.split('_')[3][-14:-3], '%Y%j%H%M')

            if DateTimeFile >= DateTimeIni and DateTimeFile <= DateTimeFin :

               if Rename == False :
                  NameOut = NameFile
               elif Rename == True :
                  NameOut = NameFile.split('_')[0] + '_' + NameFile.split('_')[1] + '_' + NameFile.split('_')[2] + '_s' + DateTimeFile.strftime('%Y%m%d%H%M') + '.nc'

               print(DateTimeFile, NameOut)
               fs.get(line, PathOut+NameOut)


         elif Product == 'GLM' :
            NameFile = line.split('/')[-1]
            DateTimeFile = datetime.strptime(NameFile.split('_')[3][-14:-1], '%Y%j%H%M%S')

            if DateTimeFile >= DateTimeIni and DateTimeFile <= DateTimeFin :

               if Rename == False :
                  NameOut = NameFile
               elif Rename == True :
                  NameOut = NameFile.split('_')[0] + '_' + NameFile.split('_')[1] + '_' + NameFile.split('_')[2] + '_s' + DateTimeFile.strftime('%Y%m%d%H%M%S') + '.nc'

               print(DateTimeFile, NameOut)
               fs.get(line, PathOut+NameOut)

      DateTimeIni = DateTimeIni + timedelta(minutes=60)

#-----------------------------------------------------------------------------------------------------------------------------------

