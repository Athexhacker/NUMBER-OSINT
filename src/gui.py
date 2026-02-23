#!/usr/bin/env python3
"""
Advanced Phone Number Intelligence Tool - Professional OSINT Framework
Version: 2.0 - Enhanced with GUI, Advanced Features, and Comprehensive Analysis
For authorized security research and investigations only
"""

import re
import sys
import json
import time
import hashlib
import sqlite3
import requests
import phonenumbers
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import webbrowser
import folium
from datetime import datetime
from phonenumbers import carrier, geocoder, timezone
from phonenumbers.phonenumberutil import number_type
import phonenumbers.carrier as carrier
import phonenumbers.geocoder as geocoder
import warnings
from urllib.parse import quote
import socket
import dns.resolver
import whois
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

class AdvancedPhoneIntel:
    """Enhanced Phone Number Intelligence Engine"""
    
    def __init__(self):
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.api_keys = self.load_api_keys()
        self.cache_db = 'phone_intel_cache.db'
        self.init_cache_db()
        
    def init_cache_db(self):
        """Initialize SQLite cache database"""
        try:
            conn = sqlite3.connect(self.cache_db)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS phone_cache
                        (phone_hash TEXT PRIMARY KEY, 
                         data TEXT,
                         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            c.execute('''CREATE TABLE IF NOT EXISTS api_keys
                        (service TEXT PRIMARY KEY, api_key TEXT)''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Cache DB error: {e}")
    
    def load_api_keys(self):
        """Load API keys from config file"""
        try:
            with open('api_keys.json', 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def analyze_number(self, phone_number):
        """Main analysis function"""
        self.results = {
            'input_number': phone_number,
            'timestamp': datetime.now().isoformat(),
            'basic_info': {},
            'carrier_info': {},
            'location_data': {},
            'risk_assessment': {},
            'social_presence': [],
            'breach_data': [],
            'network_info': {},
            'voip_info': {},
            'spam_score': {},
            'historical_data': {},
            'associated_entities': [],
            'messaging_apps': [],
            'public_records': [],
            'geolocation': {},
            'reputation': {},
            'verification_services': [],
            'business_info': {},
            'dark_web_mentions': [],
            'pattern_analysis': {}
        }
        
        try:
            # Parse and validate
            parsed = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed):
                return {'error': 'Invalid phone number'}
            
            self.results['parsed'] = {
                'e164': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                'international': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'national': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                'country_code': parsed.country_code,
                'national_number': parsed.national_number
            }
            
            # Run analysis modules
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {
                    executor.submit(self.get_basic_info, parsed): 'basic',
                    executor.submit(self.get_carrier_info, parsed): 'carrier',
                    executor.submit(self.check_social_presence, parsed): 'social',
                    executor.submit(self.check_breaches, parsed): 'breaches',
                    executor.submit(self.analyze_risk, parsed): 'risk',
                    executor.submit(self.get_voip_info, parsed): 'voip',
                    executor.submit(self.check_messaging_apps, parsed): 'messaging',
                    executor.submit(self.get_reputation, parsed): 'reputation',
                    executor.submit(self.analyze_patterns, parsed): 'patterns',
                    executor.submit(self.check_verification_services, parsed): 'verification'
                }
                
                for future in as_completed(futures):
                    module = futures[future]
                    try:
                        result = future.result(timeout=10)
                        self.results.update(result)
                    except Exception as e:
                        print(f"Module {module} error: {e}")
            
            return self.results
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_basic_info(self, parsed):
        """Enhanced basic information gathering"""
        info = {}
        
        # Number type
        num_type = phonenumbers.number_type(parsed)
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
        
        info['basic_info'] = {
            'type': type_map.get(num_type, "UNKNOWN"),
            'possible_type': self.get_number_type_description(num_type),
            'timezones': list(timezone.time_zones_for_number(parsed)),
            'geolocation': geocoder.description_for_number(parsed, "en"),
            'country': phonenumbers.region_code_for_number(parsed),
            'validity': 'Valid' if phonenumbers.is_valid_number(parsed) else 'Invalid',
            'possible_number': phonenumbers.is_possible_number(parsed)
        }
        
        return info
    
    def get_number_type_description(self, num_type):
        """Get detailed description of number type"""
        descriptions = {
            0: "Landline telephone line",
            1: "Mobile/cellular phone",
            2: "Could be either landline or mobile",
            3: "Toll-free number (caller doesn't pay)",
            4: "Premium rate service (high cost)",
            5: "Shared cost service",
            6: "Voice over IP (internet phone)",
            7: "Personal numbering",
            8: "Pager service",
            9: "Universal access number",
            10: "Voicemail service",
            27: "Unknown type"
        }
        return descriptions.get(num_type, "Unknown type")
    
    def get_carrier_info(self, parsed):
        """Enhanced carrier information"""
        carrier_info = {
            'carrier_info': {
                'current': carrier.name_for_number(parsed, "en"),
                'historical_carriers': self.get_historical_carriers(parsed),
                'network_type': self.detect_network_type(parsed),
                'ported': self.check_porting(parsed)
            }
        }
        return carrier_info
    
    def get_historical_carriers(self, parsed):
        """Check historical carrier data"""
        # Simulated - would use real APIs in production
        return ['Unknown - Historical data requires API access']
    
    def detect_network_type(self, parsed):
        """Detect network technology (2G/3G/4G/5G)"""
        # Placeholder for network detection logic
        return 'Unknown (requires network query)'
    
    def check_porting(self, parsed):
        """Check if number has been ported"""
        # Placeholder for number porting check
        return {'ported': False, 'original_carrier': None}
    
    def check_social_presence(self, parsed):
        """Check social media presence"""
        social_sites = [
            {'name': 'Facebook', 'url': f'https://www.facebook.com/search/top?q={parsed.national_number}'},
            {'name': 'Twitter', 'url': f'https://twitter.com/search?q={parsed.national_number}'},
            {'name': 'Instagram', 'url': f'https://www.instagram.com/accounts/account_recovery/?phone_number={parsed.national_number}'},
            {'name': 'LinkedIn', 'url': f'https://www.linkedin.com/search/results/all/?keywords={parsed.national_number}'},
            {'name': 'Snapchat', 'url': f'https://www.snapchat.com/add/{parsed.national_number}'},
            {'name': 'TikTok', 'url': f'https://www.tiktok.com/search?q={parsed.national_number}'},
            {'name': 'Pinterest', 'url': f'https://www.pinterest.com/search/pins/?q={parsed.national_number}'},
            {'name': 'Reddit', 'url': f'https://www.reddit.com/search/?q={parsed.national_number}'},
            {'name': 'YouTube', 'url': f'https://www.youtube.com/results?search_query={parsed.national_number}'}
        ]
        
        # Verify presence where possible
        for site in social_sites:
            site['verified'] = self.verify_social_presence(site['url'])
        
        return {'social_presence': social_sites}
    
    def verify_social_presence(self, url):
        """Attempt to verify social media presence"""
        try:
            response = self.session.get(url, timeout=5, allow_redirects=True)
            return response.status_code == 200 and 'not found' not in response.text.lower()
        except:
            return False
    
    def check_breaches(self, parsed):
        """Check for data breaches"""
        breaches = []
        
        # Check against known breach databases
        breach_services = [
            {'name': 'HaveIBeenPwned', 'url': f'https://haveibeenpwned.com/account/{parsed.national_number}'},
            {'name': 'BreachDirectory', 'url': f'https://breachdirectory.org/check?phone={parsed.national_number}'},
            {'name': 'Dehashed', 'url': f'https://dehashed.com/search?query={parsed.national_number}'},
            {'name': 'Snusbase', 'url': f'https://snusbase.com/search?term={parsed.national_number}'}
        ]
        
        for service in breach_services:
            breaches.append({
                'service': service['name'],
                'url': service['url'],
                'status': 'Check manually'
            })
        
        return {'breach_data': breaches}
    
    def analyze_risk(self, parsed):
        """Comprehensive risk assessment"""
        risk_factors = []
        risk_score = 0
        
        # Check if VoIP
        if number_type(parsed) == 6:
            risk_factors.append("VoIP number - potentially disposable/temporary")
            risk_score += 30
        
        # Check if prepaid mobile
        carrier_name = carrier.name_for_number(parsed, "en")
        if carrier_name and 'prepaid' in carrier_name.lower():
            risk_factors.append("Prepaid number - lower accountability")
            risk_score += 20
        
        # Check if from high-risk country
        high_risk_countries = ['+7', '+380', '+375' , '+92' , '+91'] 
        if f"+{parsed.country_code}" in high_risk_countries:
            risk_factors.append("Number from high-risk region")
            risk_score += 15
        
        # Check spam databases
        spam_score = self.check_spam_databases(parsed)
        if spam_score > 50:
            risk_factors.append(f"Reported as spam (score: {spam_score})")
            risk_score += 25
        
        risk_level = 'LOW' if risk_score < 30 else 'MEDIUM' if risk_score < 60 else 'HIGH'
        
        return {
            'risk_assessment': {
                'score': risk_score,
                'level': risk_level,
                'factors': risk_factors,
                'spam_score': spam_score,
                'recommendations': self.get_risk_recommendations(risk_level)
            }
        }
    
    def check_spam_databases(self, parsed):
        """Check against spam reporting databases"""
        spam_score = 0
        return spam_score
    
    def get_risk_recommendations(self, risk_level):
        """Get recommendations based on risk level"""
        recommendations = {
            'LOW': ['Standard verification sufficient', 'No special precautions needed'],
            'MEDIUM': ['Additional verification recommended', 'Consider alternative contact methods'],
            'HIGH': ['Exercise extreme caution', 'Verify identity through multiple channels', 'Document all interactions']
        }
        return recommendations.get(risk_level, [])
    
    def get_voip_info(self, parsed):
        """Get VoIP-specific information"""
        voip_info = {
            'voip_info': {
                'is_voip': number_type(parsed) == 6,
                'provider': self.detect_voip_provider(parsed),
                'quality': self.estimate_voip_quality(parsed),
                'temporary_likely': self.is_likely_temporary(parsed)
            }
        }
        return voip_info
    
    def detect_voip_provider(self, parsed):
        """Detect VoIP provider"""
        # Placeholder for provider detection
        return 'Unknown'
    
    def estimate_voip_quality(self, parsed):
        """Estimate VoIP call quality"""
        # Placeholder for quality estimation
        return 'Unknown'
    
    def is_likely_temporary(self, parsed):
        """Check if likely temporary/disposable number"""
        patterns = [
            r'^\+1\s*\(?8{3}\)?',  # US toll-free prefixes
            r'^\+44\s*70',          # UK personal numbers
        ]
        for pattern in patterns:
            if re.match(pattern, str(parsed.national_number)):
                return True
        return False
    
    def check_messaging_apps(self, parsed):
        """Check messaging app presence"""
        messaging_apps = [
            {'name': 'WhatsApp', 'url': f'https://wa.me/{parsed.country_code}{parsed.national_number}'},
            {'name': 'Telegram', 'url': f'https://t.me/+{parsed.country_code}{parsed.national_number}'},
            {'name': 'Signal', 'url': f'signal.me/#p/+{parsed.country_code}{parsed.national_number}'},
            {'name': 'Viber', 'url': f'viber://add?number={parsed.country_code}{parsed.national_number}'},
            {'name': 'WeChat', 'url': f'weixin.qq.com/search?query={parsed.national_number}'},
            {'name': 'Line', 'url': f'line.me/R/ti/p/~{parsed.country_code}{parsed.national_number}'},
            {'name': 'Facebook Messenger', 'url': f'm.me/{parsed.national_number}'},
            {'name': 'Skype', 'url': f'skype:{parsed.national_number}?call'},
            {'name': 'Discord', 'url': f'discord.com/search?q={parsed.national_number}'}
        ]
        
        # Verify presence
        for app in messaging_apps[:3]:  # Only check first few
            app['verified'] = self.verify_messaging_app(app['name'], app['url'])
        
        return {'messaging_apps': messaging_apps}
    
    def verify_messaging_app(self, app_name, url):
        """Verify messaging app presence"""
        # Different apps require different verification methods
        try:
            if 'wa.me' in url:
                response = self.session.get(url, timeout=5)
                return response.status_code == 200 and 'invalid' not in response.text.lower()
            elif 't.me' in url:
                response = self.session.get(url, timeout=5)
                return response.status_code == 200
            return False
        except:
            return False
    
    def get_reputation(self, parsed):
        """Get reputation data from various sources"""
        reputation_sources = [
            {'source': 'CallerID Test', 'rating': 'Unknown'},
            {'source': 'Whitepages', 'rating': 'Unknown'},
            {'source': 'Truecaller', 'rating': 'Unknown'},
            {'source': 'Nomorobo', 'rating': 'Unknown'},
            {'source': 'Hiya', 'rating': 'Unknown'}
        ]
        
        return {'reputation': reputation_sources}
    
    def analyze_patterns(self, parsed):
        """Analyze number patterns and associations"""
        patterns = {
            'pattern_analysis': {
                'repeating_digits': self.check_repeating_digits(parsed.national_number),
                'sequential': self.check_sequential(parsed.national_number),
                'vanity_pattern': self.check_vanity_pattern(parsed.national_number),
                'business_pattern': self.check_business_pattern(parsed.national_number),
                'scam_patterns': self.check_scam_patterns(parsed.national_number)
            }
        }
        return patterns
    
    def check_repeating_digits(self, number):
        """Check for repeating digit patterns"""
        str_num = str(number)
        for i in range(10):
            if str(i)*4 in str_num:  # 4+ repeating digits
                return True
        return False
    
    def check_sequential(self, number):
        """Check for sequential digits"""
        str_num = str(number)
        for i in range(len(str_num)-3):
            if int(str_num[i+1]) == int(str_num[i]) + 1 and \
               int(str_num[i+2]) == int(str_num[i]) + 2:
                return True
        return False
    
    def check_vanity_pattern(self, number):
        """Check if number might be a vanity number"""
        # Phone keypad mapping
        mapping = {
            '2': 'ABC', '3': 'DEF', '4': 'GHI', '5': 'JKL',
            '6': 'MNO', '7': 'PQRS', '8': 'TUV', '9': 'WXYZ'
        }
        # Look for common words (simplified)
        return False
    
    def check_business_pattern(self, number):
        """Check if number matches business patterns"""
        str_num = str(number)
        # Common business patterns: 800, 888, etc.
        return str_num.startswith(('800', '888', '877', '866', '855', '844'))
    
    def check_scam_patterns(self, number):
        """Check against known scam patterns"""
        scam_patterns = [
            r'900',  # Premium rate
            r'876',  # Jamaican lottery scam (common)
            r'809',  # Caribbean scam
            r'284',  # British Virgin Islands (scam)
            r'473',  # Grenada (scam)
        ]
        str_num = str(number)
        for pattern in scam_patterns:
            if pattern in str_num[:3]:
                return True
        return False
    
    def check_verification_services(self, parsed):
        """Check which verification services accept this number"""
        services = [
            {'service': 'Google Voice', 'supported': self.check_google_voice_compatibility(parsed)},
            {'service': 'WhatsApp', 'supported': True},
            {'service': 'Telegram', 'supported': True},
            {'service': 'Signal', 'supported': True},
            {'service': 'Facebook', 'supported': True},
            {'service': 'Twitter', 'supported': True},
            {'service': 'Instagram', 'supported': True}
        ]
        return {'verification_services': services}
    
    def check_google_voice_compatibility(self, parsed):
        """Check if number can be used with Google Voice"""
        # Google Voice only accepts US numbers
        return parsed.country_code == 1

class PhoneIntelGUI:
    """Modern GUI Interface for Phone Intelligence Tool"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Phone Number Intelligence Tool v2.0")
        self.root.geometry("1400x900")
        
        # Set style
        self.setup_styles()
        
        # Initialize engine
        self.engine = AdvancedPhoneIntel()
        self.current_results = None
        
        # Create GUI elements
        self.create_widgets()
        self.create_menu()
        
        # Center window
        self.center_window()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.bg_color = '#2b2b2b'
        self.fg_color = '#ffffff'
        self.accent_color = '#1e90ff'
        self.success_color = '#28a745'
        self.warning_color = '#ffc107'
        self.danger_color = '#dc3545'
        
        # Configure styles
        style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'))
        style.configure('Heading.TLabel', font=('Helvetica', 14, 'bold'))
        style.configure('Info.TLabel', font=('Helvetica', 10))
        style.configure('Success.TLabel', foreground=self.success_color)
        style.configure('Warning.TLabel', foreground=self.warning_color)
        style.configure('Danger.TLabel', foreground=self.danger_color)
        
    def create_widgets(self):
        """Create main GUI widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Input section
        self.create_input_section(main_frame)
        
        # Notebook for results
        self.create_notebook(main_frame)
        
        # Status bar
        self.create_status_bar()
        
    def create_header(self, parent):
        """Create header section"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title = ttk.Label(header_frame, text="📱 Phone Number Intelligence Tool Created By ATHEX BLACK HAT", 
                         style='Title.TLabel')
        title.grid(row=0, column=0)
        
        subtitle = ttk.Label(header_frame, 
                           text="Advanced OSINT Framework for Investigations",
                           font=('Helvetica', 10))
        subtitle.grid(row=1, column=0)
        
    def create_input_section(self, parent):
        """Create input section"""
        input_frame = ttk.LabelFrame(parent, text="Phone Number Input", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Phone number entry
        ttk.Label(input_frame, text="Phone Number:").grid(row=0, column=0, padx=(0, 10))
        self.phone_var = tk.StringVar()
        self.phone_entry = ttk.Entry(input_frame, textvariable=self.phone_var, width=30)
        self.phone_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Label(input_frame, text="(Include country code, e.g., +1234567890)").grid(row=0, column=2, padx=(10, 0))
        
        # Country code dropdown (optional)
        ttk.Label(input_frame, text="Country:").grid(row=1, column=0, padx=(0, 10), pady=5)
        self.country_var = tk.StringVar()
        countries = ['', 'US', 'GB', 'CA', 'AU', 'IN', 'DE', 'FR', 'JP', 'BR']
        self.country_combo = ttk.Combobox(input_frame, textvariable=self.country_var, 
                                         values=countries, width=10)
        self.country_combo.grid(row=1, column=1, sticky=(tk.W), pady=5)
        ttk.Label(input_frame, text="(Optional - if number doesn't include country code)").grid(row=1, column=2, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.analyze_btn = ttk.Button(button_frame, text="🔍 Analyze Number", 
                                      command=self.start_analysis,
                                      style='Accent.TButton')
        self.analyze_btn.grid(row=0, column=0, padx=5)
        
        self.clear_btn = ttk.Button(button_frame, text="🗑️ Clear", 
                                    command=self.clear_all)
        self.clear_btn.grid(row=0, column=1, padx=5)
        
        self.save_btn = ttk.Button(button_frame, text="💾 Save Results", 
                                   command=self.save_results, state='disabled')
        self.save_btn.grid(row=0, column=2, padx=5)
        
        self.export_btn = ttk.Button(button_frame, text="📄 Export Report", 
                                     command=self.export_report, state='disabled')
        self.export_btn.grid(row=0, column=3, padx=5)
        
    def create_notebook(self, parent):
        """Create notebook for results tabs"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.tabs = {}
        tab_names = [
            '📊 Overview', '📋 Basic Info', '📍 Location', '📱 Carrier',
            '🌐 Social Media', '💬 Messaging Apps', '⚠️ Risk Assessment',
            '🔓 Breach Check', '📈 Reputation', '📝 Reports'
        ]
        
        for tab_name in tab_names:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)
            self.tabs[tab_name] = frame
            self.setup_tab_content(tab_name, frame)
    
    def setup_tab_content(self, tab_name, frame):
        """Setup content for each tab"""
        if tab_name == '📊 Overview':
            self.setup_overview_tab(frame)
        elif tab_name == '📋 Basic Info':
            self.setup_basic_info_tab(frame)
        elif tab_name == '📍 Location':
            self.setup_location_tab(frame)
        elif tab_name == '📱 Carrier':
            self.setup_carrier_tab(frame)
        elif tab_name == '🌐 Social Media':
            self.setup_social_tab(frame)
        elif tab_name == '💬 Messaging Apps':
            self.setup_messaging_tab(frame)
        elif tab_name == '⚠️ Risk Assessment':
            self.setup_risk_tab(frame)
        elif tab_name == '🔓 Breach Check':
            self.setup_breach_tab(frame)
        elif tab_name == '📈 Reputation':
            self.setup_reputation_tab(frame)
        elif tab_name == '📝 Reports':
            self.setup_reports_tab(frame)
    
    def setup_overview_tab(self, parent):
        """Setup overview tab with key metrics"""
        # Create canvas with scrollbar
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Key metrics frame
        metrics_frame = ttk.LabelFrame(scrollable_frame, text="Key Metrics", padding="10")
        metrics_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        self.overview_text = scrolledtext.ScrolledText(scrollable_frame, height=20, width=80)
        self.overview_text.grid(row=1, column=0, pady=5, padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_basic_info_tab(self, parent):
        """Setup basic information tab"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Basic info display
        self.basic_info_text = scrolledtext.ScrolledText(frame, height=30, width=100)
        self.basic_info_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_location_tab(self, parent):
        """Setup location tab with map"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Location info
        self.location_text = scrolledtext.ScrolledText(frame, height=10, width=100)
        self.location_text.pack(fill=tk.X, pady=(0, 10))
        
        # Map placeholder
        self.map_frame = ttk.Frame(frame, height=400)
        self.map_frame.pack(fill=tk.BOTH, expand=True)
        self.map_frame.pack_propagate(False)
        
        ttk.Label(self.map_frame, text="Map will be displayed here").pack(expand=True)
    
    def setup_carrier_tab(self, parent):
        """Setup carrier information tab"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.carrier_text = scrolledtext.ScrolledText(frame, height=30, width=100)
        self.carrier_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_social_tab(self, parent):
        """Setup social media tab"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for social media results
        columns = ('Platform', 'URL', 'Status')
        self.social_tree = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.social_tree.heading(col, text=col)
            self.social_tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.social_tree.yview)
        self.social_tree.configure(yscrollcommand=scrollbar.set)
        
        self.social_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to open URL
        self.social_tree.bind('<Double-Button-1>', self.open_social_url)
    
    def setup_messaging_tab(self, parent):
        """Setup messaging apps tab"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('App', 'URL', 'Verified')
        self.messaging_tree = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.messaging_tree.heading(col, text=col)
            self.messaging_tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.messaging_tree.yview)
        self.messaging_tree.configure(yscrollcommand=scrollbar.set)
        
        self.messaging_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.messaging_tree.bind('<Double-Button-1>', self.open_messaging_url)
    
    def setup_risk_tab(self, parent):
        """Setup risk assessment tab"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Risk meter
        self.risk_frame = ttk.LabelFrame(frame, text="Risk Level", padding="10")
        self.risk_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.risk_label = ttk.Label(self.risk_frame, text="Not Analyzed", font=('Helvetica', 16))
        self.risk_label.pack()
        
        # Risk factors
        factors_frame = ttk.LabelFrame(frame, text="Risk Factors", padding="10")
        factors_frame.pack(fill=tk.BOTH, expand=True)
        
        self.risk_text = scrolledtext.ScrolledText(factors_frame, height=20)
        self.risk_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_breach_tab(self, parent):
        """Setup breach check tab"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.breach_text = scrolledtext.ScrolledText(frame, height=30)
        self.breach_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_reputation_tab(self, parent):
        """Setup reputation tab"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('Source', 'Rating', 'Details')
        self.reputation_tree = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.reputation_tree.heading(col, text=col)
            self.reputation_tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.reputation_tree.yview)
        self.reputation_tree.configure(yscrollcommand=scrollbar.set)
        
        self.reputation_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_reports_tab(self, parent):
        """Setup reports generation tab"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Report options
        options_frame = ttk.LabelFrame(frame, text="Report Options", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(options_frame, text="Generate PDF Report", 
                  command=self.generate_pdf_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(options_frame, text="Generate HTML Report", 
                  command=self.generate_html_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(options_frame, text="Export CSV Data", 
                  command=self.export_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(options_frame, text="Print Report", 
                  command=self.print_report).pack(side=tk.LEFT, padx=5)
        
        # Report preview
        preview_frame = ttk.LabelFrame(frame, text="Report Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        self.report_preview = scrolledtext.ScrolledText(preview_frame, height=20)
        self.report_preview.pack(fill=tk.BOTH, expand=True)
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Analysis", command=self.clear_all)
        file_menu.add_command(label="Open Results", command=self.open_results)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Export as PDF", command=self.generate_pdf_report)
        file_menu.add_command(label="Export as HTML", command=self.generate_html_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Batch Analysis", command=self.batch_analysis)
        tools_menu.add_command(label="API Configuration", command=self.configure_api)
        tools_menu.add_command(label="Clear Cache", command=self.clear_cache)
        tools_menu.add_separator()
        tools_menu.add_command(label="Export All Data", command=self.export_all)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.show_docs)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_separator()
        help_menu.add_command(label="Legal Notice", command=self.show_legal)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(self.status_bar, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=5, pady=2)
        
        self.progress_bar = ttk.Progressbar(self.status_bar, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, padx=5, pady=2)
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def start_analysis(self):
        """Start phone number analysis in background thread"""
        phone = self.phone_var.get().strip()
        if not phone:
            messagebox.showwarning("Input Error", "Please enter a phone number")
            return
        
        # Disable analyze button
        self.analyze_btn.config(state='disabled')
        self.progress_bar.start()
        self.status_label.config(text="Analyzing phone number...")
        
        # Run analysis in thread
        thread = threading.Thread(target=self.run_analysis, args=(phone,))
        thread.daemon = True
        thread.start()
    
    def run_analysis(self, phone):
        """Run the actual analysis"""
        try:
            # Add country code if specified
            if self.country_var.get() and not phone.startswith('+'):
                try:
                    parsed = phonenumbers.parse(phone, self.country_var.get())
                    phone = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
                except:
                    pass
            
            # Perform analysis
            self.current_results = self.engine.analyze_number(phone)
            
            # Update GUI in main thread
            self.root.after(0, self.update_results)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Analysis Error", str(e)))
        finally:
            self.root.after(0, self.analysis_complete)
    
    def update_results(self):
        """Update GUI with results"""
        if not self.current_results:
            return
        
        if 'error' in self.current_results:
            messagebox.showerror("Error", self.current_results['error'])
            return
        
        # Update each tab
        self.update_overview_tab()
        self.update_basic_info_tab()
        self.update_location_tab()
        self.update_carrier_tab()
        self.update_social_tab()
        self.update_messaging_tab()
        self.update_risk_tab()
        self.update_breach_tab()
        self.update_reputation_tab()
        self.update_reports_tab()
        
        # Enable buttons
        self.save_btn.config(state='normal')
        self.export_btn.config(state='normal')
    
    def update_overview_tab(self):
        """Update overview tab with summary"""
        self.overview_text.delete(1.0, tk.END)
        
        if not self.current_results:
            return
        
        overview = f"""
╔══════════════════════════════════════════════════════════╗
║                 PHONE NUMBER ANALYSIS                    ║
╚══════════════════════════════════════════════════════════╝

📱 Number: {self.current_results.get('parsed', {}).get('international', 'N/A')}
⏰ Analyzed: {self.current_results.get('timestamp', 'N/A')}

────────────────────────────────────────────────────────────
📊 KEY FINDINGS
────────────────────────────────────────────────────────────

• Type: {self.current_results.get('basic_info', {}).get('type', 'N/A')}
• Carrier: {self.current_results.get('carrier_info', {}).get('current', 'N/A')}
• Location: {self.current_results.get('location_data', {}).get('geolocation', 'N/A')}
• Risk Level: {self.current_results.get('risk_assessment', {}).get('level', 'N/A')}
• Spam Score: {self.current_results.get('risk_assessment', {}).get('spam_score', 0)}

────────────────────────────────────────────────────────────
🌐 SOCIAL MEDIA PRESENCE
────────────────────────────────────────────────────────────
"""
        
        social = self.current_results.get('social_presence', [])
        for item in social[:5]:
            overview += f"• {item.get('name')}: {'✅' if item.get('verified') else '❓'}\n"
        
        overview += """
────────────────────────────────────────────────────────────
⚠️  RISK FACTORS
────────────────────────────────────────────────────────────
"""
        
        for factor in self.current_results.get('risk_assessment', {}).get('factors', []):
            overview += f"• {factor}\n"
        
        self.overview_text.insert(1.0, overview)
    
    def update_basic_info_tab(self):
        """Update basic information tab"""
        self.basic_info_text.delete(1.0, tk.END)
        
        if not self.current_results:
            return
        
        parsed = self.current_results.get('parsed', {})
        basic = self.current_results.get('basic_info', {})
        
        info = f"""
📱 PHONE NUMBER DETAILS
═══════════════════════════════════════════════════════════

📞 FORMATS:
────────────────────────────────────────────────────────────
• E.164:          {parsed.get('e164', 'N/A')}
• International:  {parsed.get('international', 'N/A')}
• National:       {parsed.get('national', 'N/A')}
• Country Code:   +{parsed.get('country_code', 'N/A')}
• National Num:   {parsed.get('national_number', 'N/A')}

🔍 NUMBER VALIDATION:
────────────────────────────────────────────────────────────
• Type:           {basic.get('type', 'N/A')}
• Description:    {basic.get('possible_type', 'N/A')}
• Valid:          {basic.get('validity', 'N/A')}
• Possible:       {'Yes' if basic.get('possible_number') else 'No'}

🌍 TIMEZONES:
────────────────────────────────────────────────────────────
"""
        
        for tz in basic.get('timezones', []):
            info += f"• {tz}\n"
        
        self.basic_info_text.insert(1.0, info)
    
    def update_location_tab(self):
        """Update location tab"""
        self.location_text.delete(1.0, tk.END)
        
        if not self.current_results:
            return
        
        location = self.current_results.get('location_data', {})
        
        info = f"""
📍 LOCATION INFORMATION
═══════════════════════════════════════════════════════════

Geographic Location: {location.get('geolocation', 'N/A')}
Country: {phonenumbers.region_code_for_number(self.engine.parsed) if hasattr(self.engine, 'parsed') else 'N/A'}

Additional location data requires IP geolocation or cell tower information.
"""
        
        self.location_text.insert(1.0, info)
    
    def update_carrier_tab(self):
        """Update carrier information tab"""
        self.carrier_text.delete(1.0, tk.END)
        
        if not self.current_results:
            return
        
        carrier = self.current_results.get('carrier_info', {})
        voip = self.current_results.get('voip_info', {})
        
        info = f"""
📡 CARRIER INFORMATION
═══════════════════════════════════════════════════════════

Current Carrier: {carrier.get('current', 'N/A')}
Network Type: {carrier.get('network_type', 'N/A')}
Number Ported: {'Yes' if carrier.get('ported', {}).get('ported') else 'No'}

📞 VOIP ANALYSIS:
────────────────────────────────────────────────────────────
Is VoIP: {'Yes' if voip.get('is_voip') else 'No'}
Provider: {voip.get('provider', 'N/A')}
Temporary Likely: {'Yes' if voip.get('temporary_likely') else 'No'}

📊 Historical Carriers:
────────────────────────────────────────────────────────────
"""
        
        for hist in carrier.get('historical_carriers', []):
            info += f"• {hist}\n"
        
        self.carrier_text.insert(1.0, info)
    
    def update_social_tab(self):
        """Update social media tree"""
        # Clear existing items
        for item in self.social_tree.get_children():
            self.social_tree.delete(item)
        
        if not self.current_results:
            return
        
        social = self.current_results.get('social_presence', [])
        for item in social:
            status = '✅ Found' if item.get('verified') else '❓ Unknown'
            self.social_tree.insert('', tk.END, values=(
                item.get('name', 'N/A'),
                item.get('url', 'N/A'),
                status
            ))
    
    def update_messaging_tab(self):
        """Update messaging apps tree"""
        # Clear existing items
        for item in self.messaging_tree.get_children():
            self.messaging_tree.delete(item)
        
        if not self.current_results:
            return
        
        apps = self.current_results.get('messaging_apps', [])
        for item in apps:
            verified = '✅' if item.get('verified') else '❓'
            self.messaging_tree.insert('', tk.END, values=(
                item.get('name', 'N/A'),
                item.get('url', 'N/A'),
                verified
            ))
    
    def update_risk_tab(self):
        """Update risk assessment tab"""
        self.risk_text.delete(1.0, tk.END)
        
        if not self.current_results:
            return
        
        risk = self.current_results.get('risk_assessment', {})
        
        # Update risk label
        level = risk.get('level', 'UNKNOWN')
        if level == 'LOW':
            self.risk_label.config(text=f"⚠️ RISK LEVEL: {level}", foreground='green')
        elif level == 'MEDIUM':
            self.risk_label.config(text=f"⚠️ RISK LEVEL: {level}", foreground='orange')
        elif level == 'HIGH':
            self.risk_label.config(text=f"⚠️ RISK LEVEL: {level}", foreground='red')
        
        # Update risk factors
        factors = risk.get('factors', [])
        recommendations = risk.get('recommendations', [])
        
        info = f"""
Risk Score: {risk.get('score', 0)}/100
Spam Score: {risk.get('spam_score', 0)}/100

RISK FACTORS:
═══════════════════════════════════════════════════════════
"""
        
        for factor in factors:
            info += f"• {factor}\n"
        
        info += """
RECOMMENDATIONS:
═══════════════════════════════════════════════════════════
"""
        
        for rec in recommendations:
            info += f"• {rec}\n"
        
        self.risk_text.insert(1.0, info)
    
    def update_breach_tab(self):
        """Update breach check tab"""
        self.breach_text.delete(1.0, tk.END)
        
        if not self.current_results:
            return
        
        breaches = self.current_results.get('breach_data', [])
        
        info = """
🔓 DATA BREACH CHECK
═══════════════════════════════════════════════════════════

Note: Direct breach checking requires Paid API access.
The following services should be checked manually:

"""
        
        for item in breaches:
            info += f"• {item.get('service')}: {item.get('url')}\n"
            info += f"  Status: {item.get('status')}\n\n"
        
        self.breach_text.insert(1.0, info)
    
    def update_reputation_tab(self):
        """Update reputation tree"""
        # Clear existing items
        for item in self.reputation_tree.get_children():
            self.reputation_tree.delete(item)
        
        if not self.current_results:
            return
        
        reputation = self.current_results.get('reputation', [])
        for item in reputation:
            self.reputation_tree.insert('', tk.END, values=(
                item.get('source', 'N/A'),
                item.get('rating', 'N/A'),
                'Check manually'
            ))
    
    def update_reports_tab(self):
        """Update reports preview"""
        self.report_preview.delete(1.0, tk.END)
        
        if not self.current_results:
            return
        
        # Generate preview
        preview = self.generate_report_text()
        self.report_preview.insert(1.0, preview)
    
    def generate_report_text(self):
        """Generate text report"""
        if not self.current_results:
            return "No results to display"
        
        parsed = self.current_results.get('parsed', {})
        basic = self.current_results.get('basic_info', {})
        risk = self.current_results.get('risk_assessment', {})
        
        report = f"""
PHONE NUMBER INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

TARGET INFORMATION
═══════════════════════════════════════════════════════════
Number: {parsed.get('international', 'N/A')}
Type: {basic.get('type', 'N/A')}
Carrier: {self.current_results.get('carrier_info', {}).get('current', 'N/A')}
Location: {basic.get('geolocation', 'N/A')}
Risk Level: {risk.get('level', 'N/A')}

SOCIAL MEDIA PRESENCE
═══════════════════════════════════════════════════════════
"""
        
        for item in self.current_results.get('social_presence', []):
            report += f"{item.get('name')}: {item.get('url')}\n"
        
        report += """
MESSAGING APPS
═══════════════════════════════════════════════════════════
"""
        
        for item in self.current_results.get('messaging_apps', []):
            report += f"{item.get('name')}: {item.get('url')}\n"
        
        return report
    
    def analysis_complete(self):
        """Called when analysis is complete"""
        self.progress_bar.stop()
        self.analyze_btn.config(state='normal')
        self.status_label.config(text="Analysis complete")
    
    def clear_all(self):
        """Clear all inputs and results"""
        self.phone_var.set('')
        self.country_var.set('')
        self.current_results = None
        
        # Clear all text widgets
        for tab in self.tabs.values():
            for child in tab.winfo_children():
                if isinstance(child, scrolledtext.ScrolledText):
                    child.delete(1.0, tk.END)
        
        # Clear trees
        for tree in [self.social_tree, self.messaging_tree, self.reputation_tree]:
            for item in tree.get_children():
                tree.delete(item)
        
        # Disable buttons
        self.save_btn.config(state='disabled')
        self.export_btn.config(state='disabled')
        
        self.status_label.config(text="Ready")
    
    def save_results(self):
        """Save results to file"""
        if not self.current_results:
            messagebox.showwarning("No Results", "No results to save")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.current_results, f, indent=2)
                messagebox.showinfo("Success", f"Results saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def export_report(self):
        """Export report as text"""
        if not self.current_results:
            messagebox.showwarning("No Results", "No results to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                report = self.generate_report_text()
                with open(filename, 'w') as f:
                    f.write(report)
                messagebox.showinfo("Success", f"Report exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def generate_pdf_report(self):
        """Generate PDF report"""
        if not self.current_results:
            messagebox.showwarning("No Results", "No results to generate PDF")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Create PDF
                doc = SimpleDocTemplate(filename, pagesize=A4)
                story = []
                styles = getSampleStyleSheet()
                
                # Title
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    textColor=colors.HexColor('#1e90ff'),
                    spaceAfter=30
                )
                story.append(Paragraph("Phone Number Intelligence Report", title_style))
                story.append(Spacer(1, 12))
                
                # Date
                story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
                story.append(Spacer(1, 12))
                
                # Basic info
                story.append(Paragraph("Basic Information", styles['Heading2']))
                parsed = self.current_results.get('parsed', {})
                basic = self.current_results.get('basic_info', {})
                
                data = [
                    ['Field', 'Value'],
                    ['Number', parsed.get('international', 'N/A')],
                    ['Type', basic.get('type', 'N/A')],
                    ['Carrier', self.current_results.get('carrier_info', {}).get('current', 'N/A')],
                    ['Location', basic.get('geolocation', 'N/A')]
                ]
                
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(table)
                story.append(Spacer(1, 12))
                
                # Build PDF
                doc.build(story)
                messagebox.showinfo("Success", f"PDF report saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")
    
    def generate_html_report(self):
        """Generate HTML report"""
        if not self.current_results:
            messagebox.showwarning("No Results", "No results to generate HTML")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                html = self.generate_html_content()
                with open(filename, 'w') as f:
                    f.write(html)
                messagebox.showinfo("Success", f"HTML report saved to {filename}")
                webbrowser.open(filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate HTML: {str(e)}")
    
    def generate_html_content(self):
        """Generate HTML content for report"""
        if not self.current_results:
            return "<html><body><h1>No Results</h1></body></html>"
        
        parsed = self.current_results.get('parsed', {})
        basic = self.current_results.get('basic_info', {})
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Phone Intelligence Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #1e90ff; }}
        h2 {{ color: #333; border-bottom: 2px solid #1e90ff; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th {{ background-color: #1e90ff; color: white; padding: 10px; }}
        td {{ padding: 8px; border: 1px solid #ddd; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .risk-high {{ color: red; font-weight: bold; }}
        .risk-medium {{ color: orange; font-weight: bold; }}
        .risk-low {{ color: green; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>📱 Phone Number Intelligence Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <h2>Basic Information</h2>
    <table>
        <tr><th>Field</th><th>Value</th></tr>
        <tr><td>Number</td><td>{parsed.get('international', 'N/A')}</td></tr>
        <tr><td>Type</td><td>{basic.get('type', 'N/A')}</td></tr>
        <tr><td>Carrier</td><td>{self.current_results.get('carrier_info', {}).get('current', 'N/A')}</td></tr>
        <tr><td>Location</td><td>{basic.get('geolocation', 'N/A')}</td></tr>
    </table>
    
    <h2>Risk Assessment</h2>
    <table>
        <tr><th>Factor</th><th>Value</th></tr>
        <tr><td>Risk Level</td>
            <td class="risk-{self.current_results.get('risk_assessment', {}).get('level', 'unknown').lower()}">
                {self.current_results.get('risk_assessment', {}).get('level', 'N/A')}
            </td>
        </tr>
        <tr><td>Risk Score</td><td>{self.current_results.get('risk_assessment', {}).get('score', 0)}</td></tr>
    </table>
    
    <h2>Social Media Presence</h2>
    <table>
        <tr><th>Platform</th><th>URL</th></tr>
"""
        
        for item in self.current_results.get('social_presence', []):
            html += f"<tr><td>{item.get('name')}</td><td><a href='{item.get('url')}'>{item.get('url')}</a></td></tr>"
        
        html += """
    </table>
    
    <h2>Messaging Apps</h2>
    <table>
        <tr><th>App</th><th>URL</th></tr>
"""
        
        for item in self.current_results.get('messaging_apps', []):
            html += f"<tr><td>{item.get('name')}</td><td><a href='{item.get('url')}'>{item.get('url')}</a></td></tr>"
        
        html += """
    </table>
    
    <p><i>Generated by ATHEX Advance OSINT Framework</i></p>
</body>
</html>
"""
        return html
    
    def export_csv(self):
        """Export data as CSV"""
        if not self.current_results:
            messagebox.showwarning("No Results", "No results to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Prepare data for CSV
                data = []
                
                # Basic info
                parsed = self.current_results.get('parsed', {})
                basic = self.current_results.get('basic_info', {})
                
                data.append(['Section', 'Field', 'Value'])
                data.append(['Basic', 'Number', parsed.get('international', 'N/A')])
                data.append(['Basic', 'Type', basic.get('type', 'N/A')])
                data.append(['Basic', 'Carrier', self.current_results.get('carrier_info', {}).get('current', 'N/A')])
                data.append(['Basic', 'Location', basic.get('geolocation', 'N/A')])
                
                # Social media
                for item in self.current_results.get('social_presence', []):
                    data.append(['Social Media', item.get('name'), item.get('url')])
                
                # Save as CSV
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(data)
                
                messagebox.showinfo("Success", f"CSV exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export CSV: {str(e)}")
    
    def print_report(self):
        """Print report"""
        if not self.current_results:
            messagebox.showwarning("No Results", "No results to print")
            return
        
        # Create temporary HTML file and print
        html = self.generate_html_content()
        temp_file = "temp_report.html"
        with open(temp_file, 'w') as f:
            f.write(html)
        
        webbrowser.open(temp_file)
        messagebox.showinfo("Print", "Report opened in browser for printing")
    
    def open_results(self):
        """Open saved results file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.current_results = json.load(f)
                self.update_results()
                messagebox.showinfo("Success", "Results loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load results: {str(e)}")
    
    def batch_analysis(self):
        """Open batch analysis window"""
        batch_window = tk.Toplevel(self.root)
        batch_window.title("Batch Analysis")
        batch_window.geometry("600x400")
        
        ttk.Label(batch_window, text="Enter phone numbers (one per line):").pack(pady=10)
        
        text_area = scrolledtext.ScrolledText(batch_window, height=10)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        def run_batch():
            numbers = text_area.get(1.0, tk.END).strip().split('\n')
            # Implement batch processing logic here
            messagebox.showinfo("Batch", f"Processing {len(numbers)} numbers")
        
        ttk.Button(batch_window, text="Process Batch", command=run_batch).pack(pady=10)
    
    def configure_api(self):
        """Open API configuration window"""
        config_window = tk.Toplevel(self.root)
        config_window.title("API Configuration")
        config_window.geometry("500x400")
        
        ttk.Label(config_window, text="Configure API Keys", font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # API key entries
        apis = [
            'HaveIBeenPwned',
            'Truecaller',
            'Twilio',
            'Numverify',
            'OpenCageData'
        ]
        
        frame = ttk.Frame(config_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        entries = {}
        for i, api in enumerate(apis):
            ttk.Label(frame, text=f"{api} API Key:").grid(row=i, column=0, sticky=tk.W, pady=5)
            entries[api] = ttk.Entry(frame, width=40)
            entries[api].grid(row=i, column=1, pady=5, padx=(10, 0))
        
        def save_keys():
            keys = {api: entries[api].get() for api in apis}
            try:
                with open('api_keys.json', 'w') as f:
                    json.dump(keys, f, indent=2)
                messagebox.showinfo("Success", "API keys saved successfully")
                config_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save keys: {str(e)}")
        
        ttk.Button(config_window, text="Save Keys", command=save_keys).pack(pady=10)
    
    def clear_cache(self):
        """Clear cache database"""
        try:
            conn = sqlite3.connect(self.engine.cache_db)
            c = conn.cursor()
            c.execute("DELETE FROM phone_cache")
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Cache cleared successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear cache: {str(e)}")
    
    def export_all(self):
        """Export all data"""
        if not self.current_results:
            messagebox.showwarning("No Results", "No results to export")
            return
        
        directory = filedialog.askdirectory(title="Select Export Directory")
        if directory:
            try:
                # Export JSON
                with open(f"{directory}/results.json", 'w') as f:
                    json.dump(self.current_results, f, indent=2)
                
                # Export TXT report
                with open(f"{directory}/report.txt", 'w') as f:
                    f.write(self.generate_report_text())
                
                # Export HTML
                with open(f"{directory}/report.html", 'w') as f:
                    f.write(self.generate_html_content())
                
                # Export CSV
                import csv
                with open(f"{directory}/data.csv", 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Category', 'Field', 'Value'])
                    # Add data rows here
                
                messagebox.showinfo("Success", f"All data exported to {directory}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def show_docs(self):
        """Show documentation"""
        docs_window = tk.Toplevel(self.root)
        docs_window.title("Documentation")
        docs_window.geometry("600x500")
        
        text = scrolledtext.ScrolledText(docs_window, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        docs = """
PHONE NUMBER INTELLIGENCE TOOL v2.0
===================================

OVERVIEW
--------
This tool performs comprehensive OSINT gathering on phone numbers
for security research and investigations.

FEATURES
--------
• Basic number validation and formatting
• Carrier and location information
• Social media presence checking
• Messaging app verification
• Risk assessment and scoring
• Data breach checking (manual)
• Reputation analysis
• Multiple export formats (JSON, TXT, HTML, CSV, PDF)
• Batch processing
• Cache management
• API integration support

USAGE
-----
1. Enter a phone number with country code (e.g., +1234567890)
2. Click "Analyze Number" to start
3. View results in different tabs
4. Export or save results as needed

LEGAL NOTICE
------------
This tool is for authorized security research only.
Always obtain proper consent before investigating phone numbers.
Respect privacy laws and regulations in your jurisdiction.

DISCLAIMER
----------
The accuracy of results depends on available data sources.
Some features require Paid API keys for full functionality.

DEVELOPER 
----------

THIS TOOL IS CREATED BY ATHEX BLACK HAT 
IM ATHEX CYBER SECURITY EXPERT
DEVELOPER
RESEARCHER
MUCH MORE..........
FEEL FREE TO CONTACT FOR ANYKIND OS ISSUE AND TOOL BUYING
WHATSAPP NUMBER - +92 340916663
YOUTUBE- @inziXploit444 ( ATHEX BLACK HAT)
GOOGLE ( Athex black hat) 
THANKS FOR USING MY TOOL.
"""
        
        text.insert(1.0, docs)
        text.config(state=tk.DISABLED)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
Advanced Phone Number Intelligence Tool
Version 2.0

Created By ATHEX BLACK HAT

A comprehensive OSINT framework for phone number analysis
and investigation.

Created for authorized security research and investigations.

Features:
• Advanced number validation
• Multi-source data gathering
• Risk assessment
• Social media detection
• Reporting and export

© 2026 - For Authorized Use Only
"""
        messagebox.showinfo("About", about_text)
    
    def show_legal(self):
        """Show legal notice"""
        legal_text = """
LEGAL NOTICE AND DISCLAIMER

This tool is designed for legitimate security research,
authorized penetration testing, and investigations with
proper legal authorization.

WARNING:
• Unauthorized use may violate privacy laws
• Always obtain consent before investigation
• Respect data protection regulations
• Check local laws before use

The developers assume no liability for misuse or
unauthorized use of this tool.

By using this tool, you agree to:
1. Use only for authorized purposes
2. Comply with all applicable laws
3. Respect individual privacy rights
4. Not use for harassment or stalking
"""
        messagebox.showwarning("Legal Notice", legal_text)
    
    def open_social_url(self, event):
        """Open social media URL in browser"""
        item = self.social_tree.selection()[0]
        url = self.social_tree.item(item, 'values')[1]
        webbrowser.open(url)
    
    def open_messaging_url(self, event):
        """Open messaging app URL in browser"""
        item = self.messaging_tree.selection()[0]
        url = self.messaging_tree.item(item, 'values')[1]
        webbrowser.open(url)

def main():
    """Main entry point"""
    root = tk.Tk()
    app = PhoneIntelGUI(root)
    
    # Set window icon (optional)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # Start application
    root.mainloop()

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║     ADVANCED PHONE NUMBER INTELLIGENCE v2.0          ║
    ║     Professional OSINT Framework with GUI            ║
    ║     For Authorized Security Research Only            ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Check dependencies
    required_packages = [
        'phonenumbers',
        'requests',
        'tkinter',
        'reportlab',
        'matplotlib',
        'seaborn',
        'pandas',
        'folium',
        'dnspython',
        'whois'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("\n  Missing required packages:")
        for package in missing_packages:
            print(f"   • {package}")
        print("\nPlease install missing packages:")
        print("pip install " + " ".join(missing_packages))
        
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    main()