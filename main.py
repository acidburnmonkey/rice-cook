#!/bin/python3

import os
import re
import subprocess
import importlib
import requests

from rich.console import Console
from rich.progress import Progress
from rich.theme import Theme

ap_theme = Theme({'ok':'green', 'error':'red', 'checkt':'bold cyan','promp':'orange1'})
console = Console(theme=ap_theme)

def main():

    setup = 'z'
    sudo_check() 


    user_answer = input("set resolution 1920x1080? y/n: ").lower()
    console.print("run aranddr to proper set up", style='ok')
    try:
         if user_answer == 'y':
             os.system('xrandr -s 1920x1080')
    except Exception():
         print(Exception())       

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
    


#END OF MAIN

def dnf_config():
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

    subprocess.check_call('sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm', shell=True)  
    subprocess.check_call('sudo dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm', shell=True)
    console.print('rpmfusion added to repos :heavy_check_mark:', style='ok')


# install programs dnfmax list i can pass to dnf of programs to install
def install_programs_dnf():
    programs =[]

    with open("data.txt", 'r') as file:
        for line in file:
            programs.append(line.strip())

#for some reason they have to be passed to dnf individually 
# instead of unpacked list *programs
    for program in programs: 
        try:
            subprocess.run(f'dnf install -y {program} ', shell=True)
        except:
            console.print(Exception(),":x:" , style='error')
    


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
    user = os.getenv("SUDO_USER")
    if user is None:
        console.print("this program need 'sudo'", style='error')
        exit()
    else:
        console.print('ok :heavy_check_mark:', style='ok')

# Oh my zsh setup + flathub 
def zsh_fonts():
    with Progress() as progress:
        task = progress.add_task("[cyan]Installing Zhs etc...", total=5)
        while not progress.finished:
    
            console.print("installing oh my zsh ", style='ok')
            #installs oh my zsh
            url = "https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh"
            response = requests.get(url)
            script = response.text
            subprocess.run(script, shell=True, check=True)
            progress.update(task, advance=1)

            console.print("installing oh my zsh auto sugestions ", style='ok')
            # zsh auto sugestions
            subprocess.run('git clone https://github.com/zsh-users/zsh-autosuggestions ${zsh_custom:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions', shell=True)
            progress.update(task, advance=1)

            console.print("installing powerlevel10k ", style='ok')
            #powerlevel 10k
            subprocess.run('git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${zsh_custom:-$home/.oh-my-zsh/custom}/themes/powerlevel10k', shell=True)
            progress.update(task, advance=1)
            
            console.print("installing microsoft fonts", style='ok')
            # microsoft fonts fedora
            subprocess.run('sudo rpm -i https://downloads.sourceforge.net/project/mscorefonts2/rpms/msttcore-fonts-installer-2.6-1.noarch.rpm', shell=True)
            progress.update(task, advance=1)

            console.print("installing flathub", style='ok')
            # flathub
            subprocess.run('flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo', shell=True)
            progress.update(task, advance=1)

# copy and override dotfiles 
def copy_dotfiles(setup):

    home = os.path.expanduser("~")

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
        lis.append('desktop/i3', 'desktop/polybar')

        # copying files recusrsively
        for dir in lis:
            print(subprocess.run(f'cp -r {dir} {destination}', shell=True))


def executable_scripts():
    pass


if __name__ == '__main__':
    copy_dotfiles('d')
    executable_scripts()
