# Download GOES-16 and GOES-17 files
This jupyter notebook shows how to download data from GOES-16/17 using the GOES package.

Index:
- [Usage of GOES](#usage_goes)
- [Download ABI's channels](#donwload_abi_channels)
    - [Download Level 2 ABI data (one channel) of GOES-16](#download_L2_ABI_one_channel_g16)
    - [Download Level 2 ABI data (multiple channels) of GOES-16](#download_L2_ABI_multiple_channels_g16)
    - [Download Level 2 ABI data (multiple channels) of GOES-17](#download_L2_ABI_multiple_channels_g17)
    - [Download Level 1b ABI data](#download_L1b_ABI)
    - [Download ABI data with a CONUS domain](#download_ABI_conus)
    - [Download ABI data with a Mesoscale domain](#download_ABI_mesoscale)
- [Download Level-2 products derived from ABI](#download_ABI_product)
- [Download GLM data](#download_glm)
- [Rename downloaded file](#rename_download_file)

<a id='usage_goes'></a>
## Usage of GOES

Import the GOES package.


```python
import GOES
```

The function that allows download data is **GOES.download()**. Use the *help* function to get more information about **GOES.download()**.


```python
help(GOES.download)
```

    Help on function download in module GOES.downloads.download_data:
    
    download(Satellite, Product, DateTimeIni=None, DateTimeFin=None, domain=None, channel=None, rename_fmt=False, path_out='', retries=10, backoff=10, size_format='Decimal', show_download_progress=True)
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
        
        
        rename_fmt : bool or str, optional, default False
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
        
        show_download_progress : bool, optional, default True
            Parameter to enable and disable the visualization of download progress.
        
        Return
        ------
        Download_files : list
            List with the downloaded files (path+filename).
    


Get a list with products of GOES-16/17 available on Amazon server writing the follow:


```python
GOES.show_products()
```

     
    Products for goes16:
    	ABI-L1b-RadC
    	ABI-L1b-RadF
    	ABI-L1b-RadM
    	ABI-L2-ACHAC
    	ABI-L2-ACHAF
    	ABI-L2-ACHAM
    	ABI-L2-ACHTF
    	ABI-L2-ACHTM
    	ABI-L2-ACMC
    	ABI-L2-ACMF
    	ABI-L2-ACMM
    	ABI-L2-ACTPC
    	ABI-L2-ACTPF
    	ABI-L2-ACTPM
    	ABI-L2-ADPC
    	ABI-L2-ADPF
    	ABI-L2-ADPM
    	ABI-L2-AODC
    	ABI-L2-AODF
    	ABI-L2-CMIPC
    	ABI-L2-CMIPF
    	ABI-L2-CMIPM
    	ABI-L2-CODC
    	ABI-L2-CODF
    	ABI-L2-CPSC
    	ABI-L2-CPSF
    	ABI-L2-CPSM
    	ABI-L2-CTPC
    	ABI-L2-CTPF
    	ABI-L2-DMWC
    	ABI-L2-DMWF
    	ABI-L2-DMWM
    	ABI-L2-DSIC
    	ABI-L2-DSIF
    	ABI-L2-DSIM
    	ABI-L2-DSRC
    	ABI-L2-DSRF
    	ABI-L2-DSRM
    	ABI-L2-FDCC
    	ABI-L2-FDCF
    	ABI-L2-LSTC
    	ABI-L2-LSTF
    	ABI-L2-LSTM
    	ABI-L2-LVMPC
    	ABI-L2-LVMPF
    	ABI-L2-LVMPM
    	ABI-L2-LVTPC
    	ABI-L2-LVTPF
    	ABI-L2-LVTPM
    	ABI-L2-MCMIPC
    	ABI-L2-MCMIPF
    	ABI-L2-MCMIPM
    	ABI-L2-RRQPEF
    	ABI-L2-RSRC
    	ABI-L2-RSRF
    	ABI-L2-SSTF
    	ABI-L2-TPWC
    	ABI-L2-TPWF
    	ABI-L2-TPWM
    	ABI-L2-VAAF
    	GLM-L2-LCFA
    	SUVI-L1b-Fe093
    	SUVI-L1b-Fe131
    	SUVI-L1b-Fe171
    	SUVI-L1b-Fe195
    	SUVI-L1b-Fe284
    	SUVI-L1b-He303
     
    Products for goes17:
    	ABI-L1b-RadC
    	ABI-L1b-RadF
    	ABI-L1b-RadM
    	ABI-L2-ACHAC
    	ABI-L2-ACHAF
    	ABI-L2-ACHAM
    	ABI-L2-ACHTF
    	ABI-L2-ACHTM
    	ABI-L2-ACMC
    	ABI-L2-ACMF
    	ABI-L2-ACMM
    	ABI-L2-ACTPC
    	ABI-L2-ACTPF
    	ABI-L2-ACTPM
    	ABI-L2-ADPC
    	ABI-L2-ADPF
    	ABI-L2-ADPM
    	ABI-L2-AODC
    	ABI-L2-AODF
    	ABI-L2-CMIPC
    	ABI-L2-CMIPF
    	ABI-L2-CMIPM
    	ABI-L2-CODC
    	ABI-L2-CODF
    	ABI-L2-CPSC
    	ABI-L2-CPSF
    	ABI-L2-CPSM
    	ABI-L2-CTPC
    	ABI-L2-CTPF
    	ABI-L2-DMWC
    	ABI-L2-DMWF
    	ABI-L2-DMWM
    	ABI-L2-DSIC
    	ABI-L2-DSIF
    	ABI-L2-DSIM
    	ABI-L2-DSRC
    	ABI-L2-DSRF
    	ABI-L2-DSRM
    	ABI-L2-FDCC
    	ABI-L2-FDCF
    	ABI-L2-LSTC
    	ABI-L2-LSTF
    	ABI-L2-LSTM
    	ABI-L2-LVMPC
    	ABI-L2-LVMPF
    	ABI-L2-LVMPM
    	ABI-L2-LVTPC
    	ABI-L2-LVTPF
    	ABI-L2-LVTPM
    	ABI-L2-MCMIPC
    	ABI-L2-MCMIPF
    	ABI-L2-MCMIPM
    	ABI-L2-RRQPEF
    	ABI-L2-RSRC
    	ABI-L2-RSRF
    	ABI-L2-SSTF
    	ABI-L2-TPWC
    	ABI-L2-TPWF
    	ABI-L2-TPWM
    	ABI-L2-VAAF
    	GLM-L2-LCFA
    	SUVI-L1b-Fe093
    	SUVI-L1b-Fe13
    	SUVI-L1b-Fe131
    	SUVI-L1b-Fe17
    	SUVI-L1b-Fe171
    	SUVI-L1b-Fe195
    	SUVI-L1b-Fe284
    	SUVI-L1b-He303
     
    Descriptions of each product is shown in https://docs.opendata.aws/noaa-goes16/cics-readme.html#about-the-data 
    


<a id='donwload_abi_channels'></a>
## Download ABI's Channels

<a id='download_L2_ABI_one_channel_g16'></a>
### Download Level 2 ABI data (one channel) of GOES-16
In this example we will download one ABI's channel from *the Advanced Baseline Imager Level 2 Cloud and Moisture Imagery Full Disk* (**ABI-L2-CMIPF**) product of **GOES-16**.


```python
GOES.download('goes16', 'ABI-L2-CMIPF',
             DateTimeIni = '20200320-203000', DateTimeFin = '20200320-210000', 
             channel = ['13'], path_out='/home/joao/Downloads/')
```

    Files:
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802030177_e20200802039497_c20200802039590.nc 100% 27.0MB 17s
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802040177_e20200802049497_c20200802049583.nc 100% 27.0MB 13s
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802050177_e20200802059497_c20200802059576.nc 100% 27.0MB 11s





    ['/home/joao/Downloads/OR_ABI-L2-CMIPF-M6C13_G16_s20200802030177_e20200802039497_c20200802039590.nc',
     '/home/joao/Downloads/OR_ABI-L2-CMIPF-M6C13_G16_s20200802040177_e20200802049497_c20200802049583.nc',
     '/home/joao/Downloads/OR_ABI-L2-CMIPF-M6C13_G16_s20200802050177_e20200802059497_c20200802059576.nc']



Keep in mind that the start scan time that appear in the filename is considered as a the date and time of file.

In the last example was request the download of files between  **20200320-203000** and **20200320-210000**, however no file from 21 hours was downloaded, this is because sometimes the files have a date and time with some seconds later to DateTimeFin. In this cases is recomended add one minute to the DateTimeFin to ensure that download include files from this date and time. See the follow example:


```python
GOES.download('goes16', 'ABI-L2-CMIPF',
              DateTimeIni = '20200320-203000', DateTimeFin = '20200320-210100', 
              channel = ['13'], path_out='/home/joao/Downloads/')
```

    Files:
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802030177_e20200802039497_c20200802039590.nc 100% 27.0MB 34s
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802040177_e20200802049497_c20200802049583.nc 100% 27.0MB 17s
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802050177_e20200802059497_c20200802059576.nc 100% 27.0MB 27s
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802100177_e20200802109497_c20200802109572.nc 100% 27.0MB 15s





    ['/home/joao/Downloads/OR_ABI-L2-CMIPF-M6C13_G16_s20200802030177_e20200802039497_c20200802039590.nc',
     '/home/joao/Downloads/OR_ABI-L2-CMIPF-M6C13_G16_s20200802040177_e20200802049497_c20200802049583.nc',
     '/home/joao/Downloads/OR_ABI-L2-CMIPF-M6C13_G16_s20200802050177_e20200802059497_c20200802059576.nc',
     '/home/joao/Downloads/OR_ABI-L2-CMIPF-M6C13_G16_s20200802100177_e20200802109497_c20200802109572.nc']



When download finished, the function return the name and the path where file was download. If you wish, you can save this information in a variable to you will use it after.


```python
flist = GOES.download('goes16', 'ABI-L2-CMIPF',
                      DateTimeIni = '20200320-203000', DateTimeFin = '20200320-210100', 
                      channel = ['13'], path_out='/home/joao/Downloads/')
```

    Files:
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802030177_e20200802039497_c20200802039590.nc 100% 27.0MB 27s
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802040177_e20200802049497_c20200802049583.nc 100% 27.0MB 12s
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802050177_e20200802059497_c20200802059576.nc 100% 27.0MB 18s
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802100177_e20200802109497_c20200802109572.nc 100% 27.0MB 11s


<a id='download_L2_ABI_multiple_channels_g16'></a>
### Download Level 2 ABI data (multiple channels) of GOES-16
In the following example is shown how to download multiple ABI's channels from *the Advanced Baseline Imager Level 2 Cloud and Moisture Imagery Full Disk* (**ABI-L2-CMIPF**) product of **GOES-16**.


```python
flist = GOES.download('goes16', 'ABI-L2-CMIPF',
                      DateTimeIni = '20200320-203000', DateTimeFin = '20200320-205100', 
                      channel = ['08-10','13','14'], path_out='/home/joao/Downloads/')
```

    Files:
      OR_ABI-L2-CMIPF-M6C08_G16_s20200802030177_e20200802039485_c20200802039575.nc 100% 19.7MB 12s
      OR_ABI-L2-CMIPF-M6C08_G16_s20200802040177_e20200802049485_c20200802049572.nc 100% 19.7MB 9s
      OR_ABI-L2-CMIPF-M6C08_G16_s20200802050177_e20200802059485_c20200802059566.nc 100% 19.7MB 12s
      OR_ABI-L2-CMIPF-M6C09_G16_s20200802030177_e20200802039491_c20200802039586.nc 100% 18.6MB 14s
      OR_ABI-L2-CMIPF-M6C09_G16_s20200802040177_e20200802049491_c20200802049579.nc 100% 18.6MB 6s
      OR_ABI-L2-CMIPF-M6C09_G16_s20200802050177_e20200802059491_c20200802059574.nc 100% 18.6MB 8s
      OR_ABI-L2-CMIPF-M6C10_G16_s20200802030177_e20200802039497_c20200802039585.nc 100% 21.9MB 15s
      OR_ABI-L2-CMIPF-M6C10_G16_s20200802040177_e20200802049497_c20200802049578.nc 100% 21.9MB 16s
      OR_ABI-L2-CMIPF-M6C10_G16_s20200802050177_e20200802059497_c20200802059589.nc 100% 21.9MB 13s
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802030177_e20200802039497_c20200802039590.nc 100% 27.0MB 19s
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802040177_e20200802049497_c20200802049583.nc 100% 27.0MB 18s
      OR_ABI-L2-CMIPF-M6C13_G16_s20200802050177_e20200802059497_c20200802059576.nc 100% 27.0MB 16s
      OR_ABI-L2-CMIPF-M6C14_G16_s20200802030177_e20200802039485_c20200802039592.nc 100% 27.1MB 10s
      OR_ABI-L2-CMIPF-M6C14_G16_s20200802040177_e20200802049485_c20200802049590.nc 100% 27.1MB 15s
      OR_ABI-L2-CMIPF-M6C14_G16_s20200802050177_e20200802059485_c20200802059592.nc 100% 27.1MB 13s


<a id='download_L2_ABI_multiple_channels_g17'></a>
### Download Level 2 ABI data (multiple channels) of GOES-17
In the following example we will download multiple ABI's channels from *the Advanced Baseline Imager Level 2 Cloud and Moisture Imagery Full Disk* (**ABI-L2-CMIPF**) product of **GOES-17**.


```python
flist = GOES.download('goes17', 'ABI-L2-CMIPF',
                      DateTimeIni = '20200320-203000', DateTimeFin = '20200320-205100', 
                      channel = ['08-10','13','14'], path_out='/home/joao/Downloads/')
```

    Files:
      OR_ABI-L2-CMIPF-M6C08_G17_s20200802030321_e20200802039388_c20200802039456.nc 100% 20.5MB 7s
      OR_ABI-L2-CMIPF-M6C08_G17_s20200802040321_e20200802049388_c20200802049451.nc 100% 20.5MB 8s
      OR_ABI-L2-CMIPF-M6C08_G17_s20200802050321_e20200802059388_c20200802059457.nc 100% 20.5MB 7s
      OR_ABI-L2-CMIPF-M6C09_G17_s20200802030321_e20200802039393_c20200802039452.nc 100% 19.0MB 8s
      OR_ABI-L2-CMIPF-M6C09_G17_s20200802040321_e20200802049393_c20200802049473.nc 100% 19.0MB 10s
      OR_ABI-L2-CMIPF-M6C09_G17_s20200802050321_e20200802059393_c20200802059447.nc 100% 19.0MB 16s
      OR_ABI-L2-CMIPF-M6C10_G17_s20200802030321_e20200802039399_c20200802039454.nc 100% 22.6MB 9s
      OR_ABI-L2-CMIPF-M6C10_G17_s20200802040321_e20200802049399_c20200802049453.nc 100% 22.6MB 11s
      OR_ABI-L2-CMIPF-M6C10_G17_s20200802050321_e20200802059399_c20200802059458.nc 100% 22.6MB 9s
      OR_ABI-L2-CMIPF-M6C13_G17_s20200802030321_e20200802039399_c20200802039457.nc 100% 26.8MB 14s
      OR_ABI-L2-CMIPF-M6C13_G17_s20200802040321_e20200802049399_c20200802049460.nc 100% 26.8MB 13s
      OR_ABI-L2-CMIPF-M6C13_G17_s20200802050321_e20200802059399_c20200802059452.nc 100% 26.8MB 12s
      OR_ABI-L2-CMIPF-M6C14_G17_s20200802030321_e20200802039388_c20200802039460.nc 100% 26.9MB 13s
      OR_ABI-L2-CMIPF-M6C14_G17_s20200802040321_e20200802049388_c20200802049454.nc 100% 26.9MB 13s
      OR_ABI-L2-CMIPF-M6C14_G17_s20200802050321_e20200802059388_c20200802059476.nc 100% 26.9MB 11s


<a id='download_L1b_ABI'></a>
### Download Level 1b ABI data
In this example we will download multiple ABI's channels from *Advanced Baseline Imager Level 1b Full Disk* (**ABI-L1b-RadF**) product of **GOES-16**.


```python
flist = GOES.download('goes16', 'ABI-L1b-RadF',
                      DateTimeIni = '20200320-203000', DateTimeFin = '20200320-205100',
                      channel = ['10','13','14'], path_out='/home/joao/Downloads/')
```

    Files:
      OR_ABI-L1b-RadF-M6C10_G16_s20200802030177_e20200802039497_c20200802039560.nc 100% 22.7MB 8s
      OR_ABI-L1b-RadF-M6C10_G16_s20200802040177_e20200802049497_c20200802049556.nc 100% 22.7MB 11s
      OR_ABI-L1b-RadF-M6C10_G16_s20200802050177_e20200802059497_c20200802059577.nc 100% 22.7MB 8s
      OR_ABI-L1b-RadF-M6C13_G16_s20200802030177_e20200802039497_c20200802039578.nc 100% 29.8MB 10s
      OR_ABI-L1b-RadF-M6C13_G16_s20200802040177_e20200802049497_c20200802049570.nc 100% 29.8MB 12s
      OR_ABI-L1b-RadF-M6C13_G16_s20200802050177_e20200802059497_c20200802059567.nc 100% 29.8MB 9s
      OR_ABI-L1b-RadF-M6C14_G16_s20200802030177_e20200802039485_c20200802039583.nc 100% 29.8MB 13s
      OR_ABI-L1b-RadF-M6C14_G16_s20200802040177_e20200802049485_c20200802049574.nc 100% 29.7MB 16s
      OR_ABI-L1b-RadF-M6C14_G16_s20200802050177_e20200802059485_c20200802059581.nc 100% 29.7MB 11s


<a id='download_ABI_conus'></a>
### Download ABI data with a CONUS domain
The previous examples showed how to download data with a Full Disk domain, however, this is not the only GOES-16/17 scan domain. In total, the GOES-16/17 scan domains are: Full Disk, CONUS, Mesoscale 1 and Mesoscale 2. The following example shows how to download channels from *Advanced Baseline Imager Level 2 Cloud and Moisture Imagery* ***CONUS*** (**ABI-L2-CMIPC**) product with a **CONUS** domain.


```python
flist = GOES.download('goes16', 'ABI-L2-CMIPC',
                      DateTimeIni = '20200320-203000', DateTimeFin = '20200320-203500',
                      channel = ['10','13','14'], path_out='/home/joao/Downloads/')
```

    Files:
      OR_ABI-L2-CMIPC-M6C10_G16_s20200802031145_e20200802033529_c20200802034015.nc 100% 3.4MB 2s
      OR_ABI-L2-CMIPC-M6C13_G16_s20200802031145_e20200802033529_c20200802034057.nc 100% 4.3MB 3s
      OR_ABI-L2-CMIPC-M6C14_G16_s20200802031145_e20200802033518_c20200802034049.nc 100% 4.3MB 2s


<a id='download_ABI_mesoscale'></a>
### Download ABI data with a Mesoscale domain
To download mesoscale data it is necessary to specify if the domain is mesoscale 1 or mesoscale 2. To do this, we must use the **domain** parameter. The following example shows how to download channels from *Advanced Baseline Imager Level 2 Cloud and Moisture Imagery* ***Mesoscale*** (**ABI-L2-CMIPM**) product with a **mesoscale 1** domain.


```python
flist = GOES.download('goes16', 'ABI-L2-CMIPM',
                      DateTimeIni = '20200320-203000', DateTimeFin = '20200320-203500',
                      domain='M1', channel = ['10','13','14'], path_out='/home/joao/Downloads/')
```

    Files:
      OR_ABI-L2-CMIPM1-M6C10_G16_s20200802030253_e20200802030322_c20200802030383.nc 100% 0.3MB 0s
      OR_ABI-L2-CMIPM1-M6C10_G16_s20200802031224_e20200802031292_c20200802031338.nc 100% 0.3MB 1s
      OR_ABI-L2-CMIPM1-M6C10_G16_s20200802032224_e20200802032293_c20200802032333.nc 100% 0.3MB 0s
      OR_ABI-L2-CMIPM1-M6C10_G16_s20200802033224_e20200802033293_c20200802033341.nc 100% 0.3MB 1s
      OR_ABI-L2-CMIPM1-M6C10_G16_s20200802034224_e20200802034293_c20200802034343.nc 100% 0.3MB 1s
      OR_ABI-L2-CMIPM1-M6C13_G16_s20200802030253_e20200802030321_c20200802030400.nc 100% 0.4MB 1s
      OR_ABI-L2-CMIPM1-M6C13_G16_s20200802031224_e20200802031293_c20200802031358.nc 100% 0.4MB 1s
      OR_ABI-L2-CMIPM1-M6C13_G16_s20200802032224_e20200802032293_c20200802032371.nc 100% 0.4MB 0s
      OR_ABI-L2-CMIPM1-M6C13_G16_s20200802033224_e20200802033293_c20200802033359.nc 100% 0.4MB 1s
      OR_ABI-L2-CMIPM1-M6C13_G16_s20200802034224_e20200802034293_c20200802034360.nc 100% 0.4MB 1s
      OR_ABI-L2-CMIPM1-M6C14_G16_s20200802030253_e20200802030310_c20200802030401.nc 100% 0.4MB 0s
      OR_ABI-L2-CMIPM1-M6C14_G16_s20200802031224_e20200802031281_c20200802031356.nc 100% 0.4MB 0s
      OR_ABI-L2-CMIPM1-M6C14_G16_s20200802032224_e20200802032281_c20200802032361.nc 100% 0.4MB 0s
      OR_ABI-L2-CMIPM1-M6C14_G16_s20200802033224_e20200802033281_c20200802033371.nc 100% 0.4MB 1s
      OR_ABI-L2-CMIPM1-M6C14_G16_s20200802034224_e20200802034281_c20200802034370.nc 100% 0.4MB 1s


<a id='download_ABI_product'></a>
## Download Level-2 products derived from ABI

Level-2 products derived from ABI, as the *Rainfall Rate (Quantitative Precipitation Estimate) Full Disk* (**ABI-L2-RRQPEF**), can be download as following:


```python
flist = GOES.download('goes16', 'ABI-L2-RRQPEF',
                      DateTimeIni = '20200320-203000', DateTimeFin = '20200320-210100',
                      path_out='/home/joao/Downloads/')
```

    Files:
      OR_ABI-L2-RRQPEF-M6_G16_s20200802030177_e20200802039485_c20200802040007.nc 100% 1.8MB 1s
      OR_ABI-L2-RRQPEF-M6_G16_s20200802040177_e20200802049485_c20200802050036.nc 100% 1.8MB 1s
      OR_ABI-L2-RRQPEF-M6_G16_s20200802050177_e20200802059485_c20200802059585.nc 100% 1.8MB 2s
      OR_ABI-L2-RRQPEF-M6_G16_s20200802100177_e20200802109485_c20200802109583.nc 100% 1.8MB 1s


<a id='download_glm'></a>
## Download GLM data

The following example show how to download the GLM data:


```python
flist = GOES.download('goes16', 'GLM-L2-LCFA',
                      DateTimeIni = '20200320-203000', DateTimeFin = '20200320-203300',
                      path_out='/home/joao/Downloads/')
```

    Files:
      OR_GLM-L2-LCFA_G16_s20200802030000_e20200802030200_c20200802030227.nc 100% 0.4MB 1s
      OR_GLM-L2-LCFA_G16_s20200802030200_e20200802030400_c20200802030430.nc 100% 0.4MB 1s
      OR_GLM-L2-LCFA_G16_s20200802030400_e20200802031000_c20200802031031.nc 100% 0.4MB 1s
      OR_GLM-L2-LCFA_G16_s20200802031000_e20200802031200_c20200802031228.nc 100% 0.4MB 1s
      OR_GLM-L2-LCFA_G16_s20200802031200_e20200802031400_c20200802031425.nc 100% 0.4MB 1s
      OR_GLM-L2-LCFA_G16_s20200802031400_e20200802032000_c20200802032026.nc 100% 0.4MB 1s
      OR_GLM-L2-LCFA_G16_s20200802032000_e20200802032200_c20200802032228.nc 100% 0.4MB 0s
      OR_GLM-L2-LCFA_G16_s20200802032200_e20200802032400_c20200802032428.nc 100% 0.4MB 0s
      OR_GLM-L2-LCFA_G16_s20200802032400_e20200802033000_c20200802033027.nc 100% 0.3MB 1s
      OR_GLM-L2-LCFA_G16_s20200802033000_e20200802033200_c20200802033228.nc 100% 0.4MB 1s


<a id='rename_download_file'></a>
## Rename downloaded file

The name of GOES-16/17 data is very long because saves the start scan time, the end scan time and the scan file creation time, all of them is in julian day format. If you want to download files with a short name, keeping only the start scan time (with a custom date and time format), then use the **rename_fmt** parameter. This parameter uses the "C" date and time format. In the follow example is shown an example.


```python
GOES.download('goes16', 'ABI-L2-CMIPF',
              DateTimeIni = '20200320-203000', DateTimeFin = '20200320-210100', 
              channel = ['13'], rename_fmt = '%Y%m%d%H%M', path_out='/home/joao/Downloads/')
```

    Files:
      OR_ABI-L2-CMIPF-M6C13_G16_s202003202030.nc 100% 27.0MB 14s
      OR_ABI-L2-CMIPF-M6C13_G16_s202003202040.nc 100% 27.0MB 16s
      OR_ABI-L2-CMIPF-M6C13_G16_s202003202050.nc 100% 27.0MB 9s
      OR_ABI-L2-CMIPF-M6C13_G16_s202003202100.nc 100% 27.0MB 12s





    ['/home/joao/Downloads/OR_ABI-L2-CMIPF-M6C13_G16_s202003202030.nc',
     '/home/joao/Downloads/OR_ABI-L2-CMIPF-M6C13_G16_s202003202040.nc',
     '/home/joao/Downloads/OR_ABI-L2-CMIPF-M6C13_G16_s202003202050.nc',
     '/home/joao/Downloads/OR_ABI-L2-CMIPF-M6C13_G16_s202003202100.nc']



In the last example the **rename_fmt** was **'%Y%m%d%H%M'**, which means: **year** (4-digits), **month** (2-digits), **day** (2-digits), **hour** (2-digits) and **minutes** (2-digits).

For cases where the data have a higher temporal resolution, as the GLM data, you going to need add the **seconds** code in **rename_fmt**. See the follow example.


```python
GOES.download('goes16', 'GLM-L2-LCFA',
              DateTimeIni = '20200320-203000', DateTimeFin = '20200320-203200',
              rename_fmt = '%Y%m%d%H%M%S', path_out='/home/joao/Downloads/')
```

    Files:
      OR_GLM-L2-LCFA_G16_s20200320203000.nc 100% 0.4MB 1s
      OR_GLM-L2-LCFA_G16_s20200320203020.nc 100% 0.4MB 0s
      OR_GLM-L2-LCFA_G16_s20200320203040.nc 100% 0.4MB 0s
      OR_GLM-L2-LCFA_G16_s20200320203100.nc 100% 0.4MB 1s
      OR_GLM-L2-LCFA_G16_s20200320203120.nc 100% 0.4MB 1s
      OR_GLM-L2-LCFA_G16_s20200320203140.nc 100% 0.4MB 1s
      OR_GLM-L2-LCFA_G16_s20200320203200.nc 100% 0.4MB 1s





    ['/home/joao/Downloads/OR_GLM-L2-LCFA_G16_s20200320203000.nc',
     '/home/joao/Downloads/OR_GLM-L2-LCFA_G16_s20200320203020.nc',
     '/home/joao/Downloads/OR_GLM-L2-LCFA_G16_s20200320203040.nc',
     '/home/joao/Downloads/OR_GLM-L2-LCFA_G16_s20200320203100.nc',
     '/home/joao/Downloads/OR_GLM-L2-LCFA_G16_s20200320203120.nc',
     '/home/joao/Downloads/OR_GLM-L2-LCFA_G16_s20200320203140.nc',
     '/home/joao/Downloads/OR_GLM-L2-LCFA_G16_s20200320203200.nc']


