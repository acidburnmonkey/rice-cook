#!/bin/python3

# Program Shoud run with sudo -HE 
# https://github.com/acidburnmonkey
#

import os
import re
import subprocess
import importlib
import requests
import logging
import gdown
from rich.console import Console
from rich.theme import Theme

# pylint: disable=subprocess-run-check
# pylint: disable=broad-exception-caught
# pylint: disable=logging-fstring-interpolation

logging.basicConfig(
        format="%(asctime)s | %(levelno)s | %(funcName)s| %(message)s ",
        filename='installer.log'
        )

ap_theme = Theme({'ok':'green', 'error':'red', 'checkt':'bold cyan','promp':'orange1'})
console = Console(theme=ap_theme)

user = input("Type user name: ")
home = os.path.join('/home',user)

def main():

    setup = ''
    confirm_user =''

    sudo_check()
    
    console.print(f"Setting up for user {user} ", style='promp')
    while(True):
        confirm_user = input(" y/n ")
        if (confirm_user.lower() == 'n'):
            exit()
        elif (confirm_user.lower() == 'y'):
            break


    #set temporary resolution for sesion 
    user_answer = input("Set resolution 1920x1080? y/n: ").lower()
    console.print("Run aranddr to proper set up", style='ok')
    try:
         if user_answer == 'y':
             os.system('xrandr -s 1920x1080')
    except Exception as e:
        logging.critical(f"Error at xrandr: {str(e)}")    

    console.print('optimizing dnf.conf', style='ok')
    dnf_config()

    # modules_to_check = ["rich", "pandas"]
    # pip_modules(modules_to_check)
    
    install_programs_dnf()
    zsh_fonts()

# Pass D or L to copy_dotfiles function
    while (True): 
        console.print('Set up dotfiles for Desktop (D) or Laptop  (L) ?', style='promp')
        setup = input('>').lower()
        if setup == 'l' or setup == 'd':
            copy_dotfiles(setup)
            break
 
    executable_scripts()
    msic_configs()
    
    #correcting ownership
    subprocess.run(f"chown -R {user}:{user} {home}",shell=True ,stdout=subprocess.DEVNULL)

################
# END OF MAIN #
################

def dnf_config():
    console.rule("Configuring dnf", style='checkt')

    # dnf conf
    with open('/etc/dnf/dnf.conf' , 'r+') as f:
        text = 'max_parallel_downloads=10 \nfastestmirror=true' 
        match = re.search(r'(max_parallel_downloads=10)', f.read())
        if not match:
            with open('/etc/dnf/dnf.conf', 'a+') as f:
                f.write(text)
                console.print(' changes made to dnf_config :heavy_check_mark:', style='ok')
        else:
            console.print(' dnf.conf already optimized :heavy_check_mark:', style='checkt')

    subprocess.check_call('sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm',stdout=subprocess.DEVNULL,  shell=True)  
    subprocess.check_call('sudo dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm',stdout=subprocess.DEVNULL, shell=True)
    console.print('rpmfusion added to repos :heavy_check_mark:', style='ok')


# install programs dnfmax list i can pass to dnf of programs to install
def install_programs_dnf():
    console.rule("Installing All Programs DNF ", style='checkt')

    programs =[]
    with open("data.txt", 'r') as file:
        for line in file:
            programs.append(line.strip())

#for some reason they have to be passed to dnf individually 
# instead of unpacked list *programs
    for program in programs: 
        try:
            subprocess.run(f'dnf install -y {program} ', shell=True)
        except Exception as e:
            console.print(Exception(),":x:" , style='error')
            logging.critical(f"Error at Installing programs: {str(e)}")    
    

## pip 
def install_pip_modules(modules):

    subprocess.check_call(['pip', 'install', *modules])

def pip_modules(modules):
    missing_modules = []
    for module in modules:
        try:
            importlib.import_module(module)
        except ImportError():
            missing_modules.append(module)
    if missing_modules:
        console.print(f"the following modules are missing: {', '.join(missing_modules)}", style='checkt')
        install_pip_modules(missing_modules)
        return False

    else:
        console.print("all modules are installed. :heavy_check_mark:", style='ok')
        return True


