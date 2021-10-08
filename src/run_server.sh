
INSTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $INSTDIR
SOURCEDIR="$(dirname "$INSTDIR")"
echo $SOURCEDIR

cd /opt
source TuroCardEnv/bin/activate
cd $INSTDIR
start()
{
python3 manage.py runserver 0.0.0.0:9090
}
start
