# Április 21. megoldások

## 1. verzió

192.168.1.0/24
70->128(126)
20->32(30)

1.alhálózat
192.168.1.0/25 -> 255.255.255.128
192.168.1.127-ig
2.alhálózat
192.168.1.128/27 -> 255.255.255.224
192.168.1.159-ig

```
en
conf t
hostname S1
vlan 10
exit
vlan 20
exit
int gi0/1
no shutdown
switchport mode trunk
exit
int fa0/24
switchport mode trunk 
exit

en
conf t
hostname S2
vlan 10
exit
vlan 20
exit
int gi0/1
no shutdown
switchport mode trunk
exit
int fa0/1
switchport mode access
switchport access vlan 10
exit
int fa0/2
switchport mode access
switchport access vlan 20
exit
int range fa0/1-2
switchport port-security
switchport port-security max
switchport port-security mac-address sticky
switchport port-security violation shut
exit

R1
en
conf t
int s0/0/0
ip add 10.0.0.1 255.255.255.252
no shutdown
exit
int fa0/1
no shut
exit
int fa0/1.10
encapsulation dot1q 10
ip add 192.168.1.1 255.255.255.128
exit
int fa0/1.20
encapsulation dot1q 20
ip add 192.168.1.129 255.255.255.224
exit
no router ospf 1
router ospf 1
network 10.0.0.0 0.0.0.3 area 0
network 192.168.1.0 0.0.0.127 area 0
network 192.168.1.128 0.0.0.31 area 0
passive fa0/1.10
passive fa0/1.20
area 0 auth mess
exit
int s0/0/0
ip ospf message-digest-key 1 md5 S3cr3t12
exit
ip domain-name mindegy.hu
username admin secret admin123
crypto key generate rsa modulus 1024
ip ssh version 2
line vty 0 4
transport input ssh
login local
exit
access-list 1 permit host 192.168.1.10
line vty 0 4
access-class 1 in
exit

R2

en
conf t
int s0/0/0
ip address 10.0.0.2 255.255.255.252
clock rate 128000
ip ospf message-digest-key 1 md5 S3cr3t12
no shutdown
int s0/0/1
ip address 10.0.0.6 255.255.255.252
clock rate 128000
ip ospf message-digest-key 1 md5 S3cr3t12
no shutdown
exit
router ospf 1
network 10.0.0.0 0.0.0.3 area 0
network 10.0.0.4 0.0.0.3 area 0
area 0 auth mess
exit

R3
en 
conf t
hostname R3
int s0/0/1
ip address 10.0.0.5 255.255.255.252
no shutdown
exit
int s0/0/0
ip address 80.90.10.1 2255.255.255.240
exit
router ospf 1
network 10.0.0.4 0.0.0.3 area 0
passive s0/0/0
redistribute static
default-information originate
area 0 auth mess
exit
int s0/0/1
ip ospf message-digest-key 1 md5 S3cr3t12
no shutdown
ip route 0.0.0.0 0.0.0.0 s0/0/0

ISP
conf t
hostname ISP
ip route 0.0.0.0 0.0.0.0 s0/0/0
int s0/0/0
ip address 80.90.10.2 255.255.255.240
no shut
exit
interface fa0/1
ip address 192.168.4.1 255.255.255.0
no shut
exit
```

## 2. verzió

192.168.1.0/24
70->128(126)
20->32(30)

1.alhálózat
192.168.1.0/25 -> 255.255.255.128
192.168.1.127-ig
2.alhálózat
192.168.1.128/27 -> 255.255.255.224
192.168.1.159-ig

