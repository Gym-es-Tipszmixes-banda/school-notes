# Megoldókulcs 94%

## Hálózat felosztás

192.168.200.0/24

| Needed Size | Allocated Size | Address Mask        | Dec Mask        | Assignable Range                  | Broadcast       |
| ----------- | -------------- | ------------------- | --------------- | --------------------------------- | --------------- |
| 80          | 126            | 192.168.200.0 /25   | 255.255.255.128 | 192.168.200.1 - 192.168.200.126   | 192.168.200.127 |
| 45          | 62             | 192.168.200.128 /26 | 255.255.255.192 | 192.168.200.129 - 192.168.200.190 | 192.168.200.191 |
| 5           | 6              | 192.168.200.192 /29 | 255.255.255.248 | 192.168.200.193 - 192.168.200.198 | 192.168.200.199 |
| 5           | 6              | 192.168.200.200 /29 | 255.255.255.248 | 192.168.200.201 - 192.168.200.206 | 192.168.200.207 |

## PC5

```
ip:          172.16.3.3
subnet mask: 255.255.255.224
gateway:     172.16.3.30
```

## SRV3

```
ip:          172.16.3.38
subnet mask: 255.255.255.240
gateway:     172.16.3.33
```

## S1

```
en
conf t
line con 0
password ena44pa55
exit
ip default-gateway 192.168.200.233
enable secret ena22pa55
hostname S1
ip domain-name cisco.com
int g0/1
switchport mode trunk
int g0/2
switchport mode trunk
exit
int vlan40
ip address 192.168.200.235 255.255.255.248
no shutdown
exit
service password-encryption
ip ssh version 2
username admin secret ena44pa55
vlan 20
name VLAN0020
exit
vlan 30
name VLAN0030
vlan 40
name Management
exit
line vty 0
login local
transport input ssh
end
copy running-config startup-config

```

## S2

```
en
conf t
line con 0
password ena44pa55
exit
ip default-gateway 192.168.200.233
enable secret ena22pa55
hostname S2
ip domain-name cisco.com
int f0/2
switchport access vlan 20
switchport port-security maximum 1
switchport port-security violation restrict
switchport port-security mac-address sticky
exit
int f0/3
switchport access vlan 40
switchport port-security maximum 1
switchport port-security violation restrict
switchport port-security mac-address sticky
exit
int g0/1
switchport mode trunk
exit
int vlan40
ip address 192.168.200.236 255.255.255.248
exit
ip ssh version 2
username admin secret ena44pa55
vlan 20
name VLAN0020
exit
vlan 30
name VLAN0030
exit
vlan 40
name Management
exit
line vty 0
login local
transport input ssh
end
copy running-config startup-config

```

## C-ASA

```
conf t
ntp server 192.168.200.226
domain-name cisco.com
hostname C-ASA
int vlan1
ip address 172.16.3.30 255.255.255.224
no shutdown
nameif inside
exit
int vlan2
ip address 5.5.5.5 255.255.255.248
no shutdown
nameif outside
exit
int vlan3
ip address 172.16.3.33 255.255.255.240
no shutdown
no forward interface vlan1
nameif dmz
security-level 50
exit
route outside 0.0.0.0 0.0.0.0 5.5.5.6 1
end
copy running-config startup-config

```

## R1

```
en
conf t
license boot module c2900 technology-package securityk9
yes
do reload
yes

en
conf t
ntp server 192.168.200.226
ntp update-calendar
access-list 100 permit ip 192.168.200.224 0.0.0.7 193.6.44.0 0.0.0.15
access-list 100 permit ip 192.168.200.232 0.0.0.7 193.6.44.0 0.0.0.15
access-list 100 permit ip 192.168.200.192 0.0.0.31 193.6.44.0 0.0.0.15
access-list 100 permit ip 192.168.200.0 0.0.0.127 193.6.44.0 0.0.0.15
access-list 1 permit host 192.168.200.234
hostname R1
crypto isakmp policy 5
encryption aes 256
authentication pre-share
group 5
crypto isakmp key 444gut22 address 192.168.200.249
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac
crypto map VPN-MAP 5 ipsec-isakmp 
description R1-TO-R3
set peer 192.168.200.249
set transform-set VPN-SET 
match address 100
int s0/0/0
crypto map VPN-MAP
exit
int g0/2
no shutdown
int g0/2.20
encapsulation dot1Q 20
ip address 192.168.200.1 255.255.255.128
no shut
int g0/2.30
encapsulation dot1Q 30
ip address 192.168.200.225 255.255.255.248
no shut
int g0/2.40
encapsulation dot1Q 40
ip address 192.168.200.233 255.255.255.248
no shut
exit
int s0/0/0
ip ospf message-digest-key 1 md5 r0ut1ng
exit
router ospf 1
area 0 authentication message-digest
passive-interface GigabitEthernet0/2.20
passive-interface GigabitEthernet0/2.30
passive-interface GigabitEthernet0/2.40
network 192.168.200.192 0.0.0.31 area 0
network 192.168.200.0 0.0.0.127 area 0
network 192.168.200.232 0.0.0.7 area 0
network 192.168.200.224 0.0.0.7 area 0
network 192.168.200.244 0.0.0.3 area 0
exit
ip ssh version 2
line vty 0
login local
transport input ssh
access-class 1 IN
exit
username admin secret t1tkos
exit
copy running-config startup-config

```

## R2

```
en
conf t
license boot module c2900 technology-package securityk9
yes
do reload
yes

en
conf t
ntp server 192.168.200.226
ntp update-calendar
hostname R2
service timestamps log datetime msec
ip ips config location flash:ipsdir retries 1
ip ips name iosips
ip ips signature-category
category all
retired true
exit
category ios_ips basic
retired false
end
conf t
router ospf 1
area 0 authentication message-digest
passive-interface GigabitEthernet0/2
network 192.168.200.128 0.0.0.63 area 0
exit
int g0/2
ip address 192.168.200.129 255.255.255.192
no shut
int s0/0/0
ip ospf message-digest-key 1 md5 r0ut1ng
int s0/0/1
ip ospf message-digest-key 1 md5 r0ut1ng
exit
logging 192.168.200.226
exit
copy running-config startup-config

```

## R3

```
en
conf t
license boot module c2900 technology-package securityk9
yes
do reload
yes

en
conf t
ntp server 192.168.200.226
ntp update-calendar
hostname R3
access-list 100 permit ip 193.6.44.0 0.0.0.15 192.168.200.192 0.0.0.31
access-list 100 permit ip 193.6.44.0 0.0.0.15 192.168.200.0 0.0.0.127
access-list 100 permit ip 193.6.44.0 0.0.0.15 192.168.200.224 0.0.0.7
crypto isakmp policy 5
encryption aes 256
authentication pre-share
group 5
exit
crypto isakmp key 444gut22 address 192.168.200.245
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac
crypto map VPN-MAP 5 ipsec-isakmp
description VPN R3-TO-R1
set peer 192.168.200.245
set transform-set VPN-SET 
match address 100
int s0/0/0
crypto map VPN-MAP
end
conf t
router ospf 1
area 0 authentication message-digest
default-information originate
int g0/0
ip address 5.5.5.6 255.255.255.248
no shut
exit
ip route 0.0.0.0 0.0.0.0 Serial0/1/0

```
