close;
clear;

% Generate Measurements
size = 200;
t = linspace(0,2*pi,size);
theta0 = pi/9;
x0_e = -3;
y0_e = -1.8;
a_e = 1.4;
b_e = 1;
noise = 0.05;

x = a_e*sin(t) + x0_e;
y = b_e*cos(t+theta0) + y0_e;

% Add noise
xn = x + noise * 2 * (rand(1, length(x))-.5);
yn = y + noise * 2 * (rand(1, length(y))-.5);

% standard ellipse for fixed data

x_nice = sin(t);
y_nice = cos(t);

% Basis function Matrix
X_mat = [   xn.^2 ./yn.^2;   (xn.*yn) ./yn.^2;
            xn    ./yn.^2;   yn       ./yn.^2;
            1     ./yn.^2;
]';

% Least Square Estimate
P = -1 * inv(X_mat'*X_mat)*X_mat'*ones(1,size)';




syms Bh Bx By Bmx Bmy a b rho y0 x0

% Get constant field magnitude
%Bh = mean(sqrt( x.^2 + y.^2))
%Bh = mean(sqrt((x(1) - x0_e).^2 + (y-y0_e).^2))
Bh = 1

[a_solve, b_solve, rho_solve, x0_solve, y0_solve] = ...
            solve( [    b^2/a^2 == P(1), 
            (-2*sin(rho)*a*b )/a^2== P(2),
            (2*sin(rho)*a*b*y0 - 2*b^2*x0 ) /a^2 == P(3),
            (2*sin(rho)*a*b*x0 - 2*a^2*y0 ) /a^2 == P(4),
            (a^2*y0^2 + b^2*x0^2 - 2*sin(rho)*a*b*x0*y0)/a^2 ...
            + b^2*(sin(rho)^2 - 1)*Bh^2 == P(5)
        ]);
    
a_cor = double(a_solve(1)) 
b_cor = double(b_solve(1))
x0_cor = double(x0_solve(1))
y0_cor = double(y0_solve(1))
rho_cor = double(rho_solve(1))


% Fix the measured data with the correction factors

x_fixed = (xn - x0_cor) / a_cor;
y_fixed = -(y0_cor - yn + (b_cor*sin(rho_cor)*(xn - x0_cor))/a_cor)/ ...
        (b_cor*cos(rho_cor)); 


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
h1 = plot(xn, yn, 'b.')
plot(x0_e, y0_e, 'r+')
text(x0_e + 0.01*x0_e, y0_e + 0.05*y0_e, ['(' num2str(x0_e) ', ' num2str(y0_e) ')']);

% plot fixed
plot(x_nice, y_nice, 'g-', 'LineWidth', 3)
h2 = plot(x_fixed, y_fixed, 'm.')
plot(0, 0, 'r+')
text(0.01, 0.05, ['(0, 0)']);

%legend
%%
set(gca, 'Xlim', [-5 2], 'Ylim', [-3 2]);
%set(gca, 'linewidth', 1);
%set(get(gca, 'children'), 'linewidth', 1.5);

%%
hLegend = legend( ...
    [h1 h2], {'Measured data', 'Corrected data' }, ...
    'location', 'NorthWest', 'box', 'off');
hTitle = title('Two Dimensional Correction Simulation');
hXLabel = xlabel('x-Axis Magnitude' , 'fontsize', 16);
hYLabel = ylabel('y-Axis Magnitude', 'fontsize', 16);

%% Ultra fancy stuff

set( gca                       , ...
    'FontName'   , 'Helvetica' );
set([hXLabel, hYLabel], ...
    'FontName'   , 'Dejavu Sans');
set( gca             , ...
    'FontSize'   , 14         );

set( hLegend             , ...
    'FontSize'   , 26 ,...
    'FontName'   , 'Dejavu Sans');
set([hXLabel, hYLabel]  , ...
    'FontSize'   , 18          );
set( hTitle                    , ...
    'FontSize'   , 16         , ...
    'FontName'   , 'Dejavu Sans', ...
    'FontWeight' , 'bold'      );

set(gca, ...
  'Box'         , 'off'     , ...
  'TickDir'     , 'out'     , ...
  'TickLength'  , [.02 .02] , ...
  'XMinorTick'  , 'on'      , ...
  'YMinorTick'  , 'on'      , ...
  'YGrid'       , 'on'      , ...
  'XColor'      , [.3 .3 .3], ...
  'YColor'      , [.3 .3 .3], ...
  'YTick'       , -4:1:2, ...
  'LineWidth'   , 1         );

% enlarge marker size in plot legend
marksize=30;
s=get(legend);
s1=s.Children;
s2=[];

s2=findobj(s1,{'type','patch','-or','type','line'});

for m=1:length(s2)
    set(s2(m),'markersize',marksize);
end

%axis equal
hold off

