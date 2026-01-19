# Automatic Fail2ban Installation

HuduGlue can automatically install and configure fail2ban with one click!

## Quick Setup

1. **Grant Installation Permission (One-Time Setup)**

   Run this command to allow HuduGlue to install packages:
   ```bash
   sudo cp ~/deploy/huduglue-install-sudoers /etc/sudoers.d/huduglue-install
   sudo chmod 0440 /etc/sudoers.d/huduglue-install
   ```

2. **Install Fail2ban**

   Navigate to: **Settings → Fail2ban** in HuduGlue

   Click the **"Install Fail2ban Now"** button

   Wait 1-2 minutes for the installation to complete

3. **Done!**

   Refresh the page to see your fail2ban status and manage banned IPs

## What Gets Installed

- fail2ban package (via apt-get)
- Systemd service (enabled and started)
- Sudoers configuration for fail2ban-client access
- HuduGlue integration for viewing and managing bans

## Manual Installation (Alternative)

If you prefer to install manually:

```bash
sudo apt-get update
sudo apt-get install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Configure HuduGlue access
sudo cp ~/deploy/huduglue-fail2ban-sudoers /etc/sudoers.d/huduglue-fail2ban
sudo chmod 0440 /etc/sudoers.d/huduglue-fail2ban
```

## Security

The sudoers configurations grant specific, limited permissions:
- Package installation (only fail2ban)
- Service management (enable/start fail2ban)
- Fail2ban client commands (status, unban)

No root shell access or unrestricted sudo is granted.
