 # chdir
ROOT_FOLDER=$(cd "$(dirname "$0")";pwd)"/../"
cd $ROOT_FOLDER
pip uninstall chatmanager
python setup.py sdist bdist_wheel
pip install dist/*.tar.gz
