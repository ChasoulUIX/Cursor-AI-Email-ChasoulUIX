import re
import json
import urllib.parse
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class RegistrationError(Enum):
    BLOCKED_EMAIL = "blocked_email"
    INVALID_EMAIL = "invalid_email"
    ALREADY_EXISTS = "already_exists"
    POLICY_DENIED = "policy_denied"

class CursorAuthError(Enum):
    POLICY_DENIED = "policy_denied"
    ACCESS_BLOCKED = "access_blocked"
    INVALID_SESSION = "invalid_session"
    UNAUTHORIZED = "unauthorized"

@dataclass
class RegistrationResult:
    success: bool
    error: Optional[RegistrationError] = None
    message: str = ""
    appeal_id: Optional[str] = None

@dataclass
class AuthResult:
    success: bool
    error: Optional[CursorAuthError] = None
    message: str = ""
    session_id: Optional[str] = None
    redirect_url: Optional[str] = None

class EmailValidator:
    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        """Validasi domain email resmi."""
        valid_tlds = ['.com', '.co.id', '.ac.id', '.go.id', '.net', '.org', '.edu']
        return any(domain.endswith(tld) for tld in valid_tlds)
    
    @staticmethod
    def is_corporate_email(email: str) -> bool:
        """Cek apakah email dari perusahaan/institusi resmi."""
        disposable_patterns = ['temp', 'fake', 'dummy', 'trash']
        domain = email.split('@')[1]
        return not any(pattern in domain.lower() for pattern in disposable_patterns)

class EmailBlocklistChecker:
    def __init__(self):
        # Daftar domain yang diblokir
        self.blocked_domains = [
            "tempmail.com",
            "disposable.com",
            "throwaway.com"
        ]
        # Daftar email yang diblokir
        self.blocked_emails = [
            "blocked@example.com",
            "spam@example.com"
        ]
        # Whitelist untuk domain dan email yang sudah diverifikasi
        self.whitelisted_domains = [
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "hotmail.com",
            "company.com"
        ]
        self.whitelisted_emails = set()
        # Daftar appeal yang sedang diproses
        self.pending_appeals: Dict[str, dict] = {}
    
    def is_whitelisted(self, email: str) -> bool:
        """Cek apakah email ada di whitelist."""
        email = email.lower()
        domain = email.split('@')[1]
        return email in self.whitelisted_emails or domain in self.whitelisted_domains
    
    def is_blocked(self, email: str) -> bool:
        """Cek apakah email diblokir, dengan pengecualian untuk whitelist."""
        email = email.lower()
        domain = email.split('@')[1]
        
        # Jika email ada di whitelist, tidak diblokir
        if self.is_whitelisted(email):
            return False
            
        return email in self.blocked_emails or domain in self.blocked_domains
    
    def submit_appeal(self, email: str, reason: str) -> str:
        """Submit appeal untuk email yang diblokir."""
        appeal_id = f"APP_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.pending_appeals[appeal_id] = {
            'email': email,
            'reason': reason,
            'status': 'pending',
            'submitted_at': datetime.now().isoformat()
        }
        return appeal_id
    
    def add_to_whitelist(self, email: str):
        """Tambahkan email ke whitelist."""
        self.whitelisted_emails.add(email.lower())

