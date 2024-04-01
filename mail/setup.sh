echo "Setting up new environment"
python3 -m venv env
source env/bin/activate

pip install yagmail smtplib python-dotenv
echo "Environment setup complete"