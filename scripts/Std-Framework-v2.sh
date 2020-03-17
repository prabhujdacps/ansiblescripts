./Ansible_Connect.sh $1 server server1,server2 action=reinstall
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $1 application cps
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $1 config  configupdate
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $1 application ms
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $1 application srs
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $1 application vts
[[ $? -ne 0 ]] && exit
