import numpy as np
import os

def adaptive_dt(dt, a, thresh):
	#dt_new =  dt / (10*grad)
	#if dt_new < dt:
	#	dt = dt_new
	#return dt
	
	return np.min(np.sqrt(np.abs(thresh / a)))
	
def make_dir(directory):
    """ Checks if the given directory exists and creates it if it does not exist

    Parameters
    ----------
    directory: str
        Name of the directory

    """
    if directory == "":
        return
    elif not os.path.exists(directory):
        os.makedirs(directory)
        

def write_results(i, t, x, v, energy, angmom, output):
    
    write_str = str(t) + ' ' + \
                            str(x[i, 0]) + ' ' + \
                            str(x[i, 1]) + ' ' + \
                            str(x[i, 2]) + ' ' + \
                            str(v[i, 0]) + ' ' + \
                            str(v[i, 1]) + ' ' + \
                            str(v[i, 2])
    if i == len(x)-1:
        write_str = write_str + ' ' + \
                                str(energy) + ' ' + \
                                str(angmom[0]) + ' ' + \
                                str(angmom[1]) + ' ' + \
                                str(angmom[2])

    output.write(write_str + '\n')
    