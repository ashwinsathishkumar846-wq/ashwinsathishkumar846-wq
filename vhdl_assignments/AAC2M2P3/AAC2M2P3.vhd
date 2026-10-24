--------------------------------------------------------------------------------
-- AAC2M2P3 : Finite State Machine (entity FSM) - Moore machine, 3 states
--
--  State diagram from the assignment:
--
--     current | In1 = 0 | In1 = 1 | Out1
--     --------+---------+---------+------
--        A    |    A    |    B    |  0
--        B    |    C    |    B    |  0
--        C    |    C    |    A    |  1
--
--  * RST is ACTIVE HIGH and forces the machine into state A.
--  * Out1 depends only on the current state (Moore): '1' in state C, else '0'.
--  * State changes on the rising edge of CLK.
--------------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;

entity FSM is
port (In1: in std_logic;
   RST: in std_logic;
   CLK: in std_logic;
   Out1 : inout std_logic);
end FSM;

architecture RTL of FSM is
   type state_type is (A, B, C);
   signal state, next_state : state_type := A;
begin

   -- state register (asynchronous active-high reset)
   state_reg : process (CLK, RST)
   begin
      if RST = '1' then
         state <= A;
      elsif rising_edge(CLK) then
         state <= next_state;
      end if;
   end process;

   -- next-state logic
   next_logic : process (state, In1)
   begin
      case state is
         when A =>
            if In1 = '1' then next_state <= B; else next_state <= A; end if;
         when B =>
            if In1 = '0' then next_state <= C; else next_state <= B; end if;
         when C =>
            if In1 = '1' then next_state <= A; else next_state <= C; end if;
      end case;
   end process;

   -- output logic (Moore: depends on state only)
   Out1 <= '1' when state = C else '0';

end RTL;
