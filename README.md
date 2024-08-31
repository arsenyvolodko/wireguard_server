# wireguard_server

### Description
Fast Api server for handling wireguard clients

### API Specification
see [spec.yml](api/spec.yaml)

### Set Up
1. Install wg-quick on server
2. Create wireguard config file `/etc/wireguard/wg0.conf`\
example:
    ```
    [Interface]
    Address = 10.66.66.1/24
    PostUp = iptables -I INPUT -p udp --dport 49188 -j ACCEPT
    PostUp = iptables -I FORWARD -i ens3 -o wg0 -j ACCEPT
    PostUp = iptables -I FORWARD -i wg0 -j ACCEPT
    PostUp = iptables -t nat -A POSTROUTING -o ens3 -j MASQUERADE
    PostDown = iptables -D INPUT -p udp --dport 49188 -j ACCEPT
    PostDown = iptables -D FORWARD -i ens3 -o wg0 -j ACCEPT
    PostDown = iptables -D FORWARD -i wg0 -j ACCEPT
    PostDown = iptables -t nat -D POSTROUTING -o ens3 -j MASQUERADE
    ListenPort = 49188
    PrivateKey = {your private key}
    ```
3. Fill .env file

### Deploy
```bash
docker compose up --build -d
```