#!/usr/bin/python3
import argparse
import os
import subprocess
import shutil
import sys
import json
import platform
import threading
from colorama import Fore, Style, init
import ipaddress
from urllib.parse import urlparse


# Initialize colorama
init()

# ------------------------------------------------------------------
# Banner
# ------------------------------------------------------------------


def banner():
    print("               __                      ")
    print("   ____  ___  / /_______________ _____ ")
    print("  / __ \\/ _ \\/ __/ ___/ ___/ __ `/ __ \\")
    print(" / / / /  __/ /_(__  ) /__/ /_/ / / / /")
    print("/_/ /_/\\___/\\__/____/\\___/\\__,_/_/ /_/ ")
    print("                                       ")
    print("    github.com/riteshs4hu")
    print("\n")


# ------------------------------------------------------------------
# Print Functions
# ------------------------------------------------------------------

def INFO_PRINT():
    return (Fore.BLUE + " [ INFO  ] " + Style.RESET_ALL)
    
def WARNING_PRINT():
    return (Fore.YELLOW + " [WARNING] " + Style.RESET_ALL)

def ERROR_PRINT():
    return (Fore.RED + " [ ERROR ] " + Style.RESET_ALL)

def SUCCESS_PRINT():
    return (Fore.GREEN + " [SUCCESS] " + Style.RESET_ALL)

def NOTIFY_PRINT():
    return (Fore.MAGENTA + " [NOTIFY ] " + Style.RESET_ALL)


# ------------------------------------------------------------------
# Nmap Full Port Scan
# ------------------------------------------------------------------

def NMAP():
    print(f"{INFO_PRINT()} Nmap Full Scan is Running")
    if TARGET_HOST:
        subprocess.run(f"nmap -v -p- -sT -sV -sC {TARGET_HOST} -oA {NMAP_FILE} ", capture_output=True, text=True, shell=True)
    elif TARGET_HOST_LIST:
        subprocess.run(f"nmap -v -p- -sT -sV -sC -iL {TARGET_HOST_LIST} -oA {NMAP_FILE}", capture_output=True, text=True, shell=True)
    print(f"{SUCCESS_PRINT()} Nmap Full Scan Complete")

    print(f"{INFO_PRINT()} Nmap Udp Scan is Running")
    UDP_PORTS="7,53,67,68,69,88,111,123,135,137,138,161,162,445,631,749,1434,1812,1813,2049,5432"
    if TARGET_HOST:
        subprocess.run(f"nmap -v -Pn -sU -sV -sC -p {UDP_PORTS} {TARGET_HOST} -oA {NMAP_UDP_FILE}", capture_output=True, text=True, shell=True)
    elif TARGET_HOST_LIST:
        subprocess.run(f"nmap -v -Pn -sU -sV -sC -p {UDP_PORTS} -iL {TARGET_HOST_LIST} -oA {NMAP_UDP_FILE}", capture_output=True, text=True, shell=True)
    print(f"{SUCCESS_PRINT()} Nmap UDP Scan Complete")

def NUCLEI():
    print(f"{INFO_PRINT()} Nuclei Run on Naabu Top Ports Result")
    subprocess.run(f"nuclei -l {NAABU_TOP_PORT_FILE} -o {NUCLEI_SCAN}", capture_output=True, text=True, shell=True)
    print(f"{SUCCESS_PRINT()} Nuclei Scan is Complete")


def DIRSEARCH():
    print(f"{INFO_PRINT()} Dirsearch Run on Web urls")
    subprocess.run(f"dirsearch -l {WEB_URLS} -o {DIRSEARCH_SCAN}", capture_output=True, text=True, shell=True)
    print(f"{SUCCESS_PRINT()} Dirsearch Scan is Complete")

def NIKTO():
    print(f"{INFO_PRINT()} Nikto Run on Web urls")
    os.makedirs(NIKTO_SCAN_DIR)
    with open(f'{WEB_URLS}', 'r') as urls:
        for line in urls:
            url = line.strip()
            if url:
                host_name = url.split('//')[-1].split('/')[0]
                nikto_output = os.path.join(NIKTO_SCAN_DIR, f"{host_name}.txt")
                subprocess.run(f"nikto -ask auto -C all -url {url} -o {nikto_output}", capture_output=True, text=True, shell=True)
    print(f"{SUCCESS_PRINT()} Nikto Scan is Complete")

def TESTSSL():
    print(f"{INFO_PRINT()} Testssl Run on Web urls")
    subprocess.run(f"testssl --quiet --overwrite --logfile {TESTSSL_SCAN} --file {WEB_URLS}", capture_output=True, text=True, shell=True)
    print(f"{SUCCESS_PRINT()} Testssl Scan is Complete")

