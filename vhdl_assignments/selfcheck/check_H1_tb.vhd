-- Self-check for ALU
library ieee; use ieee.std_logic_1164.all; use ieee.numeric_std.all; use ieee.math_real.all;
entity check_H1_tb is end;
architecture t of check_H1_tb is
  component ALU port(Op_code: in std_logic_vector(2 downto 0); A: in std_logic_vector(31 downto 0); B: in std_logic_vector(31 downto 0); Y: out std_logic_vector(31 downto 0)); end component;
  signal op : std_logic_vector(2 downto 0); signal A,B,Y : std_logic_vector(31 downto 0);
begin
  dut: ALU port map(op,A,B,Y);
  process
    variable seed1, seed2 : positive := 11; variable r : real; variable errs, n : integer := 0;
    variable ua, ub, e : unsigned(31 downto 0);
    type vec is array(0 to 5) of unsigned(31 downto 0);
    constant corner : vec := (x"00000000", x"00000001", x"7FFFFFFF", x"80000000", x"FFFFFFFF", x"AAAAAAAA");
    procedure test is begin
      wait for 5 ns; ua := unsigned(A); ub := unsigned(B);
      case op is
        when "000" => e := ua;
        when "001" => e := ua + ub;
        when "010" => e := ua - ub;
        when "011" => e := ua and ub;
        when "100" => e := ua or ub;
        when "101" => e := ua + 1;
        when "110" => e := ua - 1;
        when others => e := ub;
      end case;
      n := n+1; if unsigned(Y) /= e then errs := errs+1; report "MISMATCH op=" & integer'image(to_integer(unsigned(op))) severity warning; end if;
    end;
  begin
    for o in 0 to 7 loop for i in 0 to 5 loop for j in 0 to 5 loop
      op <= std_logic_vector(to_unsigned(o,3)); A <= std_logic_vector(corner(i)); B <= std_logic_vector(corner(j)); test; end loop; end loop; end loop;
    for k in 1 to 5000 loop
      uniform(seed1,seed2,r); op <= std_logic_vector(to_unsigned(integer(floor(r*7.999)),3));
      uniform(seed1,seed2,r); A(31 downto 16) <= std_logic_vector(to_unsigned(integer(r*65535.0),16));
      uniform(seed1,seed2,r); A(15 downto 0)  <= std_logic_vector(to_unsigned(integer(r*65535.0),16));
      uniform(seed1,seed2,r); B(31 downto 16) <= std_logic_vector(to_unsigned(integer(r*65535.0),16));
      uniform(seed1,seed2,r); B(15 downto 0)  <= std_logic_vector(to_unsigned(integer(r*65535.0),16)); test;
    end loop;
    report "H1 checks: " & integer'image(n) & "  errors: " & integer'image(errs);
    if errs = 0 then report "H1 PASS"; else report "H1 FAIL" severity failure; end if; wait;
  end process;
end;
