# ThanuRaksha Email Service

A Flask-based email service for sending verification codes and meeting invitations for video consultations.

## Features

- Send verification emails with beautiful HTML templates
- Send meeting invitations to both patients and doctors
- Different email templates for patients (green theme) and doctors (blue theme)
- Production-ready for deployment on Render

## API Endpoints

### 1. Send Verification Email
**POST** `/send-email`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "verification_code": "123456"
}
```

### 2. Send Meeting Invitations
**POST** `/send-meeting-invite`

**Request Body:**
```json
{
  "patient_email": "patient@example.com",
  "doctor_email": "doctor@example.com",
  "room_id": "ROOM12345",
  "patient_name": "John Doe",
  "doctor_name": "Dr. Smith"
}
```

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Gmail credentials
```

3. Run the application:
```bash
python app.py
```

## Deployment on Render

1. Push your code to GitHub
2. Connect your repository to Render
3. Set the following environment variables in Render:
   - `GMAIL_USER`: Your Gmail address
   - `GMAIL_PASS`: Your Gmail App Password (not regular password)

4. Render will automatically:
   - Install dependencies from `requirements.txt`
   - Start the app using the `Procfile`
   - Set the `PORT` environment variable

## Gmail Setup

To use Gmail SMTP:

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. Use this App Password as `GMAIL_PASS` (not your regular Gmail password)

## Environment Variables

- `GMAIL_USER`: Your Gmail email address
- `GMAIL_PASS`: Your Gmail App Password
- `PORT`: Port number (automatically set by Render)
