Set-Item -Path WSMan:\localhost\Service\Auth\Basic -Value $false
Set-Item -Path WSMan:\localhost\Service\Auth\CredSSP -Value $true
Set-Item -Path WSMan:\localhost\Service\Auth\Kerberos -Value $false
Set-Item -Path WSMan:\localhost\Service\Auth\Certificate -Value $false
