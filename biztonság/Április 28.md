# Április 28

## Alap adatok

| Felosztandó hálózat | Eszközök száma | Minimális blokk méret |
| ------------------- | -------------- | --------------------- |
| PC1                 | 35             | 64                    |
| PC2                 | 84             | 128                   |

VLAN-ok:

- 50
- 100

Egyéb adatok:

```
ACL: Tfh. PC3-on több szolg. is fut
PC3 legyen pingelhető bárhonnan
HTTPS csak PC2
FTP, DNS csak PC1
```

## Felosztás

| 1. hálózat (PC2)   |                 |
| ------------------ | --------------- |
| Cím                | 192.168.50.0/25 |
| Maszk              | 255.255.255.128 |
| Helyettesítő maszk | 0.0.0.127       |
| Utolsó cím         | 192.168.50.127  |

| 2. hálózat (PC1)   |                   |
| ------------------ | ----------------- |
| Cím                | 192.168.50.128/26 |
| Maszk              | 255.255.255.192   |
| Helyettesítő maszk | 0.0.0.63          |
| Utolsó cím         | 192.168.50.191    |
