# ---------------------------------------------------------------------------
# Generates myvectorh.out for AAC2M2H1  (the file you upload to Coursera).
# Run from inside THIS folder:
#     vsim -c -do run_modelsim.do          (command line)
#   or in the ModelSim GUI: File > Change Directory (pick this folder),
#     then type   do run_modelsim.do   in the Transcript window.
# ---------------------------------------------------------------------------
quit -sim
if {[file exists work]} { vdel -lib work -all }
vlib work
vmap work work
vcom -2008 AAC2M2H1.vhd
vcom -2008 AAC2M2H1_tb.vhdp
vsim -voptargs=+acc work.AAC2M2H1_tb
run -all
puts "Done. Upload the file myvectorh.out from this folder."
quit -f
