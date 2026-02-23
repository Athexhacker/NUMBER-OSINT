<a href="https://github.com/Athexhacker/NUMBER-OSINT"><img src="/src/logo.png" alt="0" border="0" /></a> 

![Geo-Phone](https://img.shields.io/badge/version-v[2.1]-blue.svg)
![Geo-Phone](https://img.shields.io/badge/platform-Linux-blue.svg)
![Geo-Phone](https://img.shields.io/badge/language-python-red.svg)


# 📱 Advanced Phone Number Intelligence Tool v2.0
<p align="center"> <img src="https://img.shields.io/badge/Version-2.0-blue.svg" alt="Version 2.0"> <img src="https://img.shields.io/badge/Python-3.7+-green.svg" alt="Python 3.7+"> <img src="https://img.shields.io/badge/License-For%20Authorized%20Use%20Only-red.svg" alt="License: For Authorized Use Only"> <img src="https://img.shields.io/badge/OSINT-Advanced-purple.svg" alt="OSINT Advanced"> </p><p align="center"> <b>A Professional OSINT Framework for Phone Number Intelligence Gathering</b><br> <i>Created by ATHEX BLACK HAT</i> </p>


## 🔍 Overview
The Advanced Phone Number Intelligence Tool v2.0 is a comprehensive Open Source Intelligence (OSINT) framework designed for professional security researchers, investigators, and authorized personnel to gather detailed intelligence on phone numbers.

***Key Capabilities:***
✅ Validate and format phone numbers globally

✅ Identify carrier and network information

✅ Detect social media presence across 15+ platforms

✅ Check messaging app registration (WhatsApp, Telegram, Signal, etc.)

✅ Comprehensive risk assessment with scoring

✅ Pattern analysis for scam/fraud detection

✅ Data breach checking (manual/API)

✅ Professional multi-format reporting

✅ Batch processing for multiple numbers

✅ SQLite caching for performance

## ✨ Features

Core Features
Feature	Description
Number Validation	Google's libphonenumber integration for accurate parsing
Carrier Detection	Current carrier, network type, porting status
Geolocation	Country, region, timezone information
Risk Scoring	0-100 scale with color-coded risk levels
Pattern Analysis	Scam patterns, vanity numbers, business lines
Platform Coverage
Category	Platforms
Social Media	Facebook, Twitter, Instagram, LinkedIn, Snapchat, TikTok, Pinterest, Reddit, YouTube
Messaging Apps	WhatsApp, Telegram, Signal, Viber, WeChat, Line, Facebook Messenger, Skype, Discord
People Search	Truecaller, Whitepages, SpyDialer, FastPeopleSearch, Intelius
Breach Databases	HaveIBeenPwned, Dehashed, BreachDirectory, Snusbase
### Advanced Features
***🚀 Multi-threaded Analysis - Parallel processing for speed***

***💾 SQLite Caching - Store results to avoid redundant lookups***

***🔌 API Ready - Configurable integrations with paid services***

***📊 10 Specialized Tabs - Organized information display***

***🖨️ 5 Export Formats - JSON, TXT, HTML, CSV, PDF***

***🔍 Google Dorks Generation - 50+ specialized search queries***

***📍 Map Integration - Geographic visualization (placeholder)***

## 💻 Installation
Prerequisites
Python 3.7 or higher

pip package manager

Internet connection for API calls

Step 1: Clone or Download
bash
# Clone repository 
```

git clone https://github.com/Athexhacker/NUMBER-OSINT.git
cd NUMBER-OSINT
bash run.sh

```

Command Line Mode (Legacy)

***Basic analysis***
python3 number-info.py +1234567890

***With country code if omitted***
python python3 number-info.py 1234567890 --country US

***Save to file***
python python3 number-info.py +1234567890 --output report.txt

***Open in browser***
python python3 number-info.py +1234567890 --web
Batch Processing
Click Tools → Batch Analysis

Enter one number per line

Click "Process Batch"

Results saved to individual files

## 🖥️ GUI Interface Guide
Tab-by-Tab Guide
1. ***📊 Overview Tab***
Purpose: Dashboard with key findings

Number summary (formats, type)

Risk level indicator (color-coded)

Quick stats (carrier, location)

Recent social media mentions

Top risk factors

2. ***📋 Basic Info Tab***
Purpose: Detailed number validation

Formats: E.164, International, National

Validation: Valid/Possible status

Number Type: Mobile/Landline/VoIP/etc.

Timezones: All associated timezones

Country: Region code and name

3. ***📍 Location Tab***
Purpose: Geographic intelligence

Geographic description

Country of origin

Map visualization (if coordinates available)

Regional risk factors

Nearby area information

4. ***📱 Carrier Tab***
Purpose: Network intelligence

Current carrier/provider

Network type (2G/3G/4G/5G)

Porting status (ported/original carrier)

Historical carrier data

VoIP detection and provider

5. ***🌐 Social Media Tab***
Purpose: Social presence detection

Interactive tree view of platforms

Direct links to search results

Verification status indicators

Double-click to open in browser

Platform-specific notes

6. ***💬 Messaging Apps Tab***
Purpose: Real-time messaging presence

WhatsApp verification

Telegram channel detection

Signal profile check

Viber/WeChat/Line presence

Click-to-contact links

7. ***⚠️ Risk Assessment Tab***
Purpose: Comprehensive risk analysis

Risk Score: 0-100 numerical value

Risk Level: LOW/MEDIUM/HIGH (color-coded)

Risk Factors: List of identified risks

Spam Score: Database reputation

Recommendations: Actionable advice

Scam Patterns: Detected fraud indicators

8. ***🔓 Breach Check Tab***
Purpose: Data breach intelligence

Links to breach databases

Manual check instructions

Historical breach patterns

Dark web monitoring (if configured)

Recycled number detection

9. ***📈 Reputation Tab***
Purpose: Multi-source reputation

Caller ID ratings

Spam report databases

User review aggregators

Business verification status

Trust scores from various sources

10. ***📝 Reports Tab***
Purpose: Export and documentation

Report preview window

Format selection (PDF/HTML/CSV/TXT)

Print functionality

Batch export options

Custom report templates

# 🧠 Analysis Modules
Module 1: Number Validation Engine
python
Input: +1234567890
Output:
- E.164: +1234567890
- International: +1 234-567-890
- National: (234) 567-890
- Country Code: +1
- National Number: 234567890
- Type: MOBILE
- Validity: Valid
- Timezone: America/New_York
Module 2: Carrier Intelligence
Current carrier detection

Network technology identification

Number porting history

MVNO (Mobile Virtual Network Operator) detection

Roaming capabilities

Module 3: Social Media Scanner
Platform-specific search URL generation

Presence verification attempts

Profile existence checking

Account recovery page analysis

Public post scanning

Module 4: Risk Assessment Engine
Risk Factors Weights:

Factor	Weight	Description
VoIP Number	+30	Temporary/disposable potential
Prepaid Carrier	+20	Lower accountability
High-risk Country	+15	Based on fraud statistics
Spam Database	+25	Reported by users
Scam Pattern	+20	Known scam formats
Recent Breach	+35	Found in data leak
Risk Levels:

0-30: LOW - Standard verification sufficient

31-60: MEDIUM - Additional verification recommended

61-100: HIGH - Extreme caution advised

Module 5: Pattern Recognition
Detected Patterns:

Repeating digits (7777, 8888)

Sequential numbers (1234, 5678)

Vanity numbers (800-FLOWERS)

Business lines (800, 888 prefixes)

Scam patterns (809, 876, 900 prefixes)

Toll-free recognition

## 📊 Export & Reporting
Export Formats
1. JSON Export (Raw Data)
json
{
  "input_number": "+1234567890",
  "timestamp": "2026-02-22T15:30:00",
  "basic_info": {
    "type": "MOBILE",
    "carrier": "Verizon",
    "location": "United States"
  },
  "risk_assessment": {
    "score": 25,
    "level": "LOW",
    "factors": []
  }
}
2. HTML Report (Web View)
Professional styling

Clickable links

Color-coded risk indicators

Responsive design

Print-friendly

3. PDF Report (Professional)
Company branding support

Page numbering

Table of contents

Header/footer customization

Digital signature ready

4. CSV Export (Spreadsheet)
Column-organized data

Compatible with Excel/Sheets

Easy filtering/sorting

Statistical analysis ready

5. TXT Report (Plain Text)
Lightweight format

Easy to share

Command-line friendly

Email-ready

Report Sections
Header - Tool info, timestamp, analyst

Executive Summary - Key findings

Number Details - Validation results

Risk Assessment - Score and factors

Digital Presence - Social/messaging apps

Network Intelligence - Carrier/VoIP info

Breach Status - Data leak findings

Recommendations - Action items

Legal Disclaimer - Usage terms

Appendix - Raw data, search URLs

## 🔌 API Integration
Configured APIs
Service	Purpose	API Key Required	Cost
HaveIBeenPwned	Breach checking	Yes	Free Tier
Truecaller	Caller ID	Yes	Paid
Twilio	Carrier lookup	Yes	Paid
Numverify	Validation	Yes	Freemium
OpenCageData	Geolocation	Yes	Freemium
Whitepages	People search	Yes	Paid
Setup Instructions
Open API Configuration:

Tools → API Configuration

Enter API Keys:

HaveIBeenPwned: [your-key-here]
Truecaller: [your-key-here]
Twilio: [your-key-here]
Numverify: [your-key-here]
OpenCageData: [your-key-here]
Save Keys:

Click "Save Keys"

Keys stored in api_keys.json

Verify Connection:

Test each API

Check response status

Monitor rate limits

## 🎯 Use Cases
1. Security Research
Penetration Testing: Reconnaissance phase

Social Engineering: Target profiling

Threat Intelligence: Phone-based threat tracking

Fraud Detection: Scam number identification

2. Private Investigations
Background Checks: Individual verification

Asset Tracing: Finding associated accounts

Skip Tracing: Locating individuals

Due Diligence: Business partner verification

3. Business Applications
Customer Verification: KYC compliance

Fraud Prevention: Suspicious number screening

Lead Validation: Marketing list cleaning

Risk Management: High-risk customer identification

4. Personal Security
Unknown Caller Analysis: Who called me?

Spam Protection: Identify telemarketers

Dating App Safety: Verify matches

Online Purchase Safety: Seller verification

## ⚖️ Legal & Ethical Guidelines
Legal Requirements
✅ Authorized Uses
Your own phone numbers

Numbers with explicit consent

Court-ordered investigations

Law enforcement operations

Security testing with written authorization

***❌ Prohibited Uses***
Stalking or harassment

Unauthorized surveillance

Identity theft

Fraudulent activities

Violating privacy laws

Compliance Checklist
Have written authorization?

Comply with local privacy laws?

Obtained necessary consent?

Documented legal basis?

Informed data subjects (where required)?

International Laws to Consider
GDPR (Europe) - Strict privacy protections

CCPA (California) - Consumer privacy rights

PIPEDA (Canada) - Personal information protection

LGPD (Brazil) - Data privacy law

Local variations - Check your jurisdiction

Ethical Guidelines
Proportionality: Only collect necessary data

***👤 Created By: ATHEX BLACK HAT***
**🔰 Role: Cyber Security Expert & Developer**
**📱 WhatsApp: +92 3490916663**
**▶️ YouTube: @inziXploit444 (ATHEX BLACK HAT)**
**🌐 Google: Search "Athex black hat"**

Support Channels
Channel	Purpose	Response Time
WhatsApp	Urgent issues	1-2 hours
YouTube Comments	General questions	48 hours
GitHub Issues	Bug reports	48 hours
Email	Business inquiries	72 hours



## 📝 Changelog
Version 2.0 (Current)
✅ Complete GUI redesign with 10 tabs

✅ Multi-threaded analysis engine

✅ SQLite caching system

✅ 5 export formats (JSON/TXT/HTML/CSV/PDF)

✅ Risk scoring algorithm (0-100)

✅ Batch processing capability

✅ API configuration interface

✅ Pattern recognition module

✅ 15+ new platform checks

✅ Professional reporting features

## Version 1.0 (Legacy)
✅ Basic CLI interface

✅ Phone number validation

✅ Carrier/location lookup

✅ Social media URL generation

✅ Google dorks creation

✅ Simple reporting


***⚠️ Final Warning***
<p align="center"> <b>THIS TOOL IS FOR AUTHORIZED SECURITY RESEARCH ONLY</b><br> <i>Misuse may result in legal consequences</i> </p><p align="center"> <b>Always:</b><br> ✓ Get written authorization<br> ✓ Comply with local laws<br> ✓ Respect privacy rights<br> ✓ Document your activities<br> ✓ Use responsibly </p>
<p align="center"> <b>Created with 🖤 by ATHEX BLACK HAT</b><br> <i>Securing the digital world, one number at a time</i> </p><p align="center"> <sub>© 2026 ATHEX BLACK HAT. All rights reserved.</sub><br> <sub>For authorized use only. Version 2.0</sub> </p>
