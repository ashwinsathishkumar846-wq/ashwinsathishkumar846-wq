-- Self-check for FIFO8x9
library ieee; use ieee.std_logic_1164.all; use ieee.numeric_std.all; use ieee.math_real.all;
entity check_H2_tb is end;
architecture t of check_H2_tb is
  component FIFO8x9 port(clk: in std_logic; rst: in std_logic; RdPtrClr, WrPtrClr: in std_logic; rdinc, wrinc: in std_logic;
    DataIn: in std_logic_vector(8 downto 0); DataOut: out std_logic_vector(8 downto 0); rden, wren: in std_logic); end component;
  signal clk, rst, RdPtrClr, WrPtrClr, rdinc, wrinc, rden, wren : std_logic := '0';
  signal DataIn, DataOut : std_logic_vector(8 downto 0) := (others=>'0');
  signal done : boolean := false;
begin
  dut: FIFO8x9 port map(clk, rst, RdPtrClr, WrPtrClr, rdinc, wrinc, DataIn, DataOut, rden, wren);
  clk <= not clk after 10 ns when not done else clk;
  process
    type m is array(0 to 7) of std_logic_vector(8 downto 0);
    variable mem : m := (others => (others => 'U')); variable wp, rp : integer := 0; variable errs, n : integer := 0;
    variable seed1, seed2 : positive := 5; variable r : real; variable b : std_logic_vector(8 downto 0);
    variable e : std_logic_vector(8 downto 0);
    variable written : std_logic_vector(7 downto 0) := (others=>'0');
    procedure chk is begin
      wait for 2 ns; n := n+1;
      if rden = '1' then e := mem(rp); else e := (others => 'Z'); end if;
      if rden = '1' and written(rp) = '0' then null;  -- reading a never-written register: undefined, skip
      elsif DataOut /= e then errs := errs+1; report "MISMATCH rp=" & integer'image(rp) severity warning; end if;
    end;
    variable f : std_logic;
  begin
    -- clear both pointers
    WrPtrClr <= '1'; RdPtrClr <= '1'; wait until rising_edge(clk); wait for 1 ns; WrPtrClr <= '0'; RdPtrClr <= '0'; wp := 0; rp := 0;
    -- directed: write 8 words, read them back, check wrap-around and Z when rden=0
    for i in 0 to 7 loop
      DataIn <= std_logic_vector(to_unsigned(i*37+5, 9)); wren <= '1'; wrinc <= '1';
      wait until rising_edge(clk); mem(wp) := std_logic_vector(to_unsigned(i*37+5, 9)); written(wp) := '1'; wp := (wp+1) mod 8; wait for 1 ns;
    end loop;
    wren <= '0'; wrinc <= '0'; rden <= '0'; chk;
    rden <= '1';
    for i in 0 to 15 loop chk; rdinc <= '1'; wait until rising_edge(clk); rp := (rp+1) mod 8; wait for 1 ns; end loop;
    rdinc <= '0';
    -- randomised traffic
    for k in 1 to 6000 loop
      wait until falling_edge(clk);
      uniform(seed1,seed2,r); if r < 0.45 then wren <= '1'; else wren <= '0'; end if;
      uniform(seed1,seed2,r); if r < 0.45 then wrinc <= '1'; else wrinc <= '0'; end if;
      uniform(seed1,seed2,r); if r < 0.45 then rdinc <= '1'; else rdinc <= '0'; end if;
      uniform(seed1,seed2,r); if r < 0.05 then WrPtrClr <= '1'; else WrPtrClr <= '0'; end if;
      uniform(seed1,seed2,r); if r < 0.05 then RdPtrClr <= '1'; else RdPtrClr <= '0'; end if;
      uniform(seed1,seed2,r); if r < 0.60 then rden <= '1'; else rden <= '0'; end if;
      uniform(seed1,seed2,r); DataIn <= std_logic_vector(to_unsigned(integer(r*511.0), 9));
      chk;
      wait until rising_edge(clk);
      if wren = '1' then mem(wp) := DataIn; written(wp) := '1'; end if;
      if WrPtrClr = '1' then wp := 0; elsif wrinc = '1' then wp := (wp+1) mod 8; end if;
      if RdPtrClr = '1' then rp := 0; elsif rdinc = '1' then rp := (rp+1) mod 8; end if;
      wait for 2 ns; chk;
    end loop;
    -- asynchronous reset of the pointers
    wren <= '0'; wrinc <= '1'; rdinc <= '1'; wait until rising_edge(clk); wait until rising_edge(clk); wait for 1 ns;
    rst <= '1'; wait for 1 ns; wp := 0; rp := 0; wrinc <= '0'; rdinc <= '0'; rden <= '1'; chk; rst <= '0';
    report "H2 checks: " & integer'image(n) & "  errors: " & integer'image(errs);
    if errs = 0 then report "H2 PASS"; else report "H2 FAIL" severity failure; end if;
    done <= true; wait;
  end process;
end;
