filePath=$1
FileName=${filePath##*/}
FileNameBase=$(echo "$FileName" | cut -f 1 -d '.')
environment=environment/${FileNameBase}
echo "Environment file path:$filePath & environment location:$environment"
./Ansible_Connect.sh env $filePath $environment 1>/dev/null 2>/dev/null
[[ $? -ne 0 ]] && exit
./Ansible_Connect.sh $environment $2 $3 $4 $5
[[ $? -ne 0 ]] && exit
