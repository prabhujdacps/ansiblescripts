ansiblePlaybook=""
if [[ "$1" == "env" ]];then	
	pythonCommand="python3 scripts/cps_promotion/Ansible_Customer_Env.py $2 $3"
	if [[ -f "$2" ]];then
		$pythonCommand
	else
		echo "invalid file $2"
	fi
	exit 0
fi
if [[ "$1" == "--help" ]];then	
	echo "./Ansible_Connect.sh <InventoryFilePath> <Type> <Nodes> <Action(Optional)>  <Tags(Optional)>"
	exit 1
fi
validateHostFile(){
for serverName in $(echo $2 | tr "," "\n")
do
hostFile="$1/hosts.ini"
hostFileHomePath="$1"
hostVarFile=$hostFileHomePath"/host_vars/"$serverName".yaml"

  if [[ ! -f "$hostVarFile" ]];then
	echo "ERROR: Host file $hostVarFile is not present in inventory directory for Node=$serverName and file:$hostFileHomePath"
	exit 1
	fi
done
}
validateHostFile $1 $3

serverPlayBook="MRT_Install.yml"
applicationPlayBook="MRT_ApplicationDeploy.yml"
clusterPlaybook="MRT_Cluster.yml"
serverActionPlaybook="MRT_Action.yml"
exchangeAssetPlaybook="ExchangeUtil.yml"
util="roles/utils/utils.yml"
configPushPlaybook="CPS_ConfigPublish.yml"
armAPIPlaybook="ARM_APIManager.yml"


if [[ ! -f "${hostFile}" ]];then
echo "ERROR: Inventory file is not present in the ${hostFile}"
exit 1
fi

if [[ "$2" == "server" ]];then
	ansiblePlaybook=$serverPlayBook
elif [[ "$2" == "application" ]];then
	ansiblePlaybook=$applicationPlayBook
elif [[ "$2" == "cluster" ]];then
	ansiblePlaybook=$clusterPlaybook
elif [[ "$2" == "server_action" ]];then
		ansiblePlaybook=$serverActionPlaybook
elif [[ "$2" == "asset" ]];then
	ansiblePlaybook=$exchangeAssetPlaybook
elif [[ "$2" == "util" ]];then
	ansiblePlaybook=$util
elif [[ "$2" == "config" ]];then
	ansiblePlaybook=$configPushPlaybook
elif [[ "$2" == "api" ]];then
	ansiblePlaybook=$armAPIPlaybook
else 
	echo "ERROR: Pass valid argument of type[server/server_action/application/asset/util/config/api]"
	exit 1
fi


echo "Ansible playbook :${ansiblePlaybook}"
AnsibleCommand="ansible-playbook -i ${hostFile} $ansiblePlaybook"

## Action validation with $4 /$5
if [[ "$2" != "server_action" ]];then 
	if [[ "$3" != "" ]];then  
	 AnsibleCommand=$AnsibleCommand" -e $2=$3"
	fi
	if [[ "$4" == action* ]];then
		AnsibleCommand=$AnsibleCommand" -e $2_$4"
	fi
	if [[ "$5" == action* ]];then
		AnsibleCommand=$AnsibleCommand" -e $2_$5"
	fi

	if [[ "$4" == -t* ]];then
		AnsibleCommand=$AnsibleCommand" $4"
	fi
	if [[ "$5" == -t* ]];then
		AnsibleCommand=$AnsibleCommand" $5"
	fi
else
    if [[ "$4" == action* ]];then
		AnsibleCommand=$AnsibleCommand" -e server=$3 -e mrt_$4"
	else
		echo " Please pass ./Ansible_Connect.sh <InventoryFilePath> server_action <servers> action=<>"
	fi
    
fi
echo "Ansible command : $AnsibleCommand"
$AnsibleCommand
status=$?
if [ "$status" -eq 0 ]
then
  echo "Ansible execution successful"
  exit 0
else
  echo "ERROR:${status} Ansible execution failed...!!!"
  exit ${status}
fi

