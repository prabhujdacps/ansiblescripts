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
applicationsDirectories = getRuntimeArgs(1,"Applications parent directory (or) Application yml file")
if not(os.path.isdir(applicationsDirectories) or os.path.isfile(applicationsDirectories)):
    error("Invalid path in arg(1) [%s]. Please pass configuration directory (or) application updated property file"%(applicationsDirectories))

environment = getRuntimeArgs(2,"Environment name")
label = getRuntimeArgs(3,"Environment name")
protocal = getRuntimeArgs(4,"Protocal (httt/https)")
if not(protocal == 'http' or protocal == 'https'):
    error("Invalid protocal in arg(4) [%s]. Please pass http (or) https "%(applicationsDirectories))

host = getRuntimeArgs(5,"CPS host")
port = getRuntimeArgs(6,"CPS port")

applications = getRuntimeArgs(7,"Applications",True)

CPS_BASE_URL='/cps/api/v1/application/'
CPS_URL = "%s://%s:%s" % (protocal,host, port)
print("-------------------------------------")


if not isURLReachable(CPS_URL+CPS_BASE_URL):
    error(CPS_URL+CPS_BASE_URL+" is not reachable..!!!")
else:
    print("CPS URL [%s] is reachable" %(CPS_URL + CPS_BASE_URL))
print("Environment: "+environment)
print("Label: "+label)

def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out

def toJsonProperties(properties):
    jsonContent = "{\n\"properties\": \n"
    content = properties
    return jsonContent + content + "\n }\n"

def convertYamlToJson(filePath):
    with open(filePath) as file:
        yamlValues = yaml.load(file, Loader=yaml.FullLoader)
        return json.dumps(flatten_json(yamlValues))

def convertPropertiesToJson(file):
    return load_properties(file)


def updateConfigurationProperty(url,payload):
    global properties, jsonContent, headers, result
    headers = {'accept': 'application/json','Content-Type': 'application/json'}
    print("POST: " + url)
    response = curlPost(url, headers=headers, data=payload)
    if response.status_code >= 200 and response.status_code < 400:
        print("      File " + json.loads(response.text)['resource']+ ' updated in remote CPS')
    else:
        print("      Error Response: " + response.text)

def updateResources(url,payload):
    global properties, jsonContent, headers, result
    headers = {'accept': 'application/json, application/xml, application/yaml, application/octet-stream, text/plain',
               'Content-Type': 'application/json'}
    print("POST: " + url)
    response = curlPut(url, headers=headers, data=payload)
    if response.status_code >= 200 and response.status_code < 400:
        print("      File " + json.loads(response.text)['resource']+ ' updated in remote CPS')
    else:
        print("      Error Response: " + response.text)

def configurationPayload(file):
    global properties, jsonContent
    if file.endswith(".properties"):
        propertiesDist = convertPropertiesToJson(file)
        properties = []
        for property in propertiesDist:
            properties.append('"' + property + '" : "' + propertiesDist.get(property) + '"')
    if file.endswith(".yaml") or file.endswith(".yaml"):
        properties = convertYamlToJson(file)
    jsonContent = toJsonProperties(properties)
    printJsonContent = jsonContent.replace("\n", "")
    debug("      Data:" + printJsonContent)
    return jsonContent

### Get resource payload
def resourcePayload(file):
    global properties, jsonContent, headers, result
    with open(file, 'r') as myfile:
        data = myfile.read()
    printJsonContent = data.replace("\n", "")
    debug("Data:  " + printJsonContent)
    return data

########
resourceDir = 'resources'

