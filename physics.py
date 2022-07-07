import numpy as np

def get_acc(i, mu, x):

	# acceleration on body i
	acc = 0
	for j, xj in enumerate(x):
		if j != i:
			r = x[i] - x[j]
			rmag = np.sqrt(np.dot(r, r))
			acc += -mu[j] * r / rmag**3
	return acc
	
def get_energy(i, mu, x, v):

	# energy of body i
	
	vsq = np.dot(v[i], v[i])
	kinetic = 0.5 * mu[i] * vsq
	potential = 0
	for j, xj in enumerate(x):
		if j != i:
			r = x[i] - x[j]
			rmag = np.sqrt(np.dot(r, r))
			potential -= mu[j] / rmag
	potential *= mu[i]
	return kinetic + potential
 
def get_angmom(i, mu, x, v):
	
	# angular momentum of body
	
  	return mu[i] * np.cross(x[i], v[i])
  	
def propagate(i, mu, x, v, a, dt, method='leapfrog'):
	
	# evolve body i forward by a timestep
	
	if method == 'leapfrog':
		c = [0, 1]
		d = [0.5, 0.5]
	if method == 'ruth3':
		c = [1, -2/3, 2/3]
		d = [-1/24, 3/4, 7/24]
	if method == 'ruth4':
		c = [1/(2*(2-2**(1/3))),(1-2**(1/3))/(2*(2-2**(1/3))),
			 (1-2**(1/3))/(2*(2-2**(1/3))),1/(2*(2-2**(1/3)))]
		d = [1/(2-2**(1/3)),-2**(1/3)/(2-2**(1/3)),1/(2-2**(1/3)),0]
	
	vi = v[i]
	xi = x[i]
	ai = a[i]
	
	for j in range(len(c)):
		xi = xi + c[j] * dt * vi
		x[i] = xi
		ai = get_acc(i, mu, x)
		vi = vi + d[j] * dt * ai
	
	return xi, vi, ai
	
