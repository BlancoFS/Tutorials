# MoMEMta installation in lxplus

Instructions to install the MoMEMta framework to perform the matrix element method with madgraph5 MEs.

Software needed:

```
cmake (>=3.2)
LHAPDF (>=6)
BOOST (>= 1.54)
ROOT (>=5.34.09)
```



In principle, some of those libraries are not availible in lxplus. The best solution to install them is to create a conda enviroment:

```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
export PATH="/afs/cern.ch/user/s/sblancof/miniconda3/bin:$PATH"
conda config --add channels https://conda.anaconda.org/NLeSC

conda create --name=ME
conda activate ME
```

Now, we are going to install the libraries in the conda enviroment's path (/afs/cern.ch/user/s/sblancof/miniconda3/envs/ME_env/ in my case) or in the CMSSW path, depending if the library is needed for building the MoMEMta software or it's a library used by MoMEMta, like LHAPDF. It may be necessary to install a precise python 2 version in the conda enviroment, just do conda install python=2.7. 

## Install LHAPDF

```
wget https://lhapdf.hepforge.org/downloads/?f=LHAPDF-6.2.0.tar.gz -O LHAPDF-6.2.0.tar.gz
tar -xf LHAPDF-6.2.0.tar.gz
cd LHAPDF-6.2.0/
./configure --prefix=/afs/cern.ch/work/s/sblancof/public/CMSSW_10_6_10/
make
make install
```

## install cmake

```
source /cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/gcc/7.0.0/etc/profile.d/init.sh

wget https://github.com/Kitware/CMake/releases/download/v3.21.3/cmake-3.21.3.tar.gz
tar -xf cmake-3.21.3.tar.gz
cd cmake-3.21.3/
./bootstrap.sh --prefix=/afs/cern.ch/user/s/sblancof/miniconda3/envs/ME/
gmake
gmake install
```

## install BOOST

```
wget -O boost_1_56_0.tar.gz http://sourceforge.net/projects/boost/files/boost/1.56.0/boost_1_56_0.tar.gz/download
tar xzvf boost_1_56_0.tar.gz
cd boost_1_56_0/
./bootstrap.sh --prefix=/afs/cern.ch/user/s/sblancof/miniconda3/envs/ME/
./b2 
./b2 install
```


## Alternative (check if works)

```
source /cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/lhapdf/6.2.1/etc/profile.d/init.sh
source /cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/boost/1.63.0/etc/profile.d/init.sh
```

At this point, the libraries should be availible. However, first, check that your cmake version is higher than 3.2 by:

```
cmake --version
```

if not, try:

```
cmake3 --version
```

if not:

```
whereis cmake
```

search your cmake desired version and:

```
alias cmake= your desired version
```

# MoMEMta

We can start the installation of MoMEMta.

```
cd CMSSW_10_6_4/src
cmsenv

git clone https://github.com/MoMEMta/MoMEMta.git

cd MoMEMta
mkdir build
```

Now, open the **CMakeLists.txt** file and add this command in the **line 64**:

```
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")
```

This line is added to avoid an error with the c++11 version. Then:

```
source /cvmfs/cms.cern.ch/slc7_amd64_gcc700/external/gcc/7.0.0/etc/profile.d/init.sh

cd build
export LHAPDF_ROOT=/afs/cern.ch/user/s/sblancof/miniconda3/envs/ME/
cmake -DCMAKE_CXX_VERSION=c++17 -BOOST_ROOT=/afs/cern.ch/user/s/sblancof/miniconda3/envs/ME/ -DTESTS=OFF -DEXAMPLES=OFF -DPYTHON_BINDINGS=ON -DPROFILING=ON -B ./ -DCMAKE_INSTALL_PREFIX=/afs/cern.ch/work/s/sblancof/public/CMSSW_10_6_10/ -DLHAPDF_ROOT=/afs/cern.ch/work/s/sblancof/public/CMSSW_10_6_10/ ..
make 
make install
```

That's it. It should be install correctly at /afs/cern.ch/work/s/sblancof/public/CMSSW_10_6_10/. Finally, to make the MoMEMta libraries accesible:


```
cd /afs/cern.ch/work/s/sblancof/public/CMSSW_10_6_10/
cp -r include/momemta ./src/
```


# MoMEMta_MaGMEE


Instructions to convert a MadGraph5 generated process to an accesible matrix element for MoMEMta. First, download MadGraph (version 2.5.* or 2.6.0, lower and upper versions are not supported):

```
wget https://launchpad.net/mg5amcnlo/2.0/2.5.x/+download/MG5_aMC_v2.5.5.tar.gz
tar -xf MG5_aMC_v2.5.5.tar.gz
```

Now, download the MoMEMta_MaGMEE plugin and run:

```
cd MG5_aMC_v2_5_5/PLUGIN
wget https://github.com/MoMEMta/MoMEMta-MaGMEE/archive/refs/tags/v1.0.0.tar.gz
tar -xf v1.0.0.tar.gz
mv MoMEMta-MaGMEE-1.0.0 MoMEMta-MaGMEE
cd ..
```

## How to export a matrix element

Lauch madgraph with the MoMEMta_MaGMEE plugin and get the matrix element for your desired process:

```
python2 ./bin/mg5_amc
generate p p > t t~, (t > w+ b, w+ > l+ vl), (t~ > w- b~, w- > l- vl~)
output MoMEMta ttbar_leptonic_ME
```

A **ttbar_leptonic_ME** folder must be created in the MG5_aMC_v2_5_5 directory. Before running MoMEMta, the new matrix element has to be compiled:

```
cd ttbar_leptonic_ME
mkdir build
cd build
cmake -DCMAKE_CXX_VERSION=c++17 -DCMAKE_INSTALL_PREFIX=/afs/cern.ch/work/s/sblancof/public/CMSSW_10_6_10/ ..
make 
```

Important: The cmake install prefix should be the same as the MoMEMta installation folder.

After that, a file called **libme_ttbar_leptonic_ME.so** has been created in the "ttbar_leptonic_ME/build" directory, this library is used as input by the lua configuration file.


**Once the new *.lua and c++ files are generated, they must be included in the MoMEMta/MatrixElement folder and the MoMEMta framework has to be recompiled again.**


