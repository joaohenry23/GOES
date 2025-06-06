# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------------------------------------------------------
'''
Description: Downloads GOES-16/17/18/19 data from Amazon Web Services
Author: Joao Henry Huaman Chinchay
E-mail: joaohenry23@gmail.com
Created date: Mar 23, 2020
Modification date: Apr 2, 2025
'''
#-----------------------------------------------------------------------------------------------------------------------------------
import numpy as np
import s3fs
from datetime import *
import requests
import os
import subprocess

from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

#-----------------------------------------------------------------------------------------------------------------------------------
def show_products():

    '''

    Lists the products available from GOES-16, GOES-17, GOES-18, GOES-19.

    '''

    Satellite = ['goes16','goes17','goes18','goes19']
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
def download_file(URL, name_file, path_out, retries=10, backoff=0.2, size_format='Decimal', show_download_progress=True, overwrite_file=False):

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

    backoff: int, optional, default 0.2
        A backoff factor to apply between attempts after the second try.
        See: https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#module-urllib3.util.retry


    size_format: str, optional, default 'Decimal'
        Defines how is print the size of file.
        Options are:
            'Decimal' : divide file size (in bytes) by (1000*1000) 
            'Binary' : divide file size (in bytes) by (1024*1024)

    show_download_progress : boolean, optional, default True
        Parameter to enable and disable the visualization of download progress.

    overwrite_file : boolean, optional, default False
        Parameter to overwrite or keep a file already downloaded.
        If overwrite_file=False the downloaded file is keep.
        If overwrite_file=True the downloaded file is overwrite (the file is
        downloaded again).

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


    make_download = True

    if os.path.isfile(path_out+name_file)==True:
        if os.path.getsize(path_out+name_file)==total_size:
            if overwrite_file==False:
                print('  {} already exists.'.format(name_file))
                make_download = False
            else:
                print('  {} will be overwritten.'.format(name_file))
                make_download = True
        else:
            make_download = True


    if make_download == True:
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
def download(Satellite, Product, DateTimeIni=None, DateTimeFin=None, domain=None, channel=None, rename_fmt=False, path_out='', retries=10, backoff=10, size_format='Decimal', show_download_progress=True, overwrite_file=False):

    '''

    Download data of GOES-16, GOES-17, GOES-18 and GOES-19 from Amazon server.
    This function is based on the code of
    blaylockbk https://gist.github.com/blaylockbk/d60f4fce15a7f0475f975fc57da9104d


    Parameters
    ----------
    Satellite : str
        Indicates serie of GOES, the options are 'goes16', 'goes17', 'goes18' and 'goes19'


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

    overwrite_file : boolean, optional, default False
        Parameter to overwrite or keep a file already downloaded.
        If overwrite_file=False the downloaded file is keep.
        If overwrite_file=True the downloaded file is overwrite (the file is
        downloaded again).


    Return
    ------
    Download_files : list
        List with the downloaded files (path+filename).

    '''

    # ---------- Satellite -------------------
    try:
        assert Satellite == 'goes16' or Satellite == 'goes17' or Satellite == 'goes18' or Satellite == 'goes19'
    except AssertionError:
        print('\nSatellite should be goes16, goes17, goes18 or goes19\n')
        return
    else:
        if Satellite == 'goes16':
            Sat = 'G16'
        elif Satellite == 'goes17':
            Sat = 'G17'
        elif Satellite == 'goes18':
            Sat = 'G18'
        elif Satellite == 'goes19':
            Sat = 'G19'

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
                    download_file('https://noaa-'+Satellite+'.s3.amazonaws.com'+line[len('noaa-'+Satellite):], NameOut, path_out, retries=retries, backoff=backoff, size_format=size_format, show_download_progress=show_download_progress, overwrite_file=overwrite_file)
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
                    download_file('https://noaa-'+Satellite+'.s3.amazonaws.com'+line[len('noaa-'+Satellite):], NameOut, path_out, retries=retries, backoff=backoff, size_format=size_format, show_download_progress=show_download_progress, overwrite_file=overwrite_file)
                    Downloaded_files.append(path_out+NameOut)

        DateTimeIniLoop = DateTimeIniLoop + timedelta(minutes=60)

    Downloaded_files.sort()

    return Downloaded_files;

