# WireGuard Peer Configuration and Connectivity Checks

**Environment:** Ubuntu 26.04.1 LTS, WireGuard interface `wg0`, UDP port `51820`.
**Baseline evidence:** November 17, 2026. This document does not claim a new live connectivity test.

## Architecture

A remote client reaches the residential router through a dynamic DNS hostname. The router forwards the configured WireGuard UDP port to the Linux VPN server. The VPN uses a private address range, omitted from this public document.

## Peer management

Four peers were configured during the November 17 inspection. Each peer has its own public key and an assigned tunnel address. Store client private keys and optional preshared keys only on authorized systems; never commit production configuration or QR codes.

A client configuration typically defines a peer `PublicKey`, `AllowedIPs`, an `Endpoint` and, where appropriate, `PersistentKeepalive`. The endpoint should use the configured DDNS hostname rather than an old literal public IPv4 address.

Example with placeholders only:

```ini
[Peer]
PublicKey = <SERVER_PUBLIC_KEY>
Endpoint = vpn.example.invalid:51820
AllowedIPs = <AUTHORIZED_ROUTES>
```

## Read-only diagnostics

```bash
sudo wg show wg0
sudo wg show wg0 latest-handshakes
sudo wg show wg0 transfer
sudo ss -lun | grep 51820
```

The `wg` output may reveal peer public keys, endpoints and network addresses: sanitize it before sharing. A timestamp of zero means no handshake has been recorded for that peer since interface initialization. A nonzero timestamp is not proof of current connectivity; compare its age and test actual traffic.

When investigating remote access, test from a different network (for example, mobile data). Check the client endpoint, current public IP, DDNS resolution, router forwarding and UDP arrival before changing the server configuration.

## Dynamic DNS behavior

DDNS keeps a hostname pointing to a changing public IP, but WireGuard clients may not immediately re-resolve a hostname after an IP change. Toggling the client tunnel can force a fresh resolution; automatic re-resolution requires platform-specific consideration.

## Evidence and limits

On November 17, four peers were configured and none had a recorded handshake in the observed state. A client was found using a stale public-IP endpoint, while DDNS resolved to the current IP. This supports the diagnosis, but a successful post-change handshake and traffic test were not recorded in that evidence.

This document describes client configuration and diagnostics. A separate incident report will cover the November 17 outage and its remediation status.

## Security

Do not publish private keys, preshared keys, live tunnel configurations, public addresses, personal DDNS hostnames or unredacted diagnostics. No VPN configuration or production service was modified for this documentation commit.
