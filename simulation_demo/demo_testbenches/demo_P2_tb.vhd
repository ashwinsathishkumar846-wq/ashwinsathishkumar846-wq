library ieee; use ieee.std_logic_1164.all; use ieee.numeric_std.all; use std.textio.all;
entity demo_P2_tb is end;
architecture t of demo_P2_tb is
  component RAM128_32 port(address: IN STD_LOGIC_VECTOR (6 DOWNTO 0); clock: IN STD_LOGIC := '1';
    data: IN STD_LOGIC_VECTOR (31 DOWNTO 0); wren: IN STD_LOGIC; q: OUT STD_LOGIC_VECTOR (31 DOWNTO 0)); end component;
  signal address : std_logic_vector(6 downto 0) := (others=>'0'); signal clock : std_logic := '0';
  signal data, q : std_logic_vector(31 downto 0) := (others=>'0'); signal wren : std_logic := '0';
  file f : text open write_mode is "P2.csv"; signal cyc : integer := 0;
begin
  dut: RAM128_32 port map(address, clock, data, wren, q);
  process
    variable l : line; variable n : integer := 0;
    procedure step(a : integer; d : std_logic_vector(31 downto 0); w : std_logic; note : string) is begin
      address <= std_logic_vector(to_unsigned(a,7)); data <= d; wren <= w; clock <= '0'; wait for 10 ns;
      clock <= '1'; wait for 2 ns; n := n+1; cyc <= n;
      write(l, integer'image(n) & "," & integer'image(a) & "," & to_hstring(d) & "," & std_logic'image(w)(2) & "," & to_hstring(q) & "," & note); writeline(f, l);
      wait for 8 ns;
    end;
  begin
    write(l, string'("cycle,address,data,wren,q,note")); writeline(f, l);
    for i in 0 to 7 loop step(i, std_logic_vector(unsigned'(x"A5000000") + to_unsigned(i*4369, 32)), '1', "write"); end loop;
    for i in 0 to 7 loop step(i, x"FFFFFFFF", '0', "read (data ignored; wren=0)"); end loop;
    step(3, x"CAFEF00D", '1', "overwrite address 3");
    step(3, x"12345678", '0', "read 3 (wren=0; memory unchanged)");
    step(5, x"00000000", '0', "read 5");
    step(120, x"DEADBEEF", '1', "write high address 120");
    step(120, x"00000000", '0', "read 120");
    wait;
  end process;
end;
