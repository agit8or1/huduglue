"""
Management command to seed document and diagram templates
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Organization
from docs.models import Document


class Command(BaseCommand):
    help = 'Seed document and diagram templates for organizations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--org-slug',
            type=str,
            help='Organization slug to create templates for (if not provided, creates global templates)'
        )

    def handle(self, *args, **options):
        org_slug = options.get('org_slug')

        if org_slug:
            try:
                organization = Organization.objects.get(slug=org_slug)
                self.stdout.write(f"Creating templates for organization: {organization.name}")
                is_global = False
            except Organization.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Organization with slug '{org_slug}' not found"))
                return
        else:
            # Create global templates (no organization required)
            organization = None
            self.stdout.write("Creating global templates (no organization required)")
            is_global = True

        # Get superuser for created_by field
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            superuser = User.objects.first()

        # Document Templates
        document_templates = [
            {
                'title': 'Server Documentation Template',
                'slug': 'server-documentation-template',
                'body': '''# Server Documentation: [Server Name]

## Overview
- **Server Name**:
- **Purpose**:
- **Environment**: Production / Staging / Development
- **Operating System**:
- **IP Address**:
- **Location**:

## Hardware Specifications
- **CPU**:
- **RAM**:
- **Storage**:
- **Network**:

## Software & Services
### Installed Software
-

### Running Services
| Service | Port | Status | Auto-Start |
|---------|------|--------|------------|
|         |      |        |            |

## Configuration
### Network Configuration
- **Hostname**:
- **DNS**:
- **Gateway**:
- **Subnet Mask**:

### Firewall Rules
| Port | Protocol | Source | Destination | Purpose |
|------|----------|--------|-------------|---------|
|      |          |        |             |         |

## Backup & Recovery
- **Backup Schedule**:
- **Backup Location**:
- **Retention Policy**:
- **Last Backup**:
- **Recovery Time Objective (RTO)**:
- **Recovery Point Objective (RPO)**:

## Monitoring & Alerts
- **Monitoring Tool**:
- **Alert Recipients**:
- **Key Metrics**:
- **Thresholds**:

## Maintenance
### Regular Maintenance Tasks
- **Daily**:
- **Weekly**:
- **Monthly**:
- **Quarterly**:

### Patching Schedule
- **OS Patches**:
- **Application Patches**:
- **Last Patch Date**:

## Access & Security
### Administrators
| Name | Role | Access Level | Contact |
|------|------|--------------|---------|
|      |      |              |         |

### Access Methods
- **SSH**:
- **RDP**:
- **Console**:
- **Web Interface**:

### Security Measures
- [ ] Firewall enabled
- [ ] Antivirus installed
- [ ] Intrusion detection
- [ ] Regular security audits
- [ ] Compliance requirements

## Troubleshooting
### Common Issues
1. **Issue**:
   - **Solution**:

### Log Locations
- **System Logs**:
- **Application Logs**:
- **Error Logs**:

## Emergency Contacts
- **Primary Admin**:
- **Backup Admin**:
- **Vendor Support**:
- **Emergency Escalation**:

## Change Log
| Date | Changed By | Description |
|------|------------|-------------|
|      |            |             |

## Related Documentation
- [Link to network diagram]
- [Link to backup procedures]
- [Link to disaster recovery plan]
''',
                'content_type': 'markdown',
                'is_template': True,
            },
            {
                'title': 'Employee Onboarding Checklist',
                'slug': 'employee-onboarding-checklist',
                'body': '''# Employee Onboarding Checklist

## New Employee Information
- **Name**:
- **Position**:
- **Department**:
- **Start Date**:
- **Manager**:
- **Location**:

## Pre-Arrival (Before Start Date)
- [ ] Create user account in Active Directory
- [ ] Set up email account
- [ ] Request employee ID badge
- [ ] Order workstation/laptop
- [ ] Order monitor(s) and peripherals
- [ ] Request phone extension
- [ ] Request parking pass (if applicable)
- [ ] Prepare desk/workspace

## Day 1
- [ ] Welcome and office tour
- [ ] Provide employee handbook
- [ ] Complete HR paperwork
- [ ] Issue employee ID badge
- [ ] Issue building access card
- [ ] Issue parking pass
- [ ] Set up workstation
- [ ] Install required software
- [ ] Provide login credentials
- [ ] Configure email client
- [ ] Configure VPN access
- [ ] Introduce to team members
- [ ] Schedule orientation meetings

## IT Setup (Day 1-3)
### Hardware
- [ ] Computer/laptop configured
- [ ] Monitor(s) set up
- [ ] Keyboard and mouse
- [ ] Docking station (if applicable)
- [ ] Phone set up
- [ ] Headset provided
- [ ] Mobile device (if required)

### Software & Access
- [ ] Windows/macOS login
- [ ] Email account access
- [ ] Microsoft 365 / Google Workspace
- [ ] VPN access configured
- [ ] Shared drives mapped
- [ ] File sharing permissions
- [ ] CRM access
- [ ] Project management tools
- [ ] Communication tools (Teams/Slack)
- [ ] Time tracking system
- [ ] Expense reporting system
- [ ] Password manager access
- [ ] Two-factor authentication set up

### Security
- [ ] Security awareness training completed
- [ ] Acceptable use policy signed
- [ ] Confidentiality agreement signed
- [ ] Data protection training
- [ ] Password policy explained
- [ ] Social engineering awareness

## Week 1
- [ ] Department overview meeting
- [ ] Review job responsibilities
- [ ] Introduce to key stakeholders
- [ ] Tour of facilities
- [ ] Review company policies
- [ ] Assign initial tasks/projects
- [ ] Schedule regular check-ins
- [ ] Provide training schedule

## Month 1
- [ ] Product/service training
- [ ] Process and procedure training
- [ ] System-specific training
- [ ] Shadow team members
- [ ] Complete compliance training
- [ ] First project assignment
- [ ] 30-day check-in meeting

## Access Verification
| System/Resource | Username | Access Level | Verified |
|-----------------|----------|--------------|----------|
| Active Directory |         |              | [ ]      |
| Email           |         |              | [ ]      |
| VPN             |         |              | [ ]      |
| CRM             |         |              | [ ]      |
| File Shares     |         |              | [ ]      |

## Equipment Issued
| Item | Serial Number | Date Issued | Returned Date |
|------|---------------|-------------|---------------|
|      |               |             |               |

## Training Completed
| Training Topic | Date | Trainer | Status |
|----------------|------|---------|--------|
|                |      |         |        |

## Notes
[Add any special notes or requirements here]

## Sign-Off
- **IT Administrator**: _________________________ Date: _______
- **Manager**: _________________________ Date: _______
- **Employee**: _________________________ Date: _______
''',
                'content_type': 'markdown',
                'is_template': True,
            },
            {
                'title': 'Incident Response Template',
                'slug': 'incident-response-template',
                'body': '''# Incident Response Report

## Incident Overview
- **Incident ID**: [AUTO-GENERATED]
- **Date/Time Reported**:
- **Date/Time Occurred**:
- **Reported By**:
- **Severity**: Critical / High / Medium / Low
- **Status**: Open / In Progress / Resolved / Closed
- **Category**: Security / Network / Hardware / Software / Other

## Incident Description
### Summary
[Brief description of the incident]

### Impact
- **Affected Systems**:
- **Affected Users**:
- **Business Impact**:
- **Data Compromised**: Yes / No / Unknown

## Detection
- **How Detected**: Monitoring / User Report / Automated Alert / Other
- **Detection Tool**:
- **Initial Symptoms**:

## Timeline
| Time | Event | Action Taken | Personnel |
|------|-------|--------------|-----------|
|      |       |              |           |

## Investigation
### Initial Assessment
- **Root Cause**:
- **Attack Vector** (if security incident):
- **Scope of Impact**:

### Evidence Collected
- [ ] System logs
- [ ] Network traffic captures
- [ ] Screenshots
- [ ] Error messages
- [ ] User statements

### Evidence Location
-

## Response Actions
### Immediate Actions
1.
2.
3.

### Containment
- [ ] Isolated affected systems
- [ ] Disabled compromised accounts
- [ ] Blocked malicious traffic
- [ ] Other:

### Eradication
- [ ] Removed malware/threats
- [ ] Closed vulnerabilities
- [ ] Applied patches
- [ ] Other:

### Recovery
- [ ] Restored services
- [ ] Restored data from backups
- [ ] Verified system integrity
- [ ] Tested functionality
- [ ] Monitored for recurrence

## Communication
### Internal Communication
- **Notified**:
- **Method**: Email / Phone / In-Person / Chat
- **Time**:

### External Communication
- **Customers Notified**: Yes / No / N/A
- **Vendors Notified**: Yes / No / N/A
- **Authorities Notified**: Yes / No / N/A
- **Media Statement**: Yes / No / N/A

## Resolution
### Solution Implemented
[Description of final solution]

### Verification
- **Tested By**:
- **Test Results**:
- **Sign-Off**:

## Post-Incident Review
### Lessons Learned
- **What Went Well**:
- **What Could Be Improved**:
- **Surprises**:

### Recommendations
1.
2.
3.

### Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
|        |       |          |        |

## Metrics
- **Time to Detect**:
- **Time to Respond**:
- **Time to Contain**:
- **Time to Recover**:
- **Total Downtime**:
- **Users Affected**:
- **Estimated Cost**:

## Attachments
- [ ] Log files
- [ ] Screenshots
- [ ] Network diagrams
- [ ] Communication logs
- [ ] Forensic reports

## Approvals
- **Incident Manager**: _________________________ Date: _______
- **IT Director**: _________________________ Date: _______
- **CISO** (if security incident): _________________________ Date: _______
''',
                'content_type': 'markdown',
                'is_template': True,
            },
            {
                'title': 'Change Request Template',
                'slug': 'change-request-template',
                'body': '''# Change Request

## Change Information
- **Change ID**: [AUTO-GENERATED]
- **Date Requested**:
- **Requested By**:
- **Change Type**: Standard / Normal / Emergency
- **Category**: Hardware / Software / Network / Security / Other
- **Priority**: Critical / High / Medium / Low
- **Status**: Requested / Approved / Scheduled / In Progress / Completed / Rejected

## Change Description
### Summary
[Brief description of the proposed change]

### Reason for Change
[Why is this change needed?]

### Business Justification
[Business value or need]

## Impact Analysis
### Systems Affected
| System | Component | Impact Level | Downtime Required |
|--------|-----------|--------------|-------------------|
|        |           |              |                   |

### Users Affected
- **Number of Users**:
- **Departments**:
- **VIP Users**: Yes / No

### Services Affected
-

## Risk Assessment
### Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
|      | High/Med/Low | High/Med/Low |       |

### Dependencies
-

## Implementation Plan
### Pre-Implementation Tasks
- [ ] Backup current configuration
- [ ] Verify backup integrity
- [ ] Prepare rollback plan
- [ ] Test in non-production
- [ ] Communicate to stakeholders
- [ ] Schedule maintenance window
- [ ] Other:

### Implementation Steps
1.
2.
3.

### Estimated Duration
- **Preparation Time**:
- **Implementation Time**:
- **Testing Time**:
- **Total Time**:

### Implementation Team
| Name | Role | Responsibilities | Contact |
|------|------|------------------|---------|
|      |      |                  |         |

## Rollback Plan
### Rollback Trigger Conditions
-

### Rollback Steps
1.
2.
3.

### Rollback Time Estimate
-

## Testing Plan
### Test Cases
| Test Case | Expected Result | Actual Result | Pass/Fail |
|-----------|-----------------|---------------|-----------|
|           |                 |               |           |

### Verification Steps
- [ ] Functionality verified
- [ ] Performance acceptable
- [ ] No errors in logs
- [ ] User acceptance testing
- [ ] Other:

## Schedule
- **Proposed Start Date/Time**:
- **Proposed End Date/Time**:
- **Actual Start Date/Time**:
- **Actual End Date/Time**:

## Communication Plan
### Notification Schedule
- **Advance Notice**:
- **Reminder**:
- **Start Notification**:
- **Completion Notification**:

### Stakeholders to Notify
| Stakeholder | Method | Before | During | After |
|-------------|--------|--------|--------|-------|
|             |        | [ ]    | [ ]    | [ ]   |

## Cost Analysis
- **Labor Cost**:
- **Materials/Software**:
- **Third-Party Services**:
- **Total Cost**:

## Approvals
### Required Approvals
- [ ] IT Manager - _________________________ Date: _______
- [ ] Department Head - _________________________ Date: _______
- [ ] Change Advisory Board - _________________________ Date: _______
- [ ] CIO (if high impact) - _________________________ Date: _______

## Post-Implementation Review
### Outcome
- **Successful**: Yes / Partial / No
- **Issues Encountered**:

### Verification
- **All Tests Passed**: Yes / No
- **Services Restored**: Yes / No
- **Performance Acceptable**: Yes / No
- **Users Notified**: Yes / No

### Lessons Learned
- **What Went Well**:
- **What Could Be Improved**:
- **Recommendations**:

## Notes
[Additional notes or comments]

## Related Documentation
- [Link to technical specs]
- [Link to affected systems]
- [Link to previous changes]
''',
                'content_type': 'markdown',
                'is_template': True,
            },
            {
                'title': 'Network Documentation Template',
                'slug': 'network-documentation-template',
                'body': '''# Network Documentation: [Network Name]

## Network Overview
- **Site Name**:
- **Location**:
- **Network Type**: LAN / WAN / DMZ / Wireless
- **Last Updated**:
- **Network Administrator**:

## Network Diagram
[Attach or link to network diagram]

## IP Address Scheme
### Subnets
| Subnet | CIDR | Network | Gateway | VLAN | Purpose |
|--------|------|---------|---------|------|---------|
|        |      |         |         |      |         |

### DHCP Ranges
| VLAN | DHCP Start | DHCP End | Lease Time | Notes |
|------|------------|----------|------------|-------|
|      |            |          |            |       |

### Static IP Assignments
| IP Address | Hostname | Device Type | Purpose | MAC Address |
|------------|----------|-------------|---------|-------------|
|            |          |             |         |             |

## VLANs
| VLAN ID | Name | Subnet | Purpose | Ports |
|---------|------|--------|---------|-------|
|         |      |        |         |       |

## Core Network Devices
### Routers
| Device | Model | IP Address | Management URL | Location | Serial Number |
|--------|-------|------------|----------------|----------|---------------|
|        |       |            |                |          |               |

### Switches
| Device | Model | IP Address | Management URL | Location | Ports | PoE |
|--------|-------|------------|----------------|----------|-------|-----|
|        |       |            |                |          |       |     |

### Firewalls
| Device | Model | External IP | Internal IP | Management URL | Serial Number |
|--------|-------|-------------|-------------|----------------|---------------|
|        |       |             |             |                |               |

### Wireless Access Points
| Device | Model | IP Address | Location | SSID(s) | Channel |
|--------|-------|------------|----------|---------|---------|
|        |       |            |          |         |         |

## Internet Connection
- **ISP**:
- **Circuit ID**:
- **Connection Type**: Fiber / Cable / DSL / T1 / Other
- **Speed**: Download: _____ / Upload: _____
- **Public IP**:
- **Gateway**:
- **DNS Servers**:
- **Support Phone**:
- **Account Number**:

## VPN Configuration
| VPN Name | Type | Remote Endpoint | Local Subnet | Remote Subnet | Pre-Shared Key Location |
|----------|------|-----------------|--------------|---------------|-------------------------|
|          |      |                 |              |               |                         |

## Firewall Rules
### Inbound Rules
| Source | Destination | Port | Protocol | Action | Purpose |
|--------|-------------|------|----------|--------|---------|
|        |             |      |          |        |         |

### Outbound Rules
| Source | Destination | Port | Protocol | Action | Purpose |
|--------|-------------|------|----------|--------|---------|
|        |             |      |          |        |         |

### NAT Rules
| External IP | External Port | Internal IP | Internal Port | Protocol | Purpose |
|-------------|---------------|-------------|---------------|----------|---------|
|             |               |             |               |          |         |

## DNS Configuration
### Internal DNS Servers
| Server | IP Address | Primary/Secondary | Location |
|--------|------------|-------------------|----------|
|        |            |                   |          |

### DNS Records
| Hostname | Type | Value | TTL | Purpose |
|----------|------|-------|-----|---------|
|          |      |       |     |         |

## Monitoring & Management
- **Network Monitoring Tool**:
- **SNMP Community Strings**: [Link to password vault]
- **Syslog Server**:
- **Configuration Backup Location**:
- **Backup Frequency**:

## Security
### Access Control
- **Management Access**: SSH / HTTPS / Telnet / Console
- **Admin Accounts**: [Link to password vault]
- **Authentication Method**: Local / RADIUS / TACACS+ / AD

### Security Measures
- [ ] Firewall enabled and configured
- [ ] Intrusion detection/prevention
- [ ] MAC address filtering
- [ ] Port security
- [ ] Disable unused ports
- [ ] Regular firmware updates
- [ ] Strong password policy
- [ ] Two-factor authentication

## Wi-Fi Networks
| SSID | Security | Password Location | VLAN | Purpose | Hidden |
|------|----------|-------------------|------|---------|--------|
|      |          |                   |      |         |        |

## Bandwidth Allocation
| Service/Department | Guaranteed Bandwidth | Maximum Bandwidth | QoS Priority |
|-------------------|----------------------|-------------------|--------------|
|                   |                      |                   |              |

## Maintenance
### Regular Tasks
- **Daily**:
- **Weekly**:
- **Monthly**:
- **Quarterly**:

### Firmware Versions
| Device | Current Firmware | Latest Available | Last Updated |
|--------|------------------|------------------|--------------|
|        |                  |                  |              |

## Troubleshooting
### Common Issues
1. **Issue**:
   - **Solution**:

### Support Contacts
- **Internal Network Admin**:
- **ISP Support**:
- **Vendor Support**:
- **Emergency Contact**:

## Change Log
| Date | Changed By | Description |
|------|------------|-------------|
|      |            |             |

## Related Documentation
- [Network topology diagram]
- [Cable plant documentation]
- [Disaster recovery plan]
- [Security policies]
''',
                'content_type': 'markdown',
                'is_template': True,
            },
        ]

        created_count = 0
        skipped_count = 0

        for template_data in document_templates:
            slug = template_data['slug']

            # Check if template already exists
            if Document.objects.filter(organization=organization, slug=slug).exists():
                self.stdout.write(self.style.WARNING(f"Template '{template_data['title']}' already exists, skipping"))
                skipped_count += 1
                continue

            # Create template
            Document.objects.create(
                organization=organization,
                title=template_data['title'],
                slug=slug,
                body=template_data['body'],
                content_type=template_data['content_type'],
                is_template=True,
                is_published=True,
                is_global=is_global,
                created_by=superuser,
                last_modified_by=superuser,
            )

            self.stdout.write(self.style.SUCCESS(f"✓ Created template: {template_data['title']}"))
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"Templates created: {created_count}"))
        self.stdout.write(self.style.WARNING(f"Templates skipped (already exist): {skipped_count}"))
        self.stdout.write(self.style.SUCCESS(f"{'='*60}"))
