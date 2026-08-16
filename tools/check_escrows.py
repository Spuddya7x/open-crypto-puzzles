#!/usr/bin/env python3
"""
check_escrows.py -- re-check every puzzle escrow against the chain.

Purpose:
    Read every puzzle folder manifest (or the generated puzzles.json when present), query
    the relevant chain for each address, and print a table of expected versus observed state.
    This is the tool "How to read this repository" step 3 points readers at: never trust a
    stale on-chain check date, re-run this.

Usage (run from the repository root):
    python3 tools/check_escrows.py                # every address in every manifest
    python3 tools/check_escrows.py --slug <slug>   # one puzzle only
    python3 tools/check_escrows.py --update        # also writes verified_on/verified_state
                                                    # back into the folder's puzzle.json

Input:
    puzzles.json if present at the repository root, otherwise every <tier>/<slug>/puzzle.json.

Output:
    One printed row per address: slug, label, address, expected, observed, spent, verdict.
    Exit code 1 if any address that a manifest claims is "funded-unspent" is observed as
    swept or unfunded. Network errors are printed as ERROR and never counted as a sweep.

Token-backed escrows:
    Some prizes are not native coin. An address entry may carry a "token" block naming the
    contract that actually holds the prize, and the balance is then read from that contract
    instead of from the account's native balance:

        "token": {"standard": "erc20", "contract": "0x...", "decimals": 6, "symbol": "USDT"}
        "token": {"standard": "erc1155", "contract": "0x...", "token_id": "3854..."}
        "token": {"standard": "erc721", "contract": "0x...", "token_id": "42"}

    Without that block a USDT or NFT escrow reads as "unfunded", because its native balance
    is legitimately zero, and the run reports a sweep that never happened. One limit is worth
    knowing: a token balance of zero cannot be told apart from an address that never held the
    token, because that needs log history; a zero token balance is reported as "unfunded", and
    the detail line says token_balance=0 so the reader can check the explorer.

Contracts:
    An address whose code is non-empty is reported as "contract-holds-funds" when it still
    holds a balance, not as "funded-unspent": the coins are there but only the contract's own
    logic can release them.
"""

import argparse
import json
import os
import sys
from datetime import date

import requests

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIERS = ["1-big-prizes", "2-mid-prizes", "3-small-prizes", "4-solved", "archive/dead-ends"]

TIMEOUT = 15
RETRIES = 1  # one retry after the first attempt, so two attempts total

# Ordered by what they will actually serve. The first two answer eth_call, which the token
# balance reads need; drpc refuses eth_call on its free tier and is kept only as a fallback
# for the plain balance reads.
ETH_RPC_ENDPOINTS = [
    "https://ethereum-rpc.publicnode.com",
    "https://eth.merkle.io",
    "https://eth.drpc.org",
    "https://cloudflare-eth.com",
]
BASE_RPC_ENDPOINT = "https://mainnet.base.org"

# Function selectors, first four bytes of the keccak hash of each signature.
SELECTOR_ERC20_BALANCE_OF = "0x70a08231"    # balanceOf(address)
SELECTOR_ERC721_OWNER_OF = "0x6352211e"     # ownerOf(uint256)
SELECTOR_ERC1155_BALANCE_OF = "0x00fdd58e"  # balanceOf(address,uint256)


def http_get(url, **kwargs):
    last_exc = None
    for attempt in range(RETRIES + 1):
        try:
            return requests.get(url, timeout=TIMEOUT, **kwargs)
        except requests.RequestException as exc:
            last_exc = exc
    raise last_exc


def http_post(url, json_body):
    last_exc = None
    for attempt in range(RETRIES + 1):
        try:
            return requests.post(url, json=json_body, timeout=TIMEOUT)
        except requests.RequestException as exc:
            last_exc = exc
    raise last_exc


def check_bitcoin(address):
    try:
        resp = http_get(f"https://mempool.space/api/address/{address}")
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        return "ERROR", f"network error: {exc}"

    stats = data.get("chain_stats", {})
    funded = stats.get("funded_txo_sum", 0)
    spent = stats.get("spent_txo_sum", 0)
    if funded == 0:
        return "unfunded", f"funded={funded} spent={spent}"
    if spent == 0:
        return "funded-unspent", f"funded={funded} spent={spent}"
    if spent >= funded:
        return "swept", f"funded={funded} spent={spent}"
    return "partially-spent", f"funded={funded} spent={spent}"


