import os
import subprocess

this_dir = os.getcwd()


for root ,b,files in os.walk(os.path.join(this_dir,'dotfiles')):
    for element in files:
        if '.sh' in element or '.py' in element:
            try:
                subprocess.run(f"chmod +x {os.path.join(root,element)}", shell=True) 
            except Exception():
                print(Exception())


            print(os.path.join(root,element))
