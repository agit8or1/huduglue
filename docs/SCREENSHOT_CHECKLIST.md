# Client St0r Screenshot Checklist - v3.10.7

## 🆕 New Features (PRIORITY - Missing Screenshots)

### Service Vehicles (v3.9+)
- [ ] `vehicles-dashboard.png` - Dashboard with fleet statistics (total, active, maintenance, mileage cards)
- [ ] `vehicles-list.png` - Vehicle list view with DataTables
- [ ] `vehicle-detail-overview.png` - Vehicle detail page, Overview tab
- [ ] `vehicle-detail-maintenance.png` - Vehicle detail page, Maintenance tab
- [ ] `vehicle-detail-fuel.png` - Vehicle detail page, Fuel tab with MPG chart
- [ ] `vehicle-detail-damage.png` - Vehicle detail page, Damage tab with diagram
- [ ] `vehicle-damage-form.png` - Damage report form with interactive SVG diagram
- [ ] `vehicle-damage-diagram.png` - Close-up of clickable vehicle diagram

### Security Features (v3.9+)
- [ ] `package-scanner-widget.png` - OS Package Scanner widget on security dashboard
- [ ] `package-scanner-dashboard.png` - Full package scanner dashboard with scan history
- [ ] `package-scan-results.png` - Scan results showing security updates

### Rack Enhancements (v3.10+)
- [ ] `rack-drag-drop.png` - Rack device being dragged with blue highlight
- [ ] `rack-wiring.png` - Rack with connection wiring visualization
- [ ] `rack-device-ports.png` - Device port configuration modal

## 📋 Existing Screenshots to Update/Replace

### Core Features (Outdated - Jan 15)
- [ ] `dashboard.png` - Main dashboard (update to show v3.10.7 in footer)
- [ ] `quick-add.png` - Quick add menu (verify all options shown)
- [ ] `about-page.png` - About page (update to v3.10.7)

### Asset Management
- [ ] `assets-list.png` - Asset list (verify current styling)
- [ ] `racks.png` - Rack visualization (show new drag-and-drop features)
- [ ] `network-closets.png` - Network closets view
- [ ] `ipam-subnets.png` - IPAM subnet management
- [ ] `vlans.png` - VLAN list

### Password Vault
- [ ] `password-vault.png` - Main vault view
- [ ] `personal-vault.png` - Personal vault view
- [ ] `secure-notes.png` - Secure notes interface

### Documentation
- [ ] `knowledge-base.png` - Document list
- [ ] `diagrams.png` - Diagram editor

### Monitoring
- [ ] `website-monitors.png` - Website monitoring dashboard
- [ ] `expirations.png` - Expiration tracking

### Security
- [ ] `security-dashboard.png` - Security dashboard (add package scanner widget)
- [ ] `vulnerability-scans.png` - Snyk scan results
- [ ] `scan-configuration.png` - Scan settings

### System Administration
- [ ] `settings-general.png` - General settings
- [ ] `system-status.png` - System status page
- [ ] `system-updates.png` - Update system
- [ ] `organizations.png` - Organization management
- [ ] `access-management.png` - User/role management
- [ ] `integrations.png` - PSA integrations

### Workflows & Locations
- [ ] `workflows.png` - Workflow list
- [ ] `locations.png` - Location management
- [ ] `floor-plans-import.png` - Floor plan import

### MSP/Global Features
- [ ] `global-dashboard.png` - Global staff dashboard
- [ ] `global-kb.png` - Global knowledge base
- [ ] `global-workflows.png` - Global workflow templates

### Other
- [ ] `profile.png` - User profile page
- [ ] `favorites.png` - Favorites view
- [ ] `import-data.png` - Data import tools
- [ ] `login-page.png` - Login screen

## 📸 Screenshot Guidelines

### Settings for Consistency
1. **Browser**: Use Chrome/Firefox at 1920x1080 resolution
2. **Zoom**: Set to 100% (Ctrl+0)
3. **Demo Data**: Use demo/test data (no real client info)
4. **User**: Login as admin/staff user to show all features
5. **Theme**: Use default light theme
6. **Watermark**: Add "Demo Data" watermark if showing sensitive areas
7. **Format**: Save as PNG, optimize with `optipng` or similar

### Page Preparation
1. Clear notifications/alerts unless showing specific feature
2. Ensure data is visible (not empty states unless intentional)
3. Show realistic but fake data
4. Verify version shown is v3.10.7
5. Use descriptive names (e.g., "Test Vehicle 1" not "asdf")

### Browser Screenshot Tools
```bash
# Full page screenshot in Firefox
# Press Shift+F2, type: screenshot --fullpage filename.png

# Chrome extension: Full Page Screen Capture
# Or use browser DevTools: Ctrl+Shift+P, "Capture full size screenshot"
```

### After Taking Screenshots
1. Move to `/home/administrator/docs/screenshots/`
2. Verify filename matches checklist
3. Optimize: `optipng -o7 *.png` (optional)
4. Update README.md references
5. Commit: `git add docs/screenshots/ && git commit -m "Add v3.10 screenshots"`

## 🎯 Priority Order

### High Priority (New Features)
1. Service Vehicles screenshots (8 total)
2. Package Scanner (3 total)
3. Rack enhancements (3 total)

### Medium Priority (Updates)
4. Dashboard, about, security dashboard (show new version/features)

### Low Priority (Verification)
5. Verify existing screenshots still accurate

## 📊 Progress Tracker

- New Features: 0/14 (0%)
- Outdated Updates: 0/21 (0%)
- **Total: 0/35 (0%)**

Target: All screenshots updated by end of week
