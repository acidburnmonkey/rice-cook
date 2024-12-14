#!/bin/python3

# Program Shoud run with sudo -HE 
# https://github.com/acidburnmonkey
#

import os
import re
import subprocess
import requests
import shutil
import logging
import gdown
from git import Repo
from rich.console import Console
from rich.theme import Theme

# pylint: disable=subprocess-run-check
# pylint: disable=broad-exception-caught
# pylint: disable=logging-fstring-interpolation

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formater = logging.Formatter("%(asctime)s | %(levelno)s | %(funcName)s| %(message)s")
f_handler = logging.FileHandler('logg.log')
f_handler.setFormatter(formater)
logger.addHandler(f_handler)

logging.basicConfig(
        format="%(asctime)s | %(levelno)s | %(funcName)s| %(message)s ",
        filename='logg.log', level=logging.WARNING
        )

ap_theme = Theme({'ok':'green', 'error':'red', 'checkt':'bold cyan','promp':'orange1'})
console = Console(theme=ap_theme)

user = os.getlogin() 
home = os.path.join('/home',user)


def main():

    setup = ''
    # confirm_user =''
    local_user = user
    
    sudo_check()
    
    console.print(f"Setting up for user {local_user} ", style='promp')
    # while(True):
    #     confirm_user = input(" y/n ")
    #     if (confirm_user.lower() == 'n'):
    #         user := input('Type username : ')
    #         continue
    #     elif (confirm_user.lower() == 'y'):
    #         break


    console.print('optimizing dnf.conf', style='ok')
    dnf_config()
    install_programs_dnf()
    zsh_fonts()
    hyprland()
    msic_configs()
    
    #This should not need sudo
# Pass D or L to copy_dotfiles function
    while (True): 
        console.print('Set up dotfiles for Desktop (D) or Laptop  (L) ?', style='promp')
        setup = input('>').lower()
        if setup == 'l' or setup == 'd':
            copy_dotfiles(setup)
            break
 
    executable_scripts()
    systemd()

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
            logger.info('changes made to dnf_config')
        else:
            console.print(' dnf.conf already optimized :heavy_check_mark:', style='checkt')

    subprocess.check_call('sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm',stdout=subprocess.DEVNULL,  shell=True)  
    subprocess.check_call('sudo dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm',stdout=subprocess.DEVNULL, shell=True)
    console.print('rpmfusion added to repos :heavy_check_mark:', style='ok')
    logger.info('rpmfusion added to repos')
    
    #update Dnf 
    subprocess.run('dnf upgrade -y', shell=True)
    logger.info('Updated Dnf ')


def hyprland():

    console.rule("Configuring hyprland", style='checkt')
    if not os.path.exists(home +'/.local/bin'):
        os.mkdir(home +'/.local/bin')

    # create tty launcher
    with open(home +'/.local/bin/wrappedhl', 'w+') as file:
        file.write('''#!/bin/sh
    cd ~
    export _JAVA_AWT_WM_NONREPARENTING=1
    export XCURSOR_SIZE=24
    exec Hyprland ''')

        file.seek(0)
        for line in file:
            line.strip()

    # create .desktop file
    with open('/usr/share/wayland-sessions/hyprland.desktop', 'w+') as file:
        file.write(f'''[Desktop Entry]
Name=Hyprland
Comment=An intelligent dynamic tiling Wayland compositor
Exec={home}/.local/bin/wrappedhl
Type=Application ''')

        file.seek(0)
        for line in file:
            line.strip()

    #making them executable
    subprocess.run(f'chmod +x {home}/.local/bin/wrappedhl', shell=True)
    subprocess.run('chmod +x /usr/share/wayland-sessions/hyprland.desktop', shell=True)
    
    logger.info('Created hyprland .desktop and wrappedhl')
    console.print('Created hyprland .desktop and wrappedhl :heavy_check_mark:', style='ok')


