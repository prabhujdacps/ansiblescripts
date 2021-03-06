Param (
    [parameter(Position=0, Mandatory=$true)]
    [String]
    $account
)
If ($account -eq 'Domain')
{
    Set-Item -Path WSMan:\localhost\Service\Auth\Kerberos -Value $true
    Set-Item -Path WSMan:\localhost\Service\Auth\Basic -Value $false
    Set-Item -Path WSMan:\localhost\Service\Auth\CredSSP -Value $false
    Set-Item -Path WSMan:\localhost\Service\Auth\Certificate -Value $false

}
ElseIf ($account -eq 'Local')
{
    Set-Item -Path WSMan:\localhost\Service\Auth\Basic -Value $false
    Set-Item -Path WSMan:\localhost\Service\Auth\CredSSP -Value $false
    Set-Item -Path WSMan:\localhost\Service\Auth\Kerberos -Value $false
    Set-Item -Path WSMan:\localhost\Service\Auth\Certificate -Value $false
}
Else
{
    Write-Output "Please provide Domain or Local"
}
