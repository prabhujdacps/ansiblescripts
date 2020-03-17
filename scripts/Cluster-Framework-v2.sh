environment=$1
echo "Cluster setup"
./Ansible_Connect.sh $environment cluster cluster1,cluster2 action=delete
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $environment server server1,server2,server3,server4 action=reinstall
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $environment cluster cluster1,cluster2 action=reinstall -t=install
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
