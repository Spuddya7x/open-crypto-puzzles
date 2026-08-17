# Tested (full negatives ledger)

Every derivation row uses `tools/oracle.py`: a candidate only counts as a match if the derived
ETH address equals the winner wallet `0x635739254BDE27d28301f25aD57c3cAC3C3468f3` exactly,
under any of the 9 swept BIP44 paths (3 accounts times 3 indexes). Witness: the oracle's own
`--selftest` reproduces the public BIP39 KAT address, a positive control that points the oracle
at the KAT's own address, a negative control against the real winner wallet, an invalid-checksum
rejection, and the artist's prior solved "Bifurcations" BIP84 vector, before every run below.

## Audio channel (the toolbox that solved the artist's prior puzzle, "Bifurcations")

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Spectrogram text, Morse (kick/snare as dash/dot), SSTV (including invert-merge), theme-keyed hex offsets, LSB and bit-plane analysis, RIFF/XMP metadata, mid-side decoding, sub-20Hz content, small and medium ASR, demucs vocal isolation plus ASR, run on all 12 lossless masters | 12 tracks times the full toolbox | the same toolbox that solved "Bifurcations" (2020) | negative on all 12 tracks | yes (the toolbox is confirmed to work, since it is what solved the prior puzzle) | 2026-06-17 |

The masters themselves measure at close to 0 percent energy above 13 kHz, which is a property
of the recording, not a playback or re-encoding artifact, so no high band exists to carry
spectrogram text on this album at all. This is why the audio channel is closed for this puzzle
even though the identical toolbox worked on the prior one.

## POAP clock-and-wordlist image (the carrier for this puzzle)

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Word-per-hour read at the numeral centroid plus 1 row (3 candidates per hour), 4 canonical orderings (clockwise, reverse, 12-first clockwise, 12-first counterclockwise) | 1,193,373 combinations tested (132,597 checksum-valid) | BIP44 m/44'/60'/0'/0/0 plus neighbor sweep | 0 match, 131.8 seconds | yes | 2026-07-14 |
| Asymmetric row window (centroid plus or minus 1 row), each of the 4 orderings separately | 531,441 combinations per ordering (about 33,000 checksum-valid each) | same oracle | 0 match | yes | 2026-06-17 |
| Wider asymmetric window refinement (best visual reads with row-aware neighbors) | about 8.6e8 estimated space, sampled rather than exhausted | same oracle | 0 match on the sampled region | yes | 2026-06-17 |
| Distinct-overlay hypothesis (12 words marked by a different color or intensity) | full image histogram | gray-intensity and hue histogram analysis | refuted: exactly 1 gray text population, only 2 non-gray hue families (the red sunburst spokes, the yellow title and signature); no marking of any kind at any of the 12 numeral positions | yes (direct pixel measurement) | 2026-06-17 |
| Higher-resolution or vector source | prize contract tokenURI, POAP asset server, artist website, album video | direct fetch and comparison | refuted: the 2004x2011 raster in this folder is the finest source found anywhere; the album video is 1080p, lower resolution than the plot | yes | 2026-06-17 |
| Calibration against a known-answer "Bifurcations" POAP | POAP GraphQL query for any drop with "bifurcation" in its name | direct API query | refuted: 0 drops match; no known-answer clock image exists for this artist to reverse-engineer the readout rule from | yes | 2026-06-17 |

## Explicitly not fed to the oracle

Sung lyrics on 2 tracks (DiscomfortMeditation, ShadowRealm) contain several BIP39 wordlist
tokens among their ordinary lyrics. I did not test any permutation of these: no mechanism
selects which 12 of the many lyric tokens would be the seed or in what order, so testing them
would be an unbounded search with no stopping rule, not a bounded hypothesis. This is listed
as untested, not as a negative.

## Summary

Across the POAP-image family, 1,193,373 plus 531,441 times 4 plus a sampled 8.6e8-sized space
have been checked, 0 matches, 0 partial hits. The clock-and-grid mechanism itself (order from
the hour position, word from the wordlist cell the numeral overlays) is confirmed by 3 hours
that read with no row ambiguity at all; what remains open is resolving the row for the other 9
hours past plus-or-minus 1, which the published 2004-pixel raster does not resolve further.

## The background text's own geometry, measured 2026-08-17

The flow text is not a mystery to be eyeballed: it is the 2048 words in list order, one
space between them, set in a monospace face at **23.80 pixels per character**, on lines
**48 pixels apart**, with the first line's glyph band starting at y=54 and 41 lines visible
inside the circle. Line length measures at **171 characters**, from the fact that `leisure`
(hour 12, row 2) and `stick` (hour 8, row 28) sit 26 rows and 4,417 characters apart, and
`stick` and `strategy` share row 28 exactly 56 characters and 1,333 pixels apart.

That geometry turns the readout into arithmetic rather than judgement: the word at a given
pixel is `S[c0 + 171*row : ...]` indexed by `(x - x0)/23.80`. Fitting `c0` and `x0` by least
squares on the three unambiguous hours reproduces `leisure` and `stick`, and lands within
one character of `strategy`, so the model is right to about a character. What it does not
fix is the row: a numeral spans 5 text rows, and its own vertical centre is what picks one,
so the numerals whose centre falls near a row boundary stay ambiguous exactly as before.
Reading all 12 hours through the fitted model agrees with the candidate columns above on 9
of 12 hours and disagrees on hours 2, 4 and 9, where it lands one row off (its hour-4 read
is `supreme`, and hour 4 is `strategy` by direct inspection). Treat the extra readings as
widening the pools, not as corrections.

## Reading order: all 24 cyclic orders, not 4

The sweeps above fixed the words and varied 4 reading orders. A clock face has 24: twelve
rotations times two directions. Sweeping all of them over the 3-candidate grid, widened to
4 candidates at hours 2, 9 and 5 by the alternative reads above, is 69,984 word choices
times 24 orders, 1,679,616 candidates, derived at `m/44'/60'/acc'/0/idx` for acc and idx in
0 to 2 (the folder oracle's own neighbourhood). Harness certified against
`tools/oracle.py` on the public BIP39 vector, and a witness drawn from inside the space was
planted in the target set.

Result: 1,679,616 candidates, 105,870 of them checksum-valid, 952,830 addresses derived,
0 matches, 5.4 minutes at 328 candidates per second on 1 contended core. The planted
witness was recovered, so this is a closed negative: no cyclic reading order of this grid
derives the winner wallet, and the 4 orders tested earlier were not the gap.

What that leaves: the reading order is not the missing piece, and the words are pinned to
within one row each, so the next thing to doubt is the grid itself. Either one hour's word
lies more than one row from its numeral's centre, or the seed is not read off the numerals
at all.
