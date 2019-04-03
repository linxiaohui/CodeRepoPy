# 列表分组
l=[1,2,3,4,5,6,7]
list(zip(*[iter(l)]*2))

for x in range(101):print"fizz"[x%3*4::]+"buzz"[x%5*4::]or x

#python 获得本机MAC地址
import uuid
def get_mac_address():  
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]  
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

import socket
#获取本机电脑名
myname = socket.getfqdn(socket.gethostname(  ))
#获取本机ip
myaddr = socket.gethostbyname(myname)

# 生成一个UDP包，把自己的 IP 放入到 UDP 协议头中，然后从UDP包中获取本机的IP
# 这个方法并不会真实的向外部发包，所以用抓包工具是看不到的。但是会申请一个 UDP 的端口
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
ip = s.getsockname()[0]
s.close()


#在linux下可用
import fcntl
import struct
import socket
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
  
get_ip_address('lo')
#'127.0.0.1'
  
get_ip_address('eth0')
#'38.113.228.130'
