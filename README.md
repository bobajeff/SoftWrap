# SoftWrap
> [!NOTE]
> This project is a fork of [danemadsen/SoftWrap](https://github.com/danemadsen/SoftWrap) (originally created by [Jeacom](https://superhivemarket.com/products/softwrap)). 
> 
> **Key changes in this version:**
> - Updated to work with Blender 5.1.2
> - Made it a Blender Extension

Transfer topology from one model to another using a softbody simulation

## Install
1. Download the [zip for your platform](https://github.com/bobajeff/SoftWrap/releases/latest)
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

## Videos
#### [Softwrap - Getting started - YouTube](https://www.youtube.com/watch?v=8P_2RnGh46Y)

[![Softwrap - Getting started - YouTube](http://img.youtube.com/vi/8P_2RnGh46Y/mqdefault.jpg)](https://www.youtube.com/watch?v=8P_2RnGh46Y)

#### [Softwrap basic retopo. - YouTube](https://www.youtube.com/watch?v=aEH9J-YlwwQ)

[![Softwrap basic retopo. - YouTube](http://img.youtube.com/vi/aEH9J-YlwwQ/mqdefault.jpg)](https://www.youtube.com/watch?v=aEH9J-YlwwQ)

#### [SoftWrap - Fixing shapes on the fly tutorial - YouTube](https://www.youtube.com/watch?v=hRosGbzryQk)

[![SoftWrap - Fixing shapes on the fly tutorial - YouTube](http://img.youtube.com/vi/hRosGbzryQk/mqdefault.jpg)](https://www.youtube.com/watch?v=hRosGbzryQk)

#### [softwrap retopo hand - YouTube](https://www.youtube.com/watch?v=lRf6Z6PCv4E)

[![softwrap retopo hand - YouTube](http://img.youtube.com/vi/lRf6Z6PCv4E/mqdefault.jpg)](https://www.youtube.com/watch?v=lRf6Z6PCv4E)