# Linux Directory Structure Reference

A quick reference to the key directories in the Linux Filesystem Hierarchy Standard (FHS).

## Root Level

| Directory | Purpose |
|-----------|---------|
| `/` | Root of the entire filesystem. Everything lives under here. |
| `/bin` | Essential user commands (`ls`, `cp`, `cat`). Often a symlink to `/usr/bin` on modern systems. |
| `/sbin` | System administration binaries (`fdisk`, `ip`, `mount`). Often symlinked to `/usr/sbin`. |
| `/boot` | Bootloader files, kernel images (`vmlinuz`), and initramfs. |
| `/dev` | Device files representing hardware (`/dev/sda`, `/dev/null`, `/dev/tty`). |
| `/etc` | System-wide configuration files (text-based, editable). |
| `/home` | Users' personal directories (`/home/darren`). |
| `/root` | The root user's home directory (not `/home/root`). |
| `/lib`, `/lib64` | Shared libraries needed by binaries in `/bin` and `/sbin`. |
| `/media` | Auto-mount points for removable media (USB drives, DVDs). |
| `/mnt` | Temporary manual mount points. |
| `/opt` | Optional/third-party software (e.g., `/opt/google/chrome`). |
| `/proc` | Virtual filesystem exposing kernel and process info (`/proc/cpuinfo`, `/proc/<pid>/`). |
| `/run` | Runtime data since boot (PID files, sockets). Cleared on reboot. |
| `/srv` | Data served by the system (web, FTP). Rarely used in practice. |
| `/sys` | Virtual filesystem for kernel/hardware settings (sysfs). |
| `/tmp` | Temporary files. Usually cleared on reboot; world-writable. |
| `/usr` | Bulk of user-space programs and data (see below). |
| `/var` | Variable data — logs, caches, spools, databases (see below). |

## Inside /usr

| Directory | Purpose |
|-----------|---------|
| `/usr/bin` | Most user commands. |
| `/usr/sbin` | Most admin commands. |
| `/usr/lib` | Libraries and internal program files. |
| `/usr/local` | Software you compile/install yourself — kept separate from the package manager. |
| `/usr/share` | Architecture-independent data (docs, man pages, icons). |
| `/usr/include` | C/C++ header files. |

## Inside /var

| Directory | Purpose |
|-----------|---------|
| `/var/log` | System and application logs (`syslog`, `auth.log`, `journal/`). |
| `/var/cache` | Application cache (e.g., apt package cache). |
| `/var/spool` | Queued work — mail, cron jobs, print jobs. |
| `/var/lib` | Persistent state for services (databases, docker, package manager state). |
| `/var/tmp` | Temp files that survive reboots. |
| `/var/www` | Common default web server document root. |

## Inside /etc — Common Files

| File/Dir | Purpose |
|----------|---------|
| `/etc/passwd` | User account list. |
| `/etc/shadow` | Hashed passwords (root-only). |
| `/etc/group` | Group definitions. |
| `/etc/fstab` | Filesystems to mount at boot. |
| `/etc/hosts` | Static hostname → IP mappings. |
| `/etc/ssh/` | SSH server/client config. |
| `/etc/systemd/` | systemd units and config. |
| `/etc/crontab`, `/etc/cron.d/` | Scheduled tasks. |

## Quick Rules of Thumb

- **Config?** Look in `/etc`.
- **Logs?** Look in `/var/log` (or `journalctl` on systemd systems).
- **Your stuff?** `/home/<you>`; hidden config in `~/.config` and dotfiles.
- **Installing software manually?** Use `/usr/local` or `/opt`, not `/usr/bin`.
- **`/proc` and `/sys` aren't real files** — they're live views into the kernel; reading them is safe, writing changes kernel settings.
- **Don't put anything important in `/tmp`** — it may vanish on reboot.

## Directories Through a Cybersecurity Lens

The same directories matter differently to a defender, an investigator, or an attacker. This section is for hardening, incident response, and understanding where risk concentrates.

