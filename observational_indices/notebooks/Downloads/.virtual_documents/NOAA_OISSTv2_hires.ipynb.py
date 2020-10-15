mode = 'download'
# mode = 'update'


import sys


print(sys.executable)


import pathlib
import ftplib


local_path = pathlib.Path('./data')


if not local_path.exists(): 
    local_path.mkdir(parents=True)


url = 'ftp.cdc.noaa.gov'


folder = 'Datasets/noaa.oisst.v2.highres/'


with ftplib.FTP(url) as ftp: 
    
    # login 
    ftp.login()
    
    # move into the datasets directory 
    ftp.cwd(folder)
    
    # get the list of files
    filenames = ftp.nlst()
    
    # select only daily SST averages from version 2
    filenames = [f for f in filenames if 'sst.day.mean' in f and 'v2' in f]
    
    # if download mode, we download everything (the whole dataset)
    if mode == 'download': 
        for filename in filenames: 
            if local_path.joinpath(filename).exists(): 
                print(f"{filename} already downloaded in {str(local_path)}, skipping to next file")
            else:
                with open(local_path.joinpath(filename), 'wb') as f:
                    ftp.retrbinary('RETR ' + filename, f.write)
                if not local_path.joinpath(filename).exists(): 
                    print(f"download failed for {filename}")
                else:
                    print(f"{filename} successfully downloaded in {str(local_path)}")

    # if update mode, we only download the last file 
    elif mode == 'update':
        filename = filenames[-1]
        with open(local_path.joinpath(filename), 'wb') as f:
            ftp.retrbinary('RETR ' + filename, f.write)
        if not local_path.joinpath(filename).exists(): 
            print(f"download failed for {filename}")
        else:
            print(f"{filename} successfully downloaded in {str(local_path)}")       



