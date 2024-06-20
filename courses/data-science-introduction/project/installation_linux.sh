#!/bin/bash

# Add repositories, download files
sudo add-apt-repository ppa:serge-rider/dbeaver-ce
wget https://downloads.slack-edge.com/desktop-releases/linux/x64/4.38.125/slack-desktop-4.38.125-amd64.deb
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
wget https://dl.pstmn.io/download/latest/linux64 -O postman.tar.gz
wget -O vscode.deb https://go.microsoft.com/fwlink/?LinkID=760868

# Update package lists
sudo apt-get update -y
sudo apt-get upgrade -y

# Install prerequisites
sudo apt -y install build-essential cmake curl pkg-config libgtk-3-dev libgtkmm-3.0-dev liblensfun-dev librsvg2-dev liblcms2-dev libfftw3-dev libiptcdata0-dev libtiff5-dev libcanberra-gtk3-dev libexiv2-dev
sudo apt -y install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt-get install -y make libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev git
sudo apt-get install -y apt-transport-https ca-certificates software-properties-common

# Install Apache
sudo apt-get install -y apache2
# Install DBeaver
sudo apt -y install dbeaver-ce
# Install VSCode
sudo dpkg -i vscode.deb
rm vscode.deb
# Install Postman
sudo tar -xzf postman.tar.gz -C /opt
sudo ln -s /opt/Postman/Postman /usr/local/bin/postman
rm postman.tar.gz
# Install Slack
sudo dpkg -i slack-desktop-4.38.125-amd64.deb
rm slack-desktop-4.38.125-amd64.deb
# Install Docker
sudo apt-get install -y docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo apt-get install -f
sudo apt autoremove

# Install pyenv
curl https://pyenv.run | bash
# Add pyenv to bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
source ~/.bashrc
pyenv --version
exec "$SHELL"