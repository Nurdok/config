import os

repo_dir = os.path.dirname(os.path.realpath(__file__))
print repo_dir
subdirs = (node for node in os.listdir(repo_dir)
           if os.path.isdir(node)
           if not node.startswith('.'))
user_dir = os.path.expanduser("~")

for subdir in subdirs:
    print "bootstraping {}-related dotfiles...".format(subdir)
    subdir_path = os.path.join(repo_dir, subdir)
    dotfiles = os.listdir(subdir_path)
    for dotfile in dotfiles:
        dotfile_path = os.path.join(subdir_path, dotfile)
        link = os.path.join(user_dir, ".{}".format(dotfile))
        print "\tSymlinking {} to {} ...".format(link, dotfile_path),
	if not os.path.lexists(link):
            os.symlink(dotfile_path, link)
            print "done."
        else:
            print "symlink already exists."
