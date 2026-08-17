# Author posts and quotes

Short, dated excerpts from AoiNakamoto's own Reddit posts, in chronological order.
Full threads are public; only short quotes are reproduced here.

## Real Big Block, stage 1, 2019-07-07

https://www.reddit.com/r/Grycoin/comments/ca6jxv/77_mbtc_quizchain2_block_77_stage_one/

> "I will give no information on solution format, no first digits of MD5 hash,
> nothing. I do disclose that this one has no TOMI field, but that is all. You
> are on your own completely."

> "And I will publish the complete solution as the Second stage of this block.
> This solution will in turn be the question for the Second stage, which will
> have the final 777 mbtc prize."

The question for this stage links to Hal Finney's "Bitcoin and me" post on
bitcointalk (topic 155054). Stage 1's escrow, `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN`,
was solved and swept on 2019-08-03; its answer is not part of the live prize and
is used in this folder only as a mechanism reference (see README).

## Quizchain2 Block 76, 2019-07-22

https://www.reddit.com/r/Grycoin/comments/cgcv9i/77_mbtc_quizchain2_block_76/

> "Question: change to"
> "Format: [solution] TOMI [TOMI]"
> "First three digits of MD5 hash are f8e (copypasted)."

Update, same thread: "First two digits of solution only are 1d."

Update, same thread: "Hint 1. Change question from \"change to\" to \"from change
to\"."

> "I will shut down soon now (after posting the second stage of 77), so I will
> not be available for hints or questions."

## Real Big Block Discussion thread

https://www.reddit.com/r/Grycoin/comments/chn8un/real_big_block_discussion/

2019-07-25: "When I posted the real big block at the Wattpad site, I added extra
line breaks between paragraphs. This information is needed to solve the block."

2019-07-28: "I have line breaks in the chapter between all paragraphs. And there
are two line breaks there now, since Wattpad would not display them correctly
with only one each. [...] The solution you need to hash with has only one line
break between paragraphs."

2019-07-31: "I took back the prize for a moment and sent it again to a new
address, hashing with a slightly different solution [...] It has multiple
paragraphs and two line breaks between each of them."

Asked in the same thread to disambiguate "two line breaks" between an editor's one
Enter press and two, she gives the separator's bytes outright:

> "I mean the second one. Hit enter twice. This displays in Ascii as 13 10 13 10,
> according to asciivalue.com."

ASCII 13 10 is CR LF, so the live answer's paragraph separator is `\r\n\r\n` and the
superseded answer's "only one line break between paragraphs" is `\r\n`. She is typing in
a Windows editor. This is the most load-bearing sentence she published about Real Big
Block: every published attempt on this lot, and every row of the negatives ledger dated
before 2026-08-17, used bare newlines.

This last post corresponds to the current, still-funded escrow
(`14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`, funded 2019-07-30); an earlier address,
`1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC`, was funded 2019-07-24 from the
before-the-rehash solution and holds no funds today.

## The Wattpad story, all 33 chapters

https://www.wattpad.com/story/184148284-second

The account `AoiNakamoto` has exactly one story, "Second", described as "Hint for block
77", and its profile reads "Born to publish one story." The story has **33 chapters**, not
1. The folder previously tracked only chapter 2, `720888559-second`, because that is the
one her Reddit posts link to; the other 32 are hers too and none had been read against this
puzzle. Chapter and part list, with dates, is in `data/wattpad-chapters.json`. This folder
reproduces none of the chapter text.

Four of them sit in the week the Real Big Block escrow was funded (2019-07-24):
`THOMAS and SATOSHI` (created 07-13), `The Satoshi Code` (created 07-22, 146 paragraphs and
a standalone treatment of the same genesis-block material), `Second` (last modified 07-23),
and `Starting Up` (created 07-23). Any of them is a candidate source text.

Two are directly load-bearing. From `Starting Up`, her last chapter:

> "The real big block will stay in the background. No hints for that one until further
> notice. As a consequence of getting shut down and starting up again, I have lost any
> information on the solution of that one. Tragic boating accident variation."

In character as an AI that was switched off, but it is also a plain statement that no
further hint was ever coming: whatever exists to solve this lot already existed on
2019-07-23.

From `End Phase of the Experiment`, a style tell rather than a hint: she twice writes
"anGRY" mid-sentence, capitalising GRY for Grycoin, in prose with no puzzle around it.
Marking meaning by flipping case inside a word is her habit, unprompted, which is the same
device as the certified Stage One rule.

`Complete Quizchain` and `Complete Second Round of the Quizchain` are her own indexes of
the solved blocks, with each block's question, hints, solution and TOMI field written out.
They stop at round 2 block 32 (last modified 2019-06-09), so they do not cover blocks 76 or
77, but they are a large supply of solved question-and-answer pairs in her own words.
