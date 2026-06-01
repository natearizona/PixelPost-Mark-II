# Comment Survival Audit

Phase: PixelPost Archaeology Phase 9 - Public Reality Verification

Mode: read-only. No artifacts were modified, imported, restored, committed, or pushed.

## Comment Count

Recovered PixelPost export comment records:

```text
887
```

Comments appear in content files `_2.xml` through `_9.xml`. Metadata file `_1.xml` contains no post comments.

## Preserved Comment Fields

| Field | Preserved count | Notes |
| --- | ---: | --- |
| `comment_id` | 887 / 887 | Present |
| `comment_author` | 887 / 887 | Present |
| `comment_author_email` | 797 / 887 | 90 blank |
| `comment_author_url` | 794 / 887 | 93 blank |
| `comment_author_IP` | 887 / 887 | Present; 520 unique IPs reported by sidecar analysis |
| `comment_date` | 887 / 887 | Present |
| `comment_date_gmt` | 887 / 887 | Present |
| `comment_content` | 887 / 887 | Present |
| `comment_approved` | 887 / 887 | Present |
| `comment_parent` | 887 / 887 | Present, all `0` |
| `comment_user_id` | 887 / 887 | Present, all `0` |
| `comment_type` | 0 / 887 | Absent |

## Moderation And Threading

Moderation status:

```text
comment_approved = 1 for all 887 comments
```

Threading:

```text
comment_parent = 0 for all 887 comments
```

Registered-user identity:

```text
comment_user_id = 0 for all 887 comments
```

Interpretation:

- Public-facing comments are strongly preserved.
- Threaded reply structure is not present.
- Registered-user identity is not present.
- Moderation status is preserved and indicates all exported comments were approved.

## Per-Post Distribution

Sidecar read-only analysis reported:

| Comment count per post | Number of posts |
| ---: | ---: |
| 0 | 323 |
| 1 | 181 |
| 2 | 117 |

Top commented post:

```text
The Holy Ghost - Horseshoe Canyon
16 comments
```

## Public Evidence

Wayback spot checks confirm comment counts for the two named public pages:

| Public page | Wayback comments | XML comments | Result |
| --- | ---: | ---: | --- |
| `Journey to the Spirit World` | 0 | 0 | Match |
| `Sidewall in Calf Creek Canyon` | 0 | 0 | Match |
| 2011 PixelPost home page `Cedar City in Winter` | 0 visible | Not fully spot-checked in XML during Phase 9 | Partial |

## Comment Survival Answer

Comment survival is high. The XML exports preserve public-facing comment author names, dates, text, approval status, and much of the contact metadata. Public Wayback evidence confirms comment counts for the two named spot-check pages.
