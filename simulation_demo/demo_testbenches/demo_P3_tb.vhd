library ieee; use ieee.std_logic_1164.all; use std.textio.all;
entity demo_P3_tb is end;
architecture t of demo_P3_tb is
  component FSM port (In1: in std_logic; RST: in std_logic; CLK: in std_logic; Out1 : inout std_logic); end component;
  signal In1, RST, CLK, Out1 : std_logic := '0'; signal cyc : integer := 0;
  file f : text open write_mode is "P3.csv";
begin
  dut: FSM port map (In1, RST, CLK, Out1);
  process
    variable l : line; variable n, st : integer := 0;  -- 0=A 1=B 2=C
    procedure step(r, i : std_logic; note : string) is begin
      RST <= r; In1 <= i; CLK <= '0'; wait for 10 ns;
      if r = '1' then null; end if;
      CLK <= '1'; wait for 2 ns; n := n+1; cyc <= n;
      if r = '1' then st := 0; else
        case st is when 0 => if i='1' then st:=1; end if; when 1 => if i='0' then st:=2; end if; when others => if i='1' then st:=0; end if; end case;
      end if;
      write(l, integer'image(n) & "," & std_logic'image(r)(2) & "," & std_logic'image(i)(2) & "," & integer'image(st) & "," & std_logic'image(Out1)(2) & "," & note); writeline(f, l);
      wait for 8 ns;
    end;
  begin
    write(l, string'("cycle,RST,In1,state,Out1,note")); writeline(f, l);
    step('1','0',"reset -> A"); step('1','1',"reset -> A");
    step('0','0',"A stays A (In1=0)"); step('0','1',"A -> B"); step('0','1',"B stays B (In1=1)"); step('0','1',"B stays B");
    step('0','0',"B -> C"); step('0','0',"C stays C (Out1=1)"); step('0','0',"C stays C"); step('0','1',"C -> A");
    step('0','0',"A stays A"); step('0','1',"A -> B"); step('0','0',"B -> C"); step('0','1',"C -> A");
    step('0','1',"A -> B"); step('0','0',"B -> C"); step('1','0',"RST while in C -> A"); step('0','0',"A stays A");
    wait;
  end process;
end;
