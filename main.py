#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NUMBER-OSINT Main Launcher
Advanced Phone Number OSINT Tool
Version: 1.0
"""

import os
import sys
import time
import subprocess
import importlib.util
from pathlib import Path

# Try to import colorama for cross-platform colored output
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Create dummy color classes if colorama not available
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    class Back:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''

# Animation functions
def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text, color=Fore.WHITE, width=None):
    """Print centered text"""
    if width is None:
        width = os.get_terminal_size().columns
    padding = (width - len(text)) // 2
    print(' ' * padding + color + text + Fore.RESET)

def loading_animation(duration=2, text="LOADING"):
    """Display a loading animation"""
    animation = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", 
                 "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]",
                 "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", 
                 "[■■■■■■■■■■]"]
    
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f'\r{Fore.CYAN}{text} {animation[i % len(animation)]}{Fore.RESET}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print()

def matrix_rain_effect(lines=5):
    """Create a mini matrix rain effect"""
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ"
    for _ in range(lines):
        line = ''
        for _ in range(os.get_terminal_size().columns):
            line += chars[hash(str(time.time())) % len(chars)]
        print(Fore.GREEN + line[:os.get_terminal_size().columns] + Fore.RESET)
        time.sleep(0.05)

def typing_effect(text, color=Fore.WHITE, delay=0.03):
    """Type out text character by character"""
    for char in text:
        sys.stdout.write(color + char + Fore.RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def pulse_effect(text, color=Fore.CYAN, repetitions=3):
    """Create a pulsing effect on text"""
    for _ in range(repetitions):
        sys.stdout.write('\r' + ' ' * len(text))
        sys.stdout.write('\r' + Style.BRIGHT + color + text + Fore.RESET)
        sys.stdout.flush()
        time.sleep(0.3)
        sys.stdout.write('\r' + ' ' * len(text))
        sys.stdout.write('\r' + Style.NORMAL + color + text + Fore.RESET)
        sys.stdout.flush()
        time.sleep(0.3)
    print()

def progress_bar(percentage, width=50, color=Fore.GREEN):
    """Display a progress bar"""
    filled = int(width * percentage // 100)
    bar = color + '█' * filled + Fore.WHITE + '░' * (width - filled) + Fore.RESET
    sys.stdout.write(f'\r{bar} {percentage}%')
    sys.stdout.flush()

def countdown_animation(seconds=3):
    """Countdown animation"""
    for i in range(seconds, 0, -1):
        pulse_effect(f"⏰ Starting in {i}...", Fore.YELLOW, 1)

# Banner display
def display_banner():
    """Display the main ASCII banner"""
    banner = f"""
{Fore.RED}

                                                                   
   ███╗   ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗██████╗          
   ████╗  ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗         
   ██╔██╗ ██║██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝         
   ██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗         
   ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║         
   ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝        
                                                                   
   {Fore.CYAN} ██████╗ ███████╗██╗███╗   ██╗████████╗{Fore.RED}   
   {Fore.CYAN}██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝{Fore.RED}   
   {Fore.CYAN}██║   ██║███████╗██║██╔██╗ ██║   ██║{Fore.RED}   
   {Fore.CYAN}██║   ██║╚════██║██║██║╚██╗██║   ██║{Fore.RED}   
   {Fore.CYAN}╚██████╔╝███████║██║██║ ╚████║   ██║{Fore.RED}   
   {Fore.CYAN} ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝{Fore.RED}   
{Fore.RESET}"""
    
    print(banner)
    
    # Print version and info
    version_text = "⚡ PHONE NUMBER OSINT FRAMEWORK ⚡"
    creator_text = "Created for Security Researchers | Version 2.0"
    
    print_centered(version_text, Fore.YELLOW + Style.BRIGHT)
    print_centered(creator_text, Fore.CYAN)
    print()

def check_src_directory():
    """Check if src directory exists and contains required files"""
    src_path = Path(__file__).parent / "src"
    
    if not src_path.exists():
        print(f"{Fore.RED}[✗] Error: 'src' directory not found!{Fore.RESET}")
        print(f"{Fore.YELLOW}Creating src directory...{Fore.RESET}")
        src_path.mkdir(exist_ok=True)
        time.sleep(1)
        
    return src_path

def create_template_files(src_path):
    """Create template files if they don't exist"""
    cli_path = src_path / "cli.py"
    gui_path = src_path / "gui.py"
    
    # Create template cli.py if it doesn't exist
    if not cli_path.exists():
        with open(cli_path, 'w') as f:
            f.write('''#!/usr/bin/env python3
# NUMBER-OSINT CLI Interface

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def main():
    """Main CLI function"""
    print("\\n" + "="*60)
    print("NUMBER-OSINT CLI MODE")
    print("="*60)
    print("\\n📱 Phone Number OSINT Tool - Command Line Interface")
    print("🔍 This is the CLI version of NUMBER-OSINT")
    print("\\n⚡ Features:")
    print("  • Phone number validation")
    print("  • Carrier information")
    print("  • Location tracking")
    print("  • Social media lookup")
    print("  • And more...")
    print("\\n" + "="*60)
    
    # Add your CLI logic here
    phone = input("\\n📞 Enter phone number (with country code): ").strip()
    
    if phone:
        print(f"\\n{Fore.GREEN}[✓] Processing number: {phone}{Fore.RESET}")
        print(f"{Fore.YELLOW}[*] This is a template. Implement your CLI logic in src/cli.py{Fore.RESET}")
    else:
        print(f"{Fore.RED}[✗] No number provided{Fore.RESET}")

if __name__ == "__main__":
    try:
        from colorama import init, Fore, Back, Style
        init(autoreset=True)
    except ImportError:
        class Fore:
            RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    main()
''')
        print(f"{Fore.GREEN}[✓] Created template cli.py{Fore.RESET}")
    
    # Create template gui.py if it doesn't exist
    if not gui_path.exists():
        with open(gui_path, 'w') as f:
            f.write('''#!/usr/bin/env python3
# NUMBER-OSINT GUI Interface

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False

def main():
    """Main GUI function"""
    if not PYQT_AVAILABLE:
        print("\\n" + "="*60)
        print("NUMBER-OSINT GUI MODE")
        print("="*60)
        print("\\n⚠️ PyQt5 is not installed!")
        print("Please install PyQt5 to use the GUI interface:")
        print("pip install pyqt5")
        print("\\n" + "="*60)
        return
    
    # Create Qt Application
    app = QApplication(sys.argv)
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("NUMBER-OSINT - Phone Number Intelligence")
    window.setGeometry(100, 100, 800, 600)
    
    # Set window icon and style
    window.setStyleSheet("""
        QMainWindow {
            background-color: #2b2b2b;
        }
        QLabel {
            color: #ffffff;
            font-size: 14px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            padding: 8px;
            border-radius: 4px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QLineEdit {
            padding: 8px;
            border: 2px solid #555;
            border-radius: 4px;
            font-size: 14px;
            background-color: #3b3b3b;
            color: white;
        }
    """)
    
    # Create central widget
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # Create layout
    layout = QVBoxLayout(central_widget)
    
    # Add title
    title = QLabel("📱 NUMBER-OSINT GUI")
    title.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50; padding: 10px;")
    title.setAlignment(Qt.AlignCenter)
    layout.addWidget(title)
    
    # Add subtitle
    subtitle = QLabel("Phone Number Intelligence Tool")
    subtitle.setStyleSheet("font-size: 16px; color: #888; padding-bottom: 20px;")
    subtitle.setAlignment(Qt.AlignCenter)
    layout.addWidget(subtitle)
    
    # Add input field
    input_layout = QHBoxLayout()
    input_label = QLabel("Phone Number:")
    input_label.setStyleSheet("font-size: 16px;")
    input_layout.addWidget(input_label)
    
    phone_input = QLineEdit()
    phone_input.setPlaceholderText("Enter phone number with country code...")
    input_layout.addWidget(phone_input)
    layout.addLayout(input_layout)
    
    # Add analyze button
    analyze_btn = QPushButton("🔍 Analyze Number")
    analyze_btn.setCursor(QCursor(Qt.PointingHandCursor))
    layout.addWidget(analyze_btn)
    
    # Add results area
    results_label = QLabel("Results will appear here...")
    results_label.setStyleSheet("""
        background-color: #3b3b3b;
        padding: 15px;
        border-radius: 5px;
        font-family: monospace;
        margin-top: 20px;
    """)
    results_label.setAlignment(Qt.AlignTop)
    results_label.setWordWrap(True)
    layout.addWidget(results_label)
    
    # Add spacer
    layout.addStretch()
    
    # Connect button
    def analyze():
        phone = phone_input.text().strip()
        if phone:
            results_label.setText(f"Processing: {phone}\\n\\n[!] This is a template. Implement your GUI logic in src/gui.py")
        else:
            results_label.setText("Please enter a phone number!")
    
    analyze_btn.clicked.connect(analyze)
    
    # Show window
    window.show()
    
    # Execute application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
''')
        print(f"{Fore.GREEN}[✓] Created template gui.py{Fore.RESET}")

