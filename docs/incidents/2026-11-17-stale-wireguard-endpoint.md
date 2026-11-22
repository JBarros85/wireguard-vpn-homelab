# WireGuard VPN Incident: Stale Endpoint After Public IP Change

**Incident date:** November 17, 2026
**Category:** VPN / DNS / Remote connectivity
**Status:** Root cause identified; successful post-change handshake not yet evidenced

## Summary

A remote WireGuard client could not reach a self-hosted VPN after the residential public IPv4 address changed. The Linux WireGuard interface remained configured, but the observed peers had no recorded handshakes. Investigation found that a client used the former public IPv4 address as its Endpoint while the dynamic DNS hostname already resolved to the current address.

The corrective action is to configure the client Endpoint using the existing dynamic DNS hostname. The available evidence does not establish that the change was applied and verified with a new handshake.

## Environment

- Ubuntu 26.04.1 LTS running a WireGuard server interface.
- Four configured peers, each with its own tunnel address.
- Residential internet connection with a changing public IPv4 address.
- No-IP dynamic DNS and a mobile-data client used for diagnosis.
- Public IPs, the actual DDNS hostname, live tunnel addresses and key material are intentionally omitted.

## Symptoms and evidence

| Check | Observation | What it establishes |
| --- | --- | --- |
| WireGuard peer inspection | Four peers configured | Server-side peer definitions existed |
| Latest handshakes | No recorded handshake for any peer | No successful handshake recorded in the observed interface state |
| 20-second UDP capture | Zero packets captured on the VPN port | No matching UDP packets were seen during that capture window |
| Client Endpoint | Literal former public IPv4 address | The client targeted an obsolete destination |
| Current public IPv4 | Different from configured client Endpoint | An address mismatch existed |
| No-IP A record | Matched current public IPv4 | Dynamic DNS was up to date at inspection time |

Neither the lack of handshakes nor a zero-packet capture alone proves a DNS issue. Possible alternatives include no client attempts during observation, router forwarding problems or upstream filtering. The client Endpoint mismatch, combined with correct DDNS resolution, was the decisive evidence for the affected client.

## Diagnostic sequence

1. Inspect WireGuard interface and peers using `sudo wg show wg0`.
2. Review timestamps using `sudo wg show wg0 latest-handshakes`.
3. Observe incoming UDP traffic on the configured VPN port during a real external connection attempt.
4. Compare the Endpoint in the client configuration with the current public IPv4 address.
5. Resolve the configured DDNS hostname and compare it with the public address.
6. After changing the client Endpoint, initiate a new connection from mobile data and verify a fresh handshake plus traffic through the tunnel.

Useful read-only commands, with actual output kept private:

```bash
sudo wg show wg0 latest-handshakes
sudo wg show wg0
curl -4 -s https://api.ipify.org
getent ahostsv4 vpn.example.invalid
```

The hostname in this example is intentionally fictitious. UDP capture commands must use the actual authorized port, and captures should only be performed on systems you administer.

## Root cause and proposed remediation

**Confirmed for the inspected client:** its Endpoint referred to an old public IPv4 address. This configuration could not automatically follow an ISP address change.

**Recommended client change:** replace the literal IP with the existing DDNS hostname, keeping the configured WireGuard UDP port. A sanitized example is:

```ini
[Peer]
Endpoint = vpn.example.invalid:<VPN_PORT>
```

This does not require new WireGuard keys, new peers, a different VPN subnet or changes to Jellyfin. The No-IP record already matched the current public IPv4 address, so No-IP reinstallation was not indicated.

## Reconnection limitation

A hostname-based Endpoint avoids hard-coding the home public address, but a running WireGuard client may continue using a previously resolved address after an IP change. Toggling the client tunnel can trigger a fresh resolution. Automatic re-resolution may require a platform-specific mechanism; it is not demonstrated in this incident.

## Outcome and validation still required

- Root cause for the inspected client: **identified**.
- No-IP resolution at investigation time: **confirmed correct**.
- Hostname-based Endpoint: **recommended**.
- Post-change successful handshake and tunnel traffic: **not evidenced by the supplied incident record**.
- No evidence of credential compromise was identified, but this was not a security audit.

The incident must not be marked fully recovered without a fresh handshake and an external client connectivity test.

## Prevention

- Use dynamic DNS names instead of literal dynamic public IPs in client Endpoint settings.
- Monitor DDNS updater status and compare DNS resolution with the current public address.
- Keep a sanitized checklist covering handshake age, UDP arrival, routing and client Endpoint configuration.
- Test reconnect behavior after future address changes before claiming automatic recovery.
- Never commit private keys, preshared keys, live client files, public IPs or actual DDNS hostnames.

**Scope:** Documentation only. No WireGuard, router, Docker or No-IP settings were changed for this Git commit.
