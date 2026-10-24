library ieee; use ieee.std_logic_1164.all; use ieee.numeric_std.all; use std.textio.all;
entity demo_H2_tb is end;
architecture t of demo_H2_tb is
  component FIFO8x9 port(clk: in std_logic; rst: in std_logic; RdPtrClr, WrPtrClr: in std_logic; rdinc, wrinc: in std_logic;
    DataIn: in std_logic_vector(8 downto 0); DataOut: out std_logic_vector(8 downto 0); rden, wren: in std_logic); end component;
  signal clk, rst, RdPtrClr, WrPtrClr, rdinc, wrinc, rden, wren : std_logic := '0';
  signal DataIn, DataOut : std_logic_vector(8 downto 0) := (others=>'0'); signal cyc : integer := 0;
  file f : text open write_mode is "H2.csv";
begin
  dut: FIFO8x9 port map(clk, rst, RdPtrClr, WrPtrClr, rdinc, wrinc, DataIn, DataOut, rden, wren);
  process
    variable l : line; variable n, wp, rp : integer := 0;
    function hx(v : std_logic_vector(8 downto 0)) return string is begin
      if v(0) = 'Z' then return "ZZZ"; else return to_hstring("000" & v)(1 to 3); end if; end;
    procedure step(wc, rc, wi, ri, we, re : std_logic; d : integer; note : string) is begin
      WrPtrClr <= wc; RdPtrClr <= rc; wrinc <= wi; rdinc <= ri; wren <= we; rden <= re; DataIn <= std_logic_vector(to_unsigned(d,9));
      clk <= '0'; wait for 10 ns; wait for 1 ns;
      -- DataOut before the edge shows the register under the read pointer (when rden=1)
      write(l, integer'image(n+1) & "," & std_logic'image(we)(2) & "," & std_logic'image(wi)(2) & "," & std_logic'image(re)(2) & "," & std_logic'image(ri)(2) & "," &
        std_logic'image(wc)(2) & std_logic'image(rc)(2) & "," & hx(std_logic_vector(to_unsigned(d,9))) & "," & hx(DataOut) & "," & integer'image(wp) & "," & integer'image(rp) & "," & note);
      writeline(f, l);
      clk <= '1'; wait for 2 ns; n := n+1; cyc <= n;
      if wc = '1' then wp := 0; elsif wi = '1' then wp := (wp+1) mod 8; end if;
      if rc = '1' then rp := 0; elsif ri = '1' then rp := (rp+1) mod 8; end if;
      wait for 7 ns;
    end;
  begin
    write(l, string'("cycle,wren,wrinc,rden,rdinc,clr(W R),DataIn,DataOut,wrptr,rdptr,note")); writeline(f, l);
    step('1','1','0','0','0','0',0,"clear both pointers");
    for i in 1 to 5 loop step('0','0','1','0','1','0', i*17, "write " & integer'image(i*17) & " and wrinc"); end loop;
    step('0','0','0','0','0','0',0,"rden=0 -> DataOut is Z");
    for i in 1 to 5 loop step('0','0','0','1','0','1',0,"read + rdinc"); end loop;
    for i in 6 to 9 loop step('0','0','1','0','1','0', i*17, "write " & integer'image(i*17) & " and wrinc"); end loop;
    step('0','1','0','0','0','1',0,"RdPtrClr (rdptr goes to 0 at the edge)");
    for i in 1 to 3 loop step('0','0','0','1','0','1',0,"read + rdinc"); end loop;
    step('0','0','0','0','0','0',0,"rden=0 -> Z");
    wait;
  end process;
end;