# install programs dnf
def install_programs_dnf():
    console.rule("Installing All Programs DNF ", style='checkt')

    programs =[]
    others = []
    flatpaks= []

    with open("data.config", 'r') as file:
        lines = file.readlines()

        # Variables to store line numbers of headers
        main_index = 0
        others_index = 0
        flatpak_index = 0

        # Find the line numbers of headers
        for index, line in enumerate(lines):
            if '[Main]' in line:
                main_index = index
            elif '[other-programs]' in line:
                others_index = index
            elif '[Flatpak]' in line:
                flatpak_index = index
        
        file.seek(0)
        for index,line in enumerate(file):
            #empty strings
            if not line.strip():
                continue
            elif index < others_index and ('[' not in line):
                programs.append(line.strip())
            elif index > others_index and index < flatpak_index:
                others.append(line.strip())
            elif index > flatpak_index:
                flatpaks.append(line.strip())
            elif '[' in line.strip():
                   continue

    #for some reason they have to be passed to dnf individually 
    # instead of unpacked list *programs
    programs.extend(others)    
    for program in programs: 
        try:
            subprocess.run(f'dnf install -y {program} ', shell=True)
        except Exception as e:
            console.print(Exception(),":x:" , style='error')
            logging.critical(f"Error at Installing programs: {str(e)}")    

    for fp in flatpaks: 
        try:
            subprocess.run(f'flatpak install flathub -y {fp}', shell=True)
        except Exception as e:
            console.print(Exception(),":x:" , style='error')
            logging.critical(f"Error at Installing flatpaks: {str(e)}")    

    logger.info('Installed programs in data.config')


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
        
        #removing exec line 
        with open('install.sh', 'r') as f:
            contents = f.read()
        pattern = r'^\s*exec zsh -l$'
        matches = re.findall(pattern, contents, flags=re.MULTILINE)
        if matches:
            contents = re.sub(pattern, '', contents, flags=re.MULTILINE)
            with open('install.sh', 'w') as f:
                f.write(contents)

        subprocess.run('chmod +x install.sh ', stdout=subprocess.DEVNULL, shell=True, check=True)
        subprocess.run(f'sudo -u {user} ./install.sh', shell=True, check=True)

        console.print("installing oh my zsh auto sugestions ", style='ok')
        # zsh auto sugestions
        subprocess.run(f'git clone https://github.com/zsh-users/zsh-autosuggestions {home}/.oh-my-zsh/custom/plugins/zsh-autosuggestions', shell=True)

        console.print("installing powerlevel10k ", style='ok')
        #powerlevel 10k
        subprocess.run(f"git clone --depth=1 https://github.com/romkatv/powerlevel10k.git {home}/.oh-my-zsh/custom/themes/powerlevel10k", shell=True)
        logger.info('Installed  Oh_my_zsh , powerlevel10k , autosuggestions')

    except Exception as e:
        logging.warning(f"Could not set up Zsh: {str(e)}")
        console.print("Error setting up ohmyzsh :X:", style='error')

    console.print("installing flathub", style='ok')
    # flathub
    subprocess.run('flatpak remote-add --if-not-exists flathub https://flatInstalled programs in data.txthub.org/repo/flathub.flatpakrepo', shell=True, stdout=subprocess.DEVNULL)
    logger.info('Installed  Flathub')

# copy and override dotfiles 
def copy_dotfiles(setup):
    console.rule("Copying Dotfiles", style='checkt')

    # list of relevant configs
    lis = os.listdir()
    exeptions = ['.git', '.bashrc','.zshrc','retired','data.config','wrappedhl','Hyprland','install.sh',
                 'logg.log','README.md','.gitignore','rice-cook.py','Laptop-configs','.ideavimrc']
    
    for z in exeptions:
        if z in lis:
            lis.remove(z)

    destination = os.path.join(home,'.config')

    shutil.copy2('.zshrc',home)
    shutil.copy2('.p10k.zsh',home)
    shutil.copy2('.vimrc',home)
    shutil.copy2('.ideavimrc',home)

    if (setup =='l'):
        console.print("Setting up dotfiles for Laptop", style='ok')
        # copying files recusrsively
        for dir in lis:
            print(subprocess.run(f'cp -r {dir} {destination}', shell=True))
    
    elif (setup =='d'):
        console.print("Setting up dotfiles for Desktop", style='ok')

        # copying files recusrsively
        for dir in lis:
            print(subprocess.run(f'cp -r {dir} {destination}', shell=True))

    console.print("Dotfiles copied :heavy_check_mark:", style='ok')
    logger.info('Dotfiles copied')


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
    logger.info('Made scripts in .config executable')

