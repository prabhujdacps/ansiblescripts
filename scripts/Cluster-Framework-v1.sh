environment=$1
echo "Cluster setup"
./Ansible_Connect.sh $environment cluster cluster1 action=delete
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $environment server server1,server2 action=reinstall
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $environment cluster cluster1 action=reinstall -t=install
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $environment application cps
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $environment config  configupdate
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $environment application ms
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $environment application srs
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $environment application vts
[[ $? -ne 0 ]] && exit
