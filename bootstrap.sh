set -e
set -x

sudo apt-get install git
sudo pip install ansible

mkdir -p ~/code
git clone git@github.com:Nurdok/dotfiles.git ~/code/dotfiles
ansible-playbook ~/code/dotfiles/playbook.yml

set +x
set +e
