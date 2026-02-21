# New Features - v3.9.3

## 🚗 Service Vehicles - Fleet Management System

**Complete fleet management solution for service businesses**

### Overview
Track your service vehicles, maintenance schedules, fuel consumption, damage reports, and vehicle inventory in one comprehensive system. Perfect for MSPs, IT service companies, field service businesses, and any organization managing a fleet of service vehicles.

### Key Features

#### 🚙 Vehicle Management
- Track all vehicle details: make, model, year, VIN, license plate
- Vehicle status tracking (Active, Inactive, In Maintenance, Retired)
- Condition monitoring (Excellent, Good, Fair, Poor, Needs Repair)
- Real-time mileage tracking with automatic updates from fuel logs
- GPS location tracking with 6-decimal precision (~0.1m accuracy)
- QR code support for quick vehicle identification
- User assignment tracking with mileage history

#### 📦 Inventory Management
- Track tools, cables, hardware, and supplies stored in each vehicle
- Category organization (Cables, Tools, Hardware, Supplies, etc.)
- Low stock alerts with minimum quantity thresholds
- Unit cost tracking and automatic total value calculation
- Storage location tracking within vehicle
- **QR code scanning** for quick inventory lookups on tablets/phones
- **Reorder links** - Direct links to Amazon, eBay, or supplier pages for easy reordering

#### 🔧 Maintenance Tracking
- Comprehensive service history for each vehicle
- Maintenance types: oil changes, tire rotations, brake service, inspections, tune-ups, etc.
- Cost tracking: labor costs, parts costs, auto-calculated totals
- Recurring maintenance schedules
- Next due date and mileage tracking
- **Automatic overdue detection** with dashboard alerts
- Service provider tracking

#### ⛽ Fuel Logging
- Track all fuel purchases with date, location, and cost
- **Automatic MPG calculation** based on mileage between fill-ups
- Cost per gallon and total cost tracking
- Fuel station/location logging
- Historical MPG trends and cost analysis
- Auto-updates vehicle current mileage

#### 🛡️ Insurance & Registration
- Insurance provider and policy number tracking
- Insurance expiration date monitoring
- Insurance premium tracking (monthly/annual)
- Registration expiration tracking
- **Automatic expiration alerts** (30-day warning)
- Dashboard notifications for expiring policies

#### 💥 Damage Reports
- Incident reporting with date and description
- Severity levels: Minor, Moderate, Major, Total Loss
- Repair status tracking: Reported → Assessed → In Repair → Completed
- Damage location description
- Cost tracking: estimated vs. actual repair costs
- Insurance claim management (claim number, payout amount)
- Repair shop and date tracking
- Before/after condition tracking
- **Photo attachments** for damage documentation

#### 👤 User Assignments
- Assign vehicles to technicians/staff members
- Track assignment start and end dates
- Record starting and ending mileage
- Automatic miles driven calculation
- Assignment history and duration tracking
- Only one active assignment per vehicle

#### 📊 Dashboard & Reporting
- Fleet overview with key statistics
- Active vehicles, maintenance status, total mileage
- Alert system for:
  - Insurance expiring within 30 days
  - Registration expiring within 30 days
  - Overdue maintenance tasks
  - Low inventory stock alerts
- Recent activity feed (fuel logs, maintenance, damage reports)
- Fuel cost analysis and average MPG across fleet
- Total fleet mileage and average vehicle mileage

### Technical Details
- **NOT organization-scoped**: Vehicles belong to the service business (main company), not client organizations
- 6 specialized models: ServiceVehicle, VehicleInventoryItem, VehicleDamageReport, VehicleMaintenanceRecord, VehicleFuelLog, VehicleAssignment
- GPS coordinate storage with 6 decimal places (~0.1m accuracy)
- Automatic calculations: MPG, total costs, miles driven, overdue maintenance
- Feature toggle: Enable/disable entire vehicles module from settings
- Full audit trail with creation/update timestamps
- Django admin integration for all models
- 25+ views covering all CRUD operations
- Responsive design (mobile-friendly)

### Use Cases
- **MSPs & IT Service Companies**: Track technician vehicles, tools inventory, and field service costs
- **HVAC Companies**: Monitor service truck maintenance, parts inventory, and fuel expenses
- **Plumbing/Electrical**: Manage van inventory, track mileage for billing, schedule maintenance
- **General Contractors**: Fleet oversight, equipment tracking, cost analysis
- **Any Field Service Business**: Comprehensive vehicle and inventory management

