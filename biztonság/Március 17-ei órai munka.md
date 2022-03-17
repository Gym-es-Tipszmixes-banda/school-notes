# Március 17.

## ospf_alap.pkt

### Switch2

```
en
conf t
vlan 10
name tizes
exit
vlan 20
name huszas
exit
vlan 30
name harmincas
exit
int f0/1
switchport mode access
switchport access vlan 20
exit
int f0/2
switchport mode access
switchport access vlan 30
exit
int g0/2
switchport mode trunk

```

### Switch0

```
en
conf t
vlan 10
exit
vlan 20
exit
vlan 30
exit
int f0/1
switchport mode access
switchport access vlan 10
exit
int g0/2
switchport mode trunk
exit
int g0/1
switchport mode trunk
exit

```

### Router0

Fontos rész! Hallgatók gyakran elcseszik. Tanci varázsol.

```
en
conf t
int g0/1
no ip address
exit
int g0/1.10
encapsulation dot1q 10
ip address 192.168.1.1 255.255.255.0
exit
int g0/1.20
encapsulation dot1q 20
ip address 192.168.5.1 255.255.255.0
exit
int g0/1.30
encapsulation dot1q 30
ip address 192.168.4.1 255.255.255.0
exit

```

PC0, 2 és 3 pingelhető egymásról.

```
router ospf 1
network 192.168.4.0 0.0.0.255 area 0
network 192.168.5.0 0.0.0.255 area 0
passive g0/1.10
passive g0/1.20
passive g0/1.30
exit

```

Bármelyik PC pingelhető bárhonnan.

### Switch2

A `switchport port-security` parancsot először paraméter nélkül kell kiadni, utána csesztetjük.

```
en
conf t
int range f0/3-24,g0/1
shut
exit
int range f0/1-2
switchport mode access
switchport port-security
switchport port-security maximum 1
switchport port-security mac-address sticky
switchport port-security violation shutdown

```

Ajánlott ellenőrző parancsok
- `do show vlan`
- `do show port-security`
- `do show run`

Switch2-nek megtanítottuk a PC2 MAC címét és kamu PC2-ről megfogott a port-security.

1. `int f0/1 \n shutdown`
2. visszakötés PC2-be
3. `no shutdown`

Mi van ha új gépet akarunk?

`do clear port-security all`

Kész projekt fájl megtalálható mudliban `ospf alap vlan port secFile` néven.

## 14.3.11

### S1

```
en
conf t
int range f0/1-2
switchport port-security
switchport port-security max 1
switchport port-security mac sticky
switchport port-security violation restrict
no shutdown
exit
int range f0/3-24,g0/1-2
shutdown
exit

```

Gépekről 1-1 ping kell 100%-hoz.
