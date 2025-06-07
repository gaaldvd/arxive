# arXive todo

- setup
  - add arxive.sh to PATH:
    - create `.profile` file in home
    - add the line `export PATH="/home/USER/PATH/TO/ARXIVE:$PATH"` to the file
    - reload configuration: `source ~/.profile`
    - verify: `echo $PATH`
  - create symlink: `ln -s /home/USER/PATH/TO/ARXIVE/arxive.sh /home/USER/PATH/TO/ARXIVE/arxive`
  - desktop entry

## GUI

- pass additional options when running sync
  - -av is default, warn when it's added to the config 
- a checkbox to mark all deletions to delete
