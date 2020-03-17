./Ansible_Connect.sh $1 cluster cluster1 action=delete
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $1 server server1,server2 action=reinstall
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $1 cluster cluster1 action=reinstall -t=install
[[ $? -ne 0 ]] && exit

