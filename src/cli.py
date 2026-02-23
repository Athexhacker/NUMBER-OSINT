#!/usr/bin/env python3
"""
Phone Number Intelligence Tool - OSINT Framework
Use only for legitimate security research or investigations you're authorized to conduct
"""

import re
import sys
import json
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from datetime import datetime
import argparse
import webbrowser
import concurrent.futures
from urllib.parse import quote
import warnings
warnings.filterwarnings('ignore')

class PhoneNumberIntelligenceTool:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.results = {
            'basic_info': {},
            'carrier_info': {},
            'location_info': {},
            'social_media': [],
            'data_breaches': [],
            'google_dorks': [],
            'possible_accounts': [],
            'security_risks': []
        }
        
    def validate_and_format(self):
        """Validate and parse the phone number"""
        try:
            parsed = phonenumbers.parse(self.phone_number, None)
            if not phonenumbers.is_valid_number(parsed):
                raise ValueError("Invalid phone number")
            
            self.parsed_number = parsed
            self.country_code = parsed.country_code
            self.national_number = parsed.national_number
            self.formatted_international = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
            self.formatted_e164 = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164
            )
            return True
        except Exception as e:
            print(f"Error parsing number: {e}")
            return False
    
    def get_basic_information(self):
        """Get basic carrier and location info"""
        try:
            # Carrier information
            service_provider = carrier.name_for_number(self.parsed_number, "en")
            self.results['basic_info']['carrier'] = service_provider
            
            # Location information
            location = geocoder.description_for_number(self.parsed_number, "en")
            self.results['basic_info']['location'] = location
            
            # Timezone
            time_zones = timezone.time_zones_for_number(self.parsed_number)
            self.results['basic_info']['timezone'] = list(time_zones)
            
            # Number type
            number_type = phonenumbers.number_type(self.parsed_number)
            type_map = {
                0: "FIXED_LINE",
                1: "MOBILE",
                2: "FIXED_LINE_OR_MOBILE",
                3: "TOLL_FREE",
                4: "PREMIUM_RATE",
                5: "SHARED_COST",
                6: "VOIP",
                7: "PERSONAL_NUMBER",
                8: "PAGER",
                9: "UAN",
                10: "VOICEMAIL",
                27: "UNKNOWN"
            }
            self.results['basic_info']['type'] = type_map.get(number_type, "UNKNOWN")
            
            # Check if possible VoIP
            if number_type == 6:
                self.results['security_risks'].append("Number identified as VoIP (could be temporary/disposable)")
            
        except Exception as e:
            print(f"Error getting basic info: {e}")
    
    def generate_google_dorks(self):
        """Generate Google dorks for OSINT gathering"""
        number_variations = [
            self.formatted_e164,
            self.formatted_international,
            str(self.national_number),
            f"{self.country_code}{self.national_number}",
            f"+{self.country_code}{self.national_number}",
            f"{self.country_code} {self.national_number}",
        ]
        
        dork_templates = [
            'intext:"{}" site:facebook.com',
            'intext:"{}" site:twitter.com',
            'intext:"{}" site:instagram.com',
            'intext:"{}" site:linkedin.com',
            'intext:"{}" site:whatsapp.com',
            'intext:"{}" site:telegram.org',
            'intext:"{}" site:github.com',
            'intext:"{}" site:pastebin.com',
            'intext:"{}" "contact" OR "phone"',
            '"{}" filetype:pdf OR filetype:doc OR filetype:xls',
            'inurl:"{}" OR intitle:"{}"',
            '"{}" "sign up" OR "register" OR "account"',
            '"{}" "recovery" OR "verification" OR "security"',
            '"{}" "leak" OR "breach" OR "database"',
            'site:haveibeenpwned.com "{}"',
        ]
        
        for number in set(number_variations):
            for template in dork_templates:
                if '{}' in template:
                    dork = template.format(number.replace('+', '').replace(' ', ''))
                    self.results['google_dorks'].append(dork)
        
        # Social media specific dorks
        social_dorks = [
            f'site:facebook.com "mobile" "{self.national_number}"',
            f'site:twitter.com "phone" "{self.country_code}"',
            f'site:linkedin.com "contact" "{self.formatted_e164}"',
            f'site:instagram.com "phone" "{self.national_number}"',
        ]
        self.results['google_dorks'].extend(social_dorks)
    
    def check_social_media_patterns(self):
        """Generate potential social media links"""
        base_urls = {
            'Facebook': [
                f'https://www.facebook.com/search/top?q={quote(self.formatted_e164)}',
                f'https://www.facebook.com/login/identify?ctx=recover&lwv=110&email={quote(self.formatted_e164)}'
            ],
            'Twitter': [
                f'https://twitter.com/search?q={quote(self.formatted_e164)}&src=typed_query'
            ],
            'Instagram': [
                f'https://www.instagram.com/accounts/account_recovery/?phone_number={self.country_code}{self.national_number}'
            ],
            'LinkedIn': [
                f'https://www.linkedin.com/search/results/all/?keywords={quote(self.formatted_e164)}'
            ],
            'Telegram': [
                f'https://t.me/{self.formatted_e164.replace("+", "")}',
                f'https://t.me/+{self.country_code}{self.national_number}'
            ],
            'WhatsApp': [
                f'https://wa.me/{self.country_code}{self.national_number}'
            ],
            'Signal': [
                f'signal.me/#p/+{self.country_code}{self.national_number}'
            ],
            'Truecaller': [
                f'https://www.truecaller.com/search/{self.country_code}/{self.national_number}'
            ],
            'Whitepages': [
                f'https://www.whitepages.com/phone/{self.formatted_e164.replace("+", "")}'
            ],
            'SpyDialer': [
                f'https://www.spydialer.com/default.aspx?phone={self.country_code}{self.national_number}'
            ],
            'FastPeopleSearch': [
                f'https://www.fastpeoplesearch.com/{self.country_code}{self.national_number}'
            ]
        }
        
        for platform, urls in base_urls.items():
            for url in urls:
                self.results['social_media'].append({
                    'platform': platform,
                    'url': url,
                    'check_method': 'direct_link'
                })
    
    def check_data_breaches(self):
        """Check if number appears in known data breaches"""
        # Note: This is a placeholder. Actual breach checking requires APIs
        # like HaveIBeenPwned (which doesn't support phone numbers directly)
        
        # Simulated breach check via search patterns
        breach_patterns = [
            f'site:haveibeenpwned.com "{self.formatted_e164}"',
            f'site:dehashed.com "{self.formatted_e164}"',
            f'site:breachalarm.com "{self.formatted_e164}"',
            f'"phone:{self.formatted_e164}" "breach" OR "leak"',
            f'"{self.national_number}" "database dump" OR "data leak"',
        ]
        
        self.results['data_breaches'] = breach_patterns
        
        # Check recycled number databases (conceptual)
        recycled_checks = [
            f'site:recyclednumbers.com "{self.formatted_e164}"',
            f'site:numberguru.com "{self.formatted_e164}"',
        ]
        self.results['data_breaches'].extend(recycled_checks)
    
    def search_public_records(self):
        """Generate searches for public records (US focused)"""
        if self.country_code == 1:  # US/Canada
            public_record_sites = [
                f'https://www.instantcheckmate.com/search/phone/{self.national_number}',
                f'https://www.intelius.com/phone/{self.formatted_e164.replace("+", "")}',
                f'https://thatsthem.com/phone/{self.formatted_e164}',
                f'https://www.zabasearch.com/phone/{self.formatted_e164}/',
                f'https://www.411.com/phone/{self.formatted_e164}',
            ]
            self.results['possible_accounts'].extend([
                {'type': 'public_record', 'source': site} 
                for site in public_record_sites
            ])
    
    def check_messaging_apps(self):
        """Check for presence on messaging platforms"""
        messaging_checks = [
            {'app': 'WhatsApp', 'url': f'https://wa.me/{self.country_code}{self.national_number}'},
            {'app': 'Telegram', 'url': f'https://t.me/+{self.country_code}{self.national_number}'},
            {'app': 'Signal', 'url': f'signal.me/#p/+{self.country_code}{self.national_number}'},
            {'app': 'Viber', 'url': f'viber://add?number={self.country_code}{self.national_number}'},
            {'app': 'WeChat', 'url': f'weixin.qq.com/search?query={self.formatted_e164}'},
            {'app': 'Line', 'url': f'line.me/R/ti/p/~{self.country_code}{self.national_number}'},
        ]
        
        for check in messaging_checks:
            self.results['possible_accounts'].append({
                'type': 'messaging_app',
                'app': check['app'],
                'check_url': check['url']
            })
    
    def generate_report(self):
        """Generate comprehensive report"""
        report = f"""
╔══════════════════════════════════════════════════════════╗
║            PHONE NUMBER INTELLIGENCE REPORT              ║
╚══════════════════════════════════════════════════════════╝

📱 TARGET NUMBER: {self.formatted_international}
📅 REPORT GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

────────────────────────────────────────────────────────────
📊 BASIC INFORMATION
────────────────────────────────────────────────────────────
• Carrier: {self.results['basic_info'].get('carrier', 'N/A')}
• Location: {self.results['basic_info'].get('location', 'N/A')}
• Timezone: {', '.join(self.results['basic_info'].get('timezone', []))}
• Number Type: {self.results['basic_info'].get('type', 'N/A')}
• Country Code: +{self.country_code}
• National Number: {self.national_number}

────────────────────────────────────────────────────────────
🔍 SOCIAL MEDIA & PLATFORM CHECKS
────────────────────────────────────────────────────────────
"""
        
        for item in self.results['social_media']:
            report += f"• {item['platform']}: {item['url']}\n"
        
        report += """
────────────────────────────────────────────────────────────
🎯 GOOGLE DORKS FOR OSINT GATHERING
────────────────────────────────────────────────────────────
"""
        for i, dork in enumerate(self.results['google_dorks'][:15], 1):
            report += f"{i}. {dork}\n"
        
        report += """
────────────────────────────────────────────────────────────
📱 MESSAGING APPS PRESENCE
────────────────────────────────────────────────────────────
"""
        for item in [x for x in self.results['possible_accounts'] if x['type'] == 'messaging_app']:
            report += f"• {item['app']}: {item['check_url']}\n"
        
        if self.results['security_risks']:
            report += """
────────────────────────────────────────────────────────────
⚠️  SECURITY RISKS IDENTIFIED
────────────────────────────────────────────────────────────
"""
            for risk in self.results['security_risks']:
                report += f"• {risk}\n"
        
        report += """
────────────────────────────────────────────────────────────
📋 RECOMMENDED ACTIONS
────────────────────────────────────────────────────────────
1. Copy Google dorks and paste in browser for manual verification
2. Check social media links for account associations
3. Verify messaging app presence using provided links
4. Search public records if applicable
5. Document findings for legitimate investigation purposes

⚠️  LEGAL & ETHICAL DISCLAIMER
────────────────────────────────────────────────────────────
This tool is for:
• Security research on your own numbers
• Authorized penetration testing
• Legitimate investigations with proper authorization

NOT for:
• Stalking or harassment
• Unauthorized surveillance
• Illegal data collection

Always comply with local laws and privacy regulations.
"""
        return report
    
    def save_results(self, filename=None):
        """Save results to file"""
        if not filename:
            filename = f"phone_intel_{self.national_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_report())
        
        # Also save JSON data
        json_file = filename.replace('.txt', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"Results saved to {filename} and {json_file}")
        return filename
    
    def open_web_checks(self):
        """Open key web checks in browser (optional)"""
        key_checks = [
            item['url'] for item in self.results['social_media'][:5]
        ]
        
        print("Opening key web checks in browser...")
        for url in key_checks:
            webbrowser.open_new_tab(url)
    
    def run_full_scan(self):
        """Execute all checks"""
        print(f"[+] Starting intelligence gathering for: {self.phone_number}")
        
        if not self.validate_and_format():
            print("[-] Invalid phone number format")
            return False
        
        print("[+] Gathering basic information...")
        self.get_basic_information()
        
        print("[+] Generating Google dorks...")
        self.generate_google_dorks()
        
        print("[+] Checking social media patterns...")
        self.check_social_media_patterns()
        
        print("[+] Checking data breach patterns...")
        self.check_data_breaches()
        
        print("[+] Searching public records...")
        self.search_public_records()
        
        print("[+] Checking messaging apps...")
        self.check_messaging_apps()
        
        print("[+] Scan completed!")
        return True

