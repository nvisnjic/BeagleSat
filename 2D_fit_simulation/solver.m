
clear
syms Bh Bx By Bmx Bmy a b rho y0 x0
Bx_a = solve(Bmx == x0 + Bx*a, Bx)
By_a = solve(Bmy == b*(By*cos(rho) + Bx*sin(rho)) + y0, By)
By_a = subs( By_a, Bx, Bx_a)

Bh = Bx_a^2 + By_a^2

rewrite(simplify(expand(Bh)), 'cos')
pretty(rewrite(simplify(expand(Bh)), 'cos'))

pretty(simplify(expand(Bh)))
collec = collect(simplify(simplify(expand(Bh))), [Bmx Bmy] )
[param_matrix, CFS ]= coeffs(collec, [Bmx Bmy])

% equation to solve
param_matrix.' ./param_matrix(4)

if(0)
clear
syms Bh_2 Bx By Bmx Bmy a b rho y0 x0
syms AC BC DC EC FC % -1*(P1 P2 P3 P4 P5)

[a_solve, b_solve, rho_solve, x0_solve, y0_solve] = ...
            solve( [    b^2/a^2 == AC, 
            (-2*sin(rho)*a*b )/a^2== BC,
            (2*sin(rho)*a*b*y0 - 2*b^2*x0 ) /a^2 == DC,
            (2*sin(rho)*a*b*x0 - 2*a^2*y0 ) /a^2 == EC,
            (a^2*y0^2 + b^2*x0^2 - 2*sin(rho)*a*b*x0*y0)/a^2 ...
            + b^2*(sin(rho)^2 - 1)*Bh_2 == FC
        ])
end

