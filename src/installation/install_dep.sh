
INSTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $INSTDIR
SOURCEDIR="$(dirname "$INSTDIR")"
echo $SOURCEDIR

cd /opt
sudo python3 -m venv TuroCardEnv
sudo chown -R $USER:$USER /opt/TuroCardEnv/
source TuroCardEnv/bin/activate
cd $INSTDIR
echo "Virtual environment (TuroCardEnv) has been created."
echo ""
echo "Installing the Python dependencies"
pip3 install --upgrade pip
chmod +x requirements.sh
./requirements.sh
cd ..
python3 manage.py makemigrations
python3 manage.py migrate
echo ""
echo "All Python dependencies has been installed"
chmod +x run_server.sh

