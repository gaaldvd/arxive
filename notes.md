# arxive notes

rsync man: https://download.samba.org/pub/rsync/rsync.1

- session
  - mount up NAS, ask if it should be unmounted at the end of the session (optional) 
  - define SOURCE and DESTINATION
- rsync SOURCE to DESTINATION
- list files in DESTINATION that have been removed from SOURCE
  - prompt for the removal of each file from DESTINATION (checks in Qt)
  - delete files marked for removal

## usage

`arxive [SOURCE] [DESTINATION]`
