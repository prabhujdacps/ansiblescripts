from MRT_Utils import *
import yaml
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
environment = None
label = None
applications=None
selectedApps=[]
directories=[]

def getRuntimeArgs(index,errorMessage,ignoreError=False):
    if(len(sys.argv)> index):
        return sys.argv[index]
    else:
        if ignoreError:
            return None
        else:
            error(str(index)+':'+errorMessage)
###Inputs
environment = getRuntimeArgs(1,"Environment name").replace("_","-")
new_Environment =getRuntimeArgs(2,"New environment name").replace("_","-")
label = getRuntimeArgs(3,"label")
new_label = getRuntimeArgs(4,"New label")
protocal = getRuntimeArgs(5,"Protocal (httt/https)")
if not(protocal == 'http' or protocal == 'https'):
    error("Invalid protocal in arg(4) [%s]. Please pass http (or) https "%(protocal))
host = getRuntimeArgs(6,"CPS host")
port = getRuntimeArgs(7,"CPS port")

applications = getRuntimeArgs(8,"Applications").split(",")

override=getRuntimeArgs(9,"Configuration")
if not(override == 'true' or override == 'false'):
    error("Invalid override in arg(9) [%s]. Please pass true (or) false "%(protocal))

CPS_BASE_URL='/cps/api/v1/application/'
CPS_URL = "%s://%s:%s" % (protocal,host, port)

print("-------------------------------------")


if not isURLReachable(CPS_URL+CPS_BASE_URL):
    error(CPS_URL+CPS_BASE_URL+" is not reachable..!!!")
else:
    print("CPS URL [%s] is reachable" %(CPS_URL + CPS_BASE_URL))
print("Environment: "+environment)
print("Label: "+label)
print("New environment: "+new_Environment)
print("New label: "+new_label)

for application in applications:
    ## Export API
    #{applicationName}/environments/exports?environment={env}&label={label}&encryptionKey={encryptionKey}
    print("Application: " + application)
    exportURL=CPS_URL+CPS_BASE_URL+"%s/environments/exports?environment=%s&label=%s"%(application,environment,label)
    importURL=CPS_URL+CPS_BASE_URL+"%s/environments/imports?environment=%s&label=%s&overwrite=%s"%(application,
                                                                                                  new_Environment,
                                                                                                   new_label,override)

    print(exportURL)
    print(importURL)
    headers = {'accepts': 'application/json', 'Content-Type': 'application/json'}
    response=requests.get(url=exportURL,headers=headers, verify=False)
    if response.status_code >= 200 and response.status_code < 400:
        jsonResponse=response.text
        exportContent = json.loads(jsonResponse)
        exportContent.pop("meta",None)
        payload=json.dumps(exportContent)
        response = curlPost(importURL, data=payload, headers=headers)
        if response.status_code >= 200 and response.status_code < 400:
            print("Import successful on environment:%s, Label:%s, Response:\n        %s "%(new_Environment,new_label,
                                                                                    response.text))
        else:
            error(response.text)
    else:
        error(response.txt)
