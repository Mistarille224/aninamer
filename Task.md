## Function

- [x] Rename by script.
- [x] ~~Scheduled tasks implemented by the command line. (obsolete)~~
- [x] Import Configuration file. (toml)
  - [x] Auto generate Configuration file
  - [x] Modify special items. 
    - [x] Modify the before and after items individually. 
    - [x] Optimize import logic.
    - [ ] Refactor rename logic. (Some files with wrong directory cannot be renamed)
  - [x] Modify The path being monitored.
    - [ ] Support multiple directories.
- [x] Monitor folder changes and automatically rename them
- [x] Auto generate log file.
  - [x] fix folder display bug.
- [x] Auto delete outdated log file.
- [x] Code standardization.
- [x] Packaged as exe.
  - [ ] Automatic packaging.
- [ ] Support Linux.

## GUI

- [x] GUI sketch.
- [x] Add tray icon.
  - [ ] Show service status.
- [ ] Home page.
  - [ ] Service start and stop
  - [ ] Service hot-restart
  - [ ] Show service status.
  - [ ] Edit Configuration file
    - [ ] Modify The path being monitored.
      - [ ] Support multiple directories.
    - [ ] Modify special items. 
      - [ ] Modify the before and after items individually. 