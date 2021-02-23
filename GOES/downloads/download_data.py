# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------------------
'''
Description: Downloads GOES-16/17 data from amazon
Author: Joao Henry Huaman Chinchay
E-mail: joaohenry23@gmail.com
Created date: Mar 23, 2020
Modification date: Feb 23, 2021
'''
#-----------------------------------------------------------------------------------------------------------------------------------
import numpy as np
import s3fs
from datetime import *
import requests

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

#-----------------------------------------------------------------------------------------------------------------------------------
def show_products():

    '''

    Lists the products available from GOES-16 and GOES-17.

    '''

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

    print('Descriptions of each product is shown in https://docs.opendata.aws/noaa-goes16/cics-readme.html#about-the-data \n')

#-----------------------------------------------------------------------------------------------------------------------------------
def download_file(URL, name_file, path_out, retries=10, backoff=10, size_format='Decimal', show_download_progress=True):

    '''

    Save data in file.

    Parameters
    ----------
    URL : str
        Link of file.

    name_file : str 
        Name of output file.

    path_out : str, optional, default ''
        Path of folder where file will be saved.

    retries : int, optional, default 10
        Defines the retries number to connect to server.
        See: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry

    backoff: int, optional, default 10
        A backoff factor to apply between attempts after the second try.
        See: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry


    size_format: str, optional, default 'Decimal'
        Defines how is print the size of file.
        Options are:
            'Decimal' : divide file size (in bytes) by (1000*1000) 
            'Binary' : divide file size (in bytes) by (1024*1024)

    show_download_progress : boolean, optional, default True
        Parameter to enable and disable the visualization of download progress.

    '''

    StartTime = datetime.now()

    retries_config = Retry(total=retries, backoff_factor=backoff, status_forcelist=[500, 502, 503, 504])

    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=retries_config))
    session.mount('https://', HTTPAdapter(max_retries=retries_config))
    req = session.get(URL, stream=True)
    #req = requests.get(URL, stream=True)
    total_size = int(req.headers['content-length'])
    size = 0
    if size_format == 'Binary':
        dsize = 1024*1024
    else:
        dsize = 1000*1000

    with open(path_out+name_file,'wb') as output_file:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                rec_size = output_file.write(chunk)
                size = rec_size + size
                if show_download_progress==True:
                    print('  {} {:3.0f}% {:.1f}MB {}'.format(name_file,100.0*size/total_size, size/dsize, '{}m{}s'.format(round((datetime.now()-StartTime).seconds/60.0),(datetime.now()-StartTime).seconds%60) if (datetime.now()-StartTime).seconds>60 else '{}s'.format((datetime.now()-StartTime).seconds) ), end="\r") #, flush=True)
                    #print('\t{}\t{:3.0f}%\t{:.2f} min'.format(name_file,100.0*size/total_size, (datetime.now()-StartTime).seconds/60.0), end="\r") #, flush=True)
                    if size == total_size:
                        #print('\n')
                        print('  {} {:3.0f}% {:.1f}MB {}'.format(name_file,100.0*size/total_size, size/dsize, '{}m{}s'.format(round((datetime.now()-StartTime).seconds/60.0),(datetime.now()-StartTime).seconds%60) if (datetime.now()-StartTime).seconds>60 else '{}s'.format((datetime.now()-StartTime).seconds) ))

    #print('\b')

