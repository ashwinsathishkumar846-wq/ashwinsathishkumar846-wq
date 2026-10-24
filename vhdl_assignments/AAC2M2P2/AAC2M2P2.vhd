--------------------------------------------------------------------------------
-- AAC2M2P2 : 128 x 32 single-port RAM  (entity RAM128_32)
--
--   * synchronous write : when wren = '1' the word 'data' is stored at
--                         'address' on the rising edge of 'clock'
--   * asynchronous read : q always shows the word stored at 'address'
--                         (the output is NOT registered, as the assignment asks)
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
	-- 128 words, each 32 bits wide
	TYPE ram_type IS ARRAY (0 TO 127) OF STD_LOGIC_VECTOR (31 DOWNTO 0);
	SIGNAL ram : ram_type;
BEGIN

	-- write port (clocked)
	PROCESS (clock)
	BEGIN
		IF rising_edge(clock) THEN
			IF wren = '1' THEN
				ram(to_integer(unsigned(address))) <= data;
			END IF;
		END IF;
	END PROCESS;

	-- read port (not registered)
	q <= ram(to_integer(unsigned(address)));

END RTL;
