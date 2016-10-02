set -e
set -x

sudo apt-get install git python-pip libssl-dev
sudo pip install --upgrade pip wheel ansible

mkdir -p ~/code
# Using HTTPS to avoid RSA key fingerprint prompt
git clone https://github.com/Nurdok/dotfiles.git ~/code/dotfiles
ansible-playbook ~/code/dotfiles/playbook.yml

set +x
set +e
