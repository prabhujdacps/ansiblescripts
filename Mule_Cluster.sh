#MRT_ApplicationDeploy.yml <EnvironmentFile> <application> Optional(action=status/delete/reinstall) Optional(t=action)
filePath=$1
type=$2
nodeName=$3
action=$4
tag=$5
./Ansible_Connect-v1.sh $filePath cluster $2 $3 $4

