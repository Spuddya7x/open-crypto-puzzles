# Tested hypotheses, full ledger

Positions 3, 5, 8 and 9 are held at the words the site's italic-marker device fixes
(`unveil`, `deposit`, `grid`, `remind`) in every sweep below. The eight riddle positions
are the search.

The harness used for these runs derives `m/84'/0'/0'/0/0` directly rather than through
`tools/oracle.py`, for speed. It was checked two ways before being trusted: it reproduces
the public BIP39/BIP84 vector (`abandon` x11 + `about` to
`bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu`), and on 5 random candidates drawn from the
pools below it returns the same address as `tools/oracle.py` byte for byte. Every sweep
also plants a witness: a real candidate from inside that sweep's own space, whose address
is added to the target set, so a sweep that fails to report its witness has not searched
what it claims to.

## The pools

Each riddle's pool is my reading of it, ranked, every word checked to be in the BIP39
English list. The three I would bet on are position 2 `kingdom` ("a realm where the crown
is law"), position 11 `umbrella` ("it only works when it's open, and it's there to shield
you"), and position 12 `spot` ("a single mark on a map, or the act of finding it", the
noun and the verb in one word). The three vaguest are 1 ("presence without permanence"),
4 ("born twice, seen once") and 7 ("you'll probably agree this hunt is..."), and those get
the widest pools.

Worth recording for whoever picks this up: `research` and `study` are not BIP39 words, so
position 10's "systematic pursuit of the unknown" cannot be either of the two most natural
English answers. `science`, `inquiry`, `search` and `survey` are the in-dictionary
readings.

## L-001: tier A, the top reading of each riddle

30,720 combinations, 1,989 checksum-valid, each derived at 6 paths (`m/84'/0'/0'/0/0`,
`/1`, `/2`, `m/84'/0'/1'/0/0`, the Electrum layout `m/0'/0/0`, and `m/0/0`). 0 matches.
Witness recovered. 2026-08-16.

## L-002: tier B, wider pools

4,300,800 combinations, 265,502 checksum-valid, same 6 paths. 0 matches. Witness
recovered. Rate: 319 derivations per second on 1 core of 4, with other searches running.
2026-08-16.

## L-003: one riddle position free over the entire wordlist

The tiers above assume all 8 of my readings are inside their pools, which is a conjunction
of 8 guesses. This sweep assumes less: one position ranges over all 2048 BIP39 words while
the other 7 sit at their top-3 readings. 35,831,808 combinations, about 2.24 million
checksum-valid derivations at `m/84'/0'/0'/0/0`. Witness recovered.

RESULT_PENDING

## What this does and does not close

A negative here does not say the riddle readings are wrong; it says no combination inside
the searched space derives the escrow. The searched space is still a product of my
interpretations, and the honest reading of these negatives is that either two or more of
my readings are wrong at once, or one of the 4 italic-marked words is not what the article
now shows, or the wallet is not at `m/84'/0'/0'/0/0` with an empty passphrase.