#-----------------------------------------------------------------------------------------------------------------------------------
def show_products_from_google_cloud(Satellite):

    '''

    Lists the products of GOES-16, GOES-17, GOES-18 and GOES-19 available in the Google Cloud.

    Parameters
    ----------
    Satellite : str
        Indicates serie of GOES, the options are 'goes16', 'goes17', 'goes18' and 'goes19'

    '''

    if 'COLAB_GPU' in os.environ:

        if Satellite == 'goes16':
            Sat = '16'
        elif Satellite == 'goes17':
            Sat = '17'
        elif Satellite == 'goes18':
            Sat = '18'
        elif Satellite == 'goes19':
            Sat = '19'
        server = 'gs://gcp-public-data-goes-{}/'.format(Sat)
        #list_gc = !gsutil ls -d $server
        list_gc = subprocess.run(['gsutil','ls','-d',server], capture_output=True, text=True).stdout
        list_gc = list(list_gc.split('\n'))[:-1]
        print('Products of {} available in Google Cloud:'.format(Satellite))
        for folder in list_gc:
            if folder[-1] == '/':
                print('  {}'.format(folder[len(server):-1]))

    else:
        print('\n  This function only works in Colab\n')

#-----------------------------------------------------------------------------------------------------------------------------------
def get_data_to_colab(Satellite, Product, DateTimeIni=None, DateTimeFin=None, domain=None, channel=None, path_out='/content/', size_format='Decimal'):

    '''

    Copy data of GOES-16, GOES-17, GOES-18 and GOES-19 from the Google Cloud to colab folder.

    Parameters
    ----------
    Satellite : str
        Indicates serie of GOES, the options are 'goes16', 'goes17', 'goes18' and 'goes19'


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


    path_out : str, optional, default '/content/'
        Optional string that indicates the folder where data will be download.
        The default value is folder where python was open.


    size_format: str, optional, default 'Decimal'
        It defines how is print the size of file.
        Options are:
            'Decimal' : divide file size (in bytes) by (1000*1000) 
            'Binary' : divide file size (in bytes) by (1024*1024)


    Return
    ------
    Download_files : list
        List with the downloaded files (path+filename).

    '''

    if 'COLAB_GPU' in os.environ:

        # ----------------------------------------
        if size_format == 'Binary':
            dsize = 1024*1024
        else:
            dsize = 1000*1000

        # ---------- Satellite -------------------
        try:
            assert Satellite == 'goes16' or Satellite == 'goes17' or Satellite == 'goes18' or Satellite == 'goes19'
        except AssertionError:
            print('\nSatellite should be goes16, goes17, goes18 or goes19\n')
            return
        else:
            if Satellite == 'goes16':
                Sat = '16'
            elif Satellite == 'goes17':
                Sat = '17'
            elif Satellite == 'goes18':
                Sat = '18'
            elif Satellite == 'goes19':
                Sat = '19'

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
                    #assert isinstance(channel, list) == True
                    assert isinstance(channel, type([])) == True
                except AssertionError:
                    print('\nChannel must be a list\n')
                    return
                else:
                    ChannelList = []
                    for item in channel:

                        try:
                            #assert isinstance(item, str) == True
                            assert isinstance(item, type('Hola Joao')) == True
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


        Downloaded_files = []

        # ---------- Loop -------------------
        DateTimeIniLoop = DateTimeIni.replace(minute=0)
        DateTimeFinLoop = DateTimeFin.replace(minute=0)+timedelta(minutes=60)
        while DateTimeIniLoop < DateTimeFinLoop :

            DateTimeFolder = DateTimeIniLoop.strftime('%Y/%j/%H/')

            server = 'gs://gcp-public-data-goes-'+Sat+'/'+Product+'/'+DateTimeFolder
            #list_gc = !gsutil ls $server
            list_gc = subprocess.run(['gsutil','ls',server], capture_output=True, text=True).stdout
            list_gc = list(list_gc.split('\n'))[:-1]

            ListFiles = np.array(list_gc)

            for line in ListFiles:
                if Product[:-1] in ['ABI-L1b-Rad','ABI-L2-CMIP']:
                    NameFile = line.split('/')[-1]
                    ChannelFile = NameFile.split('_')[1][-2:]
                    DateTimeFile = datetime.strptime(NameFile[NameFile.find('_s')+2:NameFile.find('_e')-1], '%Y%j%H%M%S')

                    if Product2 in NameFile    and    ChannelFile in ChannelList    and    DateTimeIni <= DateTimeFile <= DateTimeFin:

                        NameOut = NameFile

                        if os.path.isfile(path_out+NameFile) == True:
                            #size_in_server = !gsutil du $line
                            #size_in_server = int(size_in_server[0].split()[0])
                            size_in_server = subprocess.run(['gsutil','du',line], capture_output=True, text=True).stdout
                            size_in_server = int(size_in_server.split(' ')[0])
                            size_in_folder = os.path.getsize(path_out+NameFile)
                            if size_in_server == size_in_folder:
                                print('{} already exists.'.format(NameFile))
                            else:
                                #!gsutil -q cp $line $path_out
                                subprocess.run(['gsutil','-q','cp',line,path_out])
                                size = os.path.getsize(path_out+NameFile)/dsize #
                                print('{} {:.1f}MB [Replaced]'.format(NameFile,size))
                        else:
                            #!gsutil -q cp $line $path_out
                            subprocess.run(['gsutil','-q','cp',line,path_out])
                            size = os.path.getsize(path_out+NameFile)/dsize #
                            print('{} {:.1f}MB'.format(NameFile,size))

                        Downloaded_files.append(path_out+NameOut)

                else:
                    NameFile = line.split('/')[-1]
                    DateTimeFile = datetime.strptime(NameFile[NameFile.find('_s')+2:NameFile.find('_e')-1], '%Y%j%H%M%S')

                    if Product2 in NameFile    and    DateTimeIni <= DateTimeFile <= DateTimeFin:

                        NameOut = NameFile

                        if os.path.isfile(path_out+NameFile) == True:
                            #size_in_server = !gsutil du $line
                            #size_in_server = int(size_in_server[0].split()[0])
                            size_in_server = subprocess.run(['gsutil','du',line], capture_output=True, text=True).stdout
                            size_in_server = int(size_in_server.split(' ')[0])
                            size_in_folder = os.path.getsize(path_out+NameFile)
                            if size_in_server == size_in_folder:
                                print('{} already exists.'.format(NameFile))
                            else:
                                #!gsutil -q cp $line $path_out
                                subprocess.run(['gsutil','-q','cp',line,path_out])
                                size = os.path.getsize(path_out+NameFile)/dsize #
                                print('{} {:.1f}MB [Replaced]'.format(NameFile,size))

                        else:
                            #!gsutil -q cp $line $path_out
                            subprocess.run(['gsutil','-q','cp',line,path_out])
                            size = os.path.getsize(path_out+NameFile)/dsize #
                            print('{} {:.1f}MB'.format(NameFile,size))

                        Downloaded_files.append(path_out+NameOut)

            DateTimeIniLoop = DateTimeIniLoop + timedelta(minutes=60)

        Downloaded_files.sort()

        return Downloaded_files;

    else:
        print('\n  This function only work in Colab\n')

#-----------------------------------------------------------------------------------------------------------------------------------

