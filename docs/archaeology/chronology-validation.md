# Chronology Validation

Phase: PixelPost Archaeology Phase 9 - Public Reality Verification

Mode: read-only. No artifacts were modified, imported, restored, committed, or pushed.

## Recovered XML Chronology

Recovered PixelPost export post count:

```text
731
```

Recovered date range:

```text
2006-10-16 16:40:08 through 2011-06-23 09:44:05
```

## Earliest Recovered Posts

| Date | Title | Slug | Image |
| --- | --- | --- | --- |
| 2006-10-16 16:40:08 | Boulder Mountain Waterfall | `boulder-mountain-waterfall` | `20061016164008_waterfall1.jpg` |
| 2006-10-16 16:44:51 | Burning Bush, North Rim, Grand Canyon | `burning-bush-north-rim-grand-canyon` | `20061016164451_grancanyon1.jpg` |
| 2006-10-16 16:46:30 | Golden Sage | `golden-sage` | `20061016164630_sage1.jpg` |
| 2006-10-16 16:53:21 | Sheep Skull | `sheep-skull` | `20061016165321_20050719202320_abstract3.jpg` |
| 2006-10-16 16:58:31 | Dead Sheep | `dead-sheep` | `20061016165831_abstract4.jpg` |

## Latest Recovered Posts

| Date | Title | Slug | Image |
| --- | --- | --- | --- |
| 2011-06-14 14:40:28 | Dumpters Behind a Hotel in Downtown Santa Fe | `dumpters-behind-a-hotel-in-downtown-santa-fe` | `20110614144028_downtown_santa_fe.jpg` |
| 2011-06-15 16:13:06 | Richardson's Cash & Pawn, Gallup, New Mexico | `richardsons-cash--pawn-gallup-new-mexico` | `20110615161306_richardson_cash_pawn.jpg` |
| 2011-06-17 08:36:05 | Driving By Shiprock | `driving-by-shiprock` | `20110617083605_shiprock.jpg` |
| 2011-06-19 16:55:02 | Corners of God's Imagination | `corners-of-gods-imagination` | `20110619165502_fallen_leaning_pine.jpg` |
| 2011-06-23 09:44:05 | 1996 Jeep Cherokee | `1996-jeep-cherokee` | `20110623094405_jeep_cherokee.jpg` |

## Wayback Chronology Checks

| Public evidence | Wayback observed date | XML date | Result |
| --- | ---: | ---: | --- |
| `Journey to the Spirit World` | 2006-10-17 | 2006-10-17 16:31:06 | Match |
| `Sidewall in Calf Creek Canyon` | 2007-09-20 | 2007-09-20 06:28:59 | Match |
| 2010 browse page | Shows thumbnails through 2010-era posts | XML includes 2006-2011 posts | Match |
| 2011 home page | Shows `Cedar City in Winter` public post | XML includes 2011 posts and image naming model | Match |

## Archive/Browse Evidence

The 2010 Wayback browse capture at:

```text
https://web.archive.org/web/20100412124631/http://talkingtree.org/index.php?x=browse
```

shows:

- PixelPost title `Browse - Desert Dream`
- hundreds of thumbnail images
- `Categories` section
- `Tags` section
- thumbnail filenames using the recovered `thumb_*.jpg` convention

This confirms that the public PixelPost site exposed chronology through browse/archive mechanics compatible with the recovered XML and thumbnail directory.

## Gaps And Anomalies

Known anomalies:

- The recovered image directories contain 734 JPEGs, while the XML references 731 unique JPEGs.
- The three extra JPEGs should be treated as supplemental/orphan candidates until inspected.
- The XML chronology ends on 2011-06-23, while later WordPress exports continue into 2012. This is expected if the PixelPost export captured the pre-WordPress content layer and WordPress continued afterward.

## Chronology Validation Answer

The recovered XML chronology is publicly plausible and directly confirmed by known Wayback post pages. The 2006-10-16 through 2011-06-23 PixelPost-era range is coherent with public captures and later WordPress migration evidence.
