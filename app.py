from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)  # Allow React Native to call Flask

# Use environment variables for production security
GMAIL_USER = os.environ.get('GMAIL_USER', 'gandalabalaji@gmail.com')
GMAIL_PASS = os.environ.get('GMAIL_PASS', 'vzcx wtee hwjo dvqd')  # Use environment variable in production

def create_html_email(name, email, verification_code):
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Verification</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: bold;">Email Verification</h1>
                <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 16px;">Welcome to  ThanuRaksha</p>
            </div>
            
            <!-- Content -->
            <div style="padding: 40px 30px;">
                <h2 style="color: #333333; margin-bottom: 20px; font-size: 24px;">Hello {name}!</h2>
                
                <p style="color: #666666; font-size: 16px; line-height: 1.6; margin-bottom: 25px;">
                    We have successfully verified your details! Please use the verification code below to access your dashboard:
                </p>
                
                <!-- Verification Code Box -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 10px; text-align: center; margin: 30px 0;">
                    <p style="color: #ffffff; margin: 0 0 10px 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">Your Verification Code</p>
                    <div style="background-color: #ffffff; color: #333333; font-size: 32px; font-weight: bold; padding: 15px; border-radius: 8px; letter-spacing: 3px; font-family: 'Courier New', monospace;">
                        {verification_code}
                    </div>
                </div>
                
                <!-- User Details -->
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
                    <h3 style="color: #333333; margin: 0 0 15px 0; font-size: 18px;">Account Details:</h3>
                    <p style="color: #666666; margin: 5px 0; font-size: 14px;"><strong>Name:</strong> {name}</p>
                    <p style="color: #666666; margin: 5px 0; font-size: 14px;"><strong>Email:</strong> {email}</p>
                </div>
                
                <!-- Instructions -->
                <div style="background-color: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; margin: 25px 0;">
                    <h4 style="color: #1976d2; margin: 0 0 10px 0; font-size: 16px;">Important Instructions:</h4>
                    <ul style="color: #666666; margin: 0; padding-left: 20px; font-size: 14px;">
                        <li>This verification code will expire in 10 minutes</li>
                        <li>Do not share this code with anyone</li>
                        <li>If you didn't request this, please ignore this email</li>
                    </ul>
                </div>
                
                <p style="color: #666666; font-size: 14px; line-height: 1.6; margin-top: 30px;">
                    If you have any questions or need assistance, please don't hesitate to contact our support team.
                </p>
                
                <p style="color: #666666; font-size: 14px; margin-top: 20px;">
                    Best regards,<br>
                    <strong style="color: #333333;">ThanuRaksha </strong>
                </p>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #333333; padding: 20px; text-align: center; border-radius: 0 0 10px 10px;">
                <p style="color: #ffffff; margin: 0; font-size: 12px;">
                    © 2025 Your Company Name. All rights reserved.
                </p>
                <p style="color: #cccccc; margin: 5px 0 0 0; font-size: 12px;">
                    This is an automated message, please do not reply to this email.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

