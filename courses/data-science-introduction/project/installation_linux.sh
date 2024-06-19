#!/bin/bash

# Add the DBeaver CE repository
wget -O - https://dbeaver.io/debs/dbeaver.gpg.key | sudo apt-key add -
echo "deb https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list
wget https://downloads.slack-edge.com/linux_releases/slack-desktop-4.20.0-amd64.deb
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"


# Update package lists
sudo apt-get update -y
sudo apt-get -y upgrade

# Install prerequisites
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Install Apache
sudo apt-get install -y apache2
# Install DBeaver
sudo apt-get install dbeaver-ce
# Install VSCode
sudo snap install code --classic
# Install Postman
sudo snap install postman --classic
# Install Slack
sudo dpkg -i slack-desktop-4.20.0-amd64.deb
# Install Docker
sudo apt-get install -y docker-ce
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo apt-get install -f

# Install pyenv
curl https://pyenv.run | bash
# Add pyenv to bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
# Create a VEnv for Python 3.11.8
curl -sSL https://install.python-poetry.org | bash
echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
poetry config virtualenvs.in-project true
pyenv install 3.11.8
pyenv virtualenv 3.11.8 data-science-introduction
pyenv activate data-science-introduction

# Install General Dependencies
pip install --upgrade pip
pip install ipython
# create poetry project and add dependencies
poetry new data-science-project
cd data-science-project
poetry add numpy pandas pandera pydantic tzdata openpyxl beaufitulsoup4 matplotlib seaborn ydata-profiling \
psycopg2-binary sqlalchemy scikit-learn xgboost uvicorn fastapi jupyterlab
poetry add -G dev black pylint pytest click pre-commit 

# Restart shell
exec "$SHELL"