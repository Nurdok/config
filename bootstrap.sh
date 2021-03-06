set -e
set -x

sudo apt-get update
sudo apt-get install git python-pip libssl-dev python-dev build-essential libffi-dev
sudo pip install --upgrade pip wheel setuptools
sudo pip install --upgrade ansible

mkdir -p ~/code
# Using HTTPS to avoid RSA key fingerprint prompt
git clone https://github.com/Nurdok/dotfiles.git ~/code/dotfiles
ansible-playbook ~/code/dotfiles/playbook.yml --ask-become-pass

set +x
set +e
