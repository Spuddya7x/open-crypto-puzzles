# Tested hypotheses, full ledger

Summary table is in the README. This file has the full detail behind each row. All
counts below were re-read from my own private research notes before writing this
folder.

## Both published image sets are identical

The rules page mentions "an alternative release, as a single image." I compared
every one of the 34 individual panel images against the corresponding region of the
combined alternative-release image, byte for byte (MD5).

Result: 34 of 34 panels match exactly. This channel is closed: the alternative
release carries no additional or different information, it is the same 34 stills
republished as one file. Date: 2026-08-03.

## Intruder criterion: MPAA rating equals R

Hypothesis: the 10 "intruder" films are exactly the ones rated R by the MPAA, and
the IMDb page field the rules point to is the certificate rating.

Method: count the films confirmed R-rated as more panels were identified.

Result: this criterion looked correct early, when only a partial set of films was
identified (10 of 18 identified films rated R at one point). It broke as soon as 2
more films were confirmed: with panel #4 (Mad Max, R) and panel #34 (rated R under
either of its 2 disputed identifications) added, the R-rated count reached 16 to 18
out of the identified films, well past 10. Refuted. Witness: this is a direct count
over the film corpus, not a search that could produce a false negative; re-counting
is immediate from `data/films.csv`. Date: 2026-08-04.

## Intruder criterion: won at least one Oscar

Hypothesis: the 10 intruders are the films that won at least one Academy Award.

Method: same approach, counting Oscar-winning films as identifications accumulated.

Result: looked correct at 10 of 21 identified films early on, refuted once panel
#24 (Ordinary People, a 4-Oscar winner including Best Picture) was confirmed
through a route independent of the reverse-image search used for most other
panels, pushing the count to 11 of 34. Date: 2026-08-04.

## Intruder criterion: adapted from a novel

Hypothesis: the 10 intruders are the films adapted from a published novel.

Method: same approach.

Result: looked correct at 10 of 31 identified films, refuted at 12 of 34 once
further identifications landed. Date: 2026-08-04.

## About 25 further intruder criteria

Method: the same accumulate-and-recount approach applied to about 25 further
candidate IMDb fields and binary properties (examples: country of origin,
decade of release, director's other Bitcoin-relevant work, runtime bracket, color
versus black and white, single-word versus multi-word title).

Result: none produced an exact 24-versus-10 split against the identified film set,
either from the start or after refutation by a later identification. Witness: each
criterion is a direct count over the film corpus and is immediately re-checkable;
no witness protocol beyond re-counting applies here. Date: 2026-08-04.

Methodological note, kept because it explains why no criterion is locked in below:
3 different criteria (MPAA=R, Oscar win, novel adaptation) each looked like the
answer while the film corpus was still incomplete, and each was broken by the very
next identification. With about 25 to 30 criteria tried against a set of only 34
films, landing on an exact 10-film split by chance is not strong evidence on its
own. My working rule is to not treat any criterion as confirmed before all 34
panels are identified with confidence.

## Title-to-word rule: base rate measurement

