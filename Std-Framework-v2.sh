filePath=$1
skippednodes=$2
FileName=${filePath##*/}
FileNameBase=$(echo "$FileName" | cut -f 1 -d '.')
environment=environment/${FileNameBase}
echo "Connect setup setup with :$filePath & environment location:$environment"
execuitedNodes=""
if [[  -f "$filePath" ]];then
./Ansible_Connect.sh env $filePath $environment 1>/dev/null 2>/dev/null
[[ $? -ne 0 ]] && exit
fi

nodeCheck(){
	node=$1
	nodeFileName=$environment/host_vars/$1.yaml
	if [[ -f "$nodeFileName" ]];then
		return 0
	else
		echo "[WARNING]: Skipping $1. Node file not available: $nodeFileName"
		return 1
	fi
}
ansible(){
if [[ ! -z "$skippednodes" ]];then
echo "Check  node state :$2"
	if [[ "$skippednodes" == *"$2"* ]]; then
	echo "[INFO]: Skipping node run:$2"
	return 0
	fi
fi
validNodes=""
for splitNodes in $(echo $2 | tr "," "\n")
	do
	if  nodeCheck $splitNodes -eq 0 
	then
		if [[ -z "$validNodes" ]];then
			validNodes=$splitNodes
		else
			validNodes=$validNodes','$splitNodes
		fi
	fi
	done
#echo "Valid nodes: $validNodes"
nodeType=$1
node=$2
action=$3
tags=$4
if [[ ! -z "$validNodes" ]];then
	if [[ ! "$skippednodes" == "--help" ]]; then
	./Ansible_Connect.sh $environment $nodeType $validNodes $action $tags
	fi
if [[ $? -ne 0 ]];then
echo "<script>.sh   skipnodes=$execuitedNodes"
exit
else
if [[ -z "$execuitedNodes" ]];then
		execuitedNodes=$validNodes
	else
		execuitedNodes=$execuitedNodes','$validNodes
	fi
fi
fi
}
ansibleRun(){
validNodes=""
for splitNodes in $(echo $2 | tr "," "\n")
	do
	if  nodeCheck $splitNodes -eq 0 
	then
		if [[ -z "$validNodes" ]];then
			validNodes=$splitNodes
		else
			validNodes=$validNodes','$splitNodes
		fi
	fi
	done
nodeType=$1
node=$2
action=$3
tags=$4
if [[ ! -z "$validNodes" ]];then
./Ansible_Connect.sh $environment $nodeType $validNodes $action $tags
if [[ $? -ne 0 ]];then
echo "<script>.sh   skipnodes=$execuitedNodes"
exit
fi
fi
}

####Scripts start from here 
ansibleRun util server1
##Servers install
ansible server server1 action=reinstall

ansible server server2 action=reinstall
##CPS
ansible application cps
##Config update
ansible config  configupdate
#MessageStore
ansible application ms
#MessageStoreUI
ansible application msui
#MessageBroker
ansible application mb
#ServiceRegistory
ansible application srs
#VTS
ansible application vts

echo "Execuited nodes: $execuitedNodes"