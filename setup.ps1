echo "Criando ambiente virtual em 'env'..."
python -m venv env

env/Scripts/activate

pip install -r requirements.txt
python main.py