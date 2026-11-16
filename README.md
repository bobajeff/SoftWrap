# SoftWrap
> [!NOTE]
> This project is a fork of [danemadsen/SoftWrap](https://github.com/danemadsen/SoftWrap) (originally created by [Jeacom](https://superhivemarket.com/products/softwrap)). 
> 
> **Key changes in this version:**
> - Updated to work with Blender 5.1.2
> - Made it a Blender Extension

Transfer topology from one model to another using a softbody simulation

## Install
1. Download the zip for your platform
2. Open Blender and go to **Edit > Preferences**.
3. Select the **Get Extensions** section in the left sidebar.
4. Click the **downward arrow** (`v`) in the top-right corner of the Preferences window.
5. Choose **Install from Disk** from the menu.
6. Browse to your downloaded .zip confirm installation.

## Build from source
### using `uv` on linux
```sh
git clone https://github.com/bobajeff/SoftWrap.git
cd softwrap_core/
uv build --wheel --python 3.13  --out-dir ../extension/wheels/
cd ../extension/
blender --command extension build
```

## Documentaion
see orginal [Softwrap Manual](https://jeacom25b.github.io/Softwrap-Manual/)

see also [Softwrap product page on Superhive](https://superhivemarket.com/products/softwrap)
