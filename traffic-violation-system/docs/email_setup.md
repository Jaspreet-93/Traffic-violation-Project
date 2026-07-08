# AURA Traffic Monitor - Email Alerts Setup Guide

This document describes how to configure the SMTP email alert routing system.

---

## 1. Local Configuration (.env)
Append the following variables to your root `.env` configuration file:
- `SMTP_HOST`: The SMTP server host address (default: `smtp.gmail.com`).
- `SMTP_PORT`: SMTP communication port (default: `587` with STARTTLS).
- `SMTP_USERNAME`: Official email address sending surveillance alerts.
- `SMTP_PASSWORD`: Secure app password (e.g. Gmail App Passwords).
- `STATION_EMAIL`: Destination email address representing the police station registry where infractions are compiled.

---

## 2. Setting Up Gmail App Passwords
If using a standard Gmail account:
1. Access your Google account settings panel.
2. Enable **2-Step Verification** (required for app passwords).
3. Search or navigate to the **App Passwords** section.
4. Generate a custom app password named e.g., "Aura Monitor" and copy the 16-character code.
5. Save this code as `SMTP_PASSWORD` value in the Settings interface or `.env` file.