This is a measurement, not a hypothesis test with a pass or fail result: of the 33
titles identified as of 2026-08-04, 29 contain at least one English BIP39 word as a
literal substring of the title (for example, "Die Hard" contains "hard"; "A
Clockwork Orange" contains 4 candidates: "clock," "orange," "range," "work"). Four
titles contain none: The Goonies, Barry Lyndon, Sharknado, and Raiders of the Lost
Ark. The literal-substring rate across the 33 identified titles is about 14%,
counted per candidate word against the full BIP39 wordlist. This measurement rules
out "every title contains exactly one obvious word" as the full rule (4 titles have
none, several have more than one), but does not by itself say which of several
candidate words is the intended one, or what the rule is for the 4 titles with none.

## Combinations of MPAA ratings, tested at the oracle, 2026-08-17

The list above says no single IMDb criterion splits 34 into 24 and 10. Ratings taken in
*combination* do, and there are exactly three such sets: APPROVED+PG+TV-14 (2+7+1),
G+PG+TV-14 (2+7+1), and APPROVED+G+PG-13+TV-14 (2+2+5+1). The counts come straight from
`data/films.csv` and panel 11's rating is unknown, so it never joins an intruder set.

One of the three is singled out by the title-to-word rule itself: the four identified
titles that contain no BIP39 word at all (The Goonies, Barry Lyndon, Sharknado, Raiders of
the Lost Ark) *have* to be intruders, and only G+PG+TV-14 contains all four. That makes it
the strongest intruder rule this folder has had.

Tested: the 24 keepers read in panel order, each panel contributing a BIP39 word from its
title, panel 11 (unidentified) ranging over the whole 2048-word list, panel 34 read as
`ring` from the Dead Ringers identification. Derivation is BIP84 `m/84'/0'/0'/0/i` for i in
0 to 2, on a harness that reproduces the folder oracle's own address for the public 24-word
vector exactly.

- APPROVED+PG+TV-14: 1,572,864 candidates, 6,137 checksum-valid, 0 matches, witness planted
  and recovered.
- G+PG+TV-14: 786,432 candidates, 3,061 checksum-valid, 0 matches, witness planted and
  recovered.
- APPROVED+G+PG-13+TV-14: not run. Its keeper set contains three of the four wordless
  titles, so under the title-to-word rule those panels have no word to contribute and the
  space blows up to 2.8e14; the rule contradicts the mechanism rather than being expensive.

So the rating channel is now closed for the two consistent partitions, under the reading
that each keeper contributes a BIP39 word found literally in its title. What is not closed:
that reading itself. Panel 34's identification is still disputed, and several panels carry
2 to 4 candidate words where the sweep tried all of them, so a negative here argues against
the rating rule rather than against any particular word.

## Every intruder set consistent with the title-to-word rule, 2026-08-17

Rather than guess which IMDb field marks the intruders, this run brute-forces the intruder
*set* under the constraint the mechanism itself imposes: if every keeper contributes a BIP39
word found literally in its title, then the four identified titles that contain none (panels
8, 25, 26, 32) are intruders, and so is panel 11 while it is unidentified. That fixes 5 of
the 10 and leaves C(29,5) = 118,755 ways to pick the rest.

Each keeper set was read in panel order, every candidate word each title offers tried, panel
34 read as `ring`: 118,755 intruder sets, 271,127 checksum-valid 24-word candidates, derived
at BIP84 `m/84'/0'/0'/0/i` for i in 0 to 2, 14.1 minutes. 0 matches.

Certification: the harness reproduces the folder oracle's own address for the public 24-word
vector exactly, and the checksum filter accepts that vector. No witness was planted inside
the candidate stream itself, so by this repository's house rule this is a well-instrumented
negative rather than a formally witnessed one.

What it closes: no choice of 10 intruders solves this puzzle *while* every keeper's word is
a literal BIP39 substring of its title, panel 34 is `ring`, and the derivation is BIP84 at
account 0, indexes 0 to 2. The intruder rule is therefore not the only thing missing. The
title-to-word rule is now the prime suspect: 4 of 33 identified titles carry no BIP39 word,
which the author's own "transform 'somehow' each movie title" wording does not require to be
a substring at all.

## Release year as a wordlist index: refuted by inspection, 2026-08-17

The obvious replacement for the substring rule is the film's release year read as a BIP39
index, which is attractive because it gives every title a word, including the four that
contain none. It does not survive a look at the numbers. Film years here run 1946 to 2018,
and BIP39 positions 1946 to 2018 are all in one narrow alphabetical band: `veteran`,
`virus`, `wagon`, `warfare`, `warrior`, `wear`, `welcome`, `wine`, `winter`, `wire`. A
24-word seed drawn from that band would be 24 words starting with v or w. Worse, five of
the 34 panels are 1979 films (Alien, Mad Max, Apocalypse Now, Escape from Alcatraz, Star
Trek: The Motion Picture), which would all map to the same word, so the seed would have to
repeat `warrior` up to five times or those five films would all have to be intruders, out
of a budget of ten. Refuted without spending compute; the same argument kills any
year-derived index, 0-based or 1-based.
