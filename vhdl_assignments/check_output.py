#!/usr/bin/env python3
"""Sanity-check a myvectorh.out file BEFORE uploading it.
Usage:  python3 check_output.py AAC2M2P1/myvectorh.out AAC2M2P1/vectorh.out
It only checks that the file looks like something the course testbench wrote."""
import sys, re
out = open(sys.argv[1], 'rb').read().decode('latin1').replace('\r', '').split('\n')
out = [l for l in out if l != '']
print(f"lines: {len(out)}  (expected 256)")
bad = [i + 1 for i, l in enumerate(out) if not re.fullmatch(r'[0-9a-fA-F]{2}\s*', l)]
print("lines that are not 2 hex digits:", bad[:10] if bad else "none")
if len(sys.argv) > 2:
    ref = [l for l in open(sys.argv[2], 'rb').read().decode('latin1').replace('\r', '').split('\n') if l != '']
    same = sum(a.strip() == b.strip() for a, b in zip(out, ref))
    print(f"lines identical to the original vectorh.out: {same}/256")
    if same == 256: print("-> identical to the input file: the testbench probably did not run (or the design failed to compile).")
ok = len(out) == 256 and not bad and not (len(sys.argv) > 2 and same == 256)
print("Looks like a valid testbench output - OK to upload." if ok else "Do NOT upload yet - the file does not look right.")
