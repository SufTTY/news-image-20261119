[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/SufTTY/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/SufTTY/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Built for the make.fun bounty https://make.fun/bounty/news-image-20261119.

# The World Ledger — Thursday, 19 November 2026

The World Ledger of Thursday 19 November 2026 — giant date block, Shenzhen Trump-Xi-Putin summit
hero band with caption, lead headline, world map with six numbered pins, and six illustrated story
cards (ICJ Rohingya ruling, UK drones for Ukraine, Anthropic IPO, GTA VI, Senegal migrant boat, North
Korea enrichment), each with a PIL-drawn icon, UTC timestamp, headline and one-line context; footer
carries a date check and an ALSO line (Van Gogh record sale, California atmospheric river, Crimean
Bridge attack). compose20.py draws it with PIL only; main.py copies the committed entry.png to
/output; output is a deterministic 1024x1024 PNG under 1 MiB, no network at run time.

## Requirements

- The composed `entry.png` is a 1024x1024 PNG under 1 MiB.
- `main.py` is deterministic, makes no network calls, and copies the entry to the output directory.

## Run

    python3 compose20.py
    MAKEFUN_OUTPUT_DIR=/output python3 main.py
