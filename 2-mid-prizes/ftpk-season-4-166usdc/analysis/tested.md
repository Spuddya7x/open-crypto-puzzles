# Negatives ledger, FTPK Season 4

Dated 2026-07-26 unless noted otherwise.

## Page-naming scheme

Every game page is named `md5(N).html` for a decimal integer `N`; probing roughly 34,000
URLs (every N from 0 to 2200, a set of thematic word hashes, and a wider sweep up to
36,000) found exactly the 12 known game pages plus 1 further page, the one the author
announced as a Season 2 hint (its input string is the 12 Season 4 answer words
concatenated in game order, matching the site's own naming convention). No other hidden
page exists in this range.

Testing whether N itself is a direct index into the BIP39 wordlist: game 1's own hangman
mechanics fix the answer as `frog` with confidence (pattern `??o?`, corner tags "1st" and
"dance" marking already-excluded letters and the first alphabetically surviving
candidate). Game 1's page-naming integer is 1570, which indexes to "service" or "session"
in the BIP39 list depending on 0- or 1-based counting; neither word fits the `??o?`
pattern. Refuted as a direct index scheme.

**Reopened, 2026-08-16.** That refutation rests on the hangman reading, and the hangman
reading is the weaker of the two. The hidden page's own name is
`servicecricketgloomattendsupremejumpannualeagerpulpprojectdiseaseround`, and its first
word is `service`, the word at 1-based BIP39 position 1570, which is exactly game 1's page
integer. The two facts were established by different routes, one by brute-forcing `md5(N)`
against the game pages and one by reading the hidden page's URL, so their agreement on one
word out of 2048 is not a coincidence I can wave away. The direct index scheme is back on
the table and `frog` is the reading I would now drop.

## The hidden page's name, read as the word set

The name splits into BIP39 words in exactly one way. Enumerating every split of the
69-character string into dictionary words (3 to 8 characters each, all 2048 words allowed)
returns a single segmentation, the 12 words above: there is no competing reading of the
concatenation. Checked 2026-08-16.

Those 12 words, in the order the URL gives them, pass the BIP39 checksum, which only 1
ordering in 16 does. As a mnemonic in that order they derive
`0x97486102c2019ca03389024d1990a241004e8493` at `m/44'/60'/0'/0/0`, which is neither this
season's escrow nor Season 2's. Extending to 27 standard paths (`m/44'/60'/0'/0/0` through
`/5`, `m/44'/60'/i'/0/0` for i of 0 to 5, the Ledger legacy layout `m/44'/60'/0'/0`, and
BIP44/BIP49/BIP84 Bitcoin at address indexes 0 to 4) and comparing against all 78 addresses
in this repository gives 0 matches. The word set in game order is therefore not the
mnemonic; if the set is right, the mnemonic is a different ordering of it.

## Grid puzzles

Games 4 (8x8, corner tag "fall"), 6 (15x15), and 9 (11x11, corner tag "5:30") were
searched in all 8 directions, length 4 or more, against both the full BIP39 wordlist and
a 75,145-word English dictionary. Game 4 returned 2 incidental matches ("time" and
"evans"), neither fitting any established pattern; games 6 and 9 returned 0 matches.
Refuted as classic word-search puzzles.

Game 12 (a Ludo board with colored squares) and game 6 are both 15x15, which looked
intentional; overlaying the Ludo board's colored-square mask onto the letter grid in
row-major order produces unreadable sequences (for example the silver squares read
`AVEXRO`, the khaki squares `PVMIJT`). Refuted for the naive row-major alignment; other
alignments (rotations, reflections, or reading the board's own path order) were not
exhausted.

Game 3 (a subtraction problem rendered in colored dots): reading the full dot pattern as
a base-3 number under each of 6 color-to-digit assignments, then subtracting as the
puzzle's layout implies, produces 10 or 11-digit results under every assignment, none in
the 1 to 2048 range a BIP39 index would need. Refuted as stated; the puzzle's structure
is confirmed, its encoding is not yet solved.

## Oracle self-test

`tools/oracle.py --selftest` reproduces the public BIP39/BIP44 test mnemonic (12
repetitions of "abandon" followed by "about") deriving to
`0x9858EfFD232B4033E47d90003D41EC34EcaEda94`, and separately confirms the checksum filter
accepts that vector and rejects a corrupted variant of it. Measured on one CPU core: 956
mnemonic derivations per second, and 1.5 million BIP39 checksum checks per second with a
6.23 percent pass rate, matching the 1-in-16 rate BIP39's checksum design predicts.

None of the grid and page-naming checks above carries a planted witness proving a search
would find a real answer if one were in scope, since most of the 12 words are not yet
established; each row's witness reflects only whether that specific check's own method
was validated (a positive control), not whether the full derivation oracle has been
exercised on a real solution.
