library ieee; use ieee.std_logic_1164.all; use ieee.numeric_std.all; use std.textio.all;
entity demo_H1_tb is end;
architecture t of demo_H1_tb is
  component ALU port(Op_code: in std_logic_vector(2 downto 0); A: in std_logic_vector(31 downto 0); B: in std_logic_vector(31 downto 0); Y: out std_logic_vector(31 downto 0)); end component;
  signal op : std_logic_vector(2 downto 0) := "000"; signal A,B,Y : std_logic_vector(31 downto 0) := (others=>'0');
  file f : text open write_mode is "H1.csv"; signal cyc : integer := 0;
begin
  dut: ALU port map(op,A,B,Y);
  process
    variable l : line; variable n : integer := 0;
    procedure t(o : integer; av, bv : std_logic_vector(31 downto 0); note : string) is begin
      op <= std_logic_vector(to_unsigned(o,3)); A <= av; B <= bv; wait for 10 ns; n := n+1; cyc <= n;
      write(l, integer'image(n) & "," & integer'image(o) & "," & to_hstring(av) & "," & to_hstring(bv) & "," & to_hstring(Y) & "," & note); writeline(f, l);
    end;
  begin
    write(l, string'("test,opcode,A,B,Y,note")); writeline(f, l);
    for o in 0 to 7 loop t(o, x"00000064", x"00000019", "A=100 and B=25"); end loop;
    t(1, x"FFFFFFFF", x"00000001", "add wraps to 0");
    t(2, x"00000000", x"00000001", "subtract wraps to FFFFFFFF");
    t(5, x"FFFFFFFF", x"00000000", "increment wraps to 0");
    t(6, x"00000000", x"00000000", "decrement wraps to FFFFFFFF");
    t(3, x"F0F0F0F0", x"0FF0FF00", "AND of bit patterns");
    t(4, x"F0F0F0F0", x"0FF0FF00", "OR of bit patterns");
    wait;
  end process;
end;