def main():
    parser = argparse.ArgumentParser(
        description='Phone Number Intelligence Gathering Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s +1234567890
  %(prog)s 1234567890 --country US
  %(prog)s +441234567890 --output report.txt
  %(prog)s +1234567890 --web
        """
    )
    
    parser.add_argument('phone', help='Phone number to investigate')
    parser.add_argument('--country', default=None, 
                       help='Country code (e.g., US, GB) if number lacks country code')
    parser.add_argument('--output', '-o', help='Output file name')
    parser.add_argument('--web', '-w', action='store_true', 
                       help='Open web checks in browser')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Quiet mode (no console output)')
    
    args = parser.parse_args()
    
    # Format phone number
    phone_input = args.phone
    if not phone_input.startswith('+') and args.country:
        try:
            parsed = phonenumbers.parse(phone_input, args.country)
            phone_input = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164
            )
        except:
            pass
    
    # Initialize tool
    tool = PhoneNumberIntelligenceTool(phone_input)
    
    # Run scan
    if tool.run_full_scan():
        # Generate report
        report = tool.generate_report()
        
        if not args.quiet:
            print(report)
        
        # Save results
        saved_file = tool.save_results(args.output)
        
        # Open web checks if requested
        if args.web:
            tool.open_web_checks()
        
        print(f"\n[+] Analysis complete. Results saved to {saved_file}")
        
        # Print quick summary
        if not args.quiet:
            print("\n📋 Quick Summary:")
            print(f"   Carrier: {tool.results['basic_info'].get('carrier', 'N/A')}")
            print(f"   Location: {tool.results['basic_info'].get('location', 'N/A')}")
            print(f"   Google Dorks Generated: {len(tool.results['google_dorks'])}")
            print(f"   Social Media Checks: {len(tool.results['social_media'])}")
    
    else:
        print("[-] Scan failed. Please check the phone number format.")

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║     PHONE NUMBER OSINT GATHERING TOOL v1.0           ║
    ║     For Authorized Security Research Only            ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Check dependencies
    try:
        import phonenumbers
    except ImportError:
        print("Please install required packages:")
        print("pip install phonenumbers requests")
        sys.exit(1)
    
    main()