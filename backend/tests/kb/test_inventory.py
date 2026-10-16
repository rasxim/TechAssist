from pathlib import Path

import pytest

from kb.inventory import build_inventory, is_inline_answer, make_slug
from kb.links import classify

REAL_WORKBOOK = Path(__file__).resolve().parents[3] / "Tech Lounge Cheat Sheet.xlsx"


def by_question(inv, text):
    return next(i for i in inv.issues if i.question.startswith(text))


def test_every_row_except_header_becomes_an_issue(workbook, gid_map):
    inv = build_inventory(workbook, gid_map)
    assert len(inv.issues) == 8
    assert by_question(inv, "Create a Tech Lounge Ticket").issue_kind == "resource"
    assert by_question(inv, "How do I connect").issue_kind is None


def test_inline_answer_is_copied_verbatim(workbook, gid_map):
    inv = build_inventory(workbook, gid_map)
    proc = next(p for p in inv.procedures if p.kind == "steps")
    assert proc.content == "1. Upload your job\n2. Click Web Print\n3. Release it"
    assert inv.sources[proc.source_key].snapshot_text == proc.content


def test_links_are_classified(workbook, gid_map):
    inv = build_inventory(workbook, gid_map)
    kinds = {(l.cell_ref, l.link_kind, l.followed) for l in inv.links}
    assert ("Common Questions!B1", "tool", False) in kinds
    assert ("Common Questions!B3", "public_doc", True) in kinds
    assert ("Common Questions!B5", "private_doc", True) in kinds
    assert ("Common Questions!B6", "internal_tab", True) in kinds
    assert ("Common Questions!B8", "workbook_sheet", False) in kinds  # unconfirmed gid


def test_only_linked_and_confirmed_tabs_are_followed(workbook, gid_map):
    inv = build_inventory(workbook, gid_map)
    assert inv.followed_tabs == ["Software", "BIOS"]
    flags = by_question(inv, "Where can I check warranty").review_flags
    assert any("unconfirmed" in f for f in flags)


def test_links_inside_tabs_are_recorded_but_not_followed(workbook, gid_map):
    inv = build_inventory(workbook, gid_map)
    tab_links = [l for l in inv.links if l.owner_key == "tab:Software"]
    assert {l.url for l in tab_links} >= {"https://help.lafayette.edu/matlab/"}
    assert not any(l.followed for l in tab_links)
    assert not any(s.url == "https://help.lafayette.edu/matlab/" for s in inv.sources.values())


def test_tab_parsing_handles_merges_dashes_notes_and_duplicates(workbook, gid_map):
    inv = build_inventory(workbook, gid_map)
    bios = {r.row_key: r.fields for r in inv.reference_rows if r.procedure_key == "tab:BIOS"}
    assert bios["apple|hold power"]["Boot Key"] == "Hold Power"  # merged B5:C5 fills both columns
    assert "television|roku" in bios and "television|lg" in bios  # duplicate first column -> two-part keys
    software = {r.row_key: r.fields for r in inv.reference_rows if r.procedure_key == "tab:Software"}
    assert software["matlab"]["Apps"] is None  # "--" is empty
    proc = next(p for p in inv.procedures if p.procedure_key == "tab:BIOS")
    assert proc.warnings == ["NOTE: Do not change settings without approval"]
    assert "Acrobat \\| Photoshop" in next(p for p in inv.procedures if p.procedure_key == "tab:Software").content


def test_private_docs_and_extra_question_text_are_flagged(workbook, gid_map):
    inv = build_inventory(workbook, gid_map)
    assert any("private Google Doc" in f for f in by_question(inv, "How do I reset Duo").review_flags)
    erase = by_question(inv, "How do I erase")
    assert erase.inline_notes == "Extra line"
    assert any("no answer" in f for f in erase.review_flags)


def test_slug_is_stable_and_changes_when_question_changes():
    assert make_slug("How do I X?") == make_slug("How do I X?")
    assert make_slug("How do I X?") != make_slug("How do I Y?")


@pytest.mark.parametrize("text,link,expected", [
    ("Some help page title", "x", False),
    ("https://example.com/page", None, False),
    ("Collect the device model and create a ticket", None, True),
    ("https://password.lafayette.edu/guest.html\n\nGuests use the account for 72 hours", "x", True),
])
def test_inline_answer_detection(text, link, expected):
    info = classify("https://example.com", "S") if link else None
    assert is_inline_answer(text, info) is expected


@pytest.mark.skipif(not REAL_WORKBOOK.exists(), reason="internal workbook not present")
def test_real_workbook_inventory():
    from kb.config import GID_MAP_PATH

    inv = build_inventory(REAL_WORKBOOK, GID_MAP_PATH)
    assert len(inv.issues) == 48
    assert sum(p.kind == "steps" for p in inv.procedures) == 9
    assert not inv.warnings