def WHATWEB():
    print(f"{INFO_PRINT()} Whatweb Run on Web urls")
    subprocess.run(f"whatweb --input-file {WEB_URLS} --log-brief {WHATWEB_SCAN}", capture_output=True, text=True, shell=True)
    print(f"{SUCCESS_PRINT()} Whatweb Scan is Complete")

def WAPPALYZER():
    print(f"{INFO_PRINT()} Wappalyzer Run on Web urls")
    os.makedirs(WAPPALYZER_SCAN_DIR)
    with open(f'{WEB_URLS}', 'r') as urls:
        for line in urls:
            url = line.strip()
            if url and not url.endswith('/'):
                url += '/'
            if url:
                host_name = url.split('//')[-1].split('/')[0]
                wapp_output = os.path.join(WAPPALYZER_SCAN_DIR, f"{host_name}.txt")
                with open(wapp_output, "w") as f:
                    subprocess.run(["wappalyzer", "-disable-ssl", "-target", url], stdout=f, stderr=subprocess.DEVNULL)

    print(f"{SUCCESS_PRINT()} Wappalyzer Scan is Complete")

def HEADI():
    print(f"{INFO_PRINT()} Headi Run on Web urls")
    os.makedirs(HEADI_SCAN_DIR)
    with open(f'{WEB_URLS}', 'r') as urls:
        for line in urls:
            url = line.strip()
            if url and not url.endswith('/'):
                url += '/'
            if url:
                host_name = url.split('//')[-1].split('/')[0]
                headi_output = os.path.join(HEADI_SCAN_DIR, f"{host_name}.txt")
                with open(headi_output, "w") as f:
                    subprocess.run(["headi", "-u", url], stdout=f, stderr=subprocess.DEVNULL)

    print(f"{SUCCESS_PRINT()} Headi Scan is Complete")

def HTTPX():
    print(f"{INFO_PRINT()} HTTPX Running on Naabu Top Ports Result")
    subprocess.run(f"httpx -sc -probe -method -hash -title -server -td -l {NAABU_TOP_PORT_FILE} -json -silent -o {HTTPX_FILE}", capture_output=True, text=True, shell=True)
    print(f"{SUCCESS_PRINT()} Httpx is Complete")

    # ------------------------------------------------------------------
    # Filter Web and Non-Web Ports
    # ------------------------------------------------------------------

    print(f"{INFO_PRINT()} Extract Web and Non-Web Ports ulrs")

    with open(f"{HTTPX_FILE}", "r") as f:
        lines = [json.loads(line) for line in f if line.strip()]

    with open(f"{WEB_URLS}", "w") as web_out:
        for entry in lines:
            if not entry.get("failed", False):
                if "url" in entry:
                    web_out.write(entry["url"] + "\n")

    # Write input values for entries where "failed" is true
    with open(f"{NON_WEB_PORTS}", "w") as failed_out:
        for entry in lines:
            if entry.get("failed", False):
                if "input" in entry:
                    failed_out.write(entry["input"] + "\n")
    
    # ------------------------------------------------------------------
    # Run Tools in Threads If Installed 
    # ------------------------------------------------------------------
    
    if os.path.getsize(WEB_URLS) != 0: # Only run if web url file is not empty

        tools_with_functions = {
            "dirsearch": DIRSEARCH,
            "nikto": NIKTO,
            "testssl": TESTSSL,
            "whatweb": WHATWEB,
            "wappalyzer": WAPPALYZER,
            "headi": HEADI,
        }

        threads = []
        for tool, func in tools_with_functions.items():
            if shutil.which(tool):
                t = threading.Thread(target=func)
                t.start()
                threads.append(t)
            else:
                print(f"{WARNING_PRINT()} Skipping {tool} — not installed")
        
        # Wait for all threads to complete
        for t in threads:
            t.join()

def NAABU_TOP_PORTS():
    print(f"{INFO_PRINT()} Naabu Top Scan is Running on target")
    if TARGET_HOST:
        subprocess.run(f"naabu -top-ports 1000 -host {TARGET_HOST} -o {NAABU_TOP_PORT_FILE} ", capture_output=True, text=True, shell=True)
    elif TARGET_HOST_LIST:
        subprocess.run(f"naabu -top-ports 1000 -list {TARGET_HOST_LIST} -o {NAABU_TOP_PORT_FILE}", capture_output=True, text=True, shell=True)
    print(f"{SUCCESS_PRINT()} Naabu Top Ports Scanning is Complete")
    # ------------------------------------------------------------------
    # Start Nuclei and Httpx Scan Parallel
    # ------------------------------------------------------------------
    
    NUCLEI_THREAD = threading.Thread(target=NUCLEI)
    HTTPX_THREAD = threading.Thread(target=HTTPX)
    
    # Start the tasks
    NUCLEI_THREAD.start()
    HTTPX_THREAD.start()
    
    # Wait for all A tasks to finish
    NUCLEI_THREAD.join()
    HTTPX_THREAD.join()

