filePath=$1
FileName=${filePath##*/}
FileNameBase=$(echo "$FileName" | cut -f 1 -d '.')
environment=environment/${FileNameBase}
echo "Cluster setup with :$filePath & environment location:$environment"
./Ansible_Connect.sh env $filePath $environment 1>/dev/null 2>/dev/null
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $environment util server1
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $environment server server1,server2 action=reinstall
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
