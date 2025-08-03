# Rice-cook <a href="#"> <img src="./images/logo.webp" height="150" > </a>

This is a python script made to rice a blank fedora install into my custom hyprland configuration.

# What is does :

- Allows DNF to update from fastest mirrors
  - Adds +10 max parallel downloads
- Adds rpmfusion to repos
- Adds Flathub to repos
- Copies dotfliles into ~/.config
  </br> </br>
  <span style="font-size:30px;">Installs:</span>
- Oh_My_zsh
  - with zsh-autosuggestions plugin
  - powerlevel10k plugin
- 25 fonts, for developers and smooth looking
- Catppuccin themes
- candy-icons
- Hyprland
- hyprcursor ,hypridle, hyprlang, hyprloc, hyprpaper, hyprpicker, hyprutils
- Waybar
- Finally installs all programs given in data.conf
  - dnf packages, flatpaks, copr , repos from urls

---

<a href="https://github.com/catppuccin/catppuccin"><img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png"  height="100" width="100"></a>
<a href="https://ohmyz.sh/"><img src="./images/ohmyzsh.png"  height="100" width="100"></a>
<a href="https://flathub.org/"><img src="https://www.vectorlogo.zone/logos/flathub/flathub-icon.svg"  height="100" width="100"></a>
<a href="https://github.com/EliverLara/candy-icons"><img src="./images/icons.png"  height="150" width="200"></a>

##

![](images/image2.png)

# How to run :

```
git clone https://github.com/acidburnmonkey/rice-cook.git && cd rice-cook

```

```
chmod +x preinstall.sh && sudo ./preinstall.sh
```

### Now move `rice-cook.py` & data.conf into dofiles directory and run it:

```
sudo uv run rice-cook.py
```

Should look like this .

```
|-dotfiles
|---nvim
|---ranger
|---etc...
|---data.conf
|---rice-cook.py
```

### Before reboot

Need to correct ownership of home directory

```
sudo chown -R user:user /home/username
```

## A snapshot of your current fedora config can be genereted with this script

[link](https://github.com/acidburnmonkey/scripts/blob/main/fedora-apps.py)

## Donate

<a href="https://www.buymeacoffee.com/acidburn" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Monero <img src="https://www.getmonero.org/press-kit/symbols/monero-symbol-1280.png" width="60" height="60">

43Sxiso2FHsYhP7HTqZgsXa3m3uHtxHQdMeHxECqRefyazZfpGVCLVsf1gU68jxJBo1G171AC181q1BqAUaG1m554MLsspG

## Bitcon <img src="https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg" width="60" height="60">

bc1qk06cyheffclx7x434zpxjzcdl50452r9ducw0x
