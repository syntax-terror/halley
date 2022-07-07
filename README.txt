This is an N-body dynamical integrator that uses the leapfrog method for propagation of positions and velocities.

The code takes in an input file specified at run time with the following format:

	TIME STEP		INTEGRATION TIME
	MASS 1			X POSITION  Y POSITION  Z POSITION		X VELOCITY  Y VELOCITY  Z VELOCITY		MARKER SIZE		COLOR
	.
	.
	.
	MASS N			X POSITION  Y POSITION  Z POSITION		X VELOCITY  Y VELOCITY  Z VELOCITY		MARKER SIZE		COLOR

The mass is in units of solar masses, the initial positions are in units of AU, and the initial velocities are in units of mean Earth velocities (~30 km/s).

The marker size and color parameters are for plotting customization purposes.

The amount of whitespace is unimportant, just make sure to put the quantities in the correct order.

If you specify an output file, this will be in the following format

	MARKER SIZE 1  MARKER SIZE 2  ...
	COLOR 1        COLOR 2        ...
	1 * TIME STEP  X POSITION 1  Y POSITION 1  Z POSITION 1		X VELOCITY 1  Y VELOCITY 1  Z VELOCITY 1
	.
	.
	.
	1 * TIME STEP  X POSITION N  Y POSITION N  Z POSITION N		X VELOCITY N  Y VELOCITY N  Z VELOCITY N	   TOTAL ENERGY		X TOTAL ANGULAR MOMENTUM  Y TOTAL ANGULAR MOMENTUM  Z TOTAL ANGULAR MOMENTUM
	2 * TIME STEP  X POSITION 1  Y POSITION 1  Z POSITION 1		X VELOCITY 1  Y VELOCITY 1  Z VELOCITY 1
	.
	.
	.

This can be read in at any time by the plotting function in plot.py, which displays a 3D interactive plot of the system.
