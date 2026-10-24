Self-check testbenches (my own, not the course's): each compares a design with an independent
reference model using thousands of random + corner-case vectors. Run with GHDL, e.g.
  ghdl -a --std=08 ../AAC2M2P1/AAC2M2P1.vhd check_P1_tb.vhd && ghdl -e --std=08 check_P1_tb && ghdl -r --std=08 check_P1_tb
They print "... PASS". They are NOT needed for submission.
