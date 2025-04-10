sudo apt install git
sudo apt install python3-pip

mkdir projet
git clone https://github.com/Phiber57/Boiler_Controller.git


cp Boiler_Controller/Software/deployment/update.sh ~/projet
cd projet
chmod +x update.sh

sudo apt install python3
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev


installer manuellement les librairies.
sudo apt install python3.11-venv
python -m venv env_boiler
pip3 install paho-mqtt
