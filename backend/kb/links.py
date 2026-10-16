"""Classify hyperlinks found in the workbook. Deterministic rules only."""

import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

# Links that are the action itself (a form, a tool, a business), not documentation to extract.
TOOL_HOSTS = {
    "lafayettec.az1.qualtrics.com",
    "password.lafayette.edu",
    "printing.lafayette.edu",
    "ifixandrepair.com",
    "lafayette.edu",
}

# Public documentation we are allowed to fetch.
PUBLIC_DOC_HOSTS = {
    "help.lafayette.edu",
    "support.apple.com",
    "support.microsoft.com",
}

_INTERNAL_RE = re.compile(r"^#?'?(?P<tab>[^'!]+)'?!")
_GDOC_RE = re.compile(r"docs\.google\.com/(?P<kind>document|spreadsheets)/d/(?P<id>[A-Za-z0-9_-]+)")


@dataclass(frozen=True)
class LinkInfo:
    url: str
    link_kind: str  # internal_tab | workbook_sheet | public_doc | private_doc | tool | external
    target_tab: str | None = None  # tab name for internal_tab, or gid for workbook_sheet
    doc_id: str | None = None


def hyperlink_target(cell) -> str | None:
    """The raw link target of an openpyxl cell: an external URL, or '#Tab!A1' for internal links."""
    link = cell.hyperlink
    if link is None:
        return None
    if link.target:
        return link.target
    if link.location:
        return "#" + link.location
    return None


def classify(url: str, cheat_sheet_id: str) -> LinkInfo:
    if url.startswith("#"):
        match = _INTERNAL_RE.match(url)
        return LinkInfo(url, "internal_tab", target_tab=match.group("tab") if match else None)

    gdoc = _GDOC_RE.search(url)
    if gdoc:
        doc_id = gdoc.group("id")
        if doc_id == cheat_sheet_id:
            gid = (parse_qs(urlparse(url).query).get("gid") or [None])[0]
            return LinkInfo(url, "workbook_sheet", target_tab=gid, doc_id=doc_id)
        return LinkInfo(url, "private_doc", doc_id=doc_id)

    host = (urlparse(url).hostname or "").lower().removeprefix("www.")
    if host in TOOL_HOSTS:
        return LinkInfo(url, "tool")
    if host in PUBLIC_DOC_HOSTS:
        return LinkInfo(url, "public_doc")
    return LinkInfo(url, "external")
