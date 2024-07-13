def send_password_template(pin):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your Swar Saadhan PIN</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #000000;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                padding-bottom: 20px;
            }}
            .header img {{
                width: 100px;
            }}
            .content {{
                text-align: center;
            }}
            .pin {{
                font-size: 24px;
                font-weight: bold;
                margin: 20px 0;
                color: #333333;
            }}
            .footer {{
                text-align: center;
                padding-top: 20px;
                font-size: 12px;
                color: #999999;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="your-logo-url" alt="Swar Saadhan Logo">
            </div>
            <div class="content">
                <h2>Your Swar Saadhan PIN</h2>
                <p>Dear user,</p>
                <p>Your PIN for Swar Saadhan is:</p>
                <div class="pin">{pin }</div>
                <p>Please use this PIN to proceed with your login.</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 Swar Saadhan. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
