<h1 align="center">Trilium Updater</h1>
<h3 align="center"> A python script for updating your local trilium-client</h3>
<p align="center">
  Made with<br>
  <img align="center" src="https://camo.githubusercontent.com/3df944c2b99f86f1361df72285183e890f11c52d36dfcd3c2844c6823c823fc1/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f7374796c653d666f722d7468652d6261646765266d6573736167653d507974686f6e26636f6c6f723d333737364142266c6f676f3d507974686f6e266c6f676f436f6c6f723d464646464646266c6162656c3d">
  <img align="center" src="https://camo.githubusercontent.com/cbf076468b5392bc2d28d5b70841d3664279363b832a6465eb8b339098c052f2/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76313f7374796c653d666f722d7468652d6261646765266d6573736167653d57696e646f77732b5465726d696e616c26636f6c6f723d344434443444266c6f676f3d57696e646f77732b5465726d696e616c266c6f676f436f6c6f723d464646464646266c6162656c3d">
</p>

## Description

This script automates the download and installation of an update for your local Trilium client.

## Getting Started

### Compatibility

Currently only working on Windows with hardcoded paths for Python and installation directory.<br>

### Dependencies

* Python 3.9 - 3.12

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
