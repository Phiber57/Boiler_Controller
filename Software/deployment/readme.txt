Commandes à exécuter successivement pour installer la gateway. 
Il sera nécessaire d'apapter les paramètres dans le repertoire credential.

sudo apt udpate
sudo apt install git
#sudo apt install python3-pip => inutile, remplacé par python3.11-venv
sudo apt install python3.11-venv

mkdir boiler
git clone https://github.com/Phiber57/Boiler_Controller.git


cp Boiler_Controller/Software/deployment/update.sh ./boiler/
cd boiler
chmod +x update.sh

installer manuellement les librairies.
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev

python -m venv env_boiler
source ./env_boiler/bin/activate
pip3 install paho-mqtt

Changer les parametres dans le repertoire credential
