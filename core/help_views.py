"""
Integrated documentation and help system
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import markdown
import os


@login_required
def help_index(request):
    """Main help documentation index"""
    return render(request, 'core/help/index.html', {
        'title': 'Help & Documentation'
    })


@login_required
def help_getting_started(request):
    """Getting started guide"""
    return render(request, 'core/help/getting_started.html', {
        'title': 'Getting Started'
    })


@login_required
def help_features(request):
    """Features documentation"""
    # Read FEATURES.md and convert to HTML
    features_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'FEATURES.md')
    try:
        with open(features_path, 'r') as f:
            content = f.read()
            html_content = markdown.markdown(content, extensions=['tables', 'fenced_code', 'toc'])
    except:
        html_content = "<p>Features documentation not available.</p>"

    return render(request, 'core/help/features.html', {
        'title': 'Features',
        'content': html_content
    })


@login_required
def help_assets(request):
    """Asset management help"""
    content = """
    <h4>Asset Management</h4>
    <p class="lead">Track and manage all IT equipment, servers, network devices, and hardware assets.</p>

    <h5 class="mt-4"><i class="fas fa-server"></i> Asset Tracking</h5>
    <ul>
        <li><strong>Comprehensive Information:</strong> Track make, model, serial numbers, purchase dates, warranties</li>
        <li><strong>Custom Fields:</strong> Add unlimited custom fields for organization-specific needs</li>
        <li><strong>Attachments:</strong> Upload photos, manuals, invoices, and documentation</li>
        <li><strong>Relationships:</strong> Link related assets, dependencies, and parent/child relationships</li>
        <li><strong>QR Codes:</strong> Generate QR codes for physical asset labels</li>
        <li><strong>Lifecycle Tracking:</strong> Monitor asset status from purchase to retirement</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-network-wired"></i> Network Management</h5>
    <ul>
        <li><strong>IP Address Management:</strong> Track IPs, subnets, VLANs</li>
        <li><strong>MAC Addresses:</strong> Record network interface details</li>
        <li><strong>Network Diagrams:</strong> Create visual network topology maps</li>
        <li><strong>Port Assignments:</strong> Track switch ports and patch panel connections</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-warehouse"></i> Location & Rack Management</h5>
    <ul>
        <li><strong>Data Centers:</strong> Organize assets by locations and data centers</li>
        <li><strong>Racks:</strong> Visual rack layout with U-space allocation</li>
        <li><strong>Drag & Drop:</strong> Easily move devices between rack positions</li>
        <li><strong>Power Management:</strong> Track power consumption and capacity</li>
        <li><strong>Environmental Monitoring:</strong> Record temperature, humidity, and conditions</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-list"></i> Asset Categories</h5>
    <p>Supported asset types include:</p>
    <div class="row">
        <div class="col-md-6">
            <ul>
                <li>Servers & Virtual Machines</li>
                <li>Network Equipment (switches, routers, firewalls)</li>
                <li>Storage Devices (NAS, SAN)</li>
                <li>Workstations & Laptops</li>
            </ul>
        </div>
        <div class="col-md-6">
            <ul>
                <li>Mobile Devices (phones, tablets)</li>
                <li>Printers & Peripherals</li>
                <li>Security Equipment (cameras, access control)</li>
                <li>Power Distribution (UPS, PDU)</li>
            </ul>
        </div>
    </div>

    <h5 class="mt-4"><i class="fas fa-chart-line"></i> Reporting & Analytics</h5>
    <ul>
        <li><strong>Asset Reports:</strong> Generate reports on inventory, warranties, and costs</li>
        <li><strong>Export Options:</strong> Export data to CSV, PDF, or Excel</li>
        <li><strong>Depreciation Tracking:</strong> Monitor asset value over time</li>
        <li><strong>Warranty Alerts:</strong> Get notified before warranties expire</li>
    </ul>
    """
    return render(request, 'core/help/assets.html', {
        'title': 'Asset Management',
        'content': content
    })


@login_required
def help_vehicles(request):
    """Service vehicles help"""
    content = """
    <h4>Service Vehicle Fleet Management</h4>
    <p class="lead">Comprehensive fleet management for service vehicles with mileage tracking, maintenance scheduling, and inventory management.</p>

    <h5 class="mt-4"><i class="fas fa-truck"></i> Vehicle Tracking</h5>
    <ul>
        <li><strong>Vehicle Information:</strong> Track make, model, year, VIN, license plate</li>
        <li><strong>Mileage Tracking:</strong> Automatic odometer updates from fuel logs</li>
        <li><strong>Vehicle Status:</strong> Monitor active, maintenance, or retired status</li>
        <li><strong>Condition Tracking:</strong> Rate condition from excellent to needs repair</li>
        <li><strong>GPS Location:</strong> Store current vehicle coordinates (lat/long)</li>
        <li><strong>User Assignments:</strong> Track who's using each vehicle</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-shield-alt"></i> Insurance & Registration</h5>
    <ul>
        <li><strong>Insurance Tracking:</strong> Policy number, provider, expiration dates</li>
        <li><strong>Premium Management:</strong> Track insurance costs</li>
        <li><strong>Registration Expiry:</strong> Monitor registration renewal dates</li>
        <li><strong>Expiration Alerts:</strong> Get notified 30 days before expiration</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-wrench"></i> Maintenance Management</h5>
    <ul>
        <li><strong>Service History:</strong> Complete maintenance and repair logs</li>
        <li><strong>Scheduled Maintenance:</strong> Oil changes, tire rotations, inspections</li>
        <li><strong>Cost Tracking:</strong> Labor and parts costs for each service</li>
        <li><strong>Next Due:</strong> Track next service by mileage or date</li>
        <li><strong>Overdue Detection:</strong> Automatic alerts for overdue maintenance</li>
        <li><strong>Service Providers:</strong> Record mechanics and service centers</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-gas-pump"></i> Fuel Tracking</h5>
    <ul>
        <li><strong>Fuel Logs:</strong> Record every fill-up with gallons and cost</li>
        <li><strong>MPG Calculation:</strong> Automatic miles-per-gallon tracking</li>
        <li><strong>Cost Analysis:</strong> Track fuel expenses per vehicle</li>
        <li><strong>Station Locations:</strong> Record where fuel was purchased</li>
        <li><strong>Trend Analysis:</strong> Monitor fuel efficiency over time</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-car-crash"></i> Damage Reporting</h5>
    <ul>
        <li><strong>Incident Reports:</strong> Document damage with photos and descriptions</li>
        <li><strong>Severity Levels:</strong> Minor, moderate, major, or total loss</li>
        <li><strong>Repair Tracking:</strong> Monitor repair status from reported to completed</li>
        <li><strong>Cost Estimates:</strong> Track estimated and actual repair costs</li>
        <li><strong>Insurance Claims:</strong> Claim numbers and payout tracking</li>
        <li><strong>Photo Attachments:</strong> Upload damage photos for documentation</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-boxes"></i> Vehicle Inventory</h5>
    <ul>
        <li><strong>Equipment Tracking:</strong> Cables, connectors, hardware, tools</li>
        <li><strong>Quantity Management:</strong> Track item quantities and units</li>
        <li><strong>Low Stock Alerts:</strong> Get notified when inventory runs low</li>
        <li><strong>Value Tracking:</strong> Monitor total inventory value per vehicle</li>
        <li><strong>Categories:</strong> Organize by cables, tools, hardware, supplies</li>
        <li><strong>Storage Locations:</strong> Note where items are stored in vehicle</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-user-check"></i> User Assignments</h5>
    <ul>
        <li><strong>Assignment History:</strong> Track who used each vehicle and when</li>
        <li><strong>Mileage Records:</strong> Starting and ending mileage per assignment</li>
        <li><strong>Duration Tracking:</strong> Calculate how long each assignment lasted</li>
        <li><strong>Active Assignments:</strong> See current vehicle assignments</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-tachometer-alt"></i> Dashboard & Reports</h5>
    <ul>
        <li><strong>Fleet Overview:</strong> Summary of all vehicles and their status</li>
        <li><strong>Upcoming Maintenance:</strong> See scheduled services</li>
        <li><strong>Fuel Efficiency:</strong> Compare MPG across fleet</li>
        <li><strong>Cost Analysis:</strong> Total maintenance and fuel costs</li>
        <li><strong>Expiration Warnings:</strong> Insurance and registration alerts</li>
    </ul>
    """
    return render(request, 'core/help/vehicles.html', {
        'title': 'Service Vehicles',
        'content': content
    })


@login_required
def help_vault(request):
    """Password vault help"""
    content = """
    <h4>Password Vault</h4>
    <p class="lead">Securely store and manage credentials with AES-256 encryption, breach detection, and security analysis.</p>

    <h5 class="mt-4"><i class="fas fa-lock"></i> Security Features</h5>
    <ul>
        <li><strong>AES-256 Encryption:</strong> Military-grade encryption for all stored passwords</li>
        <li><strong>Zero-Knowledge Architecture:</strong> Passwords encrypted at rest and in transit</li>
        <li><strong>Master Password:</strong> Organization-level encryption keys</li>
        <li><strong>Access Control:</strong> Role-based permissions for vault access</li>
        <li><strong>Audit Logging:</strong> Track every password access and modification</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-shield-alt"></i> Breach Detection</h5>
    <ul>
        <li><strong>Have I Been Pwned Integration:</strong> Check passwords against known breaches</li>
        <li><strong>Automatic Scanning:</strong> Regular checks for compromised credentials</li>
        <li><strong>Breach Alerts:</strong> Immediate notification if password found in breach</li>
        <li><strong>Security Score:</strong> Rate password strength and security</li>
        <li><strong>Reuse Detection:</strong> Identify duplicate passwords across accounts</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-key"></i> Password Management</h5>
    <ul>
        <li><strong>Organized Storage:</strong> Group passwords by category, client, or service</li>
        <li><strong>Quick Search:</strong> Fast search across all credentials</li>
        <li><strong>Copy Protection:</strong> Secure clipboard with auto-clear</li>
        <li><strong>Show/Hide:</strong> Toggle password visibility</li>
        <li><strong>Notes & URLs:</strong> Store additional context and login URLs</li>
        <li><strong>Tags & Labels:</strong> Organize with custom tags</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-random"></i> Password Generator</h5>
    <ul>
        <li><strong>Strong Passwords:</strong> Generate cryptographically secure passwords</li>
        <li><strong>Customizable:</strong> Set length, character types, and complexity</li>
        <li><strong>Pronounceable Options:</strong> Create memorable yet secure passwords</li>
        <li><strong>Passphrase Generator:</strong> Multi-word passphrases for better memorability</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-chart-bar"></i> Security Analysis</h5>
    <ul>
        <li><strong>Strength Meter:</strong> Visual password strength indicator</li>
        <li><strong>Weak Password Detection:</strong> Identify and flag weak credentials</li>
        <li><strong>Age Tracking:</strong> Monitor how long passwords have been in use</li>
        <li><strong>Expiration Reminders:</strong> Set password rotation schedules</li>
        <li><strong>Compliance Reports:</strong> Password policy compliance tracking</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-users"></i> Sharing & Collaboration</h5>
    <ul>
        <li><strong>Secure Sharing:</strong> Share credentials within organization</li>
        <li><strong>Access Control:</strong> Grant read-only or full access</li>
        <li><strong>Temporary Access:</strong> Time-limited credential sharing</li>
        <li><strong>Sharing History:</strong> Track who accessed shared passwords</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-download"></i> Import & Export</h5>
    <ul>
        <li><strong>Import from CSV:</strong> Bulk import from other password managers</li>
        <li><strong>LastPass Import:</strong> Direct import from LastPass export</li>
        <li><strong>1Password Import:</strong> Import from 1Password exports</li>
        <li><strong>Secure Export:</strong> Export encrypted backups</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-mobile-alt"></i> Access Options</h5>
    <ul>
        <li><strong>Web Interface:</strong> Access from any browser</li>
        <li><strong>REST API:</strong> Programmatic access with API keys</li>
        <li><strong>Mobile Responsive:</strong> Optimized for phones and tablets</li>
        <li><strong>Offline Access:</strong> View cached credentials when offline</li>
    </ul>
    """
    return render(request, 'core/help/vault.html', {
        'title': 'Password Vault',
        'content': content
    })


@login_required
def help_monitoring(request):
    """Monitoring help"""
    content = """
    <h4>Infrastructure Monitoring</h4>
    <p class="lead">Monitor servers, network devices, and services with real-time alerts and comprehensive dashboards.</p>

    <h5 class="mt-4"><i class="fas fa-heartbeat"></i> System Monitoring</h5>
    <ul>
        <li><strong>Server Monitoring:</strong> Track CPU, memory, disk usage, and uptime</li>
        <li><strong>Network Devices:</strong> Monitor switches, routers, firewalls</li>
        <li><strong>Service Checks:</strong> HTTP, HTTPS, TCP, UDP, ICMP ping</li>
        <li><strong>SSL Certificate Monitoring:</strong> Track expiration dates</li>
        <li><strong>Port Monitoring:</strong> Check if specific ports are open/closed</li>
        <li><strong>Response Time:</strong> Measure latency and performance</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-bell"></i> Alerting</h5>
    <ul>
        <li><strong>Real-time Alerts:</strong> Instant notifications for issues</li>
        <li><strong>Multiple Channels:</strong> Email, webhook, Slack, Teams</li>
        <li><strong>Alert Rules:</strong> Customize thresholds and conditions</li>
        <li><strong>Escalation Policies:</strong> Multi-tier alert escalation</li>
        <li><strong>Alert Grouping:</strong> Reduce alert fatigue with smart grouping</li>
        <li><strong>Maintenance Windows:</strong> Silence alerts during maintenance</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-chart-line"></i> Dashboards & Visualization</h5>
    <ul>
        <li><strong>Real-time Dashboards:</strong> Live status of all monitored systems</li>
        <li><strong>Historical Graphs:</strong> Performance trends over time</li>
        <li><strong>Custom Views:</strong> Create dashboards for specific clients or locations</li>
        <li><strong>Heat Maps:</strong> Visual status overview of infrastructure</li>
        <li><strong>Uptime Reports:</strong> SLA compliance tracking</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-network-wired"></i> Network Monitoring</h5>
    <ul>
        <li><strong>Bandwidth Monitoring:</strong> Track network utilization</li>
        <li><strong>Latency Checks:</strong> Measure network response times</li>
        <li><strong>Packet Loss:</strong> Detect network quality issues</li>
        <li><strong>Port Scanning:</strong> Identify open ports and services</li>
        <li><strong>IP Reputation:</strong> Check for blacklisted IPs</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-database"></i> Database Monitoring</h5>
    <ul>
        <li><strong>Connection Checks:</strong> Verify database connectivity</li>
        <li><strong>Query Performance:</strong> Monitor slow queries</li>
        <li><strong>Disk Space:</strong> Track database storage usage</li>
        <li><strong>Backup Verification:</strong> Ensure backups are running</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-globe"></i> Website Monitoring</h5>
    <ul>
        <li><strong>Uptime Monitoring:</strong> Check if websites are accessible</li>
        <li><strong>Response Time:</strong> Measure page load speed</li>
        <li><strong>Status Code Checks:</strong> Detect 404, 500, and other errors</li>
        <li><strong>Content Monitoring:</strong> Verify expected content is present</li>
        <li><strong>SSL/TLS Checks:</strong> Monitor certificate validity</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-calendar-check"></i> Scheduled Checks</h5>
    <ul>
        <li><strong>Flexible Intervals:</strong> 1 minute to 24 hour check intervals</li>
        <li><strong>Custom Schedules:</strong> Business hours only or 24/7</li>
        <li><strong>Retry Logic:</strong> Automatic retries for transient failures</li>
        <li><strong>Check Dependencies:</strong> Parent/child check relationships</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-history"></i> Incident Management</h5>
    <ul>
        <li><strong>Incident Timeline:</strong> Track when issues started and resolved</li>
        <li><strong>Root Cause Analysis:</strong> Document problem resolution</li>
        <li><strong>MTTR Tracking:</strong> Measure mean time to resolution</li>
        <li><strong>Post-mortems:</strong> Create detailed incident reports</li>
    </ul>
    """
    return render(request, 'core/help/monitoring.html', {
        'title': 'Monitoring',
        'content': content
    })


@login_required
def help_security(request):
    """Security features help"""
    content = """
    <h4>Security Features</h4>
    <p class="lead">Comprehensive security tools including vulnerability scanning, breach detection, and audit logging.</p>

    <h5 class="mt-4"><i class="fas fa-shield-alt"></i> Vulnerability Scanning</h5>
    <ul>
        <li><strong>Python Package Scanner:</strong> Scan Python dependencies for known vulnerabilities</li>
        <li><strong>OS Package Scanner:</strong> Check system packages for security updates</li>
        <li><strong>CVE Database:</strong> Integration with Common Vulnerabilities and Exposures database</li>
        <li><strong>Severity Ratings:</strong> CRITICAL, HIGH, MEDIUM, LOW classifications</li>
        <li><strong>Automated Scans:</strong> Scheduled security checks (hourly, daily, weekly)</li>
        <li><strong>Fix Recommendations:</strong> Suggested remediation actions</li>
        <li><strong>Historical Tracking:</strong> Monitor vulnerability trends over time</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-user-shield"></i> Authentication & Access Control</h5>
    <ul>
        <li><strong>Two-Factor Authentication (2FA):</strong> TOTP-based 2FA with QR code setup</li>
        <li><strong>Azure AD Integration:</strong> Single sign-on with Microsoft Azure AD</li>
        <li><strong>Password Policies:</strong> Enforce strong password requirements</li>
        <li><strong>Session Management:</strong> Automatic timeout and secure session handling</li>
        <li><strong>IP Whitelisting:</strong> Restrict access by IP address</li>
        <li><strong>Failed Login Detection:</strong> Account lockout after repeated failures</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-user-tag"></i> Role-Based Access Control (RBAC)</h5>
    <ul>
        <li><strong>42 Granular Permissions:</strong> Fine-grained control over features</li>
        <li><strong>Custom Roles:</strong> Create organization-specific roles</li>
        <li><strong>Role Templates:</strong> Owner, Admin, Editor, Read-Only presets</li>
        <li><strong>Permission Inheritance:</strong> Hierarchical role structures</li>
        <li><strong>Organization Scoping:</strong> Isolate data by organization</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-clipboard-list"></i> Audit Logging</h5>
    <ul>
        <li><strong>Comprehensive Logs:</strong> Every action logged with timestamp and user</li>
        <li><strong>Change Tracking:</strong> Before/after values for all modifications</li>
        <li><strong>Search & Filter:</strong> Query logs by user, action, date, or resource</li>
        <li><strong>Export Logs:</strong> Download audit trails for compliance</li>
        <li><strong>Retention Policies:</strong> Configurable log retention periods</li>
        <li><strong>Immutable Records:</strong> Logs cannot be modified or deleted</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-user-secret"></i> Password Security</h5>
    <ul>
        <li><strong>Breach Detection:</strong> Check passwords against known breaches (HIBP)</li>
        <li><strong>Strength Requirements:</strong> Enforce minimum complexity rules</li>
        <li><strong>Password History:</strong> Prevent reuse of recent passwords</li>
        <li><strong>Expiration Policies:</strong> Force periodic password changes</li>
        <li><strong>Encrypted Storage:</strong> AES-256 encryption for all passwords</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-certificate"></i> SSL/TLS Security</h5>
    <ul>
        <li><strong>Certificate Monitoring:</strong> Track SSL certificate expiration</li>
        <li><strong>HTTPS Enforcement:</strong> Redirect HTTP to HTTPS</li>
        <li><strong>HSTS Support:</strong> HTTP Strict Transport Security headers</li>
        <li><strong>Certificate Validation:</strong> Check certificate chains</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-lock"></i> Data Protection</h5>
    <ul>
        <li><strong>Encryption at Rest:</strong> Database encryption for sensitive data</li>
        <li><strong>Encryption in Transit:</strong> TLS 1.2+ for all connections</li>
        <li><strong>Secure File Storage:</strong> Encrypted file attachments</li>
        <li><strong>Backup Encryption:</strong> Encrypted database backups</li>
        <li><strong>GDPR Compliance:</strong> Data privacy and right-to-delete support</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-bell"></i> Security Alerts</h5>
    <ul>
        <li><strong>Vulnerability Alerts:</strong> Notify when new CVEs discovered</li>
        <li><strong>Breach Notifications:</strong> Alert when passwords found in breaches</li>
        <li><strong>Failed Login Alerts:</strong> Suspicious authentication attempts</li>
        <li><strong>Permission Changes:</strong> Notify on role or access modifications</li>
        <li><strong>Certificate Expiration:</strong> Warn before SSL certificates expire</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-chart-pie"></i> Security Dashboard</h5>
    <ul>
        <li><strong>Security Score:</strong> Overall security posture rating</li>
        <li><strong>Vulnerability Summary:</strong> Count by severity level</li>
        <li><strong>At-Risk Assets:</strong> Systems with critical vulnerabilities</li>
        <li><strong>Compliance Status:</strong> Security policy compliance tracking</li>
        <li><strong>Trend Analysis:</strong> Security improvements over time</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-file-contract"></i> Compliance & Reporting</h5>
    <ul>
        <li><strong>Audit Reports:</strong> Generate compliance audit reports</li>
        <li><strong>Security Policies:</strong> Document and enforce security policies</li>
        <li><strong>Access Reviews:</strong> Periodic review of user permissions</li>
        <li><strong>Risk Assessment:</strong> Identify and prioritize security risks</li>
    </ul>
    """
    return render(request, 'core/help/security.html', {
        'title': 'Security',
        'content': content
    })


@login_required
def help_api(request):
    """API documentation"""
    content = """
    <h4>API Documentation</h4>
    <p class="lead">Programmatic access to Client St0r with REST and GraphQL APIs.</p>

    <h5 class="mt-4"><i class="fas fa-plug"></i> API Overview</h5>
    <ul>
        <li><strong>REST API:</strong> Full-featured RESTful API for all resources</li>
        <li><strong>GraphQL API:</strong> Flexible query language for complex data needs</li>
        <li><strong>Webhooks:</strong> Real-time event notifications</li>
        <li><strong>API Keys:</strong> Secure authentication tokens</li>
        <li><strong>Rate Limiting:</strong> Fair usage policies</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-key"></i> Authentication</h5>
    <p>Client St0r API supports multiple authentication methods:</p>
    <div class="card mt-3 mb-3">
        <div class="card-body">
            <h6>API Key Authentication</h6>
            <p>Include your API key in the Authorization header:</p>
            <code>Authorization: Bearer YOUR_API_KEY</code>
            <p class="mt-2 mb-0">Generate API keys from your profile settings.</p>
        </div>
    </div>

    <h5 class="mt-4"><i class="fas fa-exchange-alt"></i> REST API</h5>
    <p><strong>Base URL:</strong> <code>https://your-server.com/api/v1/</code></p>

    <h6 class="mt-3">Common Endpoints</h6>
    <table class="table table-sm">
        <thead>
            <tr>
                <th>Resource</th>
                <th>Endpoint</th>
                <th>Methods</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Assets</td>
                <td><code>/api/v1/assets/</code></td>
                <td>GET, POST, PUT, DELETE</td>
            </tr>
            <tr>
                <td>Passwords</td>
                <td><code>/api/v1/passwords/</code></td>
                <td>GET, POST, PUT, DELETE</td>
            </tr>
            <tr>
                <td>Organizations</td>
                <td><code>/api/v1/organizations/</code></td>
                <td>GET, POST, PUT, DELETE</td>
            </tr>
            <tr>
                <td>Vehicles</td>
                <td><code>/api/v1/vehicles/</code></td>
                <td>GET, POST, PUT, DELETE</td>
            </tr>
            <tr>
                <td>Monitors</td>
                <td><code>/api/v1/monitors/</code></td>
                <td>GET, POST, PUT, DELETE</td>
            </tr>
        </tbody>
    </table>

    <h6 class="mt-4">Example Request</h6>
    <pre class="bg-light p-3"><code>curl -X GET https://your-server.com/api/v1/assets/ \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json"</code></pre>

    <h6 class="mt-4">Example Response</h6>
    <pre class="bg-light p-3"><code>{
  "count": 42,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Main Server",
      "asset_type": "server",
      "organization": "Acme Corp",
      "created_at": "2026-01-15T10:30:00Z"
    }
  ]
}</code></pre>

    <h5 class="mt-4"><i class="fas fa-project-diagram"></i> GraphQL API</h5>
    <p><strong>Endpoint:</strong> <code>https://your-server.com/api/v2/graphql/</code></p>
    <p>GraphQL provides a flexible query language for requesting exactly the data you need.</p>

    <h6 class="mt-3">Example Query</h6>
    <pre class="bg-light p-3"><code>query {
  assets(organization: "Acme Corp") {
    id
    name
    assetType
    ipAddress
    createdAt
  }
}</code></pre>

    <h6 class="mt-4">Example Mutation</h6>
    <pre class="bg-light p-3"><code>mutation {
  createAsset(
    name: "New Server"
    assetType: "server"
    organizationId: 1
  ) {
    asset {
      id
      name
    }
  }
}</code></pre>

    <h5 class="mt-4"><i class="fas fa-bell"></i> Webhooks</h5>
    <p>Receive real-time notifications when events occur in Client St0r.</p>

    <h6 class="mt-3">Supported Events</h6>
    <ul>
        <li><code>asset.created</code> - New asset created</li>
        <li><code>asset.updated</code> - Asset modified</li>
        <li><code>asset.deleted</code> - Asset deleted</li>
        <li><code>password.created</code> - New password stored</li>
        <li><code>password.breached</code> - Password found in breach</li>
        <li><code>monitor.down</code> - Monitor check failed</li>
        <li><code>monitor.up</code> - Monitor recovered</li>
        <li><code>vulnerability.found</code> - Security vulnerability detected</li>
        <li><code>vehicle.maintenance_due</code> - Vehicle maintenance due</li>
    </ul>

    <h6 class="mt-3">Webhook Payload</h6>
    <pre class="bg-light p-3"><code>{
  "event": "asset.created",
  "timestamp": "2026-02-21T15:30:00Z",
  "organization": "Acme Corp",
  "data": {
    "id": 123,
    "name": "New Server",
    "asset_type": "server"
  }
}</code></pre>

    <h5 class="mt-4"><i class="fas fa-filter"></i> Filtering & Pagination</h5>
    <p>REST API supports advanced filtering and pagination:</p>
    <ul>
        <li><strong>Filtering:</strong> <code>?asset_type=server&amp;organization=1</code></li>
        <li><strong>Search:</strong> <code>?search=server</code></li>
        <li><strong>Ordering:</strong> <code>?ordering=-created_at</code></li>
        <li><strong>Pagination:</strong> <code>?page=2&amp;page_size=50</code></li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-book"></i> Interactive API Explorer</h5>
    <p>Explore the GraphQL API interactively:</p>
    <a href="/api/v2/graphql/" class="btn btn-primary" target="_blank">
        <i class="fas fa-external-link-alt"></i> Open GraphQL Explorer
    </a>

    <h5 class="mt-4"><i class="fas fa-code"></i> Client Libraries</h5>
    <p>Official client libraries available for:</p>
    <ul>
        <li><strong>Python:</strong> <code>pip install clientst0r-api</code></li>
        <li><strong>JavaScript/Node.js:</strong> <code>npm install clientst0r-api</code></li>
        <li><strong>PowerShell:</strong> Client St0r PowerShell module</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-tachometer-alt"></i> Rate Limits</h5>
    <p>API requests are rate limited to ensure fair usage:</p>
    <ul>
        <li><strong>Standard Tier:</strong> 100 requests per minute</li>
        <li><strong>Premium Tier:</strong> 1000 requests per minute</li>
        <li><strong>Burst Limit:</strong> 200 requests in 10 seconds</li>
    </ul>

    <h5 class="mt-4"><i class="fas fa-question-circle"></i> Support</h5>
    <p>Need help with the API?</p>
    <ul>
        <li><strong>Documentation:</strong> <a href="https://github.com/agit8or1/clientst0r" target="_blank">GitHub Repository</a></li>
        <li><strong>Issues:</strong> <a href="https://github.com/agit8or1/clientst0r/issues" target="_blank">Report API Issues</a></li>
    </ul>
    """
    return render(request, 'core/help/api.html', {
        'title': 'API Documentation',
        'content': content
    })