def create_meeting_email(name, room_id, role):
    """Create HTML email for video call meeting invitation"""
    # Different colors and messaging based on role
    if role == 'patient':
        primary_color = '#4CAF50'  # Green for patients
        secondary_color = '#81C784'
        role_title = 'Patient'
        greeting = 'Your consultation is ready!'
    else:  # doctor
        primary_color = '#2196F3'  # Blue for doctors
        secondary_color = '#64B5F6'
        role_title = 'Doctor'
        greeting = 'Your patient consultation is scheduled!'
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Video Consultation - Room Code</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <!-- Header -->
            <div style="background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <div style="background-color: rgba(255,255,255,0.1); border-radius: 50%; width: 80px; height: 80px; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center;">
                    <div style="font-size: 40px;">📹</div>
                </div>
                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: bold;">Video Consultation</h1>
                <p style="color: #ffffff; margin: 10px 0 0 0; font-size: 16px;">{greeting}</p>
            </div>
            
            <!-- Content -->
            <div style="padding: 40px 30px;">
                <h2 style="color: #333333; margin-bottom: 20px; font-size: 24px;">Hello {name}!</h2>
                
                <p style="color: #666666; font-size: 16px; line-height: 1.6; margin-bottom: 25px;">
                    Your video consultation meeting is ready to begin. Please use the room code below to join the session:
                </p>
                
                <!-- Room Code Box -->
                <div style="background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%); padding: 25px; border-radius: 10px; text-align: center; margin: 30px 0;">
                    <p style="color: #ffffff; margin: 0 0 10px 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">Meeting Room Code</p>
                    <div style="background-color: #ffffff; color: #333333; font-size: 32px; font-weight: bold; padding: 15px; border-radius: 8px; letter-spacing: 3px; font-family: 'Courier New', monospace;">
                        {room_id}
                    </div>
                    <p style="color: #ffffff; margin: 15px 0 0 0; font-size: 12px;">Click or copy this code to join the meeting</p>
                </div>
                
                <!-- Role Badge -->
                <div style="text-align: center; margin: 25px 0;">
                    <span style="background-color: {primary_color}; color: #ffffff; padding: 8px 20px; border-radius: 20px; font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">
                        {role_title}
                    </span>
                </div>
                
                <!-- Meeting Instructions -->
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
                    <h3 style="color: #333333; margin: 0 0 15px 0; font-size: 18px;">📋 Meeting Instructions:</h3>
                    <ul style="color: #666666; margin: 0; padding-left: 20px; font-size: 14px; line-height: 1.6;">
                        <li>Use the room code <strong>{room_id}</strong> to join the video consultation</li>
                        <li>Ensure you have a stable internet connection</li>
                        <li>Test your camera and microphone before joining</li>
                        <li>Join a few minutes early to avoid delays</li>
                    </ul>
                </div>
                
                <!-- Technical Requirements -->
                <div style="background-color: #e8f5e8; border-left: 4px solid {primary_color}; padding: 15px; margin: 25px 0;">
                    <h4 style="color: #2e7d32; margin: 0 0 10px 0; font-size: 16px;">💻 Technical Requirements:</h4>
                    <ul style="color: #666666; margin: 0; padding-left: 20px; font-size: 14px;">
                        <li>Web browser (Chrome, Firefox, Safari, Edge)</li>
                        <li>Working camera and microphone</li>
                        <li>Stable internet connection (minimum 1 Mbps)</li>
                        <li>Quiet environment for better consultation experience</li>
                    </ul>
                </div>
                
                <!-- Contact Support -->
                <div style="background-color: #fff3e0; border-left: 4px solid #ff9800; padding: 15px; margin: 25px 0;">
                    <h4 style="color: #ef6c00; margin: 0 0 10px 0; font-size: 16px;">🆘 Need Help?</h4>
                    <p style="color: #666666; margin: 0; font-size: 14px;">
                        If you experience any technical difficulties joining the meeting, please contact our support team immediately.
                    </p>
                </div>
                
                <p style="color: #666666; font-size: 14px; line-height: 1.6; margin-top: 30px;">
                    We look forward to providing you with the best consultation experience possible.
                </p>
                
                <p style="color: #666666; font-size: 14px; margin-top: 20px;">
                    Best regards,<br>
                    <strong style="color: #333333;">ThanuRaksha Medical Team</strong>
                </p>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #333333; padding: 20px; text-align: center; border-radius: 0 0 10px 10px;">
                <p style="color: #ffffff; margin: 0; font-size: 12px;">
                    © 2025 ThanuRaksha. All rights reserved.
                </p>
                <p style="color: #cccccc; margin: 5px 0 0 0; font-size: 12px;">
                    This is an automated message, please do not reply to this email.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'service': 'ThanuRaksha Email Service',
        'version': '1.0.0',
        'endpoints': [
            '/send-email',
            '/send-meeting-invite'
        ]
    }), 200

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    verification_code = data.get('verification_code')  # Changed from 'message' to 'verification_code'

    # Validate required fields
    if not all([name, email, verification_code]):
        return jsonify({'success': False, 'error': 'Missing required fields: name, email, verification_code'}), 400

    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'Email Verification Code - {verification_code}'
        msg['From'] = GMAIL_USER
        msg['To'] = email

        # Create HTML content
        html_content = create_html_email(name, email, verification_code)
        
        # Create plain text version as fallback
        text_content = f"""
        Email Verification

        Hello {name}!

        Thank you for registering with us. Your verification code is: {verification_code}

        Account Details:
        Name: {name}
        Email: {email}

        This verification code will expire in 10 minutes.
        Do not share this code with anyone.

        Best regards,
        The Support Team
        """

        # Attach parts
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        
        msg.attach(part1)
        msg.attach(part2)

        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.send_message(msg)

        return jsonify({'success': True, 'message': 'Verification email sent successfully!'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/send-meeting-invite', methods=['POST'])
def send_meeting_invite():
    data = request.get_json()
    patient_email = data.get('patient_email')
    doctor_email = data.get('doctor_email')
    room_id = data.get('room_id')
    patient_name = data.get('patient_name', 'Patient')  # Optional, defaults to 'Patient'
    doctor_name = data.get('doctor_name', 'Doctor')     # Optional, defaults to 'Doctor'

    # Validate required fields
    if not all([patient_email, doctor_email, room_id]):
        return jsonify({'success': False, 'error': 'Missing required fields: patient_email, doctor_email, room_id'}), 400

    try:
        results = []
        
        # Send email to patient
        try:
            patient_msg = MIMEMultipart('alternative')
            patient_msg['Subject'] = f'Video Consultation Ready - Room Code: {room_id}'
            patient_msg['From'] = GMAIL_USER
            patient_msg['To'] = patient_email

            # Create HTML content for patient
            patient_html = create_meeting_email(patient_name, room_id, 'patient')
            
            # Create plain text version for patient
            patient_text = f"""
            Video Consultation - Room Code

            Hello {patient_name}!

            Your video consultation meeting is ready to begin.
            
            Room Code: {room_id}

            Instructions:
            - Use the room code {room_id} to join the video consultation
            - Ensure you have a stable internet connection
            - Test your camera and microphone before joining
            - Join a few minutes early to avoid delays

            Technical Requirements:
            - Web browser (Chrome, Firefox, Safari, Edge)
            - Working camera and microphone
            - Stable internet connection (minimum 1 Mbps)

            Best regards,
            ThanuRaksha Medical Team
            """

            # Attach parts for patient
            patient_part1 = MIMEText(patient_text, 'plain')
            patient_part2 = MIMEText(patient_html, 'html')
            
            patient_msg.attach(patient_part1)
            patient_msg.attach(patient_part2)

            # Send patient email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(GMAIL_USER, GMAIL_PASS)
                smtp.send_message(patient_msg)
            
            results.append({'recipient': 'patient', 'email': patient_email, 'status': 'sent'})
            
        except Exception as e:
            results.append({'recipient': 'patient', 'email': patient_email, 'status': 'failed', 'error': str(e)})

        # Send email to doctor
        try:
            doctor_msg = MIMEMultipart('alternative')
            doctor_msg['Subject'] = f'Patient Consultation Ready - Room Code: {room_id}'
            doctor_msg['From'] = GMAIL_USER
            doctor_msg['To'] = doctor_email

            # Create HTML content for doctor
            doctor_html = create_meeting_email(doctor_name, room_id, 'doctor')
            
            # Create plain text version for doctor
            doctor_text = f"""
            Patient Consultation - Room Code

            Hello Dr. {doctor_name}!

            Your patient consultation meeting is ready to begin.
            
            Room Code: {room_id}

            Instructions:
            - Use the room code {room_id} to join the video consultation
            - Ensure you have a stable internet connection
            - Test your camera and microphone before joining
            - Join a few minutes early to avoid delays

            Technical Requirements:
            - Web browser (Chrome, Firefox, Safari, Edge)
            - Working camera and microphone
            - Stable internet connection (minimum 1 Mbps)

            Best regards,
            ThanuRaksha Medical Team
            """

            # Attach parts for doctor
            doctor_part1 = MIMEText(doctor_text, 'plain')
            doctor_part2 = MIMEText(doctor_html, 'html')
            
            doctor_msg.attach(doctor_part1)
            doctor_msg.attach(doctor_part2)

            # Send doctor email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(GMAIL_USER, GMAIL_PASS)
                smtp.send_message(doctor_msg)
            
            results.append({'recipient': 'doctor', 'email': doctor_email, 'status': 'sent'})
            
        except Exception as e:
            results.append({'recipient': 'doctor', 'email': doctor_email, 'status': 'failed', 'error': str(e)})

        # Check if both emails were sent successfully
        successful_sends = [r for r in results if r['status'] == 'sent']
        failed_sends = [r for r in results if r['status'] == 'failed']
        
        if len(successful_sends) == 2:
            return jsonify({
                'success': True, 
                'message': 'Meeting invitations sent successfully to both patient and doctor!',
                'details': results
            }), 200
        elif len(successful_sends) == 1:
            return jsonify({
                'success': True, 
                'message': f'Meeting invitation sent successfully to {successful_sends[0]["recipient"]} only. Failed to send to {failed_sends[0]["recipient"]}.',
                'details': results
            }), 207  # Multi-status
        else:
            return jsonify({
                'success': False, 
                'message': 'Failed to send meeting invitations to both recipients.',
                'details': results
            }), 500

    except Exception as e:
        return jsonify({'success': False, 'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 5008))
    app.run(debug=False, host='0.0.0.0', port=port)