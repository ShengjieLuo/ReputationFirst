sudo apt-get update -y
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
sudo pip3 install configobj python-dateutil requests bs4 goose3
sudo pip3 install newspaper3k
sudo apt-get install libxml2-dev libxslt-dev -y
sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev -y
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3