def show_menu():
    """Display the main menu with animations"""
    print(f"{Fore.CYAN}{Fore.WHITE}                   MAIN MENU                                         {Fore.CYAN}{Fore.RESET}")
    print(f"{Fore.CYAN}{Fore.YELLOW}  [1] {Fore.GREEN}CLI MODE{Fore.WHITE} - Command Line Interface     {Fore.CYAN}{Fore.RESET}")
    print(f"{Fore.CYAN}{Fore.YELLOW}  [2] {Fore.GREEN}GUI MODE{Fore.WHITE} - Graphical User Interface   {Fore.CYAN}{Fore.RESET}")
    print(f"{Fore.CYAN}{Fore.YELLOW}  [3] {Fore.RED}EXIT{Fore.WHITE} - Exit the program                 {Fore.CYAN}{Fore.RESET}")
    
    print(f"\n{Fore.YELLOW}✨ Select an option (1-3):{Fore.RESET} ", end="")

def main():
    """Main function"""
    try:
        # Clear screen and show banner
        clear_screen()
        display_banner()
        
        # Matrix rain effect
        typing_effect("Initializing NUMBER-OSINT Framework...", Fore.CYAN, 0.02)
        time.sleep(0.5)
        matrix_rain_effects = 3
        loading_animation(2, "SYSTEM BOOT")
        
        # Check src directory
        src_path = check_src_directory()
        create_template_files(src_path)
        
        while True:
            # Show menu
            show_menu()
            
            try:
                choice = input().strip()
                
                if choice == '1':
                    # CLI Mode
                    print(f"\n{Fore.GREEN}[✓] Launching CLI Mode...{Fore.RESET}")
                    pulse_effect("CLI INTERFACE", Fore.GREEN, 2)
                    
                    # Run CLI script
                    cli_script = src_path / "cli.py"
                    if cli_script.exists():
                        countdown_animation(2)
                        print(f"\n{Fore.CYAN}{'='*60}{Fore.RESET}")
                        subprocess.run([sys.executable, str(cli_script)])
                        print(f"\n{Fore.CYAN}{'='*60}{Fore.RESET}")
                    else:
                        print(f"{Fore.RED}[✗] CLI script not found!{Fore.RESET}")
                    
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Fore.RESET}")
                    clear_screen()
                    display_banner()
                    
                elif choice == '2':
                    # GUI Mode
                    print(f"\n{Fore.GREEN}[✓] Launching GUI Mode...{Fore.RESET}")
                    pulse_effect("GUI INTERFACE", Fore.BLUE, 2)
                    
                    # Run GUI script
                    gui_script = src_path / "gui.py"
                    if gui_script.exists():
                        countdown_animation(2)
                        print(f"\n{Fore.CYAN}Starting GUI application...{Fore.RESET}")
                        subprocess.run([sys.executable, str(gui_script)])
                    else:
                        print(f"{Fore.RED}[✗] GUI script not found!{Fore.RESET}")
                    
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Fore.RESET}")
                    clear_screen()
                    display_banner()
                    
                elif choice == '3':
                    # Exit
                    print(f"\n{Fore.YELLOW}Shutting down NUMBER-OSINT...{Fore.RESET}")
                    
                    # Exit animation
                    for i in range(3, 0, -1):
                        sys.stdout.write(f'\r{Fore.RED}Exiting in {i}...{Fore.RESET}')
                        sys.stdout.flush()
                        time.sleep(1)
                    
                    print(f"\n\n{Fore.GREEN}Thank you for using NUMBER-OSINT! 👋{Fore.RESET}")
                    
                    # Final message
                    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════╗{Fore.RESET}")
                    print(f"{Fore.CYAN}║{Fore.WHITE}           Stay secure, happy OSINT hunting!              {Fore.CYAN}║{Fore.RESET}")
                    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════╝{Fore.RESET}")
                    break
                    
                else:
                    print(f"{Fore.RED}[✗] Invalid option! Please select 1, 2, or 3.{Fore.RESET}")
                    time.sleep(1.5)
                    
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}Interrupted by user. Exiting...{Fore.RESET}")
                break
            except EOFError:
                print(f"\n\n{Fore.YELLOW}Input error. Exiting...{Fore.RESET}")
                break
                
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Program terminated by user.{Fore.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[✗] An error occurred: {str(e)}{Fore.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()