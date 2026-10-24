--------------------------------------------------------------------------------
-- AAC2M2H1 : simple 32-bit ALU (entity ALU)
--
--   Op_code | Operation | Function
--   --------+-----------+---------------
--    000    | Y <= A    | pass A
--    001    | Y <= A+B  | add
--    010    | Y <= A-B  | subtract
--    011    | Y <= A AND B
--    100    | Y <= A OR  B
--    101    | Y <= A+1  | increment A
--    110    | Y <= A-1  | decrement A
--    111    | Y <= B    | pass B
--
--   Purely combinational: Y changes whenever Op_code, A or B change.
--   Arithmetic wraps around modulo 2**32.
--------------------------------------------------------------------------------
LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

ENTITY ALU IS
PORT( Op_code : IN STD_LOGIC_VECTOR( 2 DOWNTO 0 );
A, B : IN STD_LOGIC_VECTOR( 31 DOWNTO 0 );
Y : OUT STD_LOGIC_VECTOR( 31 DOWNTO 0 ) );
END ALU;

ARCHITECTURE RTL OF ALU IS
BEGIN
   PROCESS (Op_code, A, B)
   BEGIN
      CASE Op_code IS
         WHEN "000"  => Y <= A;                                                  -- A
         WHEN "001"  => Y <= STD_LOGIC_VECTOR(UNSIGNED(A) + UNSIGNED(B));        -- add
         WHEN "010"  => Y <= STD_LOGIC_VECTOR(UNSIGNED(A) - UNSIGNED(B));        -- subtract
         WHEN "011"  => Y <= A AND B;                                            -- AND
         WHEN "100"  => Y <= A OR B;                                             -- OR
         WHEN "101"  => Y <= STD_LOGIC_VECTOR(UNSIGNED(A) + 1);                  -- increment A
         WHEN "110"  => Y <= STD_LOGIC_VECTOR(UNSIGNED(A) - 1);                  -- decrement A
         WHEN "111"  => Y <= B;                                                  -- B
         WHEN OTHERS => Y <= (OTHERS => '0');                                    -- unused codes
      END CASE;
   END PROCESS;
END RTL;
