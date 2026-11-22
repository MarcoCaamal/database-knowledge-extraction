"""Download and validate a real, public Sample Superstore retail CSV."""
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE = "https://raw.githubusercontent.com/mikemooreviz/superstore/master/superstore.csv"
ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/raw/Sample_Superstore.csv"

def main() -> None:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    if TARGET.is_file() and TARGET.stat().st_size > 100_000:
        print(f"Already downloaded: {TARGET}")
        return
    request = Request(SOURCE, headers={"User-Agent": "Mozilla/5.0 (educational academic project)"})
    with urlopen(request, timeout=45) as response:
        payload = response.read()
    if not payload.startswith((b"\xef\xbb\xbfRow ID,", b"Row ID,")) or len(payload) < 100_000:
        raise ValueError("Invalid dataset response")
    TARGET.write_bytes(payload)
    print(f"Downloaded {len(payload):,} bytes: {TARGET}")

if __name__ == "__main__":
    main()
