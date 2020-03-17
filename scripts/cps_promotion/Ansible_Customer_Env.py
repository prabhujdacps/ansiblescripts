from MRT_Utils import *
import yaml

def getRuntimeArgs(index,errorMessage,ignoreError=False):
    if(len(sys.argv)> index):
        return sys.argv[index]
    else:
        if ignoreError:
            return None
        else:
            error(str(index)+':'+errorMessage)


path=getRuntimeArgs(1,"Common yaml file")
targetPath=getRuntimeArgs(2,"targetPath")


data=None
with open(path, 'r') as myfile:
    data = myfile.read()

environment=yaml.load(data, Loader=yaml.FullLoader)

hostFileContent=[]

machines=environment.get("MRT")

### Cleanup and create file
hostFilePath=targetPath+os.sep+'hosts.ini'
hostVarPath=targetPath + os.sep + 'host_vars' + os.sep
groupVarPath=targetPath + os.sep + 'group_vars'+os.sep
delete(targetPath)
delete(hostFilePath)
delete(hostVarPath)
delete(groupVarPath)
mkdir(hostVarPath)
mkdir(groupVarPath)


def createFile(path,content):
    print(path)
    print('---------------------------------')
    file = open(path, "w+")
    for line in content:
        print(" "+line)
        file.write(line + '\n')

hostFileContent.append("[MRT:children]")
for machine in machines:
    hostFileContent.append(machine)
hostFileContent.append("")

## check nodes
for machine in machines:
    hostFileContent.append("")
    machineHostVars_nodes = machines.get(machine).get("host_vars")
    hostFileContent.append("[" + machine + "]")
    for machineHostVars_node in machineHostVars_nodes:
        hostFileContent.append(machineHostVars_node)
    machineHostVars=machines.get(machine).get("vars")
    hostFileContent.append("")
    hostFileContent.append("["+machine+":vars]")
    for machineHostVar in machineHostVars:
        hostFileContent.append(machineHostVar+"="+machineHostVars.get(machineHostVar))

createFile(hostFilePath,hostFileContent)



def iterateYaml1(content):
    for childContent in content:
        childContentValue = content.get(childContent)
        if isinstance(childContentValue, bool):
            fileContent.append("        " + childContent + " : " + str(childContentValue).lower())
        elif isinstance(childContentValue, str) or isinstance(childContentValue, int):
            # fileContent.append("        " + childContent + " : " + str(childContentValue))
            if "{{" in str(childContentValue):
                fileContent.append("        " + childContent + ' : "' + str(childContentValue)+'"')
            else:
                fileContent.append("        " + childContent + " : " + str(childContentValue))
        elif isinstance(childContentValue, dict):
            fileContent.append("            " +childContent + "  : ")
            iterateYaml2(childContentValue)
def iterateYaml3(content):
    for childContent in content:
        childContentValue = content.get(childContent)
        if isinstance(childContentValue,bool):
            fileContent.append("                        " + childContent + " : " + str(childContentValue).lower())
        elif isinstance(childContentValue, str) or isinstance(childContentValue, int):
            if(str(childContentValue)).startswith('"'):
                fileContent.append("                        " + childContent + " : " +"\""+ str(
                    childContentValue).replace("\"","\\\"")+"\"")
            else:
                # fileContent.append("                        " + childContent + " : " + str(childContentValue))
                if "{{" in str(childContentValue):
                    fileContent.append("                        " + childContent + ' : "' + str(childContentValue) + '"')
                else:
                    fileContent.append("                        " + childContent + " : " + str(childContentValue))

        elif isinstance(childContentValue, dict):
            error("not supported")

def iterateYaml2(content):
    for childContent in content:
        childContentValue = content.get(childContent)
        if isinstance(childContentValue,bool):
            fileContent.append("          " + childContent + " : " + str(childContentValue).lower())

        elif isinstance(childContentValue, str) or isinstance(childContentValue, int):
            # fileContent.append("          " + childContent + " : " + str(childContentValue))
            if "{{" in str(childContentValue):
                fileContent.append("          " + childContent + ' : "' + str(childContentValue) + '"')
            else:
                fileContent.append("          " + childContent + " : " + str(childContentValue))
        elif isinstance(childContentValue, dict):
            fileContent.append("                    " + childContent + "  : ")
            iterateYaml3(childContentValue)

def iterateYaml(content):
    for childContent in content:
        childContentValue = content.get(childContent)
        if isinstance(childContentValue, bool):
            fileContent.append("    " + childContent + " : " + str(childContentValue).lower())

        elif isinstance(childContentValue, str) or isinstance(childContentValue, int):
            if "{{" in str(childContentValue):
                fileContent.append("    " + childContent + ' : "' + str(childContentValue)+'"')
            else:
                fileContent.append("    " + childContent + " : " + str(childContentValue))
        elif isinstance(childContentValue, dict):
            fileContent.append("    " + childContent + "  : ")
            iterateYaml1(childContentValue)
### Group_vars
group_vars=environment.get("group_vars")
for group_var in group_vars:
    groupvar_file=[]
    fileFullPath=groupVarPath+ group_var+".yaml"
    #print(fileFullPath.replace(targetPath,''))
    groupValue=group_vars.get(group_var)## create file
    for value in groupValue:
        # groupvar_file.append((value+" : "+groupValue.get(value)))
        if "{{" in str(groupValue.get(value)):
            groupvar_file.append((value + ' : "' + str(groupValue.get(value))) + '"')
        else:
            groupvar_file.append((value+" : "+str(groupValue.get(value))))
    createFile(fileFullPath, groupvar_file)


host_vars=environment.get("host_vars")
for host_var in host_vars:
    fileFullPath=hostVarPath+ host_var + ".yaml"
    #print(fileFullPath.replace(targetPath,''))
    fileContent=[]
    hostValue=host_vars.get(host_var)## create file

    for value in hostValue:
        content=hostValue.get(value)
        if isinstance(content, dict):
            fileContent.append(value + "  : ")
            iterateYaml(content)
        elif isinstance(content, bool):
            fileContent.append(value+" : "+str(content).lower())
        else:
            if "{{" in str(content):
                fileContent.append((value+' : "'+str(content))+'"')
            else:
                fileContent.append((value+" : "+str(content)))
    createFile(fileFullPath, fileContent)


print("Environment location: \n"+targetPath)