#####Resource as directory############
if os.path.isdir(applicationsDirectories):
    ## Filter application directories
    if applications is not None and applications != '':
        filterApplications = applications.split(',')
        for filterApplication in filterApplications:
            application_path = applicationsDirectories + os.sep + filterApplication
            if (os.path.exists(application_path)):
                directories.append(application_path)
            else:
                warn("Application [%s] not found in directory [%s]" % (filterApplication, applicationsDirectories))
    else:
        directories = getCurrentDirectoryFiles(applicationsDirectories)

    for applicationDir in directories:
        selectedApps.append(os.path.basename(applicationDir))
    if len(directories) > 0:
        print("Selected applications configurations under %s directory : %s" % (applicationsDirectories,
                                                                                str(selectedApps)))
    else:
        warn("No applications configurations selected under %s directory" % (applicationsDirectories))

    print("Applications: " + str(selectedApps))
    print("-------------------------------------")

    for directory in directories:
        ApplicationName = os.path.basename(directory)
        print("-------------------------------------\n" + "APPLICATION :" +
              ApplicationName + "\n-------------------------------------")
        ##endpoints
        CPS_PROPERTIES_ENDPOINT = CPS_BASE_URL + ApplicationName + "/properties?environment=%s&label=%s" % (environment,
                                                                                                            label)
        CPS_RESOURCES_ENDPOINT = CPS_BASE_URL + ApplicationName + "/resources/{path}?environment=%s&label=%s" % (
            environment,
            label)

        applicationPropFile = None
        categories_files = []
        category_instance_files = []
        resourceFiles = []
        applicationDirFiles = getCurrentDirectoryFiles(directory)
        resoure_dir = directory + os.sep + resourceDir

        if not os.path.exists(resoure_dir):
            resoure_dir = None
        else:
            if resoure_dir in applicationDirFiles:
                applicationDirFiles.remove(resoure_dir)
            resourceFiles = getFilesList(resoure_dir)

        for propertyFile in applicationDirFiles:
            fileName = os.path.basename(propertyFile)
            if ApplicationName + '.' in fileName:
                applicationPropFile = propertyFile
            if ApplicationName + '-' in fileName:
                if '_' in fileName:
                    category_instance_files.append(propertyFile)
                else:
                    categories_files.append(propertyFile)

        ## Call CPS property update API
        # POST {applicationName}/properties?environment={env}&label={label}
        if applicationPropFile is not None:
            updateConfigurationProperty(CPS_URL + CPS_PROPERTIES_ENDPOINT, configurationPayload(applicationPropFile))

        ## Call CPS property update API with {categories}
        # POST {applicationName}/properties?environment={env}&label={label}&categories={categories}
        for appCategory in categories_files:
            category = os.path.basename(appCategory)
            if '.' in category and ApplicationName in category and ApplicationName + '-' in category:
                category = category.split('.')[0]
                category = category.replace(ApplicationName + '-', '')
                URL = CPS_PROPERTIES_ENDPOINT + "&categories=%s" % (category)
                updateConfigurationProperty(CPS_URL + URL, configurationPayload(appCategory))

        ## Call CPS property update API with categories&instance
        # POST {applicationName}/properties?environment={env}&label={label}&categories={categories}&instance={instance}
        for appCategoryInstance in category_instance_files:
            category_instance = os.path.basename(appCategoryInstance)
            if '.' in category_instance and ApplicationName in category_instance and '_' in category_instance and '-' in \
                    category_instance:
                category_instance = category_instance.replace(ApplicationName, '')
                category_instance = (category_instance.split('.')[0]).replace('-', '')
                category_instance = category_instance.split('_')
                URL = CPS_PROPERTIES_ENDPOINT + "&categories=%s&instance=%s" % (
                category_instance[0], category_instance[1])
                updateConfigurationProperty(CPS_URL + URL, configurationPayload(appCategoryInstance))

        ## Call CPS resources API
        # POST {applicationName}/resources/{path}?environment={env}&label={label}
        for resourceFile in resourceFiles:
            resourcePath = resourceFile.replace(resoure_dir + os.sep, '').replace(os.sep, "|")
            URL = CPS_RESOURCES_ENDPOINT.replace("{path}", resourcePath)
            updateResources(CPS_URL + URL, resourcePayload(resourceFile))

if os.path.isfile(applicationsDirectories):
    print("Configuration upgrade with file:"+applicationsDirectories)
    if applications is not None and applications != '':
        filterApplications = applications.split(',')
    else:
        filterApplications = None
    if filterApplications is None:
        appFile = open(applicationsDirectories, "r")
        selectedApps = []
        for line in appFile:
            jsonData = json.loads(line)
            for application in jsonData:
                selectedApps.append(application)
        print("Applications: " + str(selectedApps))
    else:
        print("Applications: " + str(filterApplications))
    print("-------------------------------------")
    appFile = open(applicationsDirectories, "r")
    for line in appFile:
        jsonData = json.loads(line)
        for application in jsonData:
            CPS_PROPERTIES_ENDPOINT = CPS_BASE_URL + application + "/properties?environment=%s&label=%s" % (environment,
                                                                                                            label)
            if filterApplications is None or (application in filterApplications):
                print("-------------------------------------\n" + "APPLICATION :" +
                      application + "\n-------------------------------------")
                jsonContent = jsonData.get(application)
                mainProperties = None
                categories = None
                categoryInstance = None
                if 'main' in jsonContent:
                    mainProperties = jsonContent['main']
                    payload = toJsonProperties(json.dumps(mainProperties))
                    print("Data:  " + (str(payload)).replace("\n",""))
                    updateConfigurationProperty(CPS_URL + CPS_PROPERTIES_ENDPOINT, payload)


                if 'categories' in jsonContent:
                    categories = jsonContent['categories']
                    for category in categories:
                        payload = toJsonProperties(json.dumps(categories.get(category)))
                        URL = CPS_PROPERTIES_ENDPOINT + "&categories=%s" % (category)
                        print("Data:  " + (str(payload)).replace("\n",""))
                        updateConfigurationProperty(CPS_URL + URL, payload)


                if 'category-instance' in jsonContent:
                    categoryInstance = jsonContent['category-instance']
                    for categoryIns in categoryInstance:
                        payload = toJsonProperties(json.dumps(categoryInstance.get(categoryIns)))
                        category_instance = (str(categoryIns)).split("_")
                        URL = CPS_PROPERTIES_ENDPOINT + "&categories=%s&instance=%s" % (
                            category_instance[0], category_instance[1])
                        print("Data:  " + (str(payload)).replace("\n",""))
                        updateConfigurationProperty(CPS_URL + URL, payload)





