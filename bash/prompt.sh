red="\e[31m"
yellow="\e[93m"
default="\e[39m"
bold="\e[1m"
unbold="\e[22m"

PS1=""  # initialize empty
PS1+="\n"  # line break
PS1+="${bold}[${yellow}\u@\h${default}]${unbold}"  # user and hostname
PS1+=":\w"  # current path
PS1+="\$(__git_ps1 \" (%s)\")"  # git status
PS1+="\n"  # line break
PS1+="\001${red}${bold}\002\$\001${default}${unbold}\002 "  # prompt line

