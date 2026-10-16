"""Knowledge base pipeline.

Run from backend/:
    python -m kb migrate                  apply supabase/migrations/*.sql
    python -m kb inventory --dry-run      parse the workbook, write kb_data/inventory.json, no database
    python -m kb inventory                parse the workbook and upsert it into the database
    python -m kb validate                 check the import against the workbook
"""

import argparse
import sys
from collections import Counter

from . import config, db
from .inventory import build_inventory
from .validate import run_checks


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m kb")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("migrate")
    inv_cmd = sub.add_parser("inventory")
    inv_cmd.add_argument("--workbook")
    inv_cmd.add_argument("--dry-run", action="store_true")
    val_cmd = sub.add_parser("validate")
    val_cmd.add_argument("--workbook")
    args = parser.parse_args(argv)

    if args.command == "migrate":
        with db.connect(config.database_url()) as conn:
            applied = db.migrate(conn)
        print("Applied: " + ", ".join(applied) if applied else "Already up to date.")
        return 0

    if args.command == "inventory":
        inv = build_inventory(config.workbook_path(args.workbook), config.GID_MAP_PATH)
        _print_summary(inv)
        if args.dry_run:
            config.KB_DATA_DIR.mkdir(exist_ok=True)
            out = config.KB_DATA_DIR / "inventory.json"
            out.write_text(db.inventory_to_json(inv), encoding="utf-8")
            print(f"\nDry run: wrote {out}")
            return 0
        with db.connect(config.database_url()) as conn:
            run_id = db.apply_inventory(conn, inv)
        print(f"\nImported (run {run_id}). Next: python -m kb validate")
        return 0

    if args.command == "validate":
        with db.connect(config.database_url()) as conn:
            checks = run_checks(conn, config.workbook_path(args.workbook))
        for c in checks:
            print(f"{'PASS' if c.ok else 'FAIL'}  {c.name}  ({c.detail})")
        failed = sum(not c.ok for c in checks)
        print(f"\n{len(checks) - failed} passed, {failed} failed")
        return 1 if failed else 0

    return 2


def _print_summary(inv) -> None:
    print(f"Workbook: {inv.workbook_name}")
    for name, count in inv.counts().items():
        print(f"  {name:18} {count}")
    print("  followed tabs:     " + ", ".join(inv.followed_tabs))
    kinds = Counter(l.link_kind for l in inv.links)
    print("  links by kind:     " + ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())))
    flagged = [i for i in inv.issues if i.review_flags]
    print(f"  issues flagged for review: {len(flagged)}")
    for w in inv.warnings:
        print(f"  WARNING: {w}")


if __name__ == "__main__":
    sys.exit(main())
