import os
import gdown
import subprocess
current_dir = os.getcwd()
try :
    os.mkdir('misic')
except FileExistsError:
    pass

os.chdir(os.path.join(current_dir,'misic'))

# https://drive.google.com/drive/folders/1BciF4x3_K3T8p1Y17lHn_xWXnSAZpvDE
url = 'https://drive.google.com/uc?id=1-3g_CjiJHKhRrJNjjZeAYu9KIGIAAAhC'
output ='fonts-c.zip' 
# gdown.download(url,output, quiet=False)

subprocess.run(f'unzip {output} ',stdout=subprocess.DEVNULL ,shell=True)
