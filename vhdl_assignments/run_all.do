# ---------------------------------------------------------------------------
# Runs all five problems and collects the REAL outputs in  upload_ready/
# Usage: start ModelSim, File > Change Directory > pick THIS folder, then type
#        do run_all.do
#   (or from a terminal in this folder:  vsim -c -do "do run_all.do; quit -f")
# ---------------------------------------------------------------------------
set root [pwd]
file mkdir $root/upload_ready
foreach p {AAC2M2P1 AAC2M2P2 AAC2M2P3 AAC2M2H1 AAC2M2H2} {
    puts "===== $p ====="
    cd $root/$p
    quit -sim
    if {[file exists work]} { vdel -lib work -all }
    vlib work
    vmap work work
    vcom -2008 $p.vhd
    vcom -2008 ${p}_tb.vhdp
    vsim -voptargs=+acc work.${p}_tb
    run -all
    quit -sim
    if {[file exists myvectorh.out]} {
        file mkdir $root/upload_ready/$p
        file copy -force myvectorh.out $root/upload_ready/$p/myvectorh.out
        puts "  -> upload_ready/$p/myvectorh.out"
    } else {
        puts "  !! no myvectorh.out was produced for $p - read the errors above"
    }
}
cd $root
puts "Finished. Upload each file in upload_ready/<problem>/ to its matching assignment."
