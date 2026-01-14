"""
Management command to seed professional-quality IT knowledge base articles.

Creates focused, practical IT documentation based on real-world scenarios.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from docs.models import Document, DocumentCategory


class Command(BaseCommand):
    help = 'Seed professional-quality global KB articles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete existing global KB articles before seeding',
        )

    def handle(self, *args, **options):
        if options['delete']:
            self.stdout.write('Deleting existing global KB articles...')
            Document.objects.filter(is_global=True, organization=None).delete()
            DocumentCategory.objects.filter(organization=None).delete()
            self.stdout.write(self.style.SUCCESS('✓ Deleted existing articles'))

        self.stdout.write('Creating professional KB categories...')
        categories = self.create_categories()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(categories)} categories'))

        self.stdout.write('Creating professional KB articles...')
        total_created = 0

        for category_name, category in categories.items():
            articles = self.get_professional_articles(category_name)
            for article_data in articles:
                self.create_article(article_data, category)
                total_created += 1

        self.stdout.write(self.style.SUCCESS(f'✓ Created {total_created} professional KB articles'))

    def create_categories(self):
        """Create focused KB categories."""
        categories_data = [
            ('Windows Administration', 'windows-admin', 'Windows server and workstation management', 'fab fa-windows', 1),
            ('Active Directory', 'active-directory', 'AD troubleshooting and management', 'fas fa-sitemap', 2),
            ('Microsoft 365', 'microsoft-365', 'Microsoft 365 and Exchange Online', 'fab fa-microsoft', 3),
            ('Network Troubleshooting', 'network-troubleshooting', 'Network connectivity and configuration', 'fas fa-network-wired', 4),
            ('Security & Compliance', 'security-compliance', 'Security best practices and compliance', 'fas fa-shield-alt', 5),
            ('Backup & Recovery', 'backup-recovery', 'Backup procedures and disaster recovery', 'fas fa-database', 6),
            ('Common Issues', 'common-issues', 'Frequently encountered IT problems and solutions', 'fas fa-wrench', 7),
            ('Hardware Setup', 'hardware-setup', 'Hardware installation and configuration', 'fas fa-server', 8),
        ]

        categories = {}
        for name, slug, description, icon, order in categories_data:
            category, created = DocumentCategory.objects.get_or_create(
                organization=None,
                slug=slug,
                defaults={
                    'name': name,
                    'description': description,
                    'icon': icon,
                    'order': order,
                }
            )
            categories[name] = category

        return categories

    def create_article(self, article_data, category):
        """Create a KB article."""
        Document.objects.get_or_create(
            organization=None,
            slug=slugify(article_data['title']),
            defaults={
                'title': article_data['title'],
                'body': article_data['body'],
                'content_type': 'markdown',
                'is_global': True,
                'is_published': True,
                'category': category,
            }
        )

    def get_professional_articles(self, category_name):
        """Return professional articles for each category."""

        articles = {
            'Windows Administration': [
                {
                    'title': 'How to Reset Windows Local Administrator Password',
                    'body': '''# Reset Windows Local Administrator Password

## Overview
This guide covers the process of resetting a local administrator password when locked out of a Windows system.

## Prerequisites
- Physical access to the machine
- Windows installation media (USB or DVD)
- OR a password reset disk

## Method 1: Using Windows Installation Media

### Steps
1. Boot from Windows installation media
2. At the "Install Now" screen, press `Shift + F10` to open Command Prompt
3. Run the following commands:
   ```
   diskpart
   list volume
   exit
   ```
4. Note the drive letter of your Windows installation (usually C: or D:)
5. Replace `utilman.exe` with `cmd.exe`:
   ```
   move c:\\windows\\system32\\utilman.exe c:\\windows\\system32\\utilman.exe.bak
   copy c:\\windows\\system32\\cmd.exe c:\\windows\\system32\\utilman.exe
   ```
6. Remove the installation media and restart
7. At the login screen, click the Ease of Access button (this now opens CMD)
8. Reset the password:
   ```
   net user username newpassword
   ```
9. Reboot and restore utilman.exe:
   ```
   move c:\\windows\\system32\\utilman.exe.bak c:\\windows\\system32\\utilman.exe
   ```

## Method 2: Using Safe Mode with Command Prompt
1. Restart and press `F8` before Windows loads
2. Select "Safe Mode with Command Prompt"
3. Login as Administrator (if available)
4. Run: `net user username newpassword`
5. Restart normally

## Best Practices
- Always document password resets in your ticketing system
- Verify user identity before resetting passwords
- Require password change on next login
- Enable BitLocker before performing this procedure on sensitive systems

## Security Note
⚠️ This method requires physical access. Systems with BitLocker or full disk encryption cannot be accessed this way without the recovery key.
'''
                },
                {
                    'title': 'Troubleshooting Windows Update Failures',
                    'body': '''# Troubleshooting Windows Update Failures

## Common Error Codes
- **0x80070002**: Files missing from update cache
- **0x80070003**: Path not found
- **0x80070005**: Access denied
- **0x8007000E**: Insufficient memory
- **0x80240034**: Windows Update service stopped

## Quick Fixes

### 1. Run Windows Update Troubleshooter
```powershell
# Windows 10/11
msdt.exe /id WindowsUpdateDiagnostic
```

### 2. Reset Windows Update Components
```cmd
net stop wuauserv
net stop cryptSvc
net stop bits
net stop msiserver

ren C:\\Windows\\SoftwareDistribution SoftwareDistribution.old
ren C:\\Windows\\System32\\catroot2 Catroot2.old

net start wuauserv
net start cryptSvc
net start bits
net start msiserver
```

### 3. Clear Windows Update Cache
```powershell
Stop-Service -Name wuauserv -Force
Remove-Item C:\\Windows\\SoftwareDistribution\\Download\\* -Recurse -Force
Start-Service -Name wuauserv
```

### 4. Use DISM and SFC
```cmd
DISM /Online /Cleanup-Image /RestoreHealth
sfc /scannow
```

## Advanced Troubleshooting

### Check CBS.log for Errors
```powershell
Get-Content C:\\Windows\\Logs\\CBS\\CBS.log | Select-String -Pattern "error"
```

### Manual Update Installation
1. Visit Microsoft Update Catalog
2. Search for KB number
3. Download appropriate version
4. Install manually with `wusa.exe`

## Prevention
- Keep 20GB+ free space on C: drive
- Ensure antivirus allows Windows Update
- Run `chkdsk /f` if disk errors suspected
- Disable unnecessary startup programs

## When to Escalate
- Multiple failed attempts with different methods
- System instability after update attempts
- Critical security updates failing repeatedly
'''
                },
                {
                    'title': 'Configure Windows Firewall Rules via PowerShell',
                    'body': '''# Configure Windows Firewall Rules via PowerShell

## View Existing Rules
```powershell
# List all firewall rules
Get-NetFirewallRule

# List enabled rules
Get-NetFirewallRule | Where-Object {$_.Enabled -eq "True"}

# Search for specific rules
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Remote Desktop*"}
```

## Create New Firewall Rules

### Allow Inbound Port
```powershell
New-NetFirewallRule -DisplayName "Allow SQL Server" `
    -Direction Inbound `
    -LocalPort 1433 `
    -Protocol TCP `
    -Action Allow
```

### Allow Program
```powershell
New-NetFirewallRule -DisplayName "Allow Custom App" `
    -Direction Inbound `
    -Program "C:\\Program Files\\MyApp\\app.exe" `
    -Action Allow
```

### Allow Specific IP Range
```powershell
New-NetFirewallRule -DisplayName "Allow Office Network" `
    -Direction Inbound `
    -LocalPort 445 `
    -Protocol TCP `
    -RemoteAddress 192.168.1.0/24 `
    -Action Allow
```

## Modify Existing Rules
```powershell
# Enable a rule
Set-NetFirewallRule -DisplayName "Rule Name" -Enabled True

# Disable a rule
Set-NetFirewallRule -DisplayName "Rule Name" -Enabled False

# Change port
Set-NetFirewallRule -DisplayName "Rule Name" -LocalPort 8080
```

## Remove Rules
```powershell
# Remove by name
Remove-NetFirewallRule -DisplayName "Rule Name"

# Remove by display group
Remove-NetFirewallRule -DisplayGroup "Remote Desktop"
```

## Common Scenarios

### Enable RDP
```powershell
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
```

### Enable File and Printer Sharing
```powershell
Enable-NetFirewallRule -DisplayGroup "File and Printer Sharing"
```

### Block Outbound to Specific IP
```powershell
New-NetFirewallRule -DisplayName "Block Malicious IP" `
    -Direction Outbound `
    -RemoteAddress 203.0.113.0 `
    -Action Block
```

## Export/Import Rules
```powershell
# Export rules
Get-NetFirewallRule | Export-Csv -Path C:\\firewall-rules.csv

# Import rules (requires custom script)
```

## Best Practices
- Always name rules descriptively
- Document business justification for exceptions
- Review rules quarterly
- Use groups for related rules
- Test rules before deploying to production
- Keep audit trail of firewall changes
'''
                },
            ],

            'Active Directory': [
                {
                    'title': 'Troubleshoot User Account Lockouts in Active Directory',
                    'body': '''# Troubleshoot User Account Lockouts in Active Directory

## Quick Check
```powershell
# Check if account is locked
Get-ADUser -Identity username -Properties LockedOut, LockoutTime

# Unlock account
Unlock-ADAccount -Identity username
```

## Find Lockout Source

### Method 1: Security Event Log
Look for Event ID 4740 on Domain Controllers:
```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4740} |
    Where-Object {$_.Properties[0].Value -eq 'username'} |
    Select-Object -First 10
```

### Method 2: Account Lockout Status Tool
1. Download Microsoft Account Lockout Status Tool
2. Run against all DCs
3. Identify source computer from "Caller Computer Name"

### Method 3: PowerShell Query All DCs
```powershell
$DCs = Get-ADDomainController -Filter *
foreach ($DC in $DCs) {
    Get-WinEvent -ComputerName $DC.Name -FilterHashtable @{
        LogName='Security'
        ID=4740
        StartTime=(Get-Date).AddHours(-24)
    } | Where-Object {$_.Properties[0].Value -eq 'username'}
}
```

## Common Causes

### 1. Saved Credentials
- Mapped drives with old credentials
- Scheduled tasks running with old password
- Mobile devices (phones, tablets)
- Web browsers with saved passwords
- Windows Credential Manager

### 2. Service Accounts
- Services running under user context
- IIS application pools
- SQL Server services

### 3. Cached Credentials
```cmd
# Clear cached credentials
rundll32.exe keymgr.dll,KRShowKeyMgr
```

### 4. Mobile Devices
- Exchange ActiveSync devices
- Check: `Get-MobileDevice -Mailbox username`

## Investigation Steps

1. **Check Event Viewer on DCs**
   - Security Log → Event ID 4740
   - Note the "Caller Computer Name"

2. **Check the Source Computer**
   ```powershell
   # On source computer, check for saved credentials
   cmdkey /list
   ```

3. **Check Scheduled Tasks**
   ```powershell
   Get-ScheduledTask | Where-Object {$_.Principal.UserId -like "*username*"}
   ```

4. **Check Services**
   ```powershell
   Get-WmiObject Win32_Service | Where-Object {$_.StartName -like "*username*"}
   ```

5. **Check IIS App Pools** (if applicable)
   ```powershell
   Import-Module WebAdministration
   Get-ChildItem IIS:\\AppPools | Where-Object {$_.ProcessModel.UserName -like "*username*"}
   ```

## Prevention

### Configure Account Lockout Policy
```powershell
# View current policy
Get-ADDefaultDomainPasswordPolicy

# Recommended settings
Set-ADDefaultDomainPasswordPolicy `
    -LockoutDuration 00:30:00 `
    -LockoutObservationWindow 00:30:00 `
    -LockoutThreshold 5
```

### Enable Advanced Auditing
```cmd
auditpol /set /subcategory:"Account Lockout" /success:enable /failure:enable
```

### Document Service Accounts
- Maintain inventory of service accounts
- Use Managed Service Accounts (MSA) when possible
- Set password expiration alerts

## Tools
- **Account Lockout Status**: Microsoft tool for DCs
- **LockoutStatus.exe**: Shows lockout info across domain
- **EventCombMT**: Aggregate events from multiple servers

## Quick Reference
| Event ID | Description |
|----------|-------------|
| 4740 | Account lockout |
| 4625 | Failed logon attempt |
| 4648 | Explicit credentials used |
| 4768 | Kerberos TGT requested |
| 4771 | Kerberos pre-auth failed |
'''
                },
                {
                    'title': 'Active Directory Group Policy Troubleshooting',
                    'body': '''# Active Directory Group Policy Troubleshooting

## Quick Diagnostics

### Check Applied GPOs
```cmd
gpresult /r
gpresult /h c:\\gpreport.html
```

### Force GP Update
```cmd
gpupdate /force
```

### Verify GPO Status
```powershell
Get-GPO -All | Where-Object {$_.GpoStatus -eq "AllSettingsDisabled"}
```

## Common Issues

### 1. GPO Not Applying

**Check GPO Links**
```powershell
Get-GPInheritance -Target "OU=Computers,DC=domain,DC=com"
```

**Verify Security Filtering**
```powershell
Get-GPPermissions -Name "GPO Name" -All
```

**Check WMI Filters**
```powershell
Get-GPO -Name "GPO Name" | Select-Object -ExpandProperty WmiFilter
```

### 2. Slow Group Policy Processing

**Enable GP Logging**
```cmd
reg add "HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Diagnostics" /v GPSvcDebugLevel /t REG_DWORD /d 0x00030002 /f
```

**Check GP Processing Times**
```powershell
Get-WinEvent -LogName "Microsoft-Windows-GroupPolicy/Operational" |
    Where-Object {$_.Id -eq 8001} |
    Select-Object TimeCreated, Message
```

### 3. "Applied" but Settings Not Taking Effect

**Check Resultant Set of Policy**
```cmd
rsop.msc
```

**Generate Advanced Report**
```cmd
gpresult /h report.html /f
```

## Advanced Troubleshooting

### GPO Replication Issues
```powershell
# Check SYSVOL replication
dcdiag /test:sysvolcheck

# Force AD replication
repadmin /syncall /AdeP
```

### Check GPO Version Consistency
```powershell
# Compare AD and SYSVOL versions
Get-GPO -All | ForEach-Object {
    $adVersion = $_.Computer.DSVersion
    $sysvolVersion = Get-ChildItem "\\\\domain.com\\SYSVOL\\domain.com\\Policies\\$($_.Id)" -ErrorAction SilentlyContinue
    if ($adVersion -ne $sysvolVersion) {
        Write-Host "$($_.DisplayName): Version mismatch"
    }
}
```

### Reset Group Policy
```cmd
# Reset local GP
RD /S /Q "%WinDir%\\System32\\GroupPolicyUsers"
RD /S /Q "%WinDir%\\System32\\GroupPolicy"
gpupdate /force
```

## GPO Processing Order
1. Local Computer Policy
2. Site GPOs
3. Domain GPOs
4. Organizational Unit GPOs (parent to child)

**Remember LSDOU (Local, Site, Domain, OU)**

## Useful Commands

### View All GPOs
```powershell
Get-GPO -All | Select-Object DisplayName, GpoStatus, CreationTime
```

### Find Unlinked GPOs
```powershell
Get-GPO -All | Where-Object {
    (Get-GPOReport -Guid $_.Id -ReportType Xml) -notmatch "<LinksTo>"
}
```

### Backup All GPOs
```powershell
Backup-GPO -All -Path C:\\GPOBackup
```

### Find Empty GPOs
```powershell
Get-GPO -All | Where-Object {
    ($_ | Get-GPOReport -ReportType Xml) -notmatch "q1:|q2:"
}
```

## Best Practices
- Test GPOs in separate OU before production
- Use security filtering sparingly
- Document all GPO changes
- Regular backup schedule
- Remove unused GPOs
- Use descriptive GPO names
- Implement least privilege
- Monitor GPO processing times

## Event IDs to Monitor
| Event ID | Log | Description |
|----------|-----|-------------|
| 1129 | Application | GPO processing started |
| 8001 | GP-Operational | GP processing completed |
| 8004 | GP-Operational | GP processing failed |
| 7016 | Application | GPO cached |
| 1030 | Application | Policy change detected |
'''
                },
            ],

            'Microsoft 365': [
                {
                    'title': 'Reset Microsoft 365 User Password via PowerShell',
                    'body': '''# Reset Microsoft 365 User Password via PowerShell

## Prerequisites
```powershell
# Install Azure AD Module (if not already installed)
Install-Module -Name AzureAD

# Connect to Azure AD
Connect-AzureAD
```

## Reset User Password

### Generate Random Password
```powershell
$Password = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 12 | ForEach-Object {[char]$_})
Write-Host "New Password: $Password" -ForegroundColor Green
```

### Reset and Force Change on Next Login
```powershell
Set-AzureADUserPassword `
    -ObjectId user@domain.com `
    -Password (ConvertTo-SecureString -String "TempPassword123!" -AsPlainText -Force) `
    -ForceChangePasswordNextLogin $true
```

### Reset Without Forcing Change
```powershell
Set-AzureADUserPassword `
    -ObjectId user@domain.com `
    -Password (ConvertTo-SecureString -String "NewPassword123!" -AsPlainText -Force) `
    -ForceChangePasswordNextLogin $false
```

## Using Microsoft Graph PowerShell (Modern Method)

### Install and Connect
```powershell
Install-Module Microsoft.Graph -Scope CurrentUser
Connect-MgGraph -Scopes "User.ReadWrite.All"
```

### Reset Password
```powershell
$PasswordProfile = @{
    Password = "TempPassword123!"
    ForceChangePasswordNextSignIn = $true
}

Update-MgUser -UserId user@domain.com -PasswordProfile $PasswordProfile
```

## Bulk Password Reset

### From CSV File
```powershell
# CSV format: Email,NewPassword
$Users = Import-Csv C:\\users.csv

foreach ($User in $Users) {
    try {
        Set-AzureADUserPassword `
            -ObjectId $User.Email `
            -Password (ConvertTo-SecureString -String $User.NewPassword -AsPlainText -Force) `
            -ForceChangePasswordNextLogin $true

        Write-Host "✓ Reset password for $($User.Email)" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Failed for $($User.Email): $_" -ForegroundColor Red
    }
}
```

## Password Reset with Notification

### Send Email After Reset
```powershell
function Reset-M365PasswordWithNotification {
    param(
        [string]$UserEmail,
        [string]$NewPassword,
        [string]$NotifyEmail
    )

    # Reset password
    Set-AzureADUserPassword `
        -ObjectId $UserEmail `
        -Password (ConvertTo-SecureString -String $NewPassword -AsPlainText -Force) `
        -ForceChangePasswordNextLogin $true

    # Send notification (requires mail-enabled account)
    Send-MailMessage `
        -To $NotifyEmail `
        -From "helpdesk@domain.com" `
        -Subject "Password Reset Completed" `
        -Body "Password has been reset for $UserEmail. User will be prompted to change on next login." `
        -SmtpServer "smtp.office365.com" `
        -Port 587 `
        -UseSsl
}
```

## Troubleshooting

### Check User's License Status
```powershell
Get-AzureADUser -ObjectId user@domain.com | Select-Object DisplayName, UserPrincipalName, AccountEnabled
```

### Verify MFA Status
```powershell
Get-MsolUser -UserPrincipalName user@domain.com | Select-Object DisplayName, StrongAuthenticationRequirements
```

### Check Sign-In Logs After Reset
```powershell
# Requires Azure AD Premium
Get-AzureADAuditSignInLogs -Filter "userPrincipalName eq 'user@domain.com'" -Top 10
```

## Security Best Practices
1. **Use complex passwords**: Minimum 12 characters, mix of upper/lower/numbers/symbols
2. **Force password change**: Always require change on next login for resets
3. **Enable MFA**: Multi-factor authentication should be mandatory
4. **Document resets**: Log all password resets in ticketing system
5. **Temporary passwords**: Never reuse or save temporary passwords
6. **Secure transmission**: Use secure channels to communicate temporary passwords

## Common Error Messages

### "Insufficient privileges"
```powershell
# Solution: Ensure you have Password Administrator or User Administrator role
Connect-AzureAD -TenantId yourtenant.onmicrosoft.com
```

### "Password does not meet requirements"
- Check tenant password policy
- Ensure password meets complexity requirements
- Minimum 8 characters for M365

### "User not found"
```powershell
# Verify user exists
Get-AzureADUser -SearchString "username"
```

## Alternative Methods
- **Azure Portal**: Azure AD → Users → Reset Password
- **Microsoft 365 Admin Center**: Users → Active users → Reset password
- **Self-Service Password Reset**: Enable SSPR for users to reset their own passwords

## Emergency Access
For global admin accounts, ensure you have:
1. Break-glass account with documented password
2. Alternative authentication method
3. Documented recovery procedure
'''
                },
            ],

            'Network Troubleshooting': [
                {
                    'title': 'Network Connectivity Troubleshooting Checklist',
                    'body': '''# Network Connectivity Troubleshooting Checklist

## Layer 1: Physical Layer

### Check Physical Connections
- [ ] Cable securely plugged in both ends
- [ ] Link lights active on NIC and switch
- [ ] Try different cable
- [ ] Try different port on switch
- [ ] Check for cable damage

### Verify Hardware Status
```powershell
# Check NIC status (Windows)
Get-NetAdapter | Select-Object Name, Status, LinkSpeed

# Disable and re-enable adapter
Disable-NetAdapter -Name "Ethernet"
Enable-NetAdapter -Name "Ethernet"
```

## Layer 2: Data Link Layer

### Check MAC Address
```cmd
# Windows
ipconfig /all
getmac

# Linux
ip link show
```

### Verify Switch Port
- Check switch logs for errors
- Verify VLAN assignment
- Check for port security violations
- Verify spanning tree status

## Layer 3: Network Layer

### Basic IP Configuration
```cmd
# Windows
ipconfig /all

# Check IP, subnet mask, default gateway
# Verify DNS servers
```

### Ping Tests (in order)
```cmd
# 1. Ping loopback (127.0.0.1)
ping 127.0.0.1

# 2. Ping local IP
ping <your-ip-address>

# 3. Ping default gateway
ping <gateway-ip>

# 4. Ping external IP (Google DNS)
ping 8.8.8.8

# 5. Ping external hostname
ping google.com
```

### Route Verification
```cmd
# Windows
route print
tracert google.com

# Linux
ip route show
traceroute google.com
```

## Layer 4-7: Upper Layers

### DNS Troubleshooting
```cmd
# Flush DNS cache
ipconfig /flushdns

# Test DNS resolution
nslookup google.com
nslookup google.com 8.8.8.8

# Check DNS suffix
ipconfig /all | findstr "DNS"
```

### Port Connectivity
```powershell
# Test TCP port (PowerShell)
Test-NetConnection -ComputerName server.com -Port 443

# Test multiple ports
80,443,3389 | ForEach-Object {
    Test-NetConnection -ComputerName server.com -Port $_
}
```

## Quick Fixes

### Reset TCP/IP Stack (Windows)
```cmd
netsh int ip reset
netsh winsock reset
ipconfig /release
ipconfig /renew
ipconfig /flushdns
```

### Renew DHCP Lease
```cmd
# Windows
ipconfig /release
ipconfig /renew

# Linux
sudo dhclient -r
sudo dhclient
```

### Reset Network Adapter
```powershell
# PowerShell
Restart-NetAdapter -Name "Ethernet"

# Or use Device Manager
devmgmt.msc → Network adapters → Disable/Enable
```

## Advanced Diagnostics

### Packet Capture
```powershell
# Windows (requires admin)
netsh trace start capture=yes
# Reproduce issue
netsh trace stop

# View capture
# Use Microsoft Message Analyzer or Wireshark
```

### Check Firewall
```powershell
# Windows Firewall status
Get-NetFirewallProfile

# Check if blocking ping
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*ICMP*"}
```

### ARP Cache Issues
```cmd
# View ARP cache
arp -a

# Clear ARP cache
netsh interface ip delete arpcache
```

## Common Issues & Solutions

### "No Internet Access" but Local Network Works
1. Check default gateway: `ping <gateway>`
2. Check DNS: `nslookup google.com`
3. Check proxy settings
4. Verify firewall rules

### Slow Network Performance
```powershell
# Check NIC settings
Get-NetAdapterAdvancedProperty

# Verify duplex settings (should be auto-negotiate)
Get-NetAdapter | Get-NetAdapterAdvancedProperty -DisplayName "Speed & Duplex"

# Check for errors
Get-NetAdapterStatistics
```

### Intermittent Connectivity
1. Check for IP conflicts: `ipconfig /all`
2. Review DHCP scope
3. Check switch port errors
4. Test with static IP
5. Check for wireless interference (if applicable)

### DNS Not Resolving
```cmd
# Try alternative DNS
netsh interface ip set dns "Ethernet" static 8.8.8.8
netsh interface ip add dns "Ethernet" 8.8.4.4 index=2

# Or edit DNS via GUI
ncpa.cpl → Properties → IPv4 → DNS Servers
```

## Documentation Template
```
Issue: ___________________________________
User: ____________________________________
Date/Time: _______________________________
Symptoms: ________________________________

Tests Performed:
[ ] Physical layer check
[ ] IP configuration verified
[ ] Ping tests completed
[ ] DNS resolution tested
[ ] Firewall checked

Results:
_________________________________________

Resolution:
_________________________________________

Notes:
_________________________________________
```

## Useful Tools
- **ping**: Basic connectivity test
- **tracert/traceroute**: Path to destination
- **nslookup**: DNS queries
- **pathping**: Combines ping and tracert
- **Wireshark**: Packet analysis
- **netstat**: Network connections
- **PuTTY**: SSH/Telnet client

## When to Escalate
- Physical layer issues (damaged cables/ports)
- Switch/router configuration needed
- ISP-related problems
- Complex routing issues
- Security policy conflicts
'''
                },
            ],

            'Security & Compliance': [
                {
                    'title': 'Implement Security Baseline for Windows 10/11',
                    'body': '''# Implement Security Baseline for Windows 10/11

## Overview
Microsoft Security Baselines are group policy settings that configure Windows for enhanced security.

## Download Security Baseline
1. Visit Microsoft Security Compliance Toolkit
2. Download Windows 10/11 Security Baseline
3. Extract to network location

## Import Baseline GPOs

### Via Group Policy Management
```powershell
# Copy GPO backup
Copy-Item -Path "\\\\server\\SecurityBaselines\\*" -Destination "C:\\GPOBackup" -Recurse

# Import GPOs
Import-GPO -BackupId <GUID> -Path "C:\\GPOBackup" -TargetName "Baseline - Windows 10" -CreateIfNeeded
```

## Key Security Settings

### 1. User Account Control (UAC)
```
Computer Configuration → Windows Settings → Security Settings → Local Policies → Security Options
- User Account Control: Run all administrators in Admin Approval Mode = Enabled
- User Account Control: Admin Approval Mode for Built-in Administrator = Enabled
```

### 2. Password Policy
```
Computer Configuration → Windows Settings → Security Settings → Account Policies → Password Policy
- Password must meet complexity requirements = Enabled
- Minimum password length = 14 characters
- Maximum password age = 60 days
- Enforce password history = 24 passwords
```

### 3. Account Lockout Policy
```
Computer Configuration → Windows Settings → Security Settings → Account Policies → Account Lockout Policy
- Account lockout threshold = 5 invalid logon attempts
- Account lockout duration = 30 minutes
- Reset account lockout counter after = 30 minutes
```

### 4. Audit Policies
```
Computer Configuration → Windows Settings → Security Settings → Advanced Audit Policy Configuration
Enable auditing for:
- Account Logon
- Account Management
- Logon/Logoff
- Object Access
- Policy Change
- Privilege Use
- System
```

### 5. Windows Firewall
```
Computer Configuration → Windows Settings → Security Settings → Windows Defender Firewall
- Domain Profile: On
- Private Profile: On
- Public Profile: On
- Block all incoming connections when on public networks = Yes
```

## BitLocker Configuration
```powershell
# Enable BitLocker via GPO
Computer Configuration → Administrative Templates → Windows Components → BitLocker Drive Encryption

Settings:
- Require additional authentication at startup = Enabled
- Allow BitLocker without compatible TPM = Disabled
- Configure TPM startup PIN = Require startup PIN with TPM
```

## Credential Guard
```powershell
# Enable via Registry (requires UEFI and TPM)
reg add "HKLM\\System\\CurrentControlSet\\Control\\Lsa" /v LsaCfgFlags /t REG_DWORD /d 1 /f

# Or via Group Policy
Computer Configuration → Administrative Templates → System → Device Guard
- Turn On Virtualization Based Security = Enabled
- Credential Guard Configuration = Enabled with UEFI lock
```

## Application Control

### Windows Defender Application Control
```powershell
# Create default policy
New-CIPolicy -Level Publisher -FilePath C:\\WDAC\\Policy.xml -UserPEs

# Convert to binary
ConvertFrom-CIPolicy C:\\WDAC\\Policy.xml C:\\WDAC\\Policy.bin

# Deploy via GPO
Copy-Item C:\\WDAC\\Policy.bin C:\\Windows\\System32\\CodeIntegrity\\SIPolicy.p7b
```

## Attack Surface Reduction Rules

### Enable ASR Rules via GPO
```
Computer Configuration → Administrative Templates → Windows Components → Microsoft Defender Antivirus → Microsoft Defender Exploit Guard → Attack Surface Reduction

Recommended Rules (set to Block):
- Block executable content from email client and webmail
- Block all Office applications from creating child processes
- Block Office applications from creating executable content
- Block Office applications from injecting code into other processes
- Block JavaScript or VBScript from launching downloaded executable content
```

### PowerShell Configuration
```powershell
# Configure via GPO
Computer Configuration → Administrative Templates → Windows Components → Windows PowerShell
- Turn on PowerShell Script Block Logging = Enabled
- Turn on PowerShell Transcription = Enabled
- Turn on Module Logging = Enabled
```

## Microsoft Defender Settings

### Real-time Protection
```powershell
# Via PowerShell
Set-MpPreference -DisableRealtimeMonitoring $false
Set-MpPreference -DisableBehaviorMonitoring $false
Set-MpPreference -DisableIOAVProtection $false
Set-MpPreference -DisableScriptScanning $false

# Cloud-delivered protection
Set-MpPreference -MAPSReporting Advanced
Set-MpPreference -SubmitSamplesConsent SendAllSamples
```

## Network Security

### SMBv1 Disable
```powershell
# Disable SMBv1
Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol

# Verify
Get-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
```

### Disable LLMNR
```
Computer Configuration → Administrative Templates → Network → DNS Client
- Turn off multicast name resolution = Enabled
```

### Disable NetBIOS
```powershell
# Via WMI
$adapters = Get-WmiObject Win32_NetworkAdapterConfiguration -Filter "IPEnabled=True"
foreach ($adapter in $adapters) {
    $adapter.SetTcpipNetbios(2)  # 2 = Disable NetBIOS over TCP/IP
}
```

## Verify Baseline Compliance

### Using PowerShell
```powershell
# Check security settings
secedit /export /cfg C:\\secpol.cfg
Get-Content C:\\secpol.cfg

# Audit Group Policy settings
gpresult /h C:\\gpreport.html
```

### Using Microsoft Security Compliance Toolkit
1. Run PolicyAnalyzer.exe
2. Compare current settings against baseline
3. Generate compliance report

## Testing Baseline

### Test in Phases
1. **Pilot Group**: Test on 10-20 machines
2. **Monitor**: 2 weeks for issues
3. **Staged Rollout**: Deploy to 25% → 50% → 100%
4. **Document Exceptions**: Track any needed exceptions

### Common Issues
- Application compatibility
- Older hardware lacking TPM 2.0
- Legacy software requiring admin rights
- Custom applications blocked by AppLocker

## Maintenance

### Regular Tasks
- Review security logs weekly
- Update baseline quarterly
- Test new updates in lab
- Document all exceptions
- Annual baseline review

### Update Baseline
```powershell
# Check for new baseline versions
# Download and test in lab environment
# Document changes
# Deploy via GPO update
```

## Compliance Reporting

### Generate Compliance Report
```powershell
# Export security configuration
secedit /export /cfg C:\\CurrentConfig.inf /areas SECURITYPOLICY

# Compare against baseline
# Document deviations
# Generate remediation plan
```

## Quick Reference

### Critical Settings Checklist
- [ ] SMBv1 disabled
- [ ] BitLocker enabled
- [ ] Windows Firewall on all profiles
- [ ] Password complexity enabled
- [ ] Account lockout configured
- [ ] Audit logging enabled
- [ ] Credential Guard enabled (if hardware supports)
- [ ] ASR rules configured
- [ ] PowerShell logging enabled
- [ ] Microsoft Defender real-time protection on

## Resources
- Microsoft Security Compliance Toolkit
- CIS Benchmarks for Windows
- DISA STIGs
- NIST Cybersecurity Framework
'''
                },
            ],

            'Backup & Recovery': [
                {
                    'title': 'Create and Test Windows System Image Backup',
                    'body': '''# Create and Test Windows System Image Backup

## Create System Image Using Windows Backup

### Via Control Panel
1. Open Control Panel → System and Security → Backup and Restore (Windows 7)
2. Click "Create a system image"
3. Select backup destination:
   - External hard drive (recommended)
   - Network location
   - DVD (not recommended for large systems)
4. Select drives to include
5. Click "Start backup"

### Via PowerShell (Windows Server)
```powershell
# Create system image using Windows Server Backup
wbadmin start backup -backupTarget:E: -include:C: -allCritical -quiet
```

## Create System Image Using Third-Party Tools

### Using Veeam Agent for Windows (Free)
```powershell
# Install Veeam Agent
# Configure backup job
# Run backup:
"C:\\Program Files\\Veeam\\Endpoint Backup\\Veeam.Endpoint.Manager.exe" start -job "System Backup"
```

## Create Recovery Drive

### Windows Recovery Drive
1. Search for "Create a recovery drive"
2. Check "Back up system files to the recovery drive"
3. Select USB drive (minimum 16GB)
4. Click "Create"

### Create Bootable Windows USB
```powershell
# Download Windows Media Creation Tool
# Or use Rufus for more control
# Create bootable USB with Windows 10/11 ISO
```

## Backup Critical Data

### User Data Backup Script
```powershell
# Backup user data to network share
$Source = "C:\\Users\\$env:USERNAME"
$Destination = "\\\\server\\backups\\$env:COMPUTERNAME\\$env:USERNAME"
$Exclude = @("AppData", "Downloads", "Temp")

robocopy $Source $Destination /MIR /R:3 /W:5 /MT:8 /XD $Exclude /LOG:C:\\backup.log
```

### Backup Registry
```cmd
reg export HKLM C:\\Backups\\HKLM.reg
reg export HKCU C:\\Backups\\HKCU.reg
```

### Backup Drivers
```powershell
# Export installed drivers
Export-WindowsDriver -Online -Destination C:\\Backups\\Drivers

# Or using DISM
dism /online /export-driver /destination:C:\\Backups\\Drivers
```

## Test System Recovery

### Test Restore to Virtual Machine
1. Create VM in Hyper-V or VMware
2. Boot from recovery media
3. Restore system image
4. Verify functionality

### Document Recovery Time
```
Backup Size: ___ GB
Recovery Time: ___ minutes
Network Speed: ___ Mbps
Storage Type: SSD / HDD / Network
```

## Automated Backup Script

### PowerShell Backup Script
```powershell
<#
.SYNOPSIS
Automated system backup script with notification
#>

param(
    [string]$BackupPath = "\\\\server\\backups\\$env:COMPUTERNAME",
    [string]$EmailTo = "admin@company.com"
)

# Create backup folder
$BackupFolder = Join-Path $BackupPath (Get-Date -Format "yyyy-MM-dd")
New-Item -ItemType Directory -Path $BackupFolder -Force | Out-Null

# Backup system state (Windows Server)
if ((Get-WmiObject Win32_OperatingSystem).ProductType -gt 1) {
    wbadmin start systemstatebackup -backupTarget:$BackupFolder -quiet
    $BackupStatus = $LASTEXITCODE
} else {
    # For workstations, use wbadmin or third-party tool
    wbadmin start backup -backupTarget:$BackupFolder -include:C: -allCritical -quiet
    $BackupStatus = $LASTEXITCODE
}

# Backup critical data
$DataBackup = @{
    "Users" = "C:\\Users"
    "ProgramData" = "C:\\ProgramData"
    "Drivers" = "C:\\Drivers"
}

foreach ($folder in $DataBackup.GetEnumerator()) {
    $dest = Join-Path $BackupFolder $folder.Key
    robocopy $folder.Value $dest /MIR /R:3 /W:5 /MT:8 /LOG+:"$BackupFolder\\robocopy.log"
}

# Verify backup
$BackupFiles = Get-ChildItem $BackupFolder -Recurse
$BackupSizeGB = [math]::Round(($BackupFiles | Measure-Object -Property Length -Sum).Sum / 1GB, 2)

# Log results
$LogMessage = @"
Backup completed on $(Get-Date)
Computer: $env:COMPUTERNAME
Backup Location: $BackupFolder
Backup Size: $BackupSizeGB GB
Status: $(if($BackupStatus -eq 0){'Success'}else{'Failed'})
File Count: $($BackupFiles.Count)
"@

Add-Content -Path "$BackupFolder\\backup.log" -Value $LogMessage

# Send email notification
if ($EmailTo) {
    Send-MailMessage `
        -To $EmailTo `
        -From "backup@company.com" `
        -Subject "Backup Report - $env:COMPUTERNAME" `
        -Body $LogMessage `
        -SmtpServer "smtp.company.com"
}

Write-Host $LogMessage
exit $BackupStatus
```

### Schedule Backup Task
```powershell
# Create scheduled task for daily backup
$Action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\\Scripts\\Backup.ps1"
$Trigger = New-ScheduledTaskTrigger -Daily -At 2:00AM
$Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName "Daily System Backup" -Action $Action -Trigger $Trigger -Principal $Principal -Description "Automated daily system backup"
```

## Restore System from Backup

### Restore from System Image
1. Boot from recovery drive or Windows installation media
2. Select "Repair your computer"
3. Choose "Troubleshoot" → "System Image Recovery"
4. Select system image
5. Follow wizard to restore

### Restore Individual Files
```powershell
# Mount backup VHD
Mount-VHD -Path "\\\\server\\backups\\SystemImage.vhd"

# Copy needed files
Copy-Item E:\\Users\\Documents\\* C:\\Recovery\\Documents -Recurse

# Dismount
Dismount-VHD -Path "\\\\server\\backups\\SystemImage.vhd"
```

## Backup Best Practices

### 3-2-1 Rule
- **3** copies of data
- **2** different media types
- **1** copy off-site

### Retention Policy Example
- Daily backups: Keep 7 days
- Weekly backups: Keep 4 weeks
- Monthly backups: Keep 12 months
- Yearly backups: Keep 7 years (compliance)

### Verification
```powershell
# Monthly backup verification script
$BackupPath = "\\\\server\\backups"
$TestFile = Join-Path $BackupPath "test-restore-$(Get-Date -Format 'yyyyMMdd').txt"

# Create test file
"Backup verification test" | Out-File $TestFile

# Verify it exists
if (Test-Path $TestFile) {
    Write-Host "✓ Backup path accessible" -ForegroundColor Green
} else {
    Write-Host "✗ Backup path not accessible" -ForegroundColor Red
}

# Test restoration quarterly
# Document RTO (Recovery Time Objective)
# Document RPO (Recovery Point Objective)
```

## Quick Reference

### Pre-Backup Checklist
- [ ] Verify backup destination has space
- [ ] Test backup destination connectivity
- [ ] Close open files
- [ ] Disable antivirus temporarily (if needed)
- [ ] Document what is being backed up

### Post-Backup Checklist
- [ ] Verify backup completed successfully
- [ ] Check backup size is reasonable
- [ ] Test random file restore
- [ ] Update backup log
- [ ] Verify backup is encrypted (if required)

## Disaster Recovery Plan

### Critical Information to Document
1. Backup location and credentials
2. Recovery media location
3. Step-by-step restore procedure
4. Contact information for support
5. Encryption keys (stored securely)
6. License keys for software
7. Network configuration details

### Recovery Time Objectives
| System Type | RTO Target |
|------------|-----------|
| Domain Controller | 4 hours |
| File Server | 8 hours |
| Workstation | 24 hours |
| Non-critical systems | 48 hours |
'''
                },
            ],

            'Common Issues': [
                {
                    'title': 'Fix: Windows 10/11 Start Menu Not Working',
                    'body': '''# Fix: Windows 10/11 Start Menu Not Working

## Quick Fixes

### Method 1: Restart Windows Explorer
1. Press `Ctrl + Shift + Esc` to open Task Manager
2. Find "Windows Explorer"
3. Right-click → Restart

Or via Command Prompt:
```cmd
taskkill /f /im explorer.exe
start explorer.exe
```

### Method 2: Run SFC and DISM
```cmd
# Run as Administrator

# System File Checker
sfc /scannow

# DISM repair
DISM /Online /Cleanup-Image /RestoreHealth

# Reboot after completion
shutdown /r /t 0
```

### Method 3: Re-register Start Menu Apps
```powershell
# Run as Administrator in PowerShell
Get-AppxPackage -AllUsers | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppXManifest.xml"}
```

### Method 4: Restart Start Menu Service
```powershell
# PowerShell as Administrator
Get-Service -Name "StartMenuExperienceHost" | Restart-Service
```

## Advanced Solutions

### Rebuild Start Menu Database
```powershell
# PowerShell as Administrator

# Stop Start Menu process
taskkill /f /im StartMenuExperienceHost.exe

# Navigate to Start Menu data folder
cd $env:LOCALAPPDATA\\Packages\\Microsoft.Windows.StartMenuExperienceHost_cw5n1h2txyewy

# Backup current data
mkdir C:\\StartMenuBackup
Copy-Item -Path .\\* -Destination C:\\StartMenuBackup -Recurse

# Delete TileDataLayer folder
Remove-Item .\\TileDataLayer -Recurse -Force

# Restart explorer
taskkill /f /im explorer.exe
start explorer.exe
```

### Create New User Profile (if issue persists)
```powershell
# Export current user's data first
$OldProfile = "C:\\Users\\<username>"
$Backup = "C:\\ProfileBackup"

# Create backup folder
New-Item -ItemType Directory -Path $Backup

# Backup important folders
robocopy "$OldProfile\\Desktop" "$Backup\\Desktop" /E
robocopy "$OldProfile\\Documents" "$Backup\\Documents" /E
robocopy "$OldProfile\\Downloads" "$Backup\\Downloads" /E

# Create new user via Settings → Accounts → Family & other users
# Login with new account
# Restore files from backup
```

### Reset Start Menu Layout
```powershell
# Delete Start Menu layout
Remove-Item "$env:LOCALAPPDATA\\Microsoft\\Windows\\Shell\\LayoutModification.xml" -Force

# Import default layout
Import-StartLayout -LayoutPath C:\\Windows\\StartMenuLayout.xml -MountPath C:\\

# Restart
Restart-Computer
```

## Fix Specific Start Menu Issues

### Start Menu Opens but Apps Don't Launch
```powershell
# Re-register Store and apps
Get-AppXPackage -AllUsers -Name Microsoft.WindowsStore | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppXManifest.xml"}

# Reset Windows Store cache
wsreset.exe
```

### Cortana/Search Not Working in Start Menu
```powershell
# Reset Cortana
Get-AppxPackage -allusers Microsoft.Windows.Cortana | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppXManifest.xml"}

# Restart Search service
Restart-Service -Name "WSearch" -Force
```

### Start Menu Appears Off-Screen
```cmd
# Reset shell settings
reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StuckRects3" /f
reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\MMStuckRects3" /f

# Restart explorer
taskkill /f /im explorer.exe
start explorer.exe
```

## Preventive Measures

### Disable Automatic Updates Temporarily
If issue started after update:
```powershell
# Pause updates for 7 days
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" -Name "NoAutoUpdate" -Value 1

# Or via Settings → Windows Update → Pause updates
```

### Check for Problematic Updates
```powershell
# View recent updates
Get-HotFix | Sort-Object -Property InstalledOn -Descending | Select-Object -First 10

# Uninstall problematic update
wusa /uninstall /kb:xxxxxxx
```

### Create System Restore Point
```powershell
# Before making changes
Enable-ComputerRestore -Drive "C:\\"
Checkpoint-Computer -Description "Before Start Menu Fix" -RestorePointType "MODIFY_SETTINGS"
```

## Troubleshooting Steps

### Check Event Viewer
```
Event Viewer → Windows Logs → Application
Look for errors from:
- ShellExperienceHost
- StartMenuExperienceHost
- Microsoft-Windows-Shell-Core
```

### Check User Profile Status
```powershell
# Verify profile loaded correctly
Get-WmiObject -Class Win32_UserProfile | Where-Object {$_.Special -eq $false} | Select-Object LocalPath, Loaded, LastUseTime
```

### Test in Clean Boot
```
1. msconfig
2. Services tab → Hide all Microsoft services → Disable all
3. Startup tab → Open Task Manager → Disable all
4. Restart
5. Test Start Menu
6. If works, enable services one by one to find culprit
```

## Known Issues and Workarounds

### After Windows 11 Update
- Clear Windows Update cache
- Reset Start Menu via PowerShell (Method 3 above)
- Check for additional Windows updates

### Third-Party Software Conflicts
Common conflicting software:
- Classic Shell / Open Shell
- Start10 / Start11
- Older versions of antivirus software
- Display driver issues

### Hardware Acceleration Issues
```
Settings → System → Display → Graphics → Change default graphics settings
Turn off "Hardware-accelerated GPU scheduling"
```

## Alternative Solutions

### Use Classic Start Menu
If issues persist, consider:
- Open-Shell (free, open source)
- Start11 by Stardock
- StartIsBack++

### Use PowerToys Run (Microsoft official)
- Install PowerToys
- Enable PowerToys Run (`Alt + Space`)
- Provides search and app launching

## Recovery Options

### Safe Mode
If Start Menu still doesn't work:
```
1. Hold Shift while clicking Restart
2. Troubleshoot → Advanced options → Startup Settings → Restart
3. Press 4 for Safe Mode
4. Apply fixes in Safe Mode
```

### In-Place Upgrade
Last resort - repairs Windows without losing data:
```
1. Download Windows 10/11 Media Creation Tool
2. Run setup from within Windows
3. Choose "Keep personal files and apps"
4. Complete upgrade process
```

## Quick Diagnostic Script
```powershell
# Run as Administrator
Write-Host "Checking Start Menu components..." -ForegroundColor Yellow

# Check services
$services = @("StartMenuExperienceHost", "WSearch", "BITS")
foreach ($svc in $services) {
    $status = (Get-Service -Name $svc -ErrorAction SilentlyContinue).Status
    if ($status -eq "Running") {
        Write-Host "✓ $svc is running" -ForegroundColor Green
    } else {
        Write-Host "✗ $svc is not running" -ForegroundColor Red
    }
}

# Check AppX packages
$packages = @("Microsoft.Windows.ShellExperienceHost", "Microsoft.Windows.StartMenuExperienceHost")
foreach ($pkg in $packages) {
    $exists = Get-AppxPackage -Name $pkg -ErrorAction SilentlyContinue
    if ($exists) {
        Write-Host "✓ $pkg is installed" -ForegroundColor Green
    } else {
        Write-Host "✗ $pkg is missing" -ForegroundColor Red
    }
}

# Check recent errors
$errors = Get-WinEvent -FilterHashtable @{LogName='Application'; Level=2; StartTime=(Get-Date).AddHours(-24)} |
    Where-Object {$_.ProviderName -like "*Shell*"} |
    Select-Object -First 5

if ($errors) {
    Write-Host "`nRecent Shell-related errors:" -ForegroundColor Yellow
    $errors | Format-Table TimeCreated, Message -AutoSize
}
```

## Prevention
- Keep Windows updated
- Regular system maintenance
- Create restore points before major changes
- Monitor Event Viewer for warnings
- Avoid modifying registry without backup
'''
                },
                {
                    'title': 'Outlook Won\'t Open or Keeps Crashing - Fix',
                    'body': '''# Outlook Won't Open or Keeps Crashing - Fix

## Quick Fixes

### Method 1: Start Outlook in Safe Mode
```cmd
# Windows + R, then type:
outlook.exe /safe

# If Outlook starts successfully, issue is likely an add-in
```

### Method 2: Disable Add-ins
```
1. File → Options → Add-ins
2. At bottom, select "COM Add-ins" → Go
3. Uncheck all add-ins
4. Click OK and restart Outlook
5. Re-enable add-ins one by one to find culprit
```

### Method 3: Repair Office Installation
```
Control Panel → Programs and Features → Microsoft Office
Right-click → Change → Quick Repair (or Online Repair if Quick fails)
```

### Method 4: Create New Outlook Profile
```cmd
# Open Mail settings
control mlcfg32.cpl

# Click "Show Profiles" → "Add"
# Create new profile
# Set as default profile
```

## Advanced Solutions

### Repair OST/PST Files

#### Repair OST File
```cmd
# Close Outlook
# Delete OST file (it will rebuild):
del "%LOCALAPPDATA%\\Microsoft\\Outlook\\*.ost"

# Restart Outlook - it will rebuild OST
```

#### Repair PST File Using ScanPST
```
# Locate ScanPST.exe:
# Office 2016/2019/365: C:\\Program Files\\Microsoft Office\\root\\Office16\\SCANPST.EXE
# Office 2013: C:\\Program Files\\Microsoft Office\\Office15\\SCANPST.EXE

# Run ScanPST.exe
# Browse to your PST file location (usually in Documents\\Outlook Files)
# Click "Start" to scan
# If errors found, click "Repair"
```

### Clear Outlook Cache

#### Clear Autocomplete Cache
```
File → Options → Mail → Empty Auto-Complete List
```

#### Clear Forms Cache
```cmd
# Close Outlook
# Delete forms cache:
del "%LOCALAPPDATA%\\Microsoft\\Forms\\*.*" /q

# Delete temporary Outlook files:
del "%TEMP%\\Outlook*" /q /s
```

### Reset Outlook Navigation Pane
```cmd
# Close Outlook
outlook.exe /resetnavpane
```

### Reset Outlook Folders
```cmd
# Close Outlook
outlook.exe /resetfolders
```

### Clear Recent Items
```cmd
# Close Outlook
outlook.exe /cleanclientrules
outlook.exe /cleanreminders
outlook.exe /cleanviews
```

## Fix Specific Issues

### Outlook Freezes When Opening
```powershell
# Disable hardware graphics acceleration
# File → Options → Advanced → Display
# Check "Disable hardware graphics acceleration"
```

### Outlook Search Not Working
```cmd
# Rebuild search index
# Control Panel → Indexing Options → Advanced → Rebuild

# Or via Registry:
reg add "HKCU\\Software\\Microsoft\\Office\\16.0\\Outlook\\Search" /v "DisableSearchBox" /t REG_DWORD /d 0 /f
```

### Profile Loading Issue
```cmd
# Reset default profile
reg add "HKCU\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Windows Messaging Subsystem\\Profiles" /v "DefaultProfile" /t REG_SZ /d "" /f
```

### Outlook Won't Send/Receive
```
1. File → Account Settings → Account Settings
2. Select account → Change
3. More Settings → Advanced
4. Test Account Settings
5. Check "Root Folder Path" settings
6. Verify ports: SMTP (587 or 465), POP3 (995), IMAP (993)
```

## Clean Boot and Test

### Perform Clean Boot
```
1. msconfig
2. Services → Hide Microsoft services → Disable all
3. Startup → Open Task Manager → Disable all
4. Restart
5. Test Outlook
```

If Outlook works in clean boot, one of the disabled services/apps is causing conflict.

## Registry Fixes

### Delete Outlook Registry Key (Caution!)
```cmd
# This resets all Outlook settings
# Backup registry first!
reg export "HKCU\\Software\\Microsoft\\Office\\16.0\\Outlook" C:\\OutlookBackup.reg

# Delete Outlook key
reg delete "HKCU\\Software\\Microsoft\\Office\\16.0\\Outlook" /f

# Restart Outlook
```

### Fix Slow Startup
```cmd
# Disable RSS feeds
reg add "HKCU\\Software\\Microsoft\\Office\\16.0\\Outlook\\Options\\Rss" /v DisableRSS /t REG_DWORD /d 1 /f

# Disable Weather Bar
reg add "HKCU\\Software\\Microsoft\\Office\\16.0\\Outlook\\Options\\Calendar" /v DisableWeatherBar /t REG_DWORD /d 1 /f
```

## Check Event Viewer
```
Event Viewer → Windows Logs → Application
Filter for Source: Outlook
Look for errors around crash time
```

## Common Error Codes

### Error 0x800CCC0F
**Cause**: Connection with server interrupted
**Fix**:
- Check internet connection
- Verify firewall settings
- Test account settings

### Error 0x800CCC0E
**Cause**: Unable to connect to server
**Fix**:
- Verify server settings
- Check antivirus/firewall
- Test with VPN disabled

### Error 0x8004010F
**Cause**: Cannot access Outlook data file
**Fix**:
- Run ScanPST on PST/OST file
- Check file permissions
- Ensure file isn't on network drive

### Error 0x80040600
**Cause**: Unknown error
**Fix**:
- Run Inbox Repair Tool (ScanPST)
- Create new Outlook profile

## Diagnostic Tools

### Enable Outlook Logging
```
1. File → Options → Advanced → Other
2. Check "Enable troubleshooting logging"
3. Restart Outlook
4. Reproduce issue
5. Check log: %TEMP%\\Outlook Logging\\
```

### Collect Diagnostics
```powershell
# Run as Administrator
$DiagPath = "C:\\OutlookDiag"
New-Item -ItemType Directory -Path $DiagPath -Force

# Export Outlook version
Get-WmiObject -Query "SELECT * FROM Win32_Product WHERE Name LIKE '%Microsoft Office%'" |
    Select-Object Name, Version |
    Out-File "$DiagPath\\OfficeVersion.txt"

# Copy Outlook logs
Copy-Item "$env:TEMP\\Outlook Logging\\*" $DiagPath -Recurse -ErrorAction SilentlyContinue

# Copy event logs
wevtutil epl Application "$DiagPath\\Application.evtx" "/q:*[System[Provider[@Name='Outlook']]]"

# List add-ins
reg query "HKCU\\Software\\Microsoft\\Office\\Outlook\\Addins" > "$DiagPath\\AddIns.txt"

Write-Host "Diagnostics collected in $DiagPath"
```

## Prevention

### Regular Maintenance
```cmd
# Schedule weekly

# 1. Compact PST file
# File → Account Settings → Data Files → Settings → Compact Now

# 2. Archive old emails
# File → Cleanup Tools → Archive

# 3. Empty Deleted Items
# Right-click Deleted Items → Empty Folder

# 4. Disable unnecessary add-ins

# 5. Keep Outlook updated
```

### Best Practices
- Keep PST files under 25GB
- Archive emails older than 1 year
- Don't store PST on network drive
- Regular backups of PST/OST files
- Keep Outlook and Windows updated
- Use cached mode for better performance

## Last Resort Options

### Reinstall Office
```powershell
# Uninstall Office
# Download Office Deployment Tool
# Reinstall with configuration

# Backup PST files first!
Copy-Item "$env:USERPROFILE\\Documents\\Outlook Files\\*" "C:\\BackupPST\\" -Recurse
```

### Use Office Removal Tool
- Download Microsoft Support and Recovery Assistant
- Run "Outlook" diagnostic
- Follow automated fixes

### Check Office Activation
```
File → Account
If not activated, click "Activate Product"
```

## Quick Diagnostic Checklist
- [ ] Can start in Safe Mode?
- [ ] Issue with specific profile only?
- [ ] Recent Office/Windows updates?
- [ ] Free disk space available?
- [ ] PST/OST file size under 50GB?
- [ ] Antivirus scanning Outlook folders?
- [ ] Add-ins enabled?
- [ ] Network connectivity OK?
- [ ] Tried different profile?
- [ ] Run ScanPST on PST files?

## Support Resources
- Microsoft Support and Recovery Assistant
- Office Support community forums
- Check Office 365 Service Health Dashboard
- Open support ticket with Microsoft
'''
                },
            ],

            'Hardware Setup': [
                {
                    'title': 'New Computer Setup Checklist - Complete Guide',
                    'body': '''# New Computer Setup Checklist - Complete Guide

## Pre-Setup Preparation

### Document Information
```
Computer Details:
- Manufacturer: _____________
- Model: _____________
- Serial Number: _____________
- Asset Tag: _____________
- Purchase Date: _____________
- Warranty Expiration: _____________

User Information:
- Name: _____________
- Department: _____________
- Email: _____________
- Phone Extension: _____________
```

### Gather Required Information
- [ ] Computer name convention
- [ ] Domain credentials
- [ ] User's Active Directory username
- [ ] Software license keys
- [ ] Network configuration (if static IP needed)
- [ ] Email configuration details
- [ ] VPN credentials
- [ ] Shared drive mappings

## Initial Setup (30-45 minutes)

### 1. Unbox and Physical Setup
- [ ] Remove from packaging
- [ ] Check for physical damage
- [ ] Note serial numbers (computer, monitor, peripherals)
- [ ] Connect power, monitor, keyboard, mouse
- [ ] Connect network cable (Ethernet recommended for setup)

### 2. BIOS/UEFI Configuration
```
1. Power on and press Del/F2/F10 (varies by manufacturer)
2. Set boot order (HDD/SSD first, then USB)
3. Enable TPM 2.0 (for BitLocker)
4. Enable Secure Boot
5. Enable Virtualization (if applicable)
6. Set system date/time
7. Save and exit
```

### 3. Windows Setup
```
1. Power on computer
2. Select region and keyboard layout
3. Connect to network
4. Sign in with Microsoft account or create local account
5. Privacy settings (review and configure)
6. Skip OneDrive setup (configure later)
7. Allow Windows to complete setup
```

## Operating System Configuration (30 minutes)

### 4. Windows Updates
```powershell
# Run Windows Update
# Settings → Windows Update → Check for updates
# Install all updates
# Restart as needed
# Repeat until no more updates available

# Or via PowerShell:
Install-Module PSWindowsUpdate
Get-WindowsUpdate
Install-WindowsUpdate -AcceptAll -AutoReboot
```

### 5. Computer Name and Domain Join
```powershell
# Rename computer
Rename-Computer -NewName "WS-IT-001"

# Join domain
Add-Computer -DomainName "company.local" -Credential (Get-Credential) -Restart

# Or manually:
# Settings → System → About → Rename this PC (advanced)
# Computer Name tab → Change → Domain
```

### 6. Activate Windows
```cmd
# Check activation status
slmgr /xpr

# If not activated
slmgr /ipk XXXXX-XXXXX-XXXXX-XXXXX-XXXXX
slmgr /ato
```

### 7. Configure Windows Settings
```
Settings to configure:
- Display resolution (recommended settings)
- Power settings (never sleep during work hours)
- Windows Update (configure active hours)
- Privacy settings (disable telemetry if policy requires)
- Default apps (browser, email client, PDF reader)
```

## Driver Installation (20 minutes)

### 8. Install Drivers
```
Priority Order:
1. Chipset drivers
2. Network drivers (if not already installed)
3. Graphics drivers (from manufacturer, not Windows Update)
4. Audio drivers
5. Peripheral drivers (printer, scanner, etc.)
6. Other hardware-specific drivers
```

### Check Drivers via PowerShell
```powershell
# Check for missing drivers
Get-WmiObject Win32_PnPEntity | Where-Object {$_.ConfigManagerErrorCode -ne 0} |
    Select-Object Name, DeviceID, ConfigManagerErrorCode

# Export installed drivers (for backup)
Export-WindowsDriver -Online -Destination "C:\\DriverBackup"
```

## Software Installation (60 minutes)

### 9. Essential Software Baseline
```
Priority 1 - Security:
- [ ] Antivirus/EDR software
- [ ] VPN client
- [ ] Password manager

Priority 2 - Productivity:
- [ ] Microsoft Office 365
- [ ] Web browsers (Chrome, Firefox, Edge)
- [ ] Adobe Acrobat Reader
- [ ] PDF printer (if not using built-in)

Priority 3 - Communication:
- [ ] Microsoft Teams
- [ ] Zoom (if applicable)
- [ ] Email client configuration

Priority 4 - Line of Business Apps:
- [ ] Industry-specific software
- [ ] Database clients
- [ ] Remote access tools
```

### 10. Office 365 Installation
```powershell
# Download and run Office Deployment Tool
# Or install from office.com
# Sign in with user's credentials
# Activate and update
```

### 11. Browser Configuration
```
Google Chrome:
- Set homepage
- Import bookmarks
- Install extensions (AdBlock, Password Manager)
- Set as default (if applicable)

Microsoft Edge:
- Configure sync
- Set search engine
- Import favorites
- Configure security settings
```

## Security Configuration (30 minutes)

### 12. Enable BitLocker
```powershell
# Check TPM status
Get-Tpm

# Enable BitLocker
Enable-BitLocker -MountPoint "C:" -EncryptionMethod XtsAes256 -UsedSpaceOnly -TpmProtector

# Backup recovery key to AD
Backup-BitLockerKeyProtector -MountPoint "C:" -KeyProtectorId (Get-BitLockerVolume -MountPoint "C:").KeyProtector[0].KeyProtectorId
```

### 13. Configure Windows Defender
```powershell
# Update definitions
Update-MpSignature

# Enable real-time protection
Set-MpPreference -DisableRealtimeMonitoring $false

# Configure scan schedule
Set-MpPreference -ScanScheduleDay 0 -ScanScheduleTime 120
```

### 14. Configure Windows Firewall
```powershell
# Ensure firewall is enabled
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True

# Allow Remote Desktop (if needed)
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
```

### 15. Create Local Admin Account (Break Glass)
```powershell
# Create local admin account for emergencies
$Password = Read-Host -AsSecureString "Enter admin password"
New-LocalUser -Name "LocalAdmin" -Password $Password -Description "Emergency admin account"
Add-LocalGroupMember -Group "Administrators" -Member "LocalAdmin"

# Document password securely
```

## Network Configuration (15 minutes)

### 16. Map Network Drives
```cmd
# Map drives via script or GPO
net use H: \\\\server\\home\\%USERNAME% /persistent:yes
net use S: \\\\server\\shared /persistent:yes

# Or via PowerShell
New-PSDrive -Name "H" -PSProvider FileSystem -Root "\\\\server\\home\\$env:USERNAME" -Persist
```

### 17. Configure Default Printer
```powershell
# Add network printer
Add-Printer -ConnectionName "\\\\printserver\\printer01"

# Set as default
$printer = Get-Printer -Name "\\\\printserver\\printer01"
Set-Printer -Name $printer.Name -DefaultPrinter $true
```

### 18. Test Network Connectivity
```cmd
# Test connectivity
ping google.com
ping domain-controller.company.local

# Test DNS
nslookup google.com

# Test file server access
dir \\\\fileserver\\shared
```

## Email Configuration (15 minutes)

### 19. Configure Outlook
```
1. Open Outlook
2. Enter email address
3. Allow auto-configuration (if Exchange/Office 365)
4. Or manually configure:
   - Server: outlook.office365.com
   - Port: 993 (IMAP) or 443 (MAPI)
   - Encryption: SSL/TLS
5. Test send/receive
6. Configure signature
7. Set up mobile sync (if applicable)
```

### 20. Configure Email Rules
```
Common rules to set up:
- Move automated emails to folders
- Flag emails from manager
- Forward certain emails (if applicable)
- Out of office auto-reply template
```

## User-Specific Configuration (20 minutes)

### 21. Desktop Personalization
- [ ] Set desktop wallpaper (corporate or user choice)
- [ ] Configure taskbar layout
- [ ] Pin frequently used applications
- [ ] Configure Start menu layout

### 22. Browser Bookmarks
- [ ] Import bookmarks from old computer
- [ ] Add company intranet links
- [ ] Add frequently accessed web apps
- [ ] Organize in folders

### 23. File Migration
```powershell
# Copy user files from old computer
robocopy \\\\oldcomputer\\C$\\Users\\username\\Desktop C:\\Users\\username\\Desktop /E /R:3 /W:5
robocopy \\\\oldcomputer\\C$\\Users\\username\\Documents C:\\Users\\username\\Documents /E /R:3 /W:5
robocopy \\\\oldcomputer\\C$\\Users\\username\\Downloads C:\\Users\\username\\Downloads /E /R:3 /W:5

# Or use Windows Easy Transfer
# Or OneDrive sync
```

## Final Configuration (20 minutes)

### 24. Power Settings
```powershell
# Set power plan
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c  # High Performance

# Configure sleep settings
powercfg /change monitor-timeout-ac 15
powercfg /change standby-timeout-ac 0  # Never sleep when plugged in
```

### 25. Windows Features
```powershell
# Enable useful features
Enable-WindowsOptionalFeature -Online -FeatureName "TelnetClient"
Enable-WindowsOptionalFeature -Online -FeatureName "TFTP"

# Disable unused features
Disable-WindowsOptionalFeature -Online -FeatureName "WindowsMediaPlayer"
```

### 26. Backup Configuration
```
- [ ] Set up Windows Backup or third-party backup
- [ ] Configure OneDrive backup for Desktop/Documents
- [ ] Verify File History is enabled
- [ ] Document backup schedule
```

## Testing & Verification (15 minutes)

### 27. Functionality Tests
```
- [ ] Internet connectivity working
- [ ] Can access email
- [ ] Network drives accessible
- [ ] Printer printing
- [ ] All required software launches
- [ ] Domain login working
- [ ] VPN connects successfully
- [ ] Shared resources accessible
- [ ] Audio/video working (test Teams call)
```

### 28. Performance Validation
```powershell
# Check system performance
Get-Counter '\\Processor(_Total)\\% Processor Time'
Get-Counter '\\Memory\\Available MBytes'

# Check startup programs
Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location, User

# Optimize startup
# Task Manager → Startup → Disable unnecessary programs
```

## Documentation (10 minutes)

### 29. Complete Asset Documentation
```
Update asset management system with:
- Computer name
- IP address (if static)
- MAC address
- Assigned user
- Location
- Software installed
- License keys used
- Setup date
- Setup technician
```

### 30. Create Quick Reference Sheet
```
Quick Reference for User:
- Computer Name: __________
- Local Admin (emergency): __________  (secured location)
- Help Desk Phone: __________
- Help Desk Email: __________
- VPN Instructions: __________
- Email Setup: __________
- Network Drives: __________
- Common Issues & Fixes: __________
```

## Handoff to User (15 minutes)

### 31. User Training
- [ ] Basic operations (shut down, restart, lock)
- [ ] How to access email
- [ ] How to access shared drives
- [ ] How to print
- [ ] How to connect to VPN
- [ ] How to request IT support
- [ ] Password change procedure
- [ ] Security awareness basics

### 32. Sign-Off
```
User Acknowledgment:
I have received the following equipment in good working order:
- Computer: ________________
- Monitor: ________________
- Keyboard: ________________
- Mouse: ________________
- Other: ________________

I acknowledge responsibility for this equipment and will report any
issues to IT immediately.

User Signature: ________________  Date: ________________
IT Technician: ________________   Date: ________________
```

## Post-Setup Tasks

### 33. Follow-Up (Week 1)
- [ ] Check-in with user after 1 day
- [ ] Verify no issues with setup
- [ ] Address any questions
- [ ] Confirm all software working
- [ ] Verify backup completed successfully

### 34. Monthly Check
- [ ] Verify Windows updates installed
- [ ] Check disk space
- [ ] Review security logs
- [ ] Confirm backup running
- [ ] User satisfaction

## Automated Setup Script

### PowerShell Automation Template
```powershell
<#
.SYNOPSIS
Automated workstation setup script
#>

param(
    [string]$ComputerName,
    [string]$UserName,
    [string]$Domain = "company.local"
)

Write-Host "Starting automated setup for $ComputerName" -ForegroundColor Green

# Install Windows Updates
Write-Host "Installing Windows Updates..."
Install-Module PSWindowsUpdate -Force
Get-WindowsUpdate -AcceptAll -Install -AutoReboot

# Rename computer and join domain
Write-Host "Configuring computer name and domain..."
Rename-Computer -NewName $ComputerName -Force
Add-Computer -DomainName $Domain -Restart

# Install chocolatey for package management
Write-Host "Installing Chocolatey..."
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install software
Write-Host "Installing software packages..."
choco install googlechrome firefox adobereader 7zip -y

# Configure power settings
Write-Host "Configuring power settings..."
powercfg /change monitor-timeout-ac 15
powercfg /change standby-timeout-ac 0

Write-Host "Setup complete!" -ForegroundColor Green
```

## Estimated Total Time
- Basic Setup: 2-3 hours
- With Migration: 3-4 hours
- Complex Setup (specialized software): 4-6 hours

## Common Issues During Setup

### Windows Update Stuck
```cmd
net stop wuauserv
del C:\\Windows\\SoftwareDistribution\\* /Q
net start wuauserv
```

### Cannot Join Domain
```
- Verify DNS settings point to domain controller
- Check network connectivity
- Ensure computer account doesn't already exist in AD
- Verify domain join account has permissions
```

### Driver Issues
```
- Download drivers directly from manufacturer website
- Use Device Manager to update manually
- Check for chipset drivers first
- Install in order: Chipset → Network → Graphics → Other
```
'''
                },
            ],
        }

        return articles.get(category_name, [])
