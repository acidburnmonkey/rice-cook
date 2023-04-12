#!/bin/python3

import os
import re
import shutil
import subprocess
import importlib

from rich.console import Console
from rich.progress import Progress
from rich.theme import Theme

ap_theme = Theme({'ok':'green', 'error':'red', 'checkt':'bold cyan','promp':'orange1'})
console = Console(theme=ap_theme)

def main():

    setup = 'z'
    
    # sudo_check() 

    # HOME = os.getenv('home')
    # os.chdir(f'{home}/scripts/')
    # console.print("Working on > ", os.getcwd())
    
    

    # user_answer = input("set resolution 1920x1080? y/n: ").lower()
    #console.print("run aranddr to proper set up", style='ok')
    # try:
    #     if user_answer == 'y':
    #      os.system('xrandr -s 1920x1080')
     # except exception():
     #    print(Exception())       
     #    pass

    console.print('optimizing dnf.conf', style='ok')
    dnf_config()

    # modules_to_check = ["rich", "pandas"]
    # pip_modules(modules_to_check)
    
    #install_programs_dnf()
    #zsh_fonts()

# Pass D or L to copy_dotfiles function
    while (True): 
        console.print('Set up dotfiles for Desktop (D) or Laptop  (L) ?', style='promp')
        setup = input('>').lower()
        if setup == 'l' or setup == 'd':
            copy_dotfile(setup)
            break
    



#END OF MAIN

def dnf_config():
    # dnf conf
    with open('tt.txt', 'r+') as f:
        text = 'max_parallel_downloads=10 \nfastestmirror=true' 
        match = re.search(r'(max_parallel_downloads=10)', f.read())
        if not match:
            with open('tt.txt', 'a+') as f:
                f.write(text)
                console.print(' changes made to dnf_config :heavy_check_mark:', style='ok')
        else:
            console.print(' dnf.conf already optimized :heavy_check_mark:', style='checkt')


# install programs dnf
def install_programs_dnf():
    programs =[]

    with open("data.txt", 'r') as file:
        for line in file:
            programs.append(line.strip())
        print(programs)

    try:
        subprocess.check_call(['dnf', 'install', *programs])   
    except:
        console.print(exception(),":x:" , style='error')


## pip 
def install_pip_modules(modules):
    subprocess.check_call(['pip', 'install', *modules])

def pip_modules(modules):
    missing_modules = []
    for module in modules:
        try:
            importlib.import_module(module)
        except importerror:
            missing_modules.append(module)
    if missing_modules:
        console.print(f"the following modules are missing: {', '.join(missing_modules)}", style='checkt')
        install_pip_modules(missing_modules)
        return false
    else:
        console.print("all modules are installed. :heavy_check_mark:", style='ok')
        return true

## checks for sudo 
def sudo_check():
    user = os.getenv("sudo_user")
    if user is none:
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
            subprocess.run('sh -c "$(curl -fssl https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"', shell= True)
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

def copy_dotfiles(setup):

    home = os.path.expanduser("~")
    dotfiles_dir = os.getcwd()

    # list of relevant configs
    lis = list(next(os.walk('.'))[1])
    lis.append('picom.conf')
    lis.remove('.git')

    if ('desktop' in lis):
        lis.remove('desktop')
    if ( '.git'in lis ):
        lis.remove('.git')
    if ('.bachrc' in lis):
        lis.remove('.bashrc')
    if ('.zshrc' in lis) :
        lis.remove('.zshrc')

    destination = os.path.join(home,'.config')

    # copying files recusrsively
    for dir in lis:
        source = os.path.join(home, 'repos/dotfiles', dir)
        print(subprocess.run(f'cp -r {dotfiles_dir} {destination}', shell=True))






def executable_scripts():
    pass





if __name__ == '__main__':
    main()
