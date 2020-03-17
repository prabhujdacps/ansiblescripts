powershell.exe -executionpolicy bypass -file <.ps>


Allow JDAConnect ports:
-----------------------
netsh advfirewall firewall add rule profile=any name="Allow WinRM CPS" dir=in localport=9810 protocol=TCP action=allow
netsh advfirewall firewall add rule profile=any name="Allow WinRM SRS" dir=in localport=9820 protocol=TCP action=allow
netsh advfirewall firewall add rule profile=any name="Allow WinRM MS" dir=in localport=9830 protocol=TCP action=allow
netsh advfirewall firewall add rule profile=any name="Allow WinRM MSUI" dir=in localport=8085 protocol=TCP action=allow



sudo firewall-cmd --zone=public --add-port=9810/tcp --permanent
sudo firewall-cmd --reload