#./Cluster-Framework-v1.sh <ansible_path> <environment_path>
cd $1
./Ansible_Connect.sh $2/hosts.ini server server1 action=reinstall
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $2/hosts.ini application cps
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $2/hosts.ini asset configrepo
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $2/hosts.ini config  configupdate
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $2/hosts.ini application ms
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $2/hosts.ini application srs
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $2/hosts.ini application vts
[[ $? -ne 0 ]] && exit
