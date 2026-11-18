[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/pattrap-motor/news-image-20261118-entry/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/pattrap-motor/news-image-20261118-entry/reward.svg)](https://make.fun/bounty/news-image-20261118)

# The World in One Day — 18 November 2026

Entry for the [news-image-20261118 bounty on make.fun](https://make.fun/bounty/news-image-20261118).

A newspaper front page that sums up Wednesday 18 November 2026 in one image:

- **Lead — THE BRIDGE FALLS:** Ukraine's second strike in two days brings down the
  Kerch road span; rail reopens on one track as Moscow vows to rebuild.
- **Bahrain:** Iran's third drone attack on US targets in five days — Tehran claims it
  hit a radar at Isa Air Base; Bahrain and the US say every drone was intercepted.
- **Manila:** the Quad strikes critical-minerals deals; ASEAN closes; Trump flies to
  Shenzhen for Thursday's talks with Xi and Putin.
- **Shenzhen:** Xi meets Carney — China cuts tariffs on C$400m of Canadian pork and seafood.
- **London:** Britain sanctions eight Israeli settlement firms and a Gaza aid-blocking
  group to protect the two-state solution.
- **Also today:** Knesset elects an Eisenkot ally as Speaker; Cyclone Akvan strengthens
  in the Bay of Bengal; Trump hints at a possible Kim meeting at APEC.

## How it is made

`draw.py` draws the whole front page with Pillow (flat illustrations, DejaVu fonts —
no AI-generated text, so nothing can come out garbled). `main.py` (standard library
only, no network) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. The program
is deterministic: two runs write identical bytes.

Rebuild the image: `python3 draw.py`
