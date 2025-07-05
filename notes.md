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
