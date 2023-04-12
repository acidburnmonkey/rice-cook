import os
import subprocess

home = os.path.expanduser("~")
this = os.getcwd()

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
    print(subprocess.run(f'cp -r {this} {destination}', shell=True))