## checks for sudo 
def sudo_check():
    sudo_user = os.getenv("SUDO_USER")
    if sudo_user is None:
        console.print("This program must run as sudo -HE ./script ", style='error')
        exit()
    else:
        console.print('ok :heavy_check_mark:', style='ok')

# Oh my zsh setup + flathub 
def zsh_fonts():
    console.rule("Installing Zsh fonts", style='checkt')
    
    try:
        console.print("installing oh my zsh ", style='ok')

        #installs oh my zsh
        ohmy_url = "https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
        zsh_installer = requests.get(ohmy_url, timeout=10)
        open('install.sh', 'wb').write(zsh_installer.content)
        subprocess.run('chmod +x install.sh ', stdout=subprocess.DEVNULL, shell=True, check=True)
        subprocess.run(f'sudo -u {user} ./install.sh', shell=True, check=True)

        console.print("installing oh my zsh auto sugestions ", style='ok')
        # zsh auto sugestions
        subprocess.run('git clone https://github.com/zsh-users/zsh-autosuggestions ${zsh_custom:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions', shell=True)

        console.print("installing powerlevel10k ", style='ok')
        #powerlevel 10k
        subprocess.run('git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${zsh_custom:-$home/.oh-my-zsh/custom}/themes/powerlevel10k', shell=True)

    except Exception as e:
        logging.warning(f"Could not set up Zsh: {str(e)}")
    

    console.print("installing flathub", style='ok')
    # flathub
    subprocess.run('flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo', shell=True, stdout=subprocess.DEVNULL)

# copy and override dotfiles 
def copy_dotfiles(setup):
    console.rule("Copying Dotfiles", style='checkt')


    # list of relevant configs
    lis = list(next(os.walk('.'))[1])

    lis.append('picom.conf')
    if ('desktop' in lis):
        lis.remove('desktop')
    if ( '.git'in lis ):
        lis.remove('.git')
    if ('.bachrc' in lis):
        lis.remove('.bashrc')
    if ('.zshrc' in lis) :
        lis.remove('.zshrc')

    dotfiles_dir = os.getcwd()
    destination = os.path.join(home,'.config')

    subprocess.run(f"cp -r {os.path.join(dotfiles_dir,'.zshrc')} {home}", shell=True)

    if (setup =='l'):
        console.print("Setting up dotfiles for Laptop", style='ok')
        # copying files recusrsively
        for dir in lis:
            print(subprocess.run(f'cp -r {dir} {destination}', shell=True))
    
    elif (setup =='d'):
        console.print("Setting up dotfiles for Desktop", style='ok')

        if ('i3' in lis):
            lis.remove('i3')
        if ('polybar' in lis):
            lis.remove('polybar')
        lis.append('desktop/i3')
        lis.append('desktop/polybar')
        # copying files recusrsively
        for dir in lis:
            print(subprocess.run(f'cp -r {dir} {destination}', shell=True))


def executable_scripts():
    console.rule('Making scripts executable', style='checkt')

    for root ,_,files in os.walk(os.path.join(home,'.config')):
        for element in files:
            if '.sh' in element or '.py' in element:
                try:
                    subprocess.run(f"chmod +x {os.path.join(root,element)}", shell=True) 
                except Exception as e:
                    logging.critical(f"Error at executable_scripts: {str(e)}")    
    console.print("Job done :heavy_check_mark:", style='ok')

def msic_configs():
    console.rule('Setting up final configs', style='checkt')

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
    subprocess.run(f"unzip {output} -d {os.path.join(home,'.fonts')}",stdout=subprocess.DEVNULL ,shell=True)
    subprocess.run("fc-cache -f",stdout=subprocess.DEVNULL ,shell=True)

    #### i3 autotiling 
    autotiling_url = 'https://raw.githubusercontent.com/nwg-piotr/autotiling/master/autotiling/main.py'
    tiler = requests.get(autotiling_url, allow_redirects=True, timeout=10)
    open('autotiling', 'wb').write(tiler.content)
    subprocess.run('chmod +x autotiling', shell=True, stdout=subprocess.DEVNULL)
    subprocess.run('cp autotiling /bin', shell=True, stdout=subprocess.DEVNULL)


if __name__ == '__main__':
    main()
