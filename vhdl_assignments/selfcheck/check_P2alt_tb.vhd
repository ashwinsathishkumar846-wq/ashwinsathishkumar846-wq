library ieee; use ieee.std_logic_1164.all; use ieee.numeric_std.all;
entity check_P2alt_tb is end;
architecture t of check_P2alt_tb is
  component RAM128_32 port(address: IN STD_LOGIC_VECTOR (6 DOWNTO 0); clock: IN STD_LOGIC := '1';
    data: IN STD_LOGIC_VECTOR (31 DOWNTO 0); wren: IN STD_LOGIC; q: OUT STD_LOGIC_VECTOR (31 DOWNTO 0)); end component;
  signal address : std_logic_vector(6 downto 0) := (others=>'0'); signal clock : std_logic := '0';
  signal data, q : std_logic_vector(31 downto 0) := (others=>'0'); signal wren : std_logic := '0';
begin
  dut: RAM128_32 port map(address, clock, data, wren, q);
  process
    variable errs : integer := 0; variable w : std_logic_vector(31 downto 0);
    procedure tick is begin clock <= '1'; wait for 10 ns; clock <= '0'; wait for 10 ns; end;
  begin
    for i in 0 to 127 loop address <= std_logic_vector(to_unsigned(i,7)); data <= std_logic_vector(to_unsigned(i*977+3,32)); wren <= '1'; wait for 5 ns; tick; end loop;
    wren <= '0';
    for i in 0 to 127 loop address <= std_logic_vector(to_unsigned(i,7)); wait for 5 ns; tick; wait for 1 ns;
      if q /= std_logic_vector(to_unsigned(i*977+3,32)) then errs := errs+1; end if; end loop;
    report "P2-alt errors: " & integer'image(errs); if errs = 0 then report "P2-alt PASS"; end if; wait;
  end process;
end;