def NAABU_FULL_PORT():
    print(f"{INFO_PRINT()} Naabu Full Ports Scan is Running on target")
    if TARGET_HOST:
        subprocess.run(f"naabu -p - -host {TARGET_HOST} -o {NAABU_FILE} ", capture_output=True, text=True, shell=True)
    elif TARGET_HOST_LIST:
        subprocess.run(f"naabu -p - -list {TARGET_HOST_LIST} -o {NAABU_FILE}", capture_output=True, text=True, shell=True)
    print(f"{SUCCESS_PRINT()} Naabu Full Port Scanning is Complete")


def WAYBACK(domain):
    os.makedirs(WAYBACK_DIR, exist_ok=True)
    wayback_output = os.path.join(WAYBACK_DIR, f"{domain}.txt")
    with open(wayback_output, "w") as f:
        subprocess.run(["waybackurls", domain], stdout=f, stderr=subprocess.DEVNULL)

def GAU(domain):
    os.makedirs(GAU_DIR, exist_ok=True)
    gau_output = os.path.join(GAU_DIR, f"{domain}.txt")
    subprocess.run(f"gau --subs {domain} --o {gau_output}", capture_output=True, text=True, shell=True)

def PROD():

    def strip_scheme(url):
        parsed = urlparse(url)
        host = parsed.netloc or parsed.path
        # Remove port if present
        return host.split(':')[0]

    def dnsx_ptr(ip):
        result = subprocess.run(["dnsx", "-ptr", "-silent", "-ro"], input=ip, text=True, capture_output=True)
        return result.stdout.strip()

    def is_ip(target):
        try:
            ipaddress.ip_address(target)
            return True
        except ValueError:
            return False
    

    print(f"{INFO_PRINT()} Prod Scan is Running on target")
    if TARGET_HOST:
        target = strip_scheme(TARGET_HOST)
        if is_ip(target):
            domain = dnsx_ptr(target)
            if domain:
                print(f"{INFO_PRINT()} PTR record found: {domain}")
                WAYBACK(domain)
                GAU(domain)
            else:
                print(f"{WARNING_PRINT()} {target} Domain not found. Skipping for Prod scanning.")
        else:
            WAYBACK(target)
            GAU(target)

    elif TARGET_HOST_LIST:
        with open(f'{TARGET_HOST_LIST}', "r") as f:
            targets = f.read().splitlines()
            for target in targets:
                if not target:
                    continue
                target = strip_scheme(target)
                if is_ip(target):
                    domain = dnsx_ptr(target)
                    if domain:
                        WAYBACK(domain)
                        GAU(domain)
                    else:
                        print(f"{WARNING_PRINT()} {target} Domain not found. Skipping for Prod scanning.")
                else:
                    WAYBACK(target)
                    GAU(target)

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(usage='netscan.py [-t|--target, -l|--list] target [Options]')
    parser.add_argument('-t', '--target', help='Target Domain or IP Address')
    parser.add_argument('-l', '--list', help='Path to file containing a List of Target Hosts to scan (one per line)')
    parser.add_argument('-o', '--output', help='Define Output Folder', default='netscan')
    parser.add_argument('-s', '--silent', action='store_true', help='Disable Print the Banner')
    parser.add_argument('-p', '--prod', action='store_true', help='Enable Production Environment Scanning')
    parser.add_argument('-f', '--force', action='store_true', help='Skipping the tools Scanning')
    parser.add_argument('-d', '--disable', action='store_true', help='Disable Other Scanning (Used for prod scan only)')
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # Files And Directory Variables
    # ------------------------------------------------------------------
    global TARGET_HOST, TARGET_HOST_LIST, NMAP_FILE, NMAP_UDP_FILE, NAABU_TOP_PORT_FILE, NAABU_FILE, NUCLEI_SCAN, HTTPX_FILE, WEB_URLS, NON_WEB_PORTS, DIRSEARCH_SCAN, WHATWEB_SCAN, WAPPALYZER_SCAN_DIR, HEADI_SCAN_DIR, TESTSSL_SCAN, NIKTO_SCAN_DIR, WAYBACK_DIR, GAU_DIR
    OUTPUT_DIR = args.output
    TARGET_HOST = args.target
    TARGET_HOST_LIST = args.list
    NMAP_FILE = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Nmap-Full-Scan'))
    NMAP_UDP_FILE = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Nmap-UDP-Scan'))
    NAABU_TOP_PORT_FILE = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Naabu-Top-1000-Ports-Scan.txt'))
    NAABU_FILE = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Naabu-Full-Scan.txt'))
    NUCLEI_SCAN = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Nuclei-Scan.txt'))
    HTTPX_FILE = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Httpx-Scan.json'))
    WEB_URLS = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Web-urls.txt'))
    NON_WEB_PORTS = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Non-Web-Ports.txt'))
    DIRSEARCH_SCAN = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Dirsearch-Scan.txt'))
    WHATWEB_SCAN = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Whatweb-Scan.txt'))
    WAPPALYZER_SCAN_DIR = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Wappalyzer-Scan'))
    HEADI_SCAN_DIR = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Headi-Scan'))
    TESTSSL_SCAN = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Testssl-Scan.txt'))
    NIKTO_SCAN_DIR = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Nikto-Scan'))
    WAYBACK_DIR = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Waybacurl-Result'))
    GAU_DIR = os.path.normpath(os.path.join(os.getcwd(), OUTPUT_DIR, 'Gau-Result'))

    # ------------------------------------------------------------------
    # Execution start
    # ------------------------------------------------------------------
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    elif not args.target and not args.list:
        print(f"{ERROR_PRINT()} Target is missing, try using -t <Target Domain or IP Address> / -l <ip_list>")
        print(f"{ERROR_PRINT()} Please provide any one TARGET Option")
    elif args.target and args.list:
        print(f"{ERROR_PRINT()} Multiple Target are provide, try using -t <Target Domain or IP Address> / -l <ip_list>")
        print(f"{ERROR_PRINT()} Please provide Only one TARGET Option")
        
    elif args.target or args.list:
        # ------------------------------------------------------------------
        # Check Avilable Tools install or Not
        # ------------------------------------------------------------------
        tools = ['nmap','naabu','nuclei','httpx','dirsearch']
        optional_tools = ['nikto','testssl','whatweb','wappalyzer','dnsx','headi','curl']
        for tool in tools:
            if args.force:
                continue
            elif not shutil.which(tool):
                print(f"{ERROR_PRINT()} {tool} Not found Please Install...")
                sys.exit(1)

        # Check Silent Mode or Not
        if not args.silent:
            banner()

        for optional in optional_tools:
            if args.force:
                continue
            elif not shutil.which(optional):
                print(f"{ERROR_PRINT()} {optional} Not found please install for more result ...")
        
        # ------------------------------------------------------------------
        # Output Directory And Files Manage
        # ------------------------------------------------------------------
        if os.path.exists(OUTPUT_DIR):
            print(f"{ERROR_PRINT()} {OUTPUT_DIR} Directory already Exists Please choose a different location")
            sys.exit(1)
        else:
            os.makedirs(OUTPUT_DIR)
        # ------------------------------------------------------------------
        # Check OS
        # ------------------------------------------------------------------
        if platform.system() == "Windows":
            print(f"{INFO_PRINT()} The script is running on Windows")
        elif platform.system() == "Linux":
            print(f"{INFO_PRINT()} The script is running on Linux")
        else:
            print(f"{INFO_PRINT()} Unknown OS")
        # ------------------------------------------------------------------
        # Start Nmap and Naabu Scan Parallel
        # ------------------------------------------------------------------


        if args.disable:
            PROD_SCAN = threading.Thread(target=PROD)
            PROD_SCAN.start()
            PROD_SCAN.join()
        else:
            NMAP_FULL_SCAN = threading.Thread(target=NMAP)
            NAABU_SCAN = threading.Thread(target=NAABU_TOP_PORTS)
            NAABU_FULL_SCAN = threading.Thread(target=NAABU_FULL_PORT)
            if args.prod:
                PROD_SCAN = threading.Thread(target=PROD)

            # Start the tasks
            NMAP_FULL_SCAN.start()
            NAABU_SCAN.start()
            NAABU_FULL_SCAN.start()
            if args.prod:
                PROD_SCAN.start()
            
            # Wait for all A tasks to finish
            NMAP_FULL_SCAN.join()
            NAABU_SCAN.join()
            NAABU_FULL_SCAN.join()
            if args.prod:
                PROD_SCAN.join()
        
        
if __name__ == "__main__":
    main()
