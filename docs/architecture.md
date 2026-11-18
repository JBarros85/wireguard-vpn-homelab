# WireGuard Network Architecture

## Purpose

Provide encrypted remote access to selected homelab resources while minimizing unnecessary public exposure. The design uses a WireGuard server on Ubuntu and Dynamic DNS to handle changes in the residential public IP address.

## Environment observed

| Component | Observed configuration |
| --- | --- |
| Operating system | Ubuntu 26.04.1 LTS |
| VPN interface | `wg0` |
| WireGuard listen port | UDP `51820` |
| Peer configurations | 4 |
| Private VPN network | Present; actual subnet omitted |
| Public hostname | No-IP dynamic DNS; hostname omitted |
| Client test network | Mobile data (4G/5G), during incident investigation |

Configured peers are not proof of an active tunnel. Handshake timestamps must be checked separately.

## Intended request path

```text
Remote device (mobile network)
          |
          v
Dynamic DNS hostname
          |
          v
Current public IPv4 address
          |
          v
Residential router
          |  UDP 51820 (forwarding must be verified)
          v
Ubuntu host: WireGuard wg0
          |
          v
Authorized private network resources
```

The diagram describes the intended connection path; it does not claim that port forwarding, firewall rules or end-to-end connectivity were independently proven during the audit.

## Components and responsibilities

**WireGuard:** maintains encrypted tunnels using peer identities and permitted IP routes. Peer entries alone do not establish connectivity.

**Router and firewall:** need to allow the expected UDP traffic and the intended internal routes. The precise rules remain outside the public repository.

**No-IP DDNS:** maps a hostname to the changing public IPv4 address. On November 17, 2026, the hostname resolved to the then-current public IP, so the observed mismatch was in a client endpoint configured with an old literal IP.

**Remote clients:** must use a reachable endpoint, matching keys and allowed-address routes. A DDNS hostname avoids storing a specific changing public IP in the client profile; automatic re-resolution during an existing session is not guaranteed.

## Technical design choices

- Use an encrypted VPN instead of exposing every internal application to the internet.
- Separate VPN client authorization from general service availability.
- Prefer a stable DDNS name to a literal residential public address.
- Keep client private keys and preshared keys off public version control.
- Verify the network path layer by layer before changing services.

## Constraints and validation

This public overview is based on the documented environment and the November 17 investigation. It is **not** a complete reproduction of the server or router configuration. A later incident report will distinguish observed evidence, proposed changes and a final verified handshake.
