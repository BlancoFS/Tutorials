# Instruction to install and use correctionlib within Latinos framework

Please follow this lines in order to run corretionlib using CMSSW in a c++ script. A CMSSW release higher than CMSSW_11_3_X should be needed for this or, at least, one with python 3.

## First 

Download from source:

```
cd CMSSW_PATH/src/
git clone --recursive git@github.com:cms-nanoAOD/correctionlib.git
```

The installation will be made using CMake (> 3.11). Then, open **CMakeLists.txt** file and substitude the following lines:

```
string(REPLACE "." ";" VERSION_SPLIT ${CORRECTIONLIB_VERSION})
list(GET VERSION_SPLIT 0 SPLIT_VERSION_MAJOR)
list(GET VERSION_SPLIT 1 SPLIT_VERSION_MINOR)

project(correctionlib VERSION ${SPLIT_VERSION_MAJOR}.${SPLIT_VERSION_MINOR} LANGUAGES CXX)
```

by:

```
project(correctionlib LANGUAGES CXX)
```

## Second

If there is not build directory, create it and:

```
cd correctionlib/build
cmake3 -DCMAKE_CXX_VERSION=c++17 -DCMAKE_INSTALL_PREFIX=/afs/cern.ch/work/s/sblancof/private/Run3Analysis/CMSSW_12_1_0 -B ./ ..
make
make install
cd ..
cp include/correction.h build/include/
```

**It should be now installed**


## Usage

To use in a c++ script within the Latinos framework, you have to call the library. In a c++ file, for example do:

```
gSystem->Load("/afs/cern.ch/work/s/sblancof/private/Run3Analysis/CMSSW_12_1_0/src/correctionlib/build/libcorrectionlib.so");

#include "correctionlib/build/include/correctionlib_version.h"
#include "correctionlib/build/include/correction.h"

using correction::CorrectionSet;

auto cset = CorrectionSet::from_file("electron.json");
auto cset_2016preID = cset->at("UL-Electron-ID-SF");
```

**DONE**