#need sudo
def msic_configs():
    console.rule('Setting up final configs', style='checkt')

    current_dir = os.getcwd()
    try :
        os.mkdir('misic')
        os.mkdir(os.path.join(home,'.themes'))
    except FileExistsError:
        pass

    os.chdir(os.path.join(current_dir,'misic'))

    fonts_url = "https://github.com/acidburnmonkey/fonts"
    fonts_dir = os.path.join(home,".fonts")
    try:
        Repo.clone_from(fonts_url, fonts_dir)
    except Exception as e:
        print(f"Failed to clone repository: {e}")
    
    # to system 
    shutil.copytree(home+"/.fonts",'/usr/share/fonts/', dirs_exist_ok=True)

    console.print("Fonts downloaded :heavy_check_mark:", style='ok')
    logger.info('Fonts donwloaded ')

    #Icons 
    subprocess.run('git clone --depth 1 https://github.com/EliverLara/candy-icons.git /usr/share/icons/candy-icons', shell=True, stdout=subprocess.DEVNULL)
    console.print("Icons have been downloaded :heavy_check_mark:", style='ok')
    logger.info('candy-icons downloaded')

    try:
        themes_urls =['https://drive.google.com/uc?id=1KkqC5vaBjePSHxjBI_8PWfm3jNW5gO7k','https://drive.google.com/uc?id=1-qq3wmuQhkKHpW_8OrRNS92AHD9LE4un' 
                              ,'https://drive.google.com/uc?id=1mxkN9b4Ws7CeqF_KaTlA3dA5e75UUa4y','https://drive.google.com/uc?id=1cYLRsxmWeQJMOS7QEGEgJenRPKxgwN7X']

        for index,file in enumerate(themes_urls):
            output = str(index)+'.zip' 
            gdown.download(file, output ,quiet=False)
            subprocess.run(f"unzip {output} -d {os.path.join(home,'.themes')}", shell=True, stdout=subprocess.DEVNULL)

        # to system 
        shutil.copytree(home+"/.themes",'/usr/share/themes/', dirs_exist_ok=True)

        console.print("Themes have been downloaded :heavy_check_mark:", style='ok')
        logger.info('Themes have been downloaded')

        ## Set themes Gtk
        subprocess.run("gsettings set org.gnome.desktop.interface icon-theme 'candy-icons'", shell=True)
        subprocess.run("gsettings set org.gnome.desktop.interface gtk-theme 'Catppuccin-Macchiato-Standard-Blue-Dark'", shell=True)
        subprocess.run("gsettings set org.gnome.desktop.interface font-name 'Roboto-Regular'", shell=True)
        
        #Flatpak force theme
        subprocess.run("flatpak override --filesystem=$HOME/.themes", shell=True)
        subprocess.run("flatpak override --env=GTK_THEME=Catppuccin-Macchiato-Standard-Blue-Dark", shell=True)
        console.print("Themes have been Set :heavy_check_mark:", style='ok')
        logger.info('Themes have been Set')

    except Exception as e:
        logging.critical(f"Could not get themes :{str(e)}")
        console.print("Error with Themes :X:", style='error')
    
    # codec and multmedia
    try:
        subprocess.run('dnf swap ffmpeg-free ffmpeg --allowerasing', shell=True)
        subprocess.run('dnf update @multimedia --setopt="install_weak_deps=False" --exclude=PackageKit-gstreamer-plugin', shell=True)
        subprocess.run('dnf update @sound-and-video', shell=True)

        console.print("ffmpeg non free installed + all codecs :heavy_check_mark:", style='ok')
        logger.info('ffmpeg non free installed + all codecs ')
    
    except Exception as e:
        logging.critical(f"Could not install codecs :{str(e)}")
        console.print("Something failed with new codecs :X:", style='error')



def systemd():
    console.rule('Enabling user services', style='checkt')
    
    user_services = ['gnome-keyring.service', 'ssh-agent.service', 'polkit-gnome-authentication-agent.service', 
                     'hypridle.service','gnome-keyring-daemon.service']
    
    try:
        for services in user_services:
            subprocess.run(f'systemctl --user enable {services}', shell=True)
    except Exception as e:
        logging.critical(f"Could not start service :{str(e)}")
        console.print("Error starting some services :X:", style='error')



if __name__ == '__main__':
    main()

