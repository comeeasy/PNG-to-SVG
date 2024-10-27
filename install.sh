pip install svgpathtools
sudo apt-get update
apt install -y imagemagick
apt-get install libtool
sudo apt install intltool imagemagick libmagickcore-dev pstoedit libpstoedit-dev autopoint

git clone https://github.com/autotrace/autotrace.git
cd ./autotrace
bash autogen.sh
bash configure
make
./autotrace --version	# test if it can print its version, before installing.
sudo make install
sudo ldconfig

autotrace -v