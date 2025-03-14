# Two-Factor Authentication (2FA) Implementation

## Overview
This document describes the implementation of Two-Factor Authentication (2FA) in the Blood Donation Web App backend.

## Changes Made

### 1. Database Changes
- **Added `otp_secret` column** to `Users` model (`models/user.py`) to store the OTP secret key.

### 2. New Model for OTP Handling
- Created `models/two_factor.py` for OTP generation and verification.

### 3. API Endpoints for 2FA (`api/user.py`)
- **Enable 2FA:** `/enable-2fa` (Stores OTP secret for user)
- **Generate OTP:** `/generate-otp` (Generates OTP using stored secret)
- **Verify OTP:** `/verify-otp` (Validates the OTP entered by the user)

## Dependencies Added
- Installed `pyotp` and `flask-mail`
- Updated `requirements.txt`

## How to Test
1. Enable 2FA for a user:
   ```json
   POST /enable-2fa
   {
     "user_id": 1
   }
