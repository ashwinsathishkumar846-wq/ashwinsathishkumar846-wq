library ieee; use ieee.std_logic_1164.all; use ieee.numeric_std.all; use ieee.math_real.all;
entity check_P3_tb is end;
architecture t of check_P3_tb is
  component FSM port (In1: in std_logic; RST: in std_logic; CLK: in std_logic; Out1 : inout std_logic); end component;
  signal In1, RST, CLK, Out1 : std_logic := '0'; signal done : boolean := false;
begin
  dut: FSM port map (In1, RST, CLK, Out1);
  CLK <= not CLK after 10 ns when not done else CLK;
  process
    variable st : integer := 0;  -- 0=A 1=B 2=C
    variable errs, n : integer := 0; variable seed1, seed2 : positive := 9; variable r : real;
    procedure chk is variable e : std_logic; begin
      if st = 2 then e := '1'; else e := '0'; end if; n := n+1;
      if Out1 /= e then errs := errs+1; report "MISMATCH state=" & integer'image(st) severity warning; end if; end;
  begin
    RST <= '1'; wait for 12 ns; st := 0; chk; wait until rising_edge(CLK); wait for 2 ns; chk; RST <= '0';
    for k in 1 to 6000 loop
      wait until falling_edge(CLK);
      uniform(seed1,seed2,r); if r < 0.5 then In1 <= '1'; else In1 <= '0'; end if;
      uniform(seed1,seed2,r); if r < 0.03 then RST <= '1'; else RST <= '0'; end if;
      wait for 1 ns;
      if RST = '1' then st := 0; chk; wait until rising_edge(CLK); wait for 2 ns; chk;
      else
        wait until rising_edge(CLK);
        case st is
          when 0 => if In1 = '1' then st := 1; end if;
          when 1 => if In1 = '0' then st := 2; end if;
          when others => if In1 = '1' then st := 0; end if;
        end case;
        wait for 2 ns; chk;
      end if;
    end loop;
    report "P3 checks: " & integer'image(n) & "  errors: " & integer'image(errs);
    if errs = 0 then report "P3 PASS"; else report "P3 FAIL" severity failure; end if; done <= true; wait;
  end process;
end;
