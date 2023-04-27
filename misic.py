import os
import gdown
import subprocess
import requests

current_dir = os.getcwd()
try :
    os.mkdir('misic')
    os.mkdir(os.path.join(home,'.fonts'))
except FileExistsError:
    pass

os.chdir(os.path.join(current_dir,'misic'))

#### Fonts 
# https://drive.google.com/drive/folders/1BciF4x3_K3T8p1Y17lHn_xWXnSAZpvDE
fonts_url = 'https://drive.google.com/uc?id=1-3g_CjiJHKhRrJNjjZeAYu9KIGIAAAhC'
output ='fonts-c.zip' 
gdown.download(fonts_url,output, quiet=False)
subprocess.run(f"unzip {output} {os.path.join(home,'.fonts')}",stdout=subprocess.DEVNULL ,shell=True)
subprocess.run("fc-cache -f",stdout=subprocess.DEVNULL ,shell=True)

#### i3 autotiling 
autotiling_url = 'https://raw.githubusercontent.com/nwg-piotr/autotiling/master/autotiling/main.py'
tiler = requests.get(autotiling_url, allow_redirects=True)
open('autotiling', 'wb').write(tiler.content)
subprocess.run('chmod +x autotiling', shell=True, stdout=subprocess.DEVNULL)
subprocess.run('cp autotiling /bin', shell=True, stdout=subprocess.DEVNULL)

