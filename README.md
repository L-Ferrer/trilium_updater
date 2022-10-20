# Trilium Updater

A python script for updating your local trilium-client

## Description

This script automates the download and installation of an update for your local Trilium client.

## Getting Started

### Compatibility

Currently only working on Windows with hardcoded paths for Python and installation directory.<br>

### Dependencies

* Python 3.9
<br>or
* Python 3.10

Install all Python modules with `pip install -r 'requirements.txt'`

### Executing program

1. Install all modules
`pip install -r 'requirements.txt'`
2. Execute **run.bat**

## ToDo
- [x] Error handling in batch script
    ~~*(currently your Trilium installation will be deleted even if the Python script fails)*~~
- [ ] Add dynamic path management
- [ ] Write a bash script for docker 

## Version History

### 20.10.2022
* Implemented error handling in **run.bat**

### 14.09.2022
* Initial Release
* Rough functionality 

## Acknowledgments
Thanks to [Zadam](https://github.com/zadam) for making [Trilium](https://github.com/zadam/trilium).
