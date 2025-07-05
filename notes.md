# arXive notes

rsync man: https://download.samba.org/pub/rsync/rsync.1

## setting up & usage

requirements: git, python3, pipenv, rsync

1. clone git repo: `git clone https://github.com/gaaldvd/arxive.git`
2. cd to the repo and run setup script: `sh setup.sh`
3. setup
  - set up pipenv and privileges
  - add arxive.sh to PATH:
    - create `.profile` file in home
    - add the line `export PATH="/home/USER/PATH/TO/ARXIVE:$PATH"` to the file
    - reload configuration: `source ~/.profile`
    - verify: `echo $PATH`
  - create symlink: `ln -s /home/USER/PATH/TO/ARXIVE/arxive.sh /home/USER/PATH/TO/ARXIVE/arxive`
  - desktop entry:
```bash
cat >> ~/.local/share/applications/arxive.desktop <<EOF
[Desktop Entry]
Type=Application
Name=arXive
Exec=sh /home/USER/PATH/TO/ARXIVE/arxive.sh -g
Terminal=false
Icon=/home/USER/PATH/TO/ARXIVE/src/ui/arxive.svg
Categories=System
EOF
```

update: `arxive -u`

run in CLI or GUI mode: `arxive -c/-g [SOURCE] [DESTINATION]`

## NAS run script

```bash

# arXive script

dest_remote="//192.168.0.20/Dokumentumok"
dest_local="/home/nas"
dest_user="anus"
dest_pw="tiZ_@nuS6432"

src_user="tiziano"
src_pw="Radeon9250"

# mount NAS
# check if NAS is mounted
# sudo mount -t cifs "$dest_remote" "$dest_local" -o
username="$dest_user",uid="$src_user"
# sudo mount -t cifs "$dest_remote" "$dest_local" -o
credentials=/home/tiziano/Programs/.credentials,uid="$src_user"
# .credentials :
# username=tiziano
# password=Radeon9250

# run arxive for directories, copy individual files from ~/

arxive -c /home/tiziano/Videos "$dest_local"
arxive -c /home/tiziano/Programs "$dest_local"
arxive -c /home/tiziano/Pictures "$dest_local"
arxive -c /home/tiziano/PDF "$dest_local"
arxive -c /home/tiziano/Downloads "$dest_local"
arxive -c /home/tiziano/Documents "$dest_local"
arxive -c /home/tiziano/.zotero "$dest_local"
arxive -c /home/tiziano/.wallpapers "$dest_local"
arxive -c /home/tiziano/.thunderbird "$dest_local"
arxive -c /home/tiziano/.icons "$dest_local"
arxive -c /home/tiziano/.conky "$dest_local"
arxive -c /home/tiziano/.config "$dest_local"
arxive -c /home/tiziano/.profile "$dest_local"
arxive -c /home/tiziano/.zshrc "$dest_local"
# arxive -c /home/tiziano/ "$dest_local"
# arxive -c "" "$dest_local"

```
