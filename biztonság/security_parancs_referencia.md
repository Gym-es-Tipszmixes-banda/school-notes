# Security parancs

[Eredeti fájl megtekintése](https://oktatas.mik.uni-pannon.hu/pluginfile.php/31638/mod_resource/content/1/security_parancs_referencia.txt)

ha elgépeltél egy parancsot a # módban, és a translating... üzenetet kapod, alkalmazd ezt:

`ctrl`+`shift`+`6`


ha nem akarod, hogy a félregépelés miatt idõt pazarolj, config módban írd be ezt:

`no ip domain lookup`


mivel szükséged lesz biztonságtechnikai funkciókra, így tudod erre felkészíteni a router-t config módból

```
license boot module c2900 technology-package securityk9
copy run start
reload
```


globális jelszó titkosítás

`service password-encryption`


jelszó minimális hosszának elõírása

`security passwords min-length 10`


virtuális terminál kapcsolat lejáratának beállítása (megszakad 5 perc után)

```
line vty 0 4
exec-timeout 5
```

vagy (megszakad 5 perc 30 másodperc után)

```
line vty 0 4
exec-timeout 5 30
```

ssh kiszolgáló konfigurálása routeren és switchen:
- legyen érvényes host név
- legyen érvényes domain név
- gyártsuk le a titkosító kulcsot
- hozzunk létre felhasználót
- finomhangoljuk az ssh kiszolgálót
- állítsuk be az ssh kapcsolatot a virtuális terminál vonalalkon

pl:

```
hostname R1
ip domain-name cisco.com
crypto key generate rsa (modulus 1024 - csak a fizikai eszközön adható ki, a packet tracer-ben csak rsa-ig, utána bekéri)
username cisco secret cisco12345 (felhasználó létrehozása)
username cisco privilege 15 secret cisco12345 (felhasználó létrehozása legmagasabb szintû hozzáféréssel)
ip ssh version 2  (ssh verziója legyen 2-es)
ip ssh timeout 60 (kapcsolat bontása aktív kapcsolat esetén 60mp elteltével)
ip ssh authentication-retries 2 (max. 2db próbálkozás lehetséges a hiteleséskor)
```

```
line vty 0 4  (kapcsolónál 0 15)
login local
transport input ssh
```
(privilege level 15 - csak a felhasználó is 15-ös szintû volt)


ssh kapcsolat tesztje a kliens oldalon, paranssorból

`ssh -l cisco 192.168.1.1`


konzol hozzáférés beállítása

```
line con 0
password cisco
login
```

vagy (ha felhasználónév és jelszó is kell)

```
username cisco secret cisco12345
line con 0
login local
```

felhasználó korlátozása  adott idõre (120), amennyiben adott idõn (60) belül (2) db sikertelen próbálkozása volt

`login block-for 120 attempts 2 within 60 `


kapcsolódás Syslog kiszolgálóhoz

```
service timestamps log datetime msec (a log üzenetek másodperces felbontású idõbélyeggel lesznek ellátva)
logging host 192.168.1.1  (az IP a syslog kiszolgáló címe)
```

kapcsolódás NTP kiszolgálóhoz

`ntp server 192.168.1.1  (az IP az NTP kiszolgáló címe)`

ethernet interfész konfigurálása router-en

```
int gi0/0
ip address 192.168.1.1 255.255.255.0
no shut
```

serial interfész konfigurálása router-en (órajeladó oldal)

```
int s0/0/0
ip add 192.168.1.1. 255.255.255.0
clock rate 128000
no shut
```

serial interfész konfigurálása router-en

```
int s0/0/0
ip add 192.168.1.2 255.255.255.0
no shut
```

interfészek állapotának lekérdezése router-en és switch-en

`show ip int brief`

OSPF irányító protokol konfigurálása

- engedélyezzük az irányító protokolt (Adjuk meg a folyamat azonosítót (process id) is
- vegyük fel a közvetlenül csatlakozó hálózatokat (a topológia ábrájáról, a feladathoz mellékelt táblázatból könnyedén leolvasható)
- csak azokat a közvetlenül csatlakozó hálózatokat vegyük fel, amelyek a belsõ irányított hálózathoz tartoznak, a publikus hálózatokat ne vegyük fel!
- a hálózat határán lévõ router-en állítsuk be az alapértelmezett útvonal terjesztését
- állítsuk be a passzív interfészeket (amelyeken nem kell frissítést küldeni az irányító protokol megfelelõ mûködéséhez
- a megfelelõ területazonosítót (area number alkalmazzuk)
- ha egy területbõl áll a hálózat, a terület azonosító rendszerint 0

pl:

```
router ospf 1
network 192.168.1.0 0.0.0.255 area 0   (a hálózat megadásakor helyettesísõ maszkot használunk, mely az alhálózati maszk 1-es komplementere, tudni kell átszámolni)
network 192.168.2.0 0.0.0.255 area 0
network 10.0.0.0 0.0.0.3 0.0.0.3 area 0
passive-interface gi0/0
default-information originate  (az alapértelmezett útvonal terjesztése a szomszéd router-ek felé)
```

alapértelmezett útvonal használata (csak a határponti routeren, esetleg a külsõ hálózati routeren állítjuk be)

`ip route 0.0.0.0 0.0.0.0 s0/0/0`		(ahol s0/0/0 az az interfész, amelyen a külsõ hálózat irányába elhagyják a csomagok a határponti router-t)

OSPF irányító protokol MD5 hitelesítéssel, beállítás (csak a különbségek kerülnek leírásra!)
- ospf konfigurációjában beállítjuk
- egymás felé nézõ interfészeken beállítjuk

```
router ospf 1
area 0 authentication message-digest
```

```
int s0/0/0
ip ospf message-digest-key 1 md5 cisco12345	(md5 hitelesítés, a jelszó cisco12345)
```

AAA beállítása helyi felhasználó esetén

```
username cisco secret cisco12345
aaa new-model
aaa authentication login default local
```

vagy

```
username cisco sercret cisco12345
aaa new-model
aaa authentication login default local-case
```

ACL-ek használata (normál és kiterjesztett ACL - számozott)

- normál ACL, sorszáma 1-99 közötti, csak a forráscímekre szûr, helyettesítõ maszkot használ, portokra nem szûr
- a lista végén az alább tiltás mindig szerepel, ha nem is írjuk ki, pl: ha a lista sorszáma 1, akkor: access-list 1 deny any
- mindig a megfelelõ interfészhez társítjuk kimenõ (out), vagy bejövõ (in) irányba
- spec kulcsszavak: host (ha konkrét IP-t használunk), any (ha bármely címet helyettesíteni akarjuk), egyik esetben sem kell helyettesítõ maszkot írni
- a sorrend számít a lista elkészítésekor!

pl:

```
access-list 1 permit 192.168.1.0 0.0.0.255		(a 192.168.1.0-ás hálózatból származó forgalom engedélyezése gi0/0 interfészen, bejövõ irányba)
int gi0/0
ip access-group 1 in
```

vagy

```
access-list 1 deny 192.168.1.0 0.0.0.255		(a 192.168.1.0-ás hálózatból származó forgalom kivételével bármely forgalom engedélyezése gi0/0 interfészen, bejövõ irányba)
access-list 1 permit any		
int gi0/0
ip access-group 1 in
```

vagy

```
access-list 1 permit host 192.168.1.10	0.0.0.255	(a 192.168.1.10-es címrõl származó forgalom engedélyezése gi0/0 interfészen, kimenõ irányba)
int gi0/0
ip access-group 1 out
```

- kiterjesztett ACL, sorszáma 100-199 közötti, a forráscímekre, a célcímekre és a portokra is szûr, helyettesítõ maszkot használ
- a lista végén az alább tiltás mindig szerepel, ha nem is írjuk ki, pl: ha a lista sorszáma 100, akkor: access-list 100 deny any any
- mindig a megfelelõ interfészhez társítjuk kimenõ (out), vagy bejövõ (in) irányba
- spec kulcsszavak: host (ha konkrét IP-t használunk), any (ha bármely címet helyettesíteni akarjuk), egyik esetben sem kell helyettesítõ maszkot írni
- a permitó/deny szócska után az alábbi kulcsszavak szerepelhetnek (tcp, udp, icmp, ip - az utolsó kettõnél nem konfigurálunk portot
- a sorrend számít a lista elkészítésekor!

pl:

```
access-list 100 permit tcp 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255 eq 80   (a 192.168.1.0-ból 192.168.2.0-ba forg. engedélyezése a 80-as porton gi0/0 interfészen, bejövõ irányba)
int gi0/0
ip access-group 1 in
```

Management access ACL beállítása router-en (ha azt szeretnénk, hogy csak bizonyos címekrõl lehessen rácsatlakozni - a beállítás nem teljes, csak a szükséges módosításokat adtam meg)

```
access-list 1 permit 192.168.1.0 0.0.0.255
line vty 0 4
access-class 1 in
```

IPS beállítása routeren

```
do mkdir ipsdir
(ip ips config location flash:ipsdir retries 1)		(hol van az IPS szignatúra adatbázis)
ip ips name iosips
ip ips signature-category				(minden kategória kiválasztása)
category all
retired true						(kategória tiltása)
category ios_ips basic					(basic kategória kiválasztása)
retired false						(kategória engedélyezése)
ip ips notify log					(syslog engedélyezése)
```

majd hozzárendelése az interfészhez:

```
int gi0/0
ip ips iosips out
```

ping definiálása, kifelé mehet, befelé nem

```
ip ips signature-definition
signature 2004 0
status
retired false
enabled true
engine
event-action produce-alert
event-action deny-packet-inline
event-action reset-tcp-connection
```

port biztonság beállítása kapcsoló interfészen

- tegyük a portot hozzáférés módba
- engedélyezzük a port biztonságot
- adjuk meg, hány MAC címet tanulhat meg
- adjuk meg, mi történjen a port biztonság megsérül (shutdown - a port tiltásra kerül, restrict/protect - csak a forgalom tiltott, a port nem, restrict - syslog üzenet is keletkezik)

pl:

```
int gi0/0
switchport mode access
switchport port-security
switchport port-security maximum 1		(csak 1 MAC címet tanul meg)
switchport port-security mac-address sticky	(dinamikusan tanulja meg a MAC címeket)
switchport port-security violation shutdown	(ha a portbiztonság sérül, tiltja az interfészt, de nem adminisztratív módon)
```

kapcsoló portok tiltása (csak egy)

```
int gi0/0
shut
```

kapcsoló portok tiltása (egyszerre több is, itt fa0/1-tõl fa0/10-ig)

```
int range fa0/1-10
shut
```

Site-To-Site VPN beállítása

- a forgalomirányításnak mûködnie a hálózaton
- a VPN-tunnel két végpontját adó router-ek mögötti hálózatok lesznek a forgalom forrásai illetve a céljai is egyben (a két oldalon a szerepek megcserélõdnek)
- az forrás és célhálózatokat ebben az esetben ACL definiálja
- a VPN csak akkor fog mûködni megfelelõen, ha a megfelelõ router-eken az IPSEC framework ugyanúgy van paraméterezve

Pl: (mindkét oldalon)

```
crypto isakmp policy 1						ISAKMP policy azonosítója
encr aes 256
authentication pre-share					(hitelesítés elõre megosztott kulccsal)
group 5								(diffie-helmann paraméter)
crypto isakmp key kulcs address x.x.x.x				(peer IP címe, VPN partner felénk esõ interfésze IP címe)
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac
crypto map VPN-MAP 1 ipsec-isakmp 
description leiras
set peer x.x.x.x						(peer IP címe, VPN partner felénk esõ interfésze IP címe)					
set transform-set VPN-SET 
match address 100						(hozzáférési list azonosítójának megadása)
```

VPN engedélyezése interfészen:

```
int gi0/0
crypto map VPN-MAP
```

ACL definiálása VPN-hez

```
access-list 100 permit ip 192.168.1.0 0.0.0.255	192.168.3.0 0.0.0.255
```

ASA alapszintû beállítása

- hacsak a feladat nem írja, jelszó nincs, csak jelszó prompt ha enable paranccsal belépünk a privilegizált módba


domain név beállítása ASA-n

`domain-name cisco.com`


enable jelszó beállítása ASA-n

`enable password cisco`

óra beállítása ASA-n

`clock set 12:23:34 jan 1 2017`

ASA külsõ, belsõ, DMZ, stb. hálózati interfész beállítása
- nem a fizikai interfészeket címezzük, hanem a VLAN-okat

VLAN interfész beállítása ASA-n (belsõ)

```
int vlan 1
nameif inside
ip add 192.168.1.1 255.255.255.0
security-level 100
no shut
```

VLAN interfész beállítása ASA-n (külsõ)

```
int vlan 2
nameif outside
ip add 88.22.10.10 255.255.255.0
security-level 0
no shut
```

fizikai interfész hozzárendelése inside vagy outside interfészhez

```
int e0/1
switchport access vlan 1
no shut
int e0/0
switchport access vlan 2
no shut
```

DMZ (újabb hálózat) beállítása ASA-n

```
int vlan 3
nameif dmz
ip add 192.168.2.0 255.255.255.0
security-level 50
no shut
```

fizikai interfész hozzárendelése dmz interfészhez

```
int e0/2
switchport access vlan 3
no shut
```

Inter-VLAN Routing beállítása router-en
- a fizikai interfészt csak bekapcsoljuk, nem adunk neki IP címet
- az alinterfészeket úgy hozzuk létre, hogy nevük utaljon az egyes VLAN-okra
- az alinterfészeket csak akkor kaphatnak IP címet, ha beállítottuk rajtuk a trunk beágyazást
- az alinterfészt nem kell külön no shutdown-al indítani, létrehozásakor már mûködik

Pl:

a router-en a köv. kell beállítani

```
int gi0/0
no shut
int gi0/0.10				(a 10-es VLAN-hoz tartozó alinterfész)
encapsulation dot1q 10
ip add 192.168.1.1 255.255.255.128
int gi0/0.20				(a 20-es VLAN-hoz tartozó alinterfész)
encapsulation dot1q 20
ip add 192.168.1.129 255.255.255.192
int gi0/0.30				(a 30-es VLAN-hoz tartozó alinterfész)
encapsulation dot1q 30
ip add 192.168.1.193 255.255.255.224
```

VLAN interfész definiálása kapcsolón

```
int vlan 30
ip add 192.168.1.194 255.255.255.224
no shut
```

VLAN interfész átjárójának megadása kapcsolón (amennyiben szeretnénk, hogy távolról is menedzselhetõ legyen a kapcsoló)

`ip default-gateway 192.168.1.193`

```
kapcsoló interfész beállítása trunk módba
int fa0/1
(switchport trunk encapsulation dot1q - csak ha máshogy nem megy, pl. laborban 2960-as és 3560-as kapcsolók közötti használat esetén)
switchport mode trunk
```

kapcsolón VLAN definiálása

```
vlan 10
name titkarsag
```

kapcsoló interfész hozzárendelése VLAN-hoz

```
int fa0/1
switchport mode access
switchport access vlan 10
```
