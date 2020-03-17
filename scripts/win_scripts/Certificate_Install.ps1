Param (
    [parameter(Position=0, Mandatory=$true)]
    [String]
    $certificatePath
)

#$certPath = Read-Host -Prompt 'Enter the certificate path '
Import-Certificate -FilePath $certificatePath -CertStoreLocation cert:\LocalMachine\Root

$username = Read-Host -Prompt 'Enter your Login Username '
$password = Read-Host -AsSecureString -Prompt 'Enter your Password '
$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $username, $password

$thumbprint = (Get-ChildItem -Path cert:\LocalMachine\root | Where-Object { $_.Subject -eq "CN=$username" }).Thumbprint

New-Item -Path WSMan:\localhost\ClientCertificate `
    -Subject "$username@localhost" `
    -URI * `
    -Issuer $thumbprint `
    -Credential $credential `
    -Force