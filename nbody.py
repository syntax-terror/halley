import numpy as np
from physics import get_acc, get_energy, get_angmom, propagate
from utils import adaptive_dt, make_dir, write_results
import pandas as pd
from progress.bar import IncrementalBar
from plot import PlotSol
from matplotlib.colors import is_color_like

"""
Units chosen such that 

G = 1
M = 1 = 1 Msun
t = 1 = 5.0226e6 s = 58d 3h 10m 3.88s 
v = 1 = Vearth ~ 30 km/s

"""

class Nbody:
    
    def __init__(self, params_file):
        
        self.params_file = params_file
    
    def integrate(self, animate=True, ffwd=1, ncols=3, outdir='outdir',
                  verbose=True):

        params = open(self.params_file, 'r')
        
        mu = []
        x = []
        v = []
        names = []
        ms = []
        colors = []
        for l, line in enumerate(params):
            s_ = line.split()
            s = [float(i) for i in s_[:7]]
            if l == 0:
                dt, tmax = s[0], s[1]
            else:
                mu.append(s[0])
                x.append(s[1:4])
                v.append(s[4:7])
                if len(s_) > 7:
                    opts = s_[7:]
                    inds = []
                    
                    col_bools = [(not x.replace('.','',1).isdigit() and is_color_like(x)) for x in opts]
                    col_inds = [i for i, x in enumerate(col_bools) if x]
                    if len(col_inds) > 1:
                        print('Too many colors entered for body {0}!'.format(l))
                    elif len(col_inds) != 0:
                        colors.append(opts[col_inds[0]])
                        inds.append(col_inds[0])
                    else:
                        colors.append('blue')
                        
                    ms_bools = [x.replace('.','',1).isdigit() for x in opts]
                    ms_inds = [i for i, x in enumerate(ms_bools) if x]
                    if len(ms_inds) > 1:
                        print('Too many marker sizes entered for body {0}!'.format(l))
                    elif len(ms_inds) != 0:
                        ms.append(float(opts[ms_inds[0]]))
                        inds.append(ms_inds[0])
                    else:
                        ms.append(2)
                    
                    for i in range(0, len(opts)):
                        if i not in inds:
                            names.append(opts[i])
                            
                    if len(names) != l:
                        names.append('body{0}'.format(str(l)))
                        
        mu = np.array(mu)
        x = np.array(x)
        v = np.array(v)
        
        nbodies = len(x)
        
        a = []
        energy_prev = 0
        for i in range(len(x)):  # initial acceleration
            ai = get_acc(i, mu, x)
            a.append(ai)
            energyi = get_energy(i, mu, x, v)
            energy_prev += energyi
        a = np.array(a)
        
        nsteps = int(tmax / dt)
        
        make_dir(outdir)
        outfile = outdir + '/integration_results.dat'
        output = open(outfile, 'w+')
        names_str = ''
        color_str = ''
        ms_str = ''
        for i in range(len(names)):
            names_str += str(names[i]) + ' '
        for i in range(len(ms)):
            ms_str += str(ms[i]) + ' '
        for i in range(len(colors)):
            color_str += colors[i] + ' '
        output.write(str(nbodies) + '\n' + names_str + '\n' + ms_str + '\n' \
                     + color_str + '\n')
        
        dti = dt
        time = 0
        time_prev = time
        n = 1
        with IncrementalBar('Integrating', max=nsteps) as bar:
            while time < (tmax - dt):
                time += dt
                energy = 0
                angmom = np.zeros(3)
                for i in range(nbodies):
                    x[i], v[i], a[i] = propagate(i, mu, x, v, a, dt)
                    energyi = get_energy(i, mu, x, v)
                    energy += energyi
                    angmomi = get_angmom(i, mu, x, v)
                    angmom += angmomi
                    write_results(i, time, x, v, energy, angmom, output)
                #energy_grad = np.abs((energy - energy_prev) / dti)
                #dt = adaptive_dt(dt, a, thresh=1e-8)
                # if n < 100:
                #print(dt, energy_grad)
                energy_prev = energy
                if n == 1:
                    energy_init = energy
                    angmom_init = angmom
                n += 1
        
                if (time - time_prev) > dti:
                    time_prev += dti
                    bar.next()
                    
        if verbose:
            labels = [['x', 'y', 'z'], ['v_x', 'v_y', 'v_z']]
        
            print('\nEphemerides at t =', time, '\n')
        
            df_x = pd.DataFrame(x, range(len(x)), labels[0])
            df_v = pd.DataFrame(x, range(len(x)), labels[1])
            print(df_x, '\n')
            print(df_v)
        
            print('\nEnergy =                 ', energy)
            print('Energy change =          ', energy - energy_init,
                  '(' + str(round(abs((energy - energy_init)/energy_init), 5)*100) + '%)')
            angmom_diff = angmom - angmom_init
            angmom_diff_frac = abs(angmom_diff / angmom_init) * 100
            print('\nAngular momentum =       ', angmom[0], angmom[1], angmom[2])
            print('Angular momentum change =',
                  angmom_diff[0], angmom_diff[1], angmom_diff[2])
            print('                         ',
                  angmom_diff_frac[0], angmom_diff_frac[1], angmom_diff_frac[2], '%')

        print(' Saving results...')
        output.close()        
        plotter = PlotSol(outfile)
        
        plotter.plot_curves(outdir, ncols)
            
        if animate:
            ani = plotter.animate(ffwd=ffwd, xyzlim=None, save=False)
            opt = 'f'
            while opt == 'f' or opt == 'l':
                opt = input(" Change speed factor, change x,y,z limits, save to file, or exit [f/l/s/e]: ")
                if opt == 'f':
                    ffwd = float(input(" Enter new speed factor: "))
                    ani = plotter.animate(ffwd=ffwd, xyzlim=None, save=False)
                if opt == 'l':
                    limits = input(" Enter new x,y,z limits (comma separated): ")
                    limits = [float(x) for x in limits.split(',')]
                    ani = plotter.animate(ffwd=ffwd, xyzlim=limits, save=False)
            if opt == 's':
                backend = input(" Choose backend. ffmpeg for .mp4 or imagemagick for .gif: ")
                plotter.save_animation(ani, backend, outdir)
        else:
            return
            
            
            
            
            
            
            
            