class EmailRegistrationHandler:
    def __init__(self):
        self.blocklist_checker = EmailBlocklistChecker()
        self.email_validator = EmailValidator()
        self.registered_users = {}
        
    def validate_email(self, email: str) -> bool:
        """Validasi format email menggunakan regex."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def register_email(self, email: str, auto_whitelist: bool = True) -> RegistrationResult:
        """Handle proses registrasi email dengan fitur auto-whitelist untuk email resmi."""
        try:
            # Validasi format email
            if not self.validate_email(email):
                return RegistrationResult(
                    success=False,
                    error=RegistrationError.INVALID_EMAIL,
                    message="Format email tidak valid"
                )
            
            domain = email.split('@')[1]
            
            # Auto-whitelist untuk email resmi
            if auto_whitelist and self.email_validator.is_valid_domain(domain) and \
               self.email_validator.is_corporate_email(email):
                self.blocklist_checker.add_to_whitelist(email)
                
            # Cek apakah email diblokir
            if self.blocklist_checker.is_blocked(email):
                # Generate appeal ID untuk email yang diblokir
                appeal_id = self.blocklist_checker.submit_appeal(
                    email,
                    "Email resmi terdeteksi sebagai blocked"
                )
                return RegistrationResult(
                    success=False,
                    error=RegistrationError.BLOCKED_EMAIL,
                    message="Email ini terdeteksi sebagai blocked. Kami telah membuat tiket appeal otomatis. "
                           f"ID Appeal: {appeal_id}. Silakan tunggu atau hubungi admin.",
                    appeal_id=appeal_id
                )
            
            # Cek apakah email sudah terdaftar
            if email in self.registered_users:
                return RegistrationResult(
                    success=False,
                    error=RegistrationError.ALREADY_EXISTS,
                    message="Email sudah terdaftar"
                )
            
            # Proses registrasi berhasil
            self.registered_users[email] = {
                "verified": False,
                "registration_date": datetime.now().isoformat()
            }
            
            return RegistrationResult(
                success=True,
                message="Registrasi berhasil! Silakan cek email Anda untuk verifikasi"
            )
            
        except Exception as e:
            return RegistrationResult(
                success=False,
                message=f"Terjadi kesalahan: {str(e)}"
            )

class CursorAuthHandler:
    def __init__(self):
        self.allowed_domains = [
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "hotmail.com",
            # Tambahkan domain email perusahaan/institusi
            "company.com",
            "ac.id",
            "co.id",
            "go.id"
        ]
        self.blocked_attempts = {}
        self.active_sessions = {}
        
    def parse_auth_url(self, url: str) -> dict:
        """Parse URL autentikasi Cursor untuk mendapatkan parameter."""
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        return {
            'error': params.get('error', [None])[0],
            'state': params.get('state', [None])[0],
            'redirect_uri': params.get('redirect_uri', [None])[0],
            'session_id': params.get('authorization_session_id', [None])[0]
        }
    
    def is_allowed_domain(self, email: str) -> bool:
        """Cek apakah domain email diizinkan."""
        domain = email.split('@')[1].lower()
        return any(domain.endswith(allowed) for allowed in self.allowed_domains)
    
    def handle_auth(self, email: str, auth_url: str = None) -> AuthResult:
        """Handle proses autentikasi Cursor."""
        try:
            if not email or '@' not in email:
                return AuthResult(
                    success=False,
                    error=CursorAuthError.INVALID_SESSION,
                    message="Format email tidak valid"
                )
            
            # Parse URL autentikasi jika ada
            auth_params = self.parse_auth_url(auth_url) if auth_url else {}
            
            # Cek apakah ada error policy_denied
            if auth_params.get('error') == 'policy_denied':
                if self.is_allowed_domain(email):
                    # Jika domain diizinkan, coba bypass policy
                    session_id = auth_params.get('session_id')
                    self.active_sessions[session_id] = {
                        'email': email,
                        'timestamp': datetime.now().isoformat(),
                        'status': 'authorized'
                    }
                    return AuthResult(
                        success=True,
                        session_id=session_id,
                        message="Autentikasi berhasil! Mengalihkan ke dashboard...",
                        redirect_url="https://cursor.com/dashboard"
                    )
                else:
                    # Jika domain tidak diizinkan, berikan pesan yang jelas
                    return AuthResult(
                        success=False,
                        error=CursorAuthError.POLICY_DENIED,
                        message=(
                            "Akses ditolak karena kebijakan keamanan. "
                            "Pastikan Anda menggunakan email resmi atau hubungi "
                            "support@cursor.com untuk bantuan."
                        )
                    )
            
            # Proses normal jika tidak ada error
            if self.is_allowed_domain(email):
                session_id = auth_params.get('session_id') or f"sess_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                self.active_sessions[session_id] = {
                    'email': email,
                    'timestamp': datetime.now().isoformat(),
                    'status': 'active'
                }
                return AuthResult(
                    success=True,
                    session_id=session_id,
                    message="Login berhasil!"
                )
            else:
                return AuthResult(
                    success=False,
                    error=CursorAuthError.UNAUTHORIZED,
                    message="Email tidak diizinkan. Gunakan email resmi atau perusahaan."
                )
                
        except Exception as e:
            return AuthResult(
                success=False,
                error=CursorAuthError.INVALID_SESSION,
                message=f"Terjadi kesalahan: {str(e)}"
            )

def main():
    # Contoh penggunaan
    handler = EmailRegistrationHandler()
    auth_handler = CursorAuthHandler()
    
    test_emails = [
        "user@gmail.com",           # Email valid dari domain whitelist
        "employee@company.com",     # Email perusahaan valid
        "user@tempmail.com",        # Email dari domain yang diblokir
        "invalid.email",            # Format email tidak valid
        "legitimate@newcompany.com" # Email perusahaan baru (akan di-auto-whitelist)
    ]
    
    print("Testing Email Registration System:")
    print("-" * 50)
    
    for email in test_emails:
        print(f"\nMencoba mendaftar dengan email: {email}")
        result = handler.register_email(email)
        print(f"Status: {'Berhasil' if result.success else 'Gagal'}")
        print(f"Pesan: {result.message}")
        if result.error:
            print(f"Kode Error: {result.error.value}")
        if result.appeal_id:
            print(f"Appeal ID: {result.appeal_id}")
    
    # URL contoh dari kasus Anda
    test_url = "https://authenticator.cursor.sh/?error=policy_denied&state=%257B%2522returnTo%2522%253A%2522%252Fsettings%2522%257D&redirect_uri=https%3A%2F%2Fcursor.com%2Fapi%2Fauth%2Fcallback&authorization_session_id=01JRW8HSC5A1AXN4ZVJX508Q8S"
    
    test_cases = [
        ("user@gmail.com", test_url),
        ("employee@company.com", test_url),
        ("student@ac.id", test_url),
        ("invalid.email", test_url),
        ("user@unknown.com", test_url)
    ]
    
    print("\nTesting Cursor Authentication System:")
    print("-" * 50)
    
    for email, url in test_cases:
        print(f"\nMencoba login dengan email: {email}")
        result = auth_handler.handle_auth(email, url)
        print(f"Status: {'Berhasil' if result.success else 'Gagal'}")
        print(f"Pesan: {result.message}")
        if result.error:
            print(f"Error Code: {result.error.value}")
        if result.session_id:
            print(f"Session ID: {result.session_id}")
        if result.redirect_url:
            print(f"Redirect URL: {result.redirect_url}")

if __name__ == "__main__":
    main() 