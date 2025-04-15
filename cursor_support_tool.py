#!/usr/bin/env python3

import re
import json
import os
import webbrowser
import platform
import datetime
import requests
from pathlib import Path

class CursorLoginHelper:
    def __init__(self):
        self.log_file = "cursor_login_issues.log"
        self.config_file = "cursor_config.json"
        self.support_url = "https://cursor.com/support"
        self.data = {
            "email": "",
            "error_type": "",
            "timestamp": "",
            "device_info": self._get_device_info(),
            "attempts": []
        }
        self._load_config()
        
    def _get_device_info(self):
        """Collect system information for troubleshooting."""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "machine": platform.machine()
        }
        
    def _load_config(self):
        """Load existing configuration if available."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.data = json.load(f)
            except:
                print("Could not load existing configuration. Starting fresh.")
                
    def _save_config(self):
        """Save current configuration."""
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f, indent=2)
        
    def _log_attempt(self, details):
        """Log an attempt with timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {details}\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        self.data["attempts"].append({
            "timestamp": timestamp,
            "details": details
        })
        self._save_config()
        
    def is_valid_email(self, email):
        """Check if email format is valid."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def report_issue(self):
        """Generate a detailed report for support."""
        print("\n===== Issue Report for Cursor AI Support =====")
        print(f"Email: {self.data['email']}")
        print(f"Error Type: {self.data['error_type']}")
        print(f"Device Info: {self.data['device_info']}")
        print(f"Number of attempts: {len(self.data['attempts'])}")
        print("Last 3 attempts:")
        
        for attempt in self.data["attempts"][-3:]:
            print(f"- [{attempt['timestamp']}] {attempt['details']}")
        
        print("\nThis report has been saved to your log file.")
        print("You can attach this information when contacting Cursor support.")
        
    def open_support_page(self):
        """Open the Cursor support page in a browser."""
        try:
            webbrowser.open(self.support_url)
            print(f"Opening {self.support_url} in your browser...")
        except:
            print(f"Could not open the browser. Please visit {self.support_url} manually.")
    
    def check_alternatives(self):
        """Suggest alternative approaches to the user."""
        print("\n===== Alternative Approaches =====")
        print("1. Try using a different email address for registration")
        print("2. Check if your network/VPN might be causing the block")
        print("3. Try using a different authentication method (Google, GitHub)")
        print("4. Contact your organization's admin if using a work email")
        print("5. Clear browser cookies and cache before trying again")
    
    def run(self):
        """Main function to run the helper tool."""
        print("===== Cursor AI Login/Registration Helper =====")
        
        # Get email information
        email = input("Enter the email address that was blocked: ").strip()
        while not self.is_valid_email(email):
            print("Invalid email format. Please enter a valid email address.")
            email = input("Enter the email address that was blocked: ").strip()
        
        self.data["email"] = email
        
        # Get error type
        print("\nWhat type of error are you experiencing?")
        print("1. Access blocked during login")
        print("2. Access blocked during registration")
        print("3. Email verification issues")
        print("4. Other issues")
        
        choice = input("Enter your choice (1-4): ").strip()
        error_types = {
            "1": "Access blocked during login",
            "2": "Access blocked during registration",
            "3": "Email verification issues",
            "4": "Other issues"
        }
        
        self.data["error_type"] = error_types.get(choice, "Unknown error")
        
        # Log this attempt
        details = input("Please describe the exact error message you received: ").strip()
        self._log_attempt(details)
        
        # Show options
        while True:
            print("\n===== Options =====")
            print("1. Report another attempt")
            print("2. Generate support report")
            print("3. Visit Cursor support page")
            print("4. View alternative approaches")
            print("5. Exit")
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                details = input("Please describe the exact error message you received: ").strip()
                self._log_attempt(details)
            elif choice == "2":
                self.report_issue()
            elif choice == "3":
                self.open_support_page()
            elif choice == "4":
                self.check_alternatives()
            elif choice == "5":
                print("Thank you for using the Cursor AI Login Helper.")
                break
            else:
                print("Invalid choice. Please try again.")
        
        self._save_config()


if __name__ == "__main__":
    helper = CursorLoginHelper()
    helper.run()