### Mobile-Friendly Features
- QR code scanning with phone/tablet cameras
- Quick inventory lookups in the field
- Mobile-responsive dashboard and forms
- One-tap reorder links for supplies
- GPS location updates from mobile devices

---

## 🔐 OS Package Scanner - System Updates (Enhanced)

**Secure, optional system package update management**

### New Features

#### Command-Line Updates
- New management command: `python manage.py update_system_packages`
- **Security-only updates**: `--security-only` flag to install ONLY security patches
- **Specific packages**: `--package package1,package2` to update selected packages
- **Dry run mode**: `--dry-run` to preview changes without applying
- **Auto-approve**: `--auto-approve` for automated scripts (no prompts)
- Multi-platform support: apt (Debian/Ubuntu), yum/dnf (RedHat/CentOS), pacman (Arch)

#### Web Interface
- **"Update Security" button**: One-click security patch installation (appears when security updates available)
- **"Update All" button**: One-click system-wide updates (appears when any updates available)
- Confirmation modal with clear warnings
- Progress indicator during updates
- Success/failure notifications
- Update history tracking

### Safety Features
- Requires superuser/staff permissions
- Displays clear warnings before system changes
- Confirmation required (unless `--auto-approve`)
- Dry-run mode for testing
- All operations logged to database
- Timeout protection (10-minute max)
- Error handling and rollback support

### Technical Details
- Uses native package managers (apt, yum/dnf, pacman)
- Respects system sudo permissions
- Async operation support for long-running updates
- JSON output option for integration
- Comprehensive error reporting

### Use Cases
- **Quick Security Patching**: One-click security updates from web interface
- **Scheduled Maintenance**: CLI automation for maintenance windows
- **Compliance**: Regular security update tracking and reporting
- **System Hardening**: Easy security-only updates without full system upgrades

---

## 🎯 UI Improvements

### Documentation Menu Relocated
- **Fixed**: Documentation link moved from Docs dropdown to User dropdown
- **New Location**: User Menu → Documentation
- **Benefit**: Cleaner navigation, easier access to docs from any page

---

## 📦 Installation & Setup

### Service Vehicles
1. Feature is enabled by default
2. Navigate to **Service Vehicles** → **Dashboard**
3. Click "Add Vehicle" to create your first vehicle
4. Add inventory items, maintenance records, and fuel logs
5. Use QR codes for quick scanning (camera permission required)

### Package Scanner Updates
1. Enabled automatically (part of existing package scanner)
2. Navigate to **Security** → **Package Scanner**
3. Click "Run Scan Now" to check for updates
4. Click "Update Security" or "Update All" as needed
5. Confirm action and wait for completion

---

## 🔄 Migration Notes

### Vehicles
- New database tables created automatically
- No data migration required (new feature)
- Feature toggle: System → Settings → Features → Service Vehicles

### Package Scanner
- No database changes
- Backwards compatible with existing scans
- Update functionality is optional (nothing changes if not used)

---

## 📚 Documentation

### User Guides
- Service Vehicles User Guide (coming soon)
- QR Code Scanning Tutorial (coming soon)
- Fleet Management Best Practices (coming soon)

### API Documentation
- REST API endpoints for vehicle data (planned)
- Webhook events for vehicle updates (planned)

---

## 🎉 What's Next?

### Upcoming Enhancements
- Mobile app for field technicians
- Vehicle routing and trip planning
- Automated maintenance reminders (email/webhook)
- Parts inventory integration
- Vendor management for service centers
- Fleet analytics dashboard with charts
- Export reports (PDF, CSV)
- QR code generation for inventory items
- Barcode scanning support
- Integration with telematics devices

---

## 🐛 Bug Fixes & Improvements

- Fixed documentation menu placement in navigation
- Improved permission checks for system updates
- Enhanced error handling in package scanner
- Better mobile responsiveness across all views

---

## 💡 Tips & Tricks

### Service Vehicles
- Use QR codes on vehicle windshields for quick identification
- Print QR codes for inventory items and stick them on toolboxes
- Set reorder links to your most-used suppliers for one-click ordering
- Schedule recurring oil changes every 3,000-5,000 miles
- Take photos of damage immediately and attach to reports
- Review low inventory alerts weekly to maintain stock levels

### Package Scanner
- Run security scans weekly
- Apply security updates immediately
- Use dry-run mode first to preview changes
- Schedule full system updates during maintenance windows
- Monitor the scan history for update trends

---

**Version**: 3.9.3
**Release Date**: 2026-02-21
**Contributors**: Claude Sonnet 4.5