### Where attackers hide and persist

| Location | Why it matters |
|----------|----------------|
| `/tmp`, `/var/tmp`, `/dev/shm` | World-writable and often executable. Classic drop zones for downloaded payloads and staging. `/dev/shm` (shared memory) is especially favored because it's memory-backed and easy to overlook. Mount these `noexec,nosuid,nodev` where possible. |
| `/etc/cron.d/`, `/etc/cron.*`, `/var/spool/cron/` | Cron is a top persistence mechanism. A rogue job here re-launches malware on a schedule. |
| `/etc/systemd/system/`, `~/.config/systemd/user/` | Malicious systemd units/timers are the modern equivalent of cron persistence. |
| `~/.bashrc`, `~/.bash_profile`, `~/.profile`, `/etc/profile.d/` | Shell startup files run code on every login — common for user-level persistence. |
| `/etc/ld.so.preload`, `LD_PRELOAD` | Library preloading is used by userland rootkits to hook functions and hide processes/files. |
| `/etc/passwd`, `/etc/shadow`, `/etc/sudoers`, `/etc/sudoers.d/` | Targets for privilege escalation — added accounts, UID 0 duplicates, or sneaky sudo rules. |
| Hidden files/dirs (names starting with `.`) | Attackers hide artifacts as dotfiles or odd names like `/tmp/...` (dot-dot-space) to evade casual `ls`. |

### Where the evidence lives (forensics & IR)

| Location | What you'll find |
|----------|------------------|
| `/var/log/` | The primary trail: `auth.log`/`secure` (logins, sudo), `syslog`/`messages`, `wtmp`/`btmp` (login history), web/app logs. |
| `journalctl` (`/var/log/journal/`) | systemd's binary logs — often richer than text logs; survives across services. |
| `~/.bash_history`, `~/.*_history` | Shell command history. Frequently cleared or symlinked to `/dev/null` by attackers — its absence is itself a signal. |
| `/proc/<pid>/` | Live process introspection: `exe` (path to binary, even if deleted), `cwd`, `cmdline`, `fd/`, `maps`, `environ`. Essential for triaging a running process. |
| `/var/lib/`, `/var/spool/` | Persistent service state and queues — useful for reconstructing activity. |
| `/etc/` timestamps | Recently modified config files can reveal tampering; compare against package manager expectations. |

### Permissions & special bits to watch

| Concept | Security relevance |
|---------|--------------------|
| SUID/SGID binaries | Files that run with owner/group privileges. Audit with `find / -perm -4000 -o -perm -2000`. Unexpected SUID root binaries are a red flag and a common privesc vector. |
| World-writable files/dirs | `find / -perm -0002 -type f` — anything writable by all is a tampering risk, especially scripts or config. |
| `/etc/shadow` permissions | Should be `root`-owned and unreadable by others (`640` or stricter). Readable shadow = offline password cracking. |
| Mount options | `noexec`, `nosuid`, `nodev` on `/tmp`, `/var`, `/home`, `/dev/shm` limit what can run and escalate. Check `/etc/fstab`. |

### Hardening quick wins

- **Integrity monitoring:** Tools like AIDE or Tripwire baseline `/bin`, `/sbin`, `/usr`, `/etc` and alert on changes to system binaries and config.
- **Immutable binaries:** Package-managed files in `/usr/bin` etc. can be verified against the package DB (`dpkg --verify`, `rpm -Va`) to detect swapped binaries.
- **Least privilege on `/etc`:** Restrict who can read/write sensitive config; keep `sudoers` minimal and use `visudo`.
- **Log forwarding:** Ship `/var/log` and journald to a remote/append-only store so an attacker who gains root can't simply wipe local evidence.
- **Lock down the drop zones:** `noexec` mounts on `/tmp`, `/var/tmp`, `/dev/shm` break a lot of commodity malware that assumes it can execute there.

> **Note:** This section is for defensive security, hardening, and incident response. It describes *where* to look and *what* to protect — not techniques for compromising systems.

