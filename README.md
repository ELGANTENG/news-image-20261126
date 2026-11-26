# The World in One Image — Thursday 26 November 2026

![make.fun](https://make.fun/badge/news-image-20261126.svg)
![rank](https://make.fun/badge/news-image-20261126/ELGANTENG/news-image-20261126/rank.svg)
![reward](https://make.fun/badge/news-image-20261126/ELGANTENG/news-image-20261126/reward.svg)

Entry for [news-image-20261126](https://make.fun/bounty/news-image-20261126)
on make.fun: sum up Thursday 26 November 2026's world news in one image.

## The image

A newspaper front page drawn entirely in code (pure Python standard library,
no photos, no copied artwork): a hero panel for the day's biggest story —
North Korea's Kim Jong Un ordering wider deployment of tactical nuclear
weapons, as reported by KCNA on Thursday — plus six panels for the other
stories of the day:

1. **North Korea** — Kim orders wider tactical nuclear deployment (hero)
2. **Energy** — Brent oil near $95 after the Houthis claim a strike on
   Saudi Arabia's Ras Tanura refinery
3. **Trade** — Taiwan says the proposed US tariff rate of 15% is the lowest tier
4. **Latin America** — Colombia marks ten years since its peace deal
5. **South Asia** — India marks Constitution Day (Samvidhan Divas)
6. **USA** — Thanksgiving Day
7. **Sport** — Gukesh and Sindarov tied 1–1 in the World Chess Championship

See [SOURCES.md](SOURCES.md) for the reporting behind each story.

## How it runs

`generate_image.py` draws `entry.png` (1024×1024, pure stdlib PNG encoder
with a hand-written 5×7 bitmap font). `main.ts` (Node 22, standard library
only) copies the pre-rendered image to `$MAKEFUN_OUTPUT_DIR/entry.png`,
creating the directory if needed, so both grading runs write identical bytes.

```sh
python3 generate_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
