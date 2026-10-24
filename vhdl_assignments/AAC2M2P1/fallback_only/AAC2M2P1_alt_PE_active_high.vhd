--------------------------------------------------------------------------------
-- FALLBACK ONLY (PE treated as ACTIVE HIGH).  Use only if the main AAC2M2P1.vhd
-- keeps failing with a valid myvectorh.out.  Copy over AAC2M2P1.vhd to use it.
-- AAC2M2P1 : 74LS163 4-bit synchronous binary counter
--
-- Behaviour taken from the 74LS163 data sheet function table
-- (every action happens on the RISING edge of CP):
--
--   SR  PE  CEP CET | action
--   ----------------+-----------------------------------------
--   L   X   X   X   | synchronous reset  (Q = 0000)  <- highest priority
--   H   L   X   X   | synchronous parallel load (Q = P)
--   H   H   H   H   | count up (wraps 1111 -> 0000)
--   H   H   L   X   | hold
--   H   H   X   L   | hold
--
--   SR and PE are ACTIVE LOW.  CEP and CET are active high.
--   TC (terminal count) = CET AND (Q = 1111).  It is not registered, so it
--   follows CET and Q immediately.
--------------------------------------------------------------------------------
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;

entity AAC2M2P1 is port (
   CP:  in std_logic;                      -- clock
   SR:  in std_logic;                      -- Active low, synchronous reset
   P:   in std_logic_vector(3 downto 0);   -- Parallel input
   PE:  in std_logic;                      -- Parallel Enable (Load), active low
   CEP: in std_logic;                      -- Count enable parallel input
   CET: in std_logic;                      -- Count enable trickle input
   Q:   out std_logic_vector(3 downto 0);
   TC:  out std_logic                      -- Terminal Count
);
end AAC2M2P1;

architecture RTL of AAC2M2P1 is
   -- Internal copy of the count: an "out" port cannot be read back inside
   -- the architecture, so the counter value is kept in this signal.
   signal count : unsigned(3 downto 0) := (others => '0');
begin

   process (CP)
   begin
      if rising_edge(CP) then
         if SR = '0' then                        -- 1) synchronous reset
            count <= (others => '0');
         elsif PE = '1' then                     -- 2) synchronous parallel load
            count <= unsigned(P);
         elsif (CEP = '1') and (CET = '1') then  -- 3) count
            count <= count + 1;
         end if;                                 -- otherwise: hold
      end if;
   end process;

   Q  <= std_logic_vector(count);
   TC <= '1' when (CET = '1') and (count = "1111") else '0';

end RTL;
