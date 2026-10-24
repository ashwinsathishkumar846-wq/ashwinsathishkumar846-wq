--------------------------------------------------------------------------------
-- AAC2M2H2 : 8-deep x 9-bit FIFO memory (entity FIFO8x9)
--
--   * 8 registers of 9 bits.
--   * Write: on the rising edge of clk, when wren = '1', DataIn is stored in
--            the register that the write pointer points to.
--   * WrInc : increments the write pointer (wraps 7 -> 0) on the clock edge.
--   * RdInc : increments the read pointer  (wraps 7 -> 0) on the clock edge.
--   * WrPtrClr / RdPtrClr : set the write / read pointer back to register 0
--            (they win over WrInc / RdInc).
--   * rst  : asynchronous reset of both pointers.
--   * Read : the register that the read pointer points to is placed on
--            DataOut when rden = '1'; otherwise DataOut is high impedance 'Z'.
--   * No full / empty flags (as the assignment says).
--------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity FIFO8x9 is
   port(
      clk, rst:		in std_logic;
      RdPtrClr, WrPtrClr:	in std_logic;
      RdInc, WrInc:	in std_logic;
      DataIn:	 in std_logic_vector(8 downto 0);
      DataOut: out std_logic_vector(8 downto 0);
      rden, wren: in std_logic
	);
end entity FIFO8x9;

architecture RTL of FIFO8x9 is
	--signal declarations
	type fifo_array is array(7 downto 0) of std_logic_vector(8 downto 0);  -- makes use of VHDL’s enumerated type
	signal fifo:  fifo_array;
	signal wrptr, rdptr: unsigned(2 downto 0) := (others => '0');
	signal en: std_logic_vector(7 downto 0);
	signal dmuxout: std_logic_vector(8 downto 0);

begin

   ---------------------------------------------------------------------------
   -- Write pointer
   ---------------------------------------------------------------------------
   wr_pointer : process (clk, rst)
   begin
      if rst = '1' then
         wrptr <= (others => '0');
      elsif rising_edge(clk) then
         if WrPtrClr = '1' then
            wrptr <= (others => '0');
         elsif WrInc = '1' then
            wrptr <= wrptr + 1;
         end if;
      end if;
   end process;

   ---------------------------------------------------------------------------
   -- Read pointer
   ---------------------------------------------------------------------------
   rd_pointer : process (clk, rst)
   begin
      if rst = '1' then
         rdptr <= (others => '0');
      elsif rising_edge(clk) then
         if RdPtrClr = '1' then
            rdptr <= (others => '0');
         elsif RdInc = '1' then
            rdptr <= rdptr + 1;
         end if;
      end if;
   end process;

   ---------------------------------------------------------------------------
   -- Write-pointer decoder: one-hot enable for the register being written
   ---------------------------------------------------------------------------
   decoder : process (wrptr, wren)
   begin
      en <= (others => '0');
      if wren = '1' then
         en(to_integer(wrptr)) <= '1';
      end if;
   end process;

   ---------------------------------------------------------------------------
   -- The 8 x 9-bit register array
   ---------------------------------------------------------------------------
   registers : process (clk)
   begin
      if rising_edge(clk) then
         for i in 0 to 7 loop
            if en(i) = '1' then
               fifo(i) <= DataIn;
            end if;
         end loop;
      end if;
   end process;

   ---------------------------------------------------------------------------
   -- Read multiplexer (selected by the read pointer) and tri-state output
   ---------------------------------------------------------------------------
   dmuxout <= fifo(to_integer(rdptr));
   DataOut <= dmuxout when rden = '1' else (others => 'Z');

end architecture RTL;
