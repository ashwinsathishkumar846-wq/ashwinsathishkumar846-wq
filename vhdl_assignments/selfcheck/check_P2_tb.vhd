-- Self-check for RAM128_32 (single-port RAM, unregistered output)
library ieee; use ieee.std_logic_1164.all; use ieee.numeric_std.all; use ieee.math_real.all;
entity check_P2_tb is end;
architecture t of check_P2_tb is
  component RAM128_32 port(address: IN STD_LOGIC_VECTOR (6 DOWNTO 0); clock: IN STD_LOGIC := '1';
    data: IN STD_LOGIC_VECTOR (31 DOWNTO 0); wren: IN STD_LOGIC; q: OUT STD_LOGIC_VECTOR (31 DOWNTO 0)); end component;
  signal address : std_logic_vector(6 downto 0) := (others=>'0'); signal clock : std_logic := '0';
  signal data, q : std_logic_vector(31 downto 0) := (others=>'0'); signal wren : std_logic := '0';
  type m is array(0 to 127) of std_logic_vector(31 downto 0);
begin
  dut: RAM128_32 port map(address, clock, data, wren, q);
  process
    variable ref : m; variable errs, n : integer := 0; variable seed1, seed2 : positive := 3; variable r : real;
    variable w : std_logic_vector(31 downto 0); variable a : integer;
    procedure tick is begin clock <= '1'; wait for 10 ns; clock <= '0'; wait for 10 ns; end;
    procedure chk(ad: integer) is begin n := n+1;
      if q /= ref(ad) then errs := errs+1; report "MISMATCH addr " & integer'image(ad) severity warning; end if; end;
  begin
    -- write every address, then read all back (no clock needed for the read)
    for i in 0 to 127 loop
      address <= std_logic_vector(to_unsigned(i,7));
      w := std_logic_vector(to_unsigned(i*16777259 + 12345, 32)); ref(i) := w; data <= w; wren <= '1'; wait for 5 ns; tick;
    end loop;
    wren <= '0';
    for i in 0 to 127 loop address <= std_logic_vector(to_unsigned(i,7)); wait for 1 ns; chk(i); end loop;
    -- random writes / reads
    for k in 1 to 4000 loop
      uniform(seed1,seed2,r); a := integer(floor(r*127.999)); address <= std_logic_vector(to_unsigned(a,7));
      uniform(seed1,seed2,r); w := std_logic_vector(to_unsigned(integer(r*2147483000.0),32)); data <= w;
      uniform(seed1,seed2,r);
      if r < 0.5 then wren <= '1'; wait for 4 ns; tick; ref(a) := w; else wren <= '0'; wait for 4 ns; tick; end if;
      wait for 1 ns; chk(a);
    end loop;
    -- wren low must never change memory even if data toggles
    wren <= '0'; address <= "0000101"; data <= x"DEADBEEF"; wait for 2 ns; tick; wait for 1 ns; chk(5);
    report "P2 checks: " & integer'image(n) & "  errors: " & integer'image(errs);
    if errs = 0 then report "P2 PASS"; else report "P2 FAIL" severity failure; end if; wait;
  end process;
end;
