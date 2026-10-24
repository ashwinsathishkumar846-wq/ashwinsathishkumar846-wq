-- Self-check for AAC2M2P1 (74LS163).  Reference model written from the data-sheet function table.
library ieee; use ieee.std_logic_1164.all; use ieee.numeric_std.all; use ieee.math_real.all;
entity check_P1_tb is end;
architecture t of check_P1_tb is
  component AAC2M2P1 port (CP: in std_logic; SR: in std_logic; P: in std_logic_vector(3 downto 0); PE: in std_logic;
    CEP: in std_logic; CET: in std_logic; Q: out std_logic_vector(3 downto 0); TC: out std_logic); end component;
  signal CP,SR,PE,CEP,CET,TC : std_logic := '0'; signal P,Q : std_logic_vector(3 downto 0) := "0000";
  signal done : boolean := false;
begin
  dut: AAC2M2P1 port map (CP,SR,P,PE,CEP,CET,Q,TC);
  CP <= not CP after 10 ns when not done else CP;
  process
    variable ref : integer := 0; variable errs, n : integer := 0;
    variable seed1, seed2 : positive := 7;
    variable r : real;
    procedure rnd(variable b : out std_logic; bias : real) is begin uniform(seed1,seed2,r); if r < bias then b := '1'; else b := '0'; end if; end;
    variable v : std_logic; variable pv : integer;
    procedure chk is
      variable exp_tc : std_logic;
    begin
      if ref = 15 and CET = '1' then exp_tc := '1'; else exp_tc := '0'; end if;
      n := n + 1;
      if to_integer(unsigned(Q)) /= ref or TC /= exp_tc then
        errs := errs + 1;
        report "MISMATCH t=" & time'image(now) & " Q=" & integer'image(to_integer(unsigned(Q))) & " ref=" & integer'image(ref) &
               " TC=" & std_logic'image(TC) & " expTC=" & std_logic'image(exp_tc) severity warning;
      end if;
    end;
  begin
    -- first reset
    SR <= '0'; PE <= '1'; CEP <= '0'; CET <= '0'; P <= "0000"; wait until rising_edge(CP); wait for 5 ns; ref := 0; chk;
    for i in 1 to 6000 loop
      -- change inputs just after the falling edge, sample just after the rising edge
      wait until falling_edge(CP);
      rnd(v, 0.15); SR <= not v;           -- SR low about 15 % of the time ... (v=1 -> SR=0)
      rnd(v, 0.25); PE <= not v;           -- PE low about 25 %
      rnd(v, 0.80); CEP <= v;
      rnd(v, 0.85); CET <= v;
      uniform(seed1,seed2,r); pv := integer(floor(r*15.999)); P <= std_logic_vector(to_unsigned(pv,4));
      wait for 1 ns; chk;                 -- TC check before the edge (combinational with CET)
      wait until rising_edge(CP);
      if SR = '0' then ref := 0;
      elsif PE = '0' then ref := pv;
      elsif CEP = '1' and CET = '1' then ref := (ref + 1) mod 16; end if;
      wait for 2 ns; chk;
    end loop;
    -- long uninterrupted count to prove wrap-around
    SR <= '1'; PE <= '1'; CEP <= '1'; CET <= '1';
    for i in 1 to 40 loop wait until rising_edge(CP); ref := (ref+1) mod 16; wait for 2 ns; chk; end loop;
    report "P1 checks: " & integer'image(n) & "  errors: " & integer'image(errs);
    if errs = 0 then report "P1 PASS"; else report "P1 FAIL" severity failure; end if;
    done <= true; wait;
  end process;
end;