#-----------------------------------------------------------------------------------------------------------------------------------
def download(Satellite, Product, DateTimeIni=None, DateTimeFin=None, domain=None, channel=None, rename_fmt=False, path_out='', retries=10, backoff=10, size_format='Decimal', show_download_progress=True):

    '''

    Download data of GOES-16 and GOES-17 from Amazon server.
    This function is based on the code of
    blaylockbk https://gist.github.com/blaylockbk/d60f4fce15a7f0475f975fc57da9104d


    Parameters
    ----------
    Satellite : str
        Indicates serie of GOES, the options are 'goes16' and 'goes17'


    Product : str
        Indicates the instrument and level of product. The products
        can be list using: GOES.show_products()


    DateTimeIni : str
        String that indicates the initial datetime. Its structure
        must be yyyymmdd-HHMMSS
        Example:
            DateTimeIni='20180520-183000'


    DateTimeFin : str
        String that indicates the final datetime. Its structure
        must be yyyymmdd-HHMMSS
        Example:
            DateTimeFin='20180520-183000'


    domain : str
        This parameter just is necessary with Mesoescale products.
        The options are:
            M1 : Mesoscale 1
            M2 : Mesoscale 2


    channel : list
        This parameter just is necessary with ABI-L1b-Rad and ABI-L2-CMIP products.
        List indicates the channel or channels that will be download.
        The channels can be mentioned individually as elements of the list
        or as a sequence of channels separated by a hyphen ('-').
        Example:
            channel = ['02','08','09','10','11','13']
            channel = ['02','08-11','13']


    rename_fmt : boolean or str, optional, default False
        Is an optional parameter and its default value is rename_fmt=False which
        indicates that the file name is kept. If would you like that the file name
        just keep the start time of scan you have to define the format of datetime.
        See the next link to know about datetime format:
        https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes).
        Example:
            rename_fmt = '%Y%m%d%H%M%S'
            rename_fmt = '%Y%m%d%H%M'
            rename_fmt = '%Y%j%H%M'


    path_out : str, optional, default ''
        Optional string that indicates the folder where data will be download.
        The default value is folder where python was open.


    retries: int, optional, default 10
        Defines the retries number to connect to server.
        See: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry

    backoff: int, optional, default 10
        A backoff factor to apply between attempts after the second try.
        See: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry


    size_format: str, optional, default 'Decimal'
        It defines how is print the size of file.
        Options are:
            'Decimal' : divide file size (in bytes) by (1000*1000) 
            'Binary' : divide file size (in bytes) by (1024*1024)

    show_download_progress : boolean, optional, default True
        Parameter to enable and disable the visualization of download progress.

    Return
    ------
    Download_files : list
        List with the downloaded files (path+filename).

    '''

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
            assert domain == 'M1' or domain == 'M2'
        except AssertionError:
            print("\nProduct domain is mesoscale so you need define domain='M1' or domain='M2'\n")
            return
        else:
            if domain == 'M1':
                Product2 = Product+'1'
            elif domain == 'M2':
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

    # ---------- channel -------------------

    if Product[:-1] in ['ABI-L1b-Rad','ABI-L2-CMIP']:

        try:
            assert channel != None
        except AssertionError:
            print('\nYou must define channel or channels\n')
            return
        else:

            try:
                assert isinstance(channel, list) == True
            except AssertionError:
                print('\nChannel must be a list\n')
                return
            else:
                ChannelList = []
                for item in channel:

                    try:
                        assert isinstance(item, str) == True
                    except AssertionError:
                        print('\nEach elements of channel must have string format\n')
                        return
                    else:

                        try:
                            assert len(item) == 2 or len(item) == 5
                        except AssertionError:
                            print('\nElement of channel must be string with two or five characters\n')
                            return
                        else:
                            if len(item) == 2 :
                                ChannelList.append(item)
                            elif len(item) == 5 :
                                ChIni, ChEnd = item.split('-')
                                for Chn in range(int(ChIni),int(ChEnd)+1):
                                    ChannelList.append('{:02d}'.format(Chn))

                #if download_info == 'minimal' or download_info == 'full':
                #    print('channel list: {}'.format(ChannelList))


    #"""
    Downloaded_files = []

    if show_download_progress == True:
        print('Files:')

    # ---------- Loop -------------------
    DateTimeIniLoop = DateTimeIni.replace(minute=0)
    DateTimeFinLoop = DateTimeFin.replace(minute=0)+timedelta(minutes=60)
    while DateTimeIniLoop < DateTimeFinLoop :

        DateTimeFolder = DateTimeIniLoop.strftime('%Y/%j/%H/')

        server = 's3://noaa-'+Satellite+'/'+Product+'/'
        fs = s3fs.S3FileSystem(anon=True)
        ListFiles = np.array(fs.ls(server+DateTimeFolder))

        for line in ListFiles:
            if Product[:-1] in ['ABI-L1b-Rad','ABI-L2-CMIP']:
                NameFile = line.split('/')[-1]
                ChannelFile = NameFile.split('_')[1][-2:]
                DateTimeFile = datetime.strptime(NameFile[NameFile.find('_s')+2:NameFile.find('_e')-1], '%Y%j%H%M%S')

                if Product2 in NameFile    and    ChannelFile in ChannelList    and    DateTimeIni <= DateTimeFile <= DateTimeFin:

                    if rename_fmt == False:
                        NameOut = NameFile
                    else:
                        NameOut = NameFile[:NameFile.find('_s')+2] + DateTimeFile.strftime(rename_fmt) + '.nc'

                    #print(ChannelFile, DateTimeFile, NameOut)
                    download_file('https://noaa-'+Satellite+'.s3.amazonaws.com'+line[len('noaa-'+Satellite):], NameOut, path_out, retries=retries, backoff=backoff, size_format=size_format, show_download_progress=show_download_progress)
                    Downloaded_files.append(path_out+NameOut)

            else:
                NameFile = line.split('/')[-1]
                DateTimeFile = datetime.strptime(NameFile[NameFile.find('_s')+2:NameFile.find('_e')-1], '%Y%j%H%M%S')

                if Product2 in NameFile    and    DateTimeIni <= DateTimeFile <= DateTimeFin:

                    if rename_fmt == False:
                        NameOut = NameFile
                    else:
                        NameOut = NameFile[:NameFile.find('_s')+2] + DateTimeFile.strftime(rename_fmt) + '.nc'

                    #print(DateTimeFile, NameOut)
                    download_file('https://noaa-'+Satellite+'.s3.amazonaws.com'+line[len('noaa-'+Satellite):], NameOut, path_out, retries=retries, backoff=backoff, size_format=size_format, show_download_progress=show_download_progress)
                    Downloaded_files.append(path_out+NameOut)

        DateTimeIniLoop = DateTimeIniLoop + timedelta(minutes=60)

    Downloaded_files.sort()

    return Downloaded_files;

#-----------------------------------------------------------------------------------------------------------------------------------

