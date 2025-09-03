<h1 align="center">NetScan</h1>

**NetScan** is an automated **network and web reconnaissance** designed for penetration testers. It combines popular security tools to perform **port scanning, service detection, vulnerability scanning, and web enumeration** in one streamlined workflow.

## Features
- Full TCP & UDP scanning with **Nmap**
- Fast port scanning with **Naabu**
- Web service detection and fingerprinting with **Httpx, WhatWeb, Wappalyzer, Headi**
- Directory brute-forcing with **Dirsearch**
- SSL/TLS testing with **Testssl**
- Vulnerability scanning with **Nuclei**
- Historical URLs gathering with **Waybackurls** and **Gau**
- Clean and organized output structure
- Parallel scanning for maximum efficiency

## Requirements

### Mandatory Tools
- [nmap](https://nmap.org/)
- [naabu](https://github.com/projectdiscovery/naabu)
- [nuclei](https://github.com/projectdiscovery/nuclei)
- [httpx](https://github.com/projectdiscovery/httpx)
- [dirsearch](https://github.com/maurosoria/dirsearch)

### Optional Tools
- nikto  
- testssl  
- whatweb  
- wappalyzer  
- dnsx 
- headi  
- waybackurls  
- gau  

> 💡 Use the `-f` flag to skip tool installation checks.


## Installation

```bash
git clone https://github.com/riteshs4hu/netscan.git
cd netscan
chmod +x netscan.py
````

## Usage

```bash
python3 netscan.py [OPTIONS]
```

### Options

| Flag                         | Description                                  |
| ---------------------------- | -------------------------------------------- |
| `-t` / `--target` `<target>` | Target domain or IP address                  |
| `-l` / `--list` `<file>`     | File containing a list of targets            |
| `-o` / `--output` `<folder>` | Output directory (default: `netscan`)        |
| `-s` / `--silent`            | Run silently (no banner)                     |
| `-p` / `--prod`              | Enable production recon (Wayback, Gau, DNSX) |
| `-f` / `--force`             | Skip tool installation checks                |
| `-d` / `--disable`           | Disable port scanning, only run prod recon   |


## Examples

```bash
# Scan a single target
python3 netscan.py -t example.com

# Scan multiple targets from a file
python3 netscan.py -l targets.txt

# Run in silent mode (no banner)
python3 netscan.py -t example.com -s

# Run only prod recon (Wayback + Gau + DNSX)
python3 netscan.py -t example.com -d

# Skip tool checks and force run
python3 netscan.py -t example.com -f

# Save results to a custom directory
python3 netscan.py -t example.com -o myscan
```

## Working Flow

```
┌─────────────────────────────────────────┐
│               Start Script              │
└─────────────────────────────────────────┘
                │
                ▼
     ┌────────────────────────┐
     │ Parse CLI Arguments    │
     │ -l (list)              │
     │ -s (silent)            │
     │ -p (prod)              │
     │ -f (force)             │
     └────────────────────────┘
                │
                ▼
     ┌────────────────────────┐
     │ Validate Input         │
     │ - Must have -t or -l   │
     │ - Error if both used   │
     └────────────────────────┘
                │
                ▼
     ┌────────────────────────┐
     │ Setup Output Folders   │
     │ (e.g., Nmap, Naabu,    │
     │ Httpx, Wayback dirs)   │
     └────────────────────────┘
                │
                ▼
 ┌────────────────────────────┐
 │ Check Installed Tools      │
 │ - Skip if (-f) Force mode  │
 │ - Warn about missing tools │
 └────────────────────────────┘
                │
                ▼
   ┌─────────────────────────┐
   │ Print Banner            │
   │ - Skip if (-s) Silent   │
   └─────────────────────────┘
                │
                ▼
   ┌─────────────────────────┐
   │ Detect OS (Linux/Win)   │
   └─────────────────────────┘
                │
                ▼
   ┌─────────────────────────────────────┐
   │ Is "-d" (disable) set?             │
   │  YES → Run PROD Scan ONLY          │
   │         (Wayback, Gau, DNSX)       │
   │         → Exit                     │
   └─────────────────────────────────────┘
                │ NO
                ▼
   ┌─────────────────────────────────────┐
   │ Run Scans in Parallel Threads:      │
   │  • Nmap Full TCP/UDP Scan          │
   │  • Naabu Top Ports → Nuclei+Httpx  │
   │  • Naabu Full Ports                │
   │  • If "-p" → Run PROD Scan too     │
   └─────────────────────────────────────┘
                │
                ▼
   ┌─────────────────────────────────────┐
   │ HTTPX Parses JSON → Extract URLs   │
   │  • Save Web URLs → Web-urls.txt    │
   │  • Save Non-Web → Non-Web-Ports.txt│
   └─────────────────────────────────────┘
                │
                ▼
   ┌─────────────────────────────────────┐
   │ Run Web Recon (Parallel Threads):   │
   │  • dirsearch                        │
   │  • nikto                            │
   │  • testssl                          │
   │  • whatweb                          │
   │  • wappalyzer                       │
   │  • headi                            │
   └─────────────────────────────────────┘
                │
                ▼
   ┌─────────────────────────┐
   │ Save All Results        │
   │ Organized in Output Dir │
   └─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│              End of Script              │
└─────────────────────────────────────────┘
```
