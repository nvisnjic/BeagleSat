close;
clear;

% Generate Measurements
size = 200;
t = linspace(0,2*pi,size);
theta0 = pi/9;
x0_e = -3;
y0_e = -2.8;
a_e = 5.3;
b_e = 2;
noise = 0.05;
Bh = 2  % IGRF expected mag. field magnitude
        % Change to force a specificl magnitude fit


x = a_e*sin(t) + x0_e;
y = b_e*cos(t+theta0) + y0_e;

% Add noise
xn = x + noise * 2 * (rand(1, length(x))-.5);
yn = y + noise * 2 * (rand(1, length(y))-.5);


% Compute Bh field expected magnitude if not set
if( Bh == 0)
    Bh = mean(sqrt( ((xn-x0_e)).^2 + ((yn -y0_e)).^2 ) )
end

% Basis function Matrix
X_mat = [   xn.^2 ./yn.^2;   (xn.*yn) ./yn.^2;
            xn    ./yn.^2;   yn       ./yn.^2;
            1     ./yn.^2;
]';
% Least Square Estimate
P = -1 * inv(X_mat'*X_mat)*X_mat'*ones(1,size)';


% Get constant field magnitude
%Bh = mean(sqrt( x.^2 + y.^2))
%Bh = mean(sqrt((x(1) - x0_e).^2 + (y-y0_e).^2))

% Used in MATLAB to solve, but we can use symbolic solution direclty
if(0)
    syms Bh_2 Bx By Bmx Bmy a b rho y0 x0
    %Bh = mean(sqrt( (xn-x0_e).^2 + (yn -y0_e).^2 ) )
    [a_solve, b_solve, rho_solve, x0_solve, y0_solve] = ...
                solve( [    b^2/a^2 == P(1), 
                (-2*sin(rho)*a*b )/a^2== P(2),
                (2*sin(rho)*a*b*y0 - 2*b^2*x0 ) /a^2 == P(3),
                (2*sin(rho)*a*b*x0 - 2*a^2*y0 ) /a^2 == P(4),
                (a^2*y0^2 + b^2*x0^2 - 2*sin(rho)*a*b*x0*y0)/a^2 ...
                + b^2*(sin(rho)^2 - 1)*Bh_2 == P(5)
            ],'Real', true);
end

% Direct solutions:

AC = P(1); BC = P(2); DC = P(3); EC = P(4); FC = P(5);

if(1)
a_cor = double( -1 * (2*(AC*(FC*BC^2 - BC*DC*EC + DC^2 + AC*EC^2 ...
                    - 4*AC*FC))^(1/2)*(1/AC)^(1/2))/(Bh*BC^2 - 4*AC*Bh) ) 
b_cor = double( -1 * (2*(AC*(FC*BC^2 - BC*DC*EC + DC^2 + AC*EC^2 ...
                    - 4*AC*FC))^(1/2))/(Bh*BC^2 - 4*AC*Bh) )
x0_cor = double(  -(2*DC - BC*EC)/(- BC^2 + 4*AC) )
y0_cor = double( -(2*AC*EC - BC*DC)/(- BC^2 + 4*AC) )
rho_cor = double(pi + asin((BC*(1/AC)^(1/2))/2) )
end


% Fix the measured data with the correction factors

x_fixed = (xn - x0_cor) / a_cor;
y_fixed = -(y0_cor - yn + (b_cor*sin(rho_cor)*(xn - x0_cor))/a_cor)/ ...
        (b_cor*cos(rho_cor)); 


% standard ellipse for fixed data

x_nice = Bh*sin(t);
y_nice = Bh*cos(t);

    
    
    
% Compute percent error
factor_error_percent = abs([a_e - a_cor, b_e - b_cor, x0_e - x0_cor, ...
            y0_e - y0_cor, ... % angle shannanigans 
            theta0 - mod(rho_cor, pi) ]) * 100
    
% Print all the good stuff


figure
hold on
grid on
% plot measured
plot(x, y, 'g-', 'LineWidth', 3)
h1 = plot(xn, yn, 'b.');
plot(x0_e, y0_e, 'r+')
text(x0_e + 0.01*x0_e, y0_e + 0.05*y0_e, ['(' num2str(x0_e) ', ' num2str(y0_e) ')']);

% plot fixed
plot(x_nice, y_nice, 'g-', 'LineWidth', 3)
h2 = plot(x_fixed, y_fixed, 'm.');
plot(0, 0, 'r+')
text(0.01, 0.05, ['(0, 0)']);

axis equal
hold off