def _eth_rpc(url, method, params):
    resp = http_post(url, {"jsonrpc": "2.0", "method": method, "params": params, "id": 1})
    resp.raise_for_status()
    body = resp.json()
    if "error" in body:
        raise RuntimeError(body["error"])
    return body["result"]


def _abi_address(address):
    return address.lower().replace("0x", "").rjust(64, "0")


def _abi_uint(value):
    return format(int(value), "064x")


def _format_units(raw, decimals):
    if not decimals:
        return str(raw)
    text = format(raw / (10 ** decimals), f".{decimals}f").rstrip("0").rstrip(".")
    return text or "0"


def check_evm_token(address, token, endpoints):
    """Read the prize from the token contract that holds it, not from the native balance."""
    standard = str(token.get("standard", "")).lower()
    contract = token.get("contract", "")
    token_id = token.get("token_id")
    symbol = token.get("symbol", "")
    decimals = token.get("decimals", 0)

    if not contract:
        return "ERROR", "token block has no contract address"
    if standard in ("erc721", "erc1155") and token_id is None:
        return "ERROR", f"token block for {standard} has no token_id"

    if standard == "erc20":
        data = SELECTOR_ERC20_BALANCE_OF + _abi_address(address)
    elif standard == "erc1155":
        data = SELECTOR_ERC1155_BALANCE_OF + _abi_address(address) + _abi_uint(token_id)
    elif standard == "erc721":
        data = SELECTOR_ERC721_OWNER_OF + _abi_uint(token_id)
    else:
        return "ERROR", f"unknown token standard: {standard}"

    last_exc = None
    for url in endpoints:
        try:
            result = _eth_rpc(url, "eth_call", [{"to": contract, "data": data}, "latest"])
            native_wei = int(_eth_rpc(url, "eth_getBalance", [address, "latest"]), 16)
            native = f" native_balance_wei={native_wei}"

            if standard == "erc721":
                owner = "0x" + result[-40:]
                if owner.lower() == address.lower():
                    return "funded-unspent", f"token_owner={owner} (the escrow){native} (via {url})"
                return "swept", f"token_owner={owner}, not the escrow{native} (via {url})"

            raw = int(result, 16)
            unit = f" {symbol}" if symbol else ""
            held = f"token_balance={_format_units(raw, decimals)}{unit} raw={raw}"
            if standard == "erc1155":
                held += f" token_id={token_id}"
            if raw == 0:
                return "unfunded", f"{held}, zero cannot be told from never-funded without log history{native} (via {url})"
            return "funded-unspent", f"{held}{native} (via {url})"
        except Exception as exc:
            last_exc = exc
            continue
    return "ERROR", f"network error: {last_exc}"


def check_evm(address, endpoints, token=None):
    if token:
        return check_evm_token(address, token, endpoints)

    last_exc = None
    for url in endpoints:
        try:
            balance_hex = _eth_rpc(url, "eth_getBalance", [address, "latest"])
            tx_count_hex = _eth_rpc(url, "eth_getTransactionCount", [address, "latest"])
            balance_wei = int(balance_hex, 16)
            tx_count = int(tx_count_hex, 16)
            try:
                is_contract = len(_eth_rpc(url, "eth_getCode", [address, "latest"])) > 2
            except Exception:
                is_contract = False
            kind = " (contract)" if is_contract else ""
            if balance_wei == 0 and tx_count == 0:
                return "unfunded", f"balance=0 nonce=0{kind} (via {url})"
            if balance_wei == 0 and tx_count > 0:
                return "swept", f"balance=0 nonce={tx_count}{kind} (via {url})"
            if is_contract:
                return "contract-holds-funds", f"balance_wei={balance_wei} nonce={tx_count} (contract) (via {url})"
            return "funded-unspent", f"balance_wei={balance_wei} nonce={tx_count} (via {url})"
        except Exception as exc:
            last_exc = exc
            continue
    return "ERROR", f"network error: {last_exc}"


def check_ethereum(address, token=None):
    return check_evm(address, ETH_RPC_ENDPOINTS, token)


def check_base(address, token=None):
    return check_evm(address, [BASE_RPC_ENDPOINT], token)


def check_arweave(address):
    try:
        resp = http_get(f"https://arweave.net/wallet/{address}/balance")
        resp.raise_for_status()
        winston = int(resp.text.strip())
    except Exception as exc:
        return "ERROR", f"network error: {exc}"
    ar = winston / 1e12
    if winston == 0:
        return "unfunded", f"balance={ar} AR"
    return "funded-unspent", f"balance={ar} AR"


