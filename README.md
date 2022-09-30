# Trilium Updater

A python script for updating your local trilium-client

## Description

This script automates the download and installation of your local Trilium client.

## Getting Started

### Compatibility

Currently only working on Windows with hardcoded paths for Python and installation directory.

### Dependencies

* Python 3.9
* Python 3.10 *(you'd need to update the path in `run.bat` accordingly)*

Install all Python modules with `pip install -r 'requirements.txt'`

### Executing program

1. Install all modules
`pip install -r 'requirements.txt'`
2. Execute `run.bat`
3. Hope you don't get any error

## ToDo
- [ ] Error handling in batch script
    *Currently your Trilium installation will be deleted even if the Python script fails*
- [ ] Add dynamic path management

## Version History

### 14.09.2022
    * Initial Release
    * Rough functionality 

## Acknowledgments
Thanks to [Zadam](https://github.com/zadam) for making [Trilium](https://github.com/zadam/trilium).
