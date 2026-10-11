"""Turn users into JSON and CSV with the standard library only.

Run with: python examples/export_json_csv.py
"""

from __future__ import annotations

import csv
import json
import sys

from testseed import TestSeed


def main() -> None:
    rows = [u.to_dict() for u in TestSeed(locale="es_CR", seed=7).users(count=3)]

    print(json.dumps(rows[0], ensure_ascii=False, indent=2))

    writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)


if __name__ == "__main__":
    main()
