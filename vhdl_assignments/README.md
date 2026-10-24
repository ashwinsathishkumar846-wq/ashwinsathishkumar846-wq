# Module 2 VHDL assignments — how to produce the files you upload

Coursera grades the file **`myvectorh.out`**, not the `.vhd`. That file is written by the
course's own (encrypted) testbench, so it can only be created by running that testbench in
ModelSim on your PC. Each folder here is ready for that.

## Fastest way: all five at once
In ModelSim: File > Change Directory > this folder, then `do run_all.do`. The five real outputs are copied to
`upload_ready/AAC2M2P1/myvectorh.out`, `upload_ready/AAC2M2P2/...`, `P3`, `H1`, `H2` - upload each to its own assignment.
(The scripts could not be tested inside ModelSim from my side; if one errors, send me the Transcript text.)

## Steps (repeat for each problem folder)

1. Open the folder (e.g. `AAC2M2P1`). It contains
   * `AAC2M2P1.vhd` — the finished design (my solution),
   * `AAC2M2P1_tb.vhdp` and `vectorh.out` — your original course files, unchanged,
   * `run_modelsim.do` — a one-click script.
2. In ModelSim: **File → Change Directory** → pick that folder, then type  
   `do run_modelsim.do`  in the Transcript window. (Or from a terminal inside the folder:
   `vsim -c -do run_modelsim.do`.)  
   Prefer a project? Create one whose source directory is this folder, add the `.vhd` and the
   `.vhdp`, compile (VHDL-2008), simulate `AAC2M2P1_tb`, and *Run -All*.
3. A new file **`myvectorh.out`** appears in the same folder (256 lines). Upload it on the
   assignment's **My submissions** tab. Rename nothing.
4. Do each problem in its own folder, otherwise a later run overwrites the earlier `myvectorh.out`.

## Which design is for which assignment

| Coursera assignment | Folder / file | What it is |
|---|---|---|
| VHDL 74LS163 Binary Counter | `AAC2M2P1/AAC2M2P1.vhd` | 4-bit sync counter: SR active-low sync reset, PE active-low sync load, CEP+CET count, TC = CET·(Q=1111) |
| VHDL Make a Memory | `AAC2M2P2/AAC2M2P2.vhd` | 128×32 single-port RAM, clocked write, unregistered (asynchronous) read |
| VHDL ALU | `AAC2M2H1/AAC2M2H1.vhd` | 32-bit ALU, 8 opcodes, combinational |
| VHDL FIFO | `AAC2M2H2/AAC2M2H2.vhd` | 8×9 FIFO, pointer clear/increment, tri-state output when rden = 0 |
| VHDL Finite State Machine | `AAC2M2P3/AAC2M2P3.vhd` | Moore FSM, states A/B/C: A→B on 1, B→C on 0, C→A on 1, others hold; Out1 = 1 only in C; RST active high → A |

## Most common reason for 0/10
The grader only accepts **`myvectorh.out`**. Uploading the `.vhd` file, or a `myvectorh.out` made by a run where the
code did not compile, gives 0/10. Check the file before uploading:

    python3 check_output.py AAC2M2P1/myvectorh.out AAC2M2P1/vectorh.out

It must have 256 lines, and must NOT be identical to `vectorh.out`. Also read the ModelSim Transcript: there must be
no `Error` lines after `vcom`, and the simulation must run to the end. If ModelSim is not installed, it comes free with
Quartus Prime Lite (select *ModelSim-Intel FPGA Starter Edition*) - see the Module 1 setup videos.

## If a problem scores below 7/10
* RAM: try `AAC2M2P2/fallback_only/AAC2M2P2_alt_registered_address.vhd` — copy it over
  `AAC2M2P2.vhd` (same entity name), re-run the script and re-upload.
* Counter: `AAC2M2P1/fallback_only/` treats PE as active HIGH instead of active low - only try it if a valid
  output of the main file scores 0. Otherwise, the first thing to re-read in the 74LS163 data sheet is the
  polarity of PE (the data sheet says active LOW) and that TC depends on CET.
* Make sure `vectorh.out` and the `.vhdp` in the folder are the originals, and that you uploaded the
  `myvectorh.out` that was produced *after* the last code change.

## What was verified
The course testbenches are encrypted, so I could not run them. I instead checked every design
with my own self-checking testbenches (in `selfcheck/`) in GHDL under both VHDL-93 and VHDL-2008:
counter 12 041 checks, RAM 4 129, ALU 5 288, FIFO 12 018 — all with 0 errors — and confirmed those
testbenches fail when I deliberately break each design.
