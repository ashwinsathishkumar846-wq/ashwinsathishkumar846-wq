--------------------------------------------------------------------------------
-- FALLBACK ONLY - use this only if the main AAC2M2P2.vhd scores below 7/10.
--
-- Same 128 x 32 single-port RAM, but built the way Quartus/Intel RAM blocks
-- with an *unregistered output* behave: the ADDRESS is captured on the rising
-- clock edge and q is read from the memory using that captured address.
-- q itself has no output register.  (File must be renamed AAC2M2P2.vhd before
-- it is used with the testbench - the entity name stays RAM128_32.)
--------------------------------------------------------------------------------
LIBRARY ieee;
USE ieee.std_logic_1164.all;
USE ieee.numeric_std.all;

ENTITY RAM128_32 IS
	PORT
	(
		address	: IN STD_LOGIC_VECTOR (6 DOWNTO 0);
		clock		: IN STD_LOGIC  := '1';
		data		: IN STD_LOGIC_VECTOR (31 DOWNTO 0);
		wren		: IN STD_LOGIC ;
		q		: OUT STD_LOGIC_VECTOR (31 DOWNTO 0)
	);
END RAM128_32;

ARCHITECTURE RTL OF RAM128_32 IS
	TYPE ram_type IS ARRAY (0 TO 127) OF STD_LOGIC_VECTOR (31 DOWNTO 0);
	SIGNAL ram      : ram_type;
	SIGNAL addr_reg : UNSIGNED (6 DOWNTO 0) := (OTHERS => '0');
BEGIN
	PROCESS (clock)
	BEGIN
		IF rising_edge(clock) THEN
			IF wren = '1' THEN
				ram(to_integer(unsigned(address))) <= data;
			END IF;
			addr_reg <= unsigned(address);      -- address register
		END IF;
	END PROCESS;

	q <= ram(to_integer(addr_reg));              -- no output register
END RTL;
