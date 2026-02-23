#!/bin/bash

# NUMBER-OSINT Installation Script
# Created with love for OSINT enthusiasts

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color
BOLD='\033[1m'

print_center() {
    term_width=$(tput cols)
    padding=$(printf '%0.1s' " "{1..500})
    printf '%*.*s %s %*.*s\n' 0 "$(((term_width-2-${#1})/2))" "$padding" "$1" 0 "$(((term_width-1-${#1})/2))" "$padding"
}

clear


echo -e "${RED}"
cat << "EOF"
    ███╗   ██╗██╗   ██╗███╗   ███╗██████╗ ███████╗██████╗     ██████╗ ███████╗██╗███╗   ██╗████████╗
    ████╗  ██║██║   ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗   ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
    ██╔██╗ ██║██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝   ██║   ██║███████╗██║██╔██╗ ██║   ██║   
    ██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗   ██║   ██║╚════██║██║██║╚██╗██║   ██║   
    ██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║   ╚██████╔╝███████║██║██║ ╚████║   ██║   
    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
EOF
echo -e "${NC}"

echo -e "${CYAN}"
print_center "⚡ Phone Number OSINT Tool Installation ⚡"
print_center "Version 2.0 | Made for Security Researchers"
echo -e "${NC}"

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

progress_bar() {
    local duration=$1
    local steps=20
    for ((i=0; i<=steps; i++)); do
        percentage=$((i * 100 / steps))
        filled=$((i * 50 / steps))
        empty=$((50 - filled))
        printf "\r${CYAN}[${GREEN}"
        printf "%0.s█" $(seq 1 $filled)
        printf "${RED}"
        printf "%0.s█" $(seq 1 $empty)
        printf "${CYAN}] ${WHITE}%d%%${NC}" "$percentage"
        sleep $(echo "$duration / $steps" | bc -l 2>/dev/null || echo "0.05")
    done
    echo
}

matrix_effect() {
    echo -e "${GREEN}"
    for ((i=0; i<3; i++)); do
        for ((j=0; j<10; j++)); do
            echo -n "$(($RANDOM % 2))"
            sleep 0.01
        done
        echo -ne "\r"
        for ((j=0; j<10; j++)); do
            echo -n " "
        done
        echo -ne "\r"
    done
    echo -e "${NC}"
}

if command -v apt &> /dev/null; then
    echo -e "${YELLOW}[!] Checking system requirements...${NC}"
    sleep 1
    
    echo -e "${BLUE}[*] Updating package list...${NC}"
    (sudo apt update > /dev/null 2>&1) &
    spinner $!
    echo -e "${GREEN}[✓] Package list updated${NC}"
    
    echo -e "${BLUE}[*] Checking Python installation...${NC}"
    if ! command -v python3 &> /dev/null; then
        echo -e "${YELLOW}[!] Python3 not found. Installing...${NC}"
        (sudo apt install python3 -y > /dev/null 2>&1) &
        spinner $!
    fi
    
    if ! command -v pip3 &> /dev/null; then
        echo -e "${YELLOW}[!] pip3 not found. Installing...${NC}"
        (sudo apt install python3-pip -y > /dev/null 2>&1) &
        spinner $!
    fi
    echo -e "${GREEN}[✓] Python requirements satisfied${NC}"
fi

echo -e "\n${PURPLE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║${YELLOW}      📦 Installing Required Python Packages 📦         ${PURPLE}║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════════╝${NC}\n"

packages=(
    "phonenumbers"
    "requests"
    "beautifulsoup4"
    "dnspython"
    "python-whois"
    "fake-useragent"
    "pycountry"
    "folium"
    "colorama"
    "pandas"
    "numpy"
    "pyqt5"
    "pyqtgraph"
    "matplotlib"
)

total=${#packages[@]}
current=0

for package in "${packages[@]}"; do
    current=$((current + 1))
    echo -e "${CYAN}[${current}/${total}]${NC} Installing ${WHITE}$package${NC}..."
    
    matrix_effect
    
    (pip3 install "$package" -q 2>/dev/null) &
    spinner $!
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}  └─✓ Successfully installed $package${NC}"
    else
        echo -e "${RED}  └─✗ Failed to install $package${NC}"
    fi
    
    progress=$(echo "scale=2; $current/$total*100" | bc -l)
    printf "${BLUE}Overall Progress:${NC} "
    progress_bar 0.1
    echo
done

echo -e "${YELLOW}[*] Installing additional dependencies...${NC}"
(pip3 install --upgrade pip setuptools wheel > /dev/null 2>&1) &
spinner $!


echo -e "${PURPLE}${GREEN} 🔍 Verifying Installation Status 🔍 ${PURPLE}${NC}"

for package in "${packages[@]}"; do
    echo -ne "${CYAN}Checking $package... ${NC}"
    if pip3 list 2>/dev/null | grep -i "$package" > /dev/null; then
        echo -e "${GREEN}✓ Installed${NC}"
    else
        echo -e "${RED}✗ Not Found${NC}"
        echo -ne "${YELLOW}  └─Retrying...${NC}"
        pip3 install "$package" -q > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "${GREEN} Success${NC}"
        else
            echo -e "${RED} Failed${NC}"
        fi
    fi
    sleep 0.3
done

echo -e "\n${CYAN}"
for i in {1..3}; do
    echo -n "."
    sleep 0.5
done
echo -e "${NC}"

echo -e "${GREEN}"
cat << "EOF"
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     ✨ ALL PACKAGES INSTALLED SUCCESSFULLY! ✨          ║
    ║                                                          ║
    ║        🚀 READY TO LAUNCH NUMBER-OSINT 🚀               ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}Launching main script in:${NC}"
for i in {3..1}; do
    echo -e "${CYAN}$i...${NC}"
    sleep 1
done

if [ -f "main.py" ]; then
    echo -e "${GREEN}[✓] Executing ${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}\n"
    
    chmod +x main.py
    python3 main.py
else
    echo -e "${RED}[✗] Error: main.py not found in current directory!${NC}"
    echo -e "${YELLOW}Please make sure main.py is in the same directory as this script.${NC}"
    exit 1
fi