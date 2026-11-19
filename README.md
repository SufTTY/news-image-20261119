# Entry: The World Ledger — front page of 19 Nov 2026

The final make.fun competition entry: a broadsheet front page titled **'THE WORLD LEDGER'** for
**Thursday, 19 November 2026**.

## The page

- Photorealistic hero photograph of the first trilateral summit between Trump, Xi and Putin in
  Shenzhen, generated via pollinations.ai through `compose19.py`.
- Red ticker strip across the page.
- Three secondary story columns below the lead.

## Requirements

- `entry.png` must be a 1024x1024 PNG under 1 MiB.
- `main.py` copies `entry.png` to the output directory (honouring `MAKEFUN_OUTPUT_DIR`) and raises
  `SystemExit` if the copy exceeds 1 MiB.
- The pipeline uses the network only for the hero photo fetch; the fallback drawing is used if it
  fails.
- `main.py` is deterministic and makes no network calls.
