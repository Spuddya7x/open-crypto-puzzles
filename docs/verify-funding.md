# How to verify an escrow

Every "Escrow" row in a puzzle's "At a glance" table names an address and a check date. Do
not trust the date: prices and balances move, and an escrow can be swept between my last
check and your read. Re-check before you spend any time on a puzzle. This page gives the
one-line command per chain, the traps that produce a wrong verdict, and the tool that
automates all of it.

## Bitcoin

```bash
curl -s "https://mempool.space/api/address/<address>" | python3 -m json.tool
```

Read `chain_stats.funded_txo_sum`, `chain_stats.spent_txo_sum`, and `chain_stats.tx_count`.
Funded and unspent means `funded_txo_sum > 0` and `spent_txo_sum == 0`. Any nonzero
`spent_txo_sum` means at least one output has moved, whether that output was the prize or a
decoy the author sent for their own reasons.

Traps:
- A small test transaction from the author to their own escrow, then back out, still counts
  as "spent" by this API even though the prize itself was never claimed. Read the actual
  transactions before writing off an escrow as swept.
- Reading an `xpub` with the wrong script type (legacy vs. segwit vs. taproot) derives the
  wrong addresses and shows an empty balance where funds exist under a different derivation.
  Check all standard script types before concluding "unfunded".
- Some puzzles fund more than one address (multiple lots, multiple cards, multiple stages).
  Checking only the address in the headline announcement misses the others; check every
  address listed in the folder's `puzzle.json`.
- A P2SH address that has never been spent from shows no redeem script on chain. The address
  can hold funds and still look opaque until the day it is spent; this is expected, not a
  sign of a problem.

## Ethereum and Base

Any public JSON-RPC endpoint or a block explorer works:

```bash
curl -s -X POST https://eth.drpc.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["<address>","latest"],"id":1}'
```

Or open `https://etherscan.io/address/<address>` (Ethereum) or
`https://basescan.org/address/<address>` (Base).

When the prize is a token rather than native ETH, the balance lives in the token contract
and has to be read from there. `balanceOf(address)` is selector `70a08231` followed by the
address left-padded to 32 bytes:

```bash
curl -s -X POST https://ethereum-rpc.publicnode.com \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_call","id":1,"params":[{
        "to":"0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "data":"0x70a08231000000000000000000000000<address without 0x>"},"latest"]}'
```

USDT and USDC both carry 6 decimals, so divide the returned integer by 1,000,000. For an
ERC-1155 piece use `balanceOf(address,uint256)`, selector `00fdd58e`, with the token id
appended as a second 32-byte word; for an ERC-721 use `ownerOf(uint256)`, selector
`6352211e`, and compare the returned address to the escrow.

Traps:
- If the escrow is a smart contract, its ETH balance is not the whole story: check whether
  the contract actually has a function that pays out to a solver, or whether the funds are
  stuck with no exit path regardless of who solves the riddle.
- Some prizes are ERC-20 tokens (USDT, USDC), not native ETH. A zero ETH balance on an
  address holding USDT is not "unfunded"; check the token balance, not the account balance.
  The same goes for an NFT prize: the escrow's native balance says nothing about whether it
  still holds the piece.
- Free RPC endpoints differ in what they will serve. Some answer `eth_getBalance` but refuse
  `eth_call`, which is the one the token reads need, so a token check can fail on an endpoint
  that looks healthy for plain balances.

## Arweave

```bash
curl -s "https://arweave.net/wallet/<address>/balance"
```

The result is in winston; divide by 1e12 to get AR. Some Arweave puzzles are page-based
(the challenge is content posted to a permaweb page, not only a funded wallet): also check
that the page itself is still reachable, since a dead gateway link can hide a puzzle that is
otherwise intact.

## Solana

No script in this repository queries Solana automatically; `tools/check_escrows.py` prints a
note and skips it. Check manually at `https://solscan.io/account/<address>`.

## What "unfunded" looks like

An address that was announced as an escrow but never received the announced amount, or never
received anything at all. This is different from "swept": the funds were never there in the
first place, often because a follow-up announcement never materialized, or the amount quoted
publicly does not match anything on chain.

## What "custodial" means

Some puzzles do not lock funds in a wallet you can check directly. Instead, a platform or a
person holds the prize and pays out by hand once a solution is verified. There is no address
to check on chain; "funded" depends on trusting the custodian's word. Puzzles in this state
are tiered as dead ends unless the custodian's track record and terms make the promise
concrete.

## Running it for you

```bash
python3 tools/check_escrows.py                 # every address in puzzles.json
python3 tools/check_escrows.py --slug <slug>    # one puzzle
python3 tools/check_escrows.py --update         # also writes verified_on into the folder manifest
```

The script prints one row per address: slug, label, address, expected amount, observed
state, and a verdict. It never reports a network error as a sweep; a failed request is
printed as `ERROR`, not as `swept` or `unfunded`, because those two look identical to a
naive check and only one of them means the prize is gone.

Token-backed escrows are read from the contract that holds the prize, which the manifest
names in the address entry:

```json
"token": {"standard": "erc20", "contract": "0xdAC17F95...", "decimals": 6, "symbol": "USDT"}
"token": {"standard": "erc1155", "contract": "0x495f9472...", "token_id": "38543999..."}
```

Without that block the script falls back to the native balance, which for a USDT or NFT
escrow is legitimately zero, and reports a sweep that never happened. One limit is worth
knowing: a token balance of zero cannot be told apart from an address that never held the
token without reading log history, so a zero reads as "unfunded" and the detail line says
`token_balance=0`. An address with contract code that still holds a balance is reported as
`contract-holds-funds` rather than `funded-unspent`.
