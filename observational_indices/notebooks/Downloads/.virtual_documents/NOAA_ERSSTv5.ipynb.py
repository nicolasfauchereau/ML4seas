get_ipython().run_line_magic("matplotlib", " inline")


import sys


print(sys.executable)


from datetime import datetime
from dateutil.relativedelta import relativedelta


import pathlib
import requests


def get_url_paths(url, ext='', params={}):
    import requests 
    from bs4 import BeautifulSoup
    response = requests.get(url, params=params)
    if response.ok:
        response_text = response.text
    else:
        return response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    parent = [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
    return parent


local_path = pathlib.Path('./data')


if not local_path.exists(): 
    local_path.mkdir(parents=True)


base_url = 'https://www1.ncdc.noaa.gov/pub/data/cmb/ersst/v5/netcdf/'


ext = 'nc'


remote_files = get_url_paths(base_url, ext)


remote_files[0]


remote_files[-1]


remote_files = [f.split('/')[-1] for f in remote_files]


last_avail = datetime.strptime(f"{remote_files[-1].split('.')[-2]}01", "get_ipython().run_line_magic("Y%m%d")", "")


lag = (datetime.utcnow() - last_avail).days


if lag >= 70: 
    print(f"Warning, the last available date on the NOAA server ({last_avail:get_ipython().run_line_magic("Y-%m})", " is more than 70 days old ({lag} days ...)\")")


local_files  = list(local_path.glob("ersst.*.nc"))


local_files  = [f.name for f in local_files]


missing_files = list(set(remote_files) - set(local_files))


missing_files.sort()


missing_files[0]


missing_files[-1]


len(missing_files)


for filename in missing_files: 
    print(f"now trying to download {filename} from {base_url}")
    r = requests.get(f"{base_url}/{filename}") 
    if r.status_code == 200:
        with open(local_path.joinpath(filename), 'wb') as f:
            f.write(r.content) 
        if local_path.joinpath(filename).exists():
            print(f"{filename} successfully saved in {str(local_path)}")
        else: 
            print(f"{filename} was available remotely but could not be saved locally in {str(local_path)}")
    else: 
        print(f"unable to access {filename} at {base_url}")