def check_address(entry):
    chain = entry.get("chain", "")
    address = entry.get("address", "")
    token = entry.get("token")
    if chain == "bitcoin":
        return check_bitcoin(address)
    if chain == "ethereum":
        return check_ethereum(address, token)
    if chain == "base":
        return check_base(address, token)
    if chain == "arweave":
        return check_arweave(address)
    if chain == "solana":
        return "SKIPPED", "Solana is not queried automatically; check https://solscan.io/account/<address> by hand."
    return "ERROR", f"unknown chain: {chain}"


def load_puzzles(slug_filter=None):
    puzzles_json_path = os.path.join(REPO_ROOT, "puzzles.json")
    puzzles = []
    if os.path.isfile(puzzles_json_path):
        with open(puzzles_json_path, encoding="utf-8") as f:
            doc = json.load(f)
        puzzles = doc.get("puzzles", [])
    else:
        for tier_dir_name in TIERS:
            tier_dir = os.path.join(REPO_ROOT, tier_dir_name)
            if not os.path.isdir(tier_dir):
                continue
            for entry in sorted(os.listdir(tier_dir)):
                manifest_path = os.path.join(tier_dir, entry, "puzzle.json")
                if os.path.isfile(manifest_path):
                    with open(manifest_path, encoding="utf-8") as f:
                        manifest = json.load(f)
                    manifest["folder"] = f"{tier_dir_name}/{entry}"
                    puzzles.append(manifest)

    if slug_filter:
        puzzles = [p for p in puzzles if p.get("slug") == slug_filter]
    return puzzles


def update_manifest(puzzle, results_by_address):
    folder = puzzle.get("folder")
    if not folder:
        print(f"  (skip --update: {puzzle.get('slug')} has no folder, it is a row-only entry)")
        return
    manifest_path = os.path.join(REPO_ROOT, folder, "puzzle.json")
    if not os.path.isfile(manifest_path):
        print(f"  (skip --update: {manifest_path} not found)")
        return
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)
    today = date.today().isoformat()
    changed = False
    for addr_entry in manifest.get("addresses", []):
        address = addr_entry.get("address")
        if address in results_by_address:
            state, _detail = results_by_address[address]
            if state != "ERROR" and state != "SKIPPED":
                addr_entry["verified_on"] = today
                addr_entry["verified_state"] = state
                changed = True
    if changed:
        manifest["last_updated"] = today
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"  updated {manifest_path}")


def main():
    parser = argparse.ArgumentParser(description="Re-check puzzle escrows against the chain.")
    parser.add_argument("--slug", default=None, help="only check this puzzle slug")
    parser.add_argument("--update", action="store_true", help="write verified_on/verified_state back into the folder manifest")
    args = parser.parse_args()

    puzzles = load_puzzles(args.slug)
    if not puzzles:
        print("No puzzles found (0 manifests). Nothing to check.")
        sys.exit(0)

    header = f"{'slug':<45} {'label':<10} {'address':<44} {'expected':<20} {'observed':<16} {'verdict'}"
    print(header)
    print("-" * len(header))

    any_drift = False

    for puzzle in puzzles:
        slug = puzzle.get("slug", "")
        addresses = puzzle.get("addresses", [])
        results_by_address = {}
        for addr_entry in addresses:
            address = addr_entry.get("address", "")
            label = addr_entry.get("label", "")
            expected = addr_entry.get("expected", "")
            claimed_state = addr_entry.get("verified_state", "unknown")

            state, detail = check_address(addr_entry)
            results_by_address[address] = (state, detail)

            verdict = "OK"
            if state == "ERROR":
                verdict = "ERROR (network, not a verdict)"
            elif state == "SKIPPED":
                verdict = "SKIPPED"
            elif claimed_state == "funded-unspent" and state in ("swept", "unfunded"):
                verdict = f"DRIFT: manifest says funded-unspent, chain says {state}"
                any_drift = True
            elif claimed_state != state:
                verdict = f"NOTE: manifest says {claimed_state}, chain says {state}"

            print(f"{slug:<45} {label:<10} {address:<44} {expected:<20} {state:<16} {verdict}")
            if detail:
                print(f"  detail: {detail}")

        if args.update and addresses:
            update_manifest(puzzle, results_by_address)

    if any_drift:
        print("\nAt least one address that a manifest claims is funded-unspent is now swept or unfunded.")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
