library ieee; use ieee.std_logic_1164.all; use ieee.numeric_std.all; use std.textio.all;
entity demo_P1_tb is end;
architecture t of demo_P1_tb is
  component AAC2M2P1 port (CP: in std_logic; SR: in std_logic; P: in std_logic_vector(3 downto 0); PE: in std_logic;
    CEP: in std_logic; CET: in std_logic; Q: out std_logic_vector(3 downto 0); TC: out std_logic); end component;
  signal CP,SR,PE,CEP,CET,TC : std_logic := '0'; signal P,Q : std_logic_vector(3 downto 0) := "0000";
  file f : text open write_mode is "P1.csv"; signal cyc : integer := 0;
begin
  dut: AAC2M2P1 port map (CP,SR,P,PE,CEP,CET,Q,TC);
  process
    variable l : line; variable n : integer := 0;
    procedure step(s,pe0,cep0,cet0 : std_logic; pv : std_logic_vector(3 downto 0); note : string) is begin
      SR <= s; PE <= pe0; CEP <= cep0; CET <= cet0; P <= pv; CP <= '0'; wait for 10 ns;
      CP <= '1'; wait for 2 ns; n := n+1; cyc <= n;
      write(l, integer'image(n) & "," & std_logic'image(s)(2) & "," & std_logic'image(pe0)(2) & "," & std_logic'image(cep0)(2) & "," & std_logic'image(cet0)(2) & "," &
        to_hstring(pv) & "," & to_hstring(Q) & "," & std_logic'image(TC)(2) & "," & note); writeline(f, l);
      wait for 8 ns;
    end;
  begin
    write(l, string'("cycle,SR,PE,CEP,CET,P,Q,TC,note")); writeline(f, l);
    for i in 1 to 2 loop step('0','1','0','0',"0000","reset"); end loop;
    for i in 1 to 18 loop step('1','1','1','1',"0000","count up"); end loop;
    for i in 1 to 3 loop step('1','1','0','1',"0000","hold (CEP=0)"); end loop;
    for i in 1 to 2 loop step('1','1','1','0',"0000","hold (CET=0)"); end loop;
    step('1','0','1','1',"1010","parallel load 1010");
    for i in 1 to 7 loop step('1','1','1','1',"0000","count up"); end loop;
    step('1','0','1','1',"1111","load 1111 (TC=1)");
    for i in 1 to 2 loop step('1','1','1','1',"0000","count: wraps to 0"); end loop;
    step('0','0','1','1',"0101","SR=0 wins over load");
    step('1','1','1','1',"0000","count up");
    wait;
  end process;
end;
