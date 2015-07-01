% test ellipsoid fit
clear all
close all
% create the test data:
% radii
a = 2.8;
b = 3.2;
c = 3.7;
[ s, t ] = meshgrid( -pi/2 : 0.3 : pi/2, -pi : 0.3 : pi );
x = a * cos(s) .* cos( t );
y = b * cos(s) .* sin( t );
z = c * sin(s);
% rotation
ang = -pi/2;
xt = x * cos( ang ) - y * sin( ang );
yt = x * sin( ang ) + y * cos( ang );
% translation
shiftx = 4;
shifty = -3;
shiftz = 4;
x = xt + shiftx;
y = yt + shifty;
z = z  + shiftz;

% Bh IGRF, magnitude of magnetic field to fit to
Bh = 1; 

% add testing noise:
noiseIntensity = 0.05;
xold = x + randn( size( s ) ) * noiseIntensity;
yold = y + randn( size( s ) ) * noiseIntensity;
zold = z + randn( size( s ) ) * noiseIntensity;
x = xold(:);
y = yold(:);
z = zold(:);

% do the fitting
[ center, radii, evecs, v ] = ellipsoid_fit( [x y z ] );
fprintf( 'Ellipsoid center: %.3g %.3g %.3g\n', center );
fprintf( 'Ellipsoid radii : %.3g %.3g %.3g\n', radii );
fprintf( 'Ellipsoid evecs :\n' );
fprintf( '%.3g %.3g %.3g\n%.3g %.3g %.3g\n%.3g %.3g %.3g\n', ...
    evecs(1), evecs(2), evecs(3), evecs(4), evecs(5), evecs(6), evecs(7), evecs(8), evecs(9) );
fprintf( 'Algebraic form  :\n' );
fprintf( '%.3g ', v );
fprintf( '\n' );

% draw data
plot3( x, y, z, '.r' );
hold on;

%draw fit
maxd = max( [ a b c ] );
step = maxd / 50;
[ x_iso, y_iso, z_iso ] = meshgrid( -maxd:step:maxd + shiftx, -maxd:step:maxd + shifty, -maxd:step:maxd + shiftz );

Ellipsoid = v(1) *x_iso.*x_iso +   v(2) * y_iso.*y_iso + v(3) * z_iso.*z_iso + ...
          2*v(4) *x_iso.*y_iso + 2*v(5)*x_iso.*z_iso + 2*v(6) * y_iso.*z_iso + ...
          2*v(7) *x_iso    + 2*v(8)*y_iso    + 2*v(9) * z_iso;
p = patch( isosurface( x_iso, y_iso, z_iso, Ellipsoid, 1 ) );
set( p, 'FaceColor', 'g', 'EdgeColor', 'none' );
%view( -70, 40 );
%axis vis3d;
camlight;
lighting phong;
grid on


if(1)
% fix data 
% center
xf = x - ones(size(x)) * center(1);
yf = y - ones(size(y)) * center(2);
zf = z - ones(size(z)) * center(3);

% scale
xf = xf./(radii(2)) * Bh;
yf = yf./(radii(3)) * Bh;
zf = zf./(radii(1)) * Bh;

% Bx_a = (Bmx - x0)/a
% By_a = -(y0 - Bmy + (b*sin(rho)*(Bmx - x0))/a)/(b*cos(rho))
% Bz_a = (Bmz - z0 - (c*cos(lambda)*sin(phi)*(Bmx - x0))/a + (c*sin(lambda)*(y0 - Bmy + (b*sin(rho)*(Bmx - x0))/a))/(b*cos(rho)))/(c*cos(lambda)*cos(phi))

% draw fixed data
plot3( xf, yf, zf, '.c');

% draw comparison sphere
[xc, yc, zc] = sphere();
S1 = surf(Bh*xc, Bh*yc, Bh*zc);
set(S1,'FaceColor',[0.2 0.7 1],'FaceAlpha',0.4,'edgecolor','none');

axis equal;
end