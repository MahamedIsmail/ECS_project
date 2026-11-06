import ipaddress
import re
import socket
from urllib.parse import urlsplit

# A valid public domain: labels of letters, numbers and hyphens, separated by dots,
# ending in a letters-only top-level domain (.com, .se...). Max 253 characters.
DOMAIN_PATTERN = re.compile(
    r"^(?=.{1,253}$)(?!-)([a-z0-9-]{1,63}(?<!-)\.)+[a-z]{2,63}$"
)


class InvalidDomain(ValueError):
    """Raised when user input isn't a safe, checkable domain."""


def clean_domain(raw: str) -> str:
    """Turn user input like ' https://Skool.com/coderco ' into 'skool.com'."""
    text = raw.strip().lower()
    if "://" not in text:
        text = "//" + text                  # lets urlsplit treat it as a host
    host = (urlsplit(text).hostname or "").rstrip(".")

    if not DOMAIN_PATTERN.match(host):
        raise InvalidDomain("not a valid domain name")
    return host


def resolve_public_ip(domain: str) -> str:
    """Look up the domain's IPs and refuse it if ANY of them is non-public."""
    try:
        results = socket.getaddrinfo(domain, 443, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        raise InvalidDomain("domain does not exist")

    ips = sorted({result[4][0] for result in results})
    for ip in ips:
        if not ipaddress.ip_address(ip).is_global:
            raise InvalidDomain("domain points to a private or internal address")
    return ips[0]