```
en
conf t
hostname S1
vlan 10
exit
vlan 20
exit
int gi0/1
no shutdown
switchport mode trunk
exit
int fa0/24
switchport mode trunk 
exit

en
conf t
hostname S2
vlan 10
exit
vlan 20
exit
int gi0/1
no shutdown
switchport mode trunk
exit
int fa0/1
switchport mode access
switchport access vlan 10
exit
int fa0/2
switchport mode access
switchport access vlan 20
exit
int range fa0/1-2
switchport port-security
switchport port-security max
switchport port-security mac-address sticky
switchport port-security violation shut
exit

R1
en
conf t
int s0/0/0
ip add 10.0.0.1 255.255.255.252
no shutdown
exit
int fa0/1
no shut
exit
int fa0/1.10
encapsulation dot1q 10
ip add 192.168.1.1 255.255.255.128
exit
int fa0/1.20
encapsulation dot1q 20
ip add 192.168.1.129 255.255.255.224
exit
no router ospf 1
router ospf 1
network 10.0.0.0 0.0.0.3 area 0
network 192.168.1.0 0.0.0.127 area 0
network 192.168.1.128 0.0.0.31 area 0
passive fa0/1.10
passive fa0/1.20
area 0 auth mess
exit
int s0/0/0
ip ospf message-digest-key 1 md5 S3cr3t12
exit
ip domain-name mindegy.hu
username admin secret admin123
crypto key generate rsa modulus 1024
ip ssh version 2
line vty 0 4
transport input ssh
login local
exit
access-list 1 permit host 192.168.1.10
line vty 0 4
access-class 1 in
exit
logging host 192.168.1.130
logging on
service timestamps log datetime
ntp server 192.168.1.130



R2

en
conf t
int s0/0/0
ip address 10.0.0.2 255.255.255.252
clock rate 128000
ip ospf message-digest-key 1 md5 S3cr3t12
no shutdown
int s0/0/1
ip address 10.0.0.6 255.255.255.252
clock rate 128000
ip ospf message-digest-key 1 md5 S3cr3t12
no shutdown
exit
router ospf 1
network 10.0.0.0 0.0.0.3 area 0
network 10.0.0.4 0.0.0.3 area 0
area 0 auth mess
exit

R3
en 
conf t
hostname R3
int s0/0/1
ip address 10.0.0.5 255.255.255.252
no shutdown
exit
int s0/0/0
ip address 80.90.10.1 2255.255.255.240
exit
router ospf 1
network 10.0.0.4 0.0.0.3 area 0
passive s0/0/0
redistribute static
default-information originate
area 0 auth mess
exit
int s0/0/1
ip ospf message-digest-key 1 md5 S3cr3t12
no shutdown
ip route 0.0.0.0 0.0.0.0 s0/0/0

ISP
conf t
hostname ISP
ip route 0.0.0.0 0.0.0.0 s0/0/0
int s0/0/0
ip address 80.90.10.2 255.255.255.240
no shut
exit
interface fa0/1
ip address 192.168.4.1 255.255.255.0
no shut
exit
en 
conf t
acces-list 100 permit tcp 192.168.1.128 0.0.0.31 host 192.168.4.10 eq 21
acces-list 100 permit tcp 192.168.1.128 0.0.0.31 host 192.168.4.10 eq 80
acces-list 100 permit tcp 192.168.1.0 0.0.0.127 hots 192.168.4.10 eq 443
acces-list 100 permit any any
inf fa0/1
ip acces-group 100 out
exit


***********
R1 és R3
crypto isakmp policy 1
encr aes 256
authentication pre-share
group 5
lifetime 86400
hash sha
exit

crypto isakmp key kulcs address 10.0.0.5 *****R1
crypto isakmp key kulcs address 10.0.0.1 *****R2

crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac
crypto map VPN-MAP 1 ipsec-isakmp 

set peer 10.0.0.5 *******R1
set peer 10.0.0.1 *******R2

set transform-set VPN-SET 
match address 100
exit

R1
int s0/0/0
crypro map VPN-MAP
access-list 100 permit ip 192.168.1.0 0.0.0.127 192.168.4.0 0.0.0.255
access-list 100 permit ip 192.168.1.128 0.0.0.31 192.168.4.0 0.0.0.255


R3
int s0/0/1
access-list 100 permit ip 192.168.4.0 0.0.0.255 192.168.1.0 0.0.0.127
access-list 100 permit ip 192.168.4.0 0.0.0.255 192.168.1.128 0.0.0.31
```
