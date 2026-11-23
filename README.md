# WireGuard VPN Homelab

A documented Linux homelab project focused on secure remote access using WireGuard, network diagnostics and operational reliability.

This repository presents an existing self-hosted WireGuard environment and records its architecture, operational checks and troubleshooting process. It is intended as a **technical portfolio**, not a copy of the production configuration.

## Technology stack

- **Host:** Ubuntu 26.04.1 LTS
- **VPN:** WireGuard (`wg0`), UDP port `51820`
- **Configured clients:** four peers (observed during the November 17, 2026 investigation)
- **Dynamic DNS:** No-IP, for an internet connection with a changing public IPv4 address
- **Administration:** Linux CLI, networking diagnostics and systemd service management

Private addressing, the real DDNS hostname, public IP history, client identities, cryptographic keys and secrets are intentionally omitted.

## Documentation

- [Network architecture and design](docs/architecture.md)
- [Operations, diagnostics and security](docs/operations-security.md)

## Project roadmap

1. **Foundation:** existing network design and security principles (this commit).
2. **Operations:** monitoring, connectivity checks and peer management (documented without credentials).
3. **Incident study:** November 17, 2026 connection failure after a public IP change, with its root cause and recommended DDNS endpoint adjustment.
4. **Recovery validation:** record a successful client handshake and tunnel connectivity only after they have actually been tested.

## Evidence and limitations

The November 17 investigation confirmed a configured WireGuard interface and four peers, but **no successful handshakes during that diagnostic window**. The dynamic DNS hostname was verified against the current public IPv4 address. Client recovery through the hostname has not yet been marked as validated.

## Security and privacy

No live WireGuard configuration, private keys, preshared keys, QR codes, client IP allocations or personal hostnames are stored in this public repository. Commands and diagrams are illustrative and must be adapted to the actual deployment.

## Peer Operations

- [WireGuard peer configuration and connectivity checks](docs/peer-connectivity.md)
- [Incident: WireGuard stale endpoint after public IP change](docs/incidents/2026-11-17-stale-wireguard-endpoint.md)

## Peer Health Monitoring

Run `sudo python3 scripts/peer-health.py` to inspect handshake age without printing peer identities. A recent handshake does not, by itself, prove full tunnel connectivity.

- [Privacy-safe WireGuard handshake monitor](scripts/peer-health.py)
