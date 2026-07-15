#!/usr/bin/env python3
"""Download Northwind CSV datasets into northwind_dw_duckdb/analyses/datasets."""

from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = "https://raw.githubusercontent.com/jpwhite3/northwind-SQLite/master/csv"
FILES = [
    "Category.csv",
    "Customer.csv",
    "Employee.csv",
    "EmployeeTerritory.csv",
    "OrderDetail.csv",
    "Order.csv",
    "Product.csv",
    "Region.csv",
    "Shipper.csv",
    "Supplier.csv",
    "Territory.csv",
]


def download_file(filename: str, directory: Path) -> None:
    url = f"{BASE_URL}/{filename}"
    dest_path = directory / filename
    print(f"Downloading {filename}...")

    request = Request(url, headers={"User-Agent": "python-urllib/3"})
    try:
        with urlopen(request, timeout=30) as response, open(dest_path, "wb") as out_file:
            while chunk := response.read(8192):
                out_file.write(chunk)
    except HTTPError as exc:
        raise RuntimeError(f"HTTP error {exc.code} downloading {url}: {exc.reason}") from exc
    except URLError as exc:
        raise RuntimeError(f"URL error downloading {url}: {exc}") from exc

    print(f"Saved {dest_path}")


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    target_dir = script_dir / "datasets"
    target_dir.mkdir(parents=True, exist_ok=True)

    print(f"Target dataset directory: {target_dir}")
    for filename in FILES:
        download_file(filename, target_dir)

    print("\nAll Northwind datasets downloaded successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
