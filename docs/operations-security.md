# WireGuard Operations, Diagnostics and Security

## Read-only checks

Verify that the interface exists and inspect status locally:

```bash
sudo wg show wg0
```

To inspect latest peer handshakes:

```bash
sudo wg show wg0 latest-handshakes
```

To count configured peers without displaying their public keys:

```bash
sudo wg show wg0 peers | wc -w
```

To observe whether UDP traffic arrives during a **controlled** external test:

```bash
sudo timeout 20 tcpdump -ni any 'udp port 51820'
```

A zero-packet capture does not, by itself, identify the reason for the failure; the client may not have attempted a connection during the capture, or packets may be lost before reaching the host.

## Endpoint and DDNS

For a connection with a dynamic public address, a client may use an endpoint shaped like:

```ini
Endpoint = vpn.example.net:51820
```

`vpn.example.net` is **a placeholder**, not the production hostname.

A Dynamic DNS hostname is preferable to a stale literal public IPv4 address, but some clients may need the tunnel to be toggled to resolve a changed address again. Do not claim automatic reconnection without a platform-specific test.

## Failure isolation

1. Check the host WireGuard interface and configured peers.
2. Inspect the latest handshake timestamps, not only interface state.
3. Confirm that the client endpoint resolves to the expected current IP.
4. Check external UDP traffic during an intentional client connection attempt.
5. Verify router forwarding and firewall rules if packets do not arrive.
6. Once a handshake succeeds, test authorized private resource access.
7. Record the successful test before marking an incident resolved.

## Security requirements

- Do not commit `/etc/wireguard/*.conf`, private keys, preshared keys or QR codes.
- Avoid exposing production public IPs, actual DDNS names, personal identifiers and peer public keys in incident reports.
- Apply least-privilege routes and firewall rules appropriate to each client.
- Keep SSH and administrative interfaces restricted to trusted networks.
- Treat diagnostic output as sensitive until reviewed and sanitized.
- Avoid changing unrelated Docker or host services during VPN troubleshooting.

## Incident evidence already established (November 17, 2026)

- WireGuard `wg0` existed and four peers were configured.
- No handshakes were recorded in the diagnostic output.
- No matching UDP packets were captured during the observed 20-second interval.
- At least one client profile used an outdated literal public IP endpoint.
- The No-IP hostname matched the current public IPv4 address.

**Not yet established:** a subsequent successful handshake and end-to-end tunnel connectivity using the DNS hostname. The detailed incident analysis belongs in a separate future commit.
