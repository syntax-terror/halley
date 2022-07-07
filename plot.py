import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.axes3d import get_test_data
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')


class PlotSol:

    def __init__(self, datafile):
        """

        data_file : file with position-velocity-time data of the bodies
                        in the required format

        """

        t = []
        tt = []
        x = []
        v = []
        energy = []
        angmom = []
        with open(datafile) as data:
            for l, line in enumerate(data):
                if l == 0:
                    nbodies = int(line.split()[0])
                elif l == 1:
                    names = line.split()
                elif l == 2:
                    ms = [float(i) for i in line.split()]
                elif l == 3:
                    colors = line.split()
                else:
                    s = [float(i) for i in line.split()]
                    t.append(s[0])
                    x.append(s[1:4])
                    v.append(s[4:7])
                    if ((l - 3) % nbodies == 0):
                        tt.append(s[0])
                        energy.append(s[7])
                        angmom.append(np.dot(np.array(s[8:11]),
                                             np.array(s[8:11])))

        self.datafile = datafile

        self.nbodies = nbodies
        self.names = names
        self.ms = ms
        self.colors = colors

        self.x = np.array(x)
        self.v = np.array(v)
        self.t = np.array(t)
        self.tt = np.array(tt)
        self.energy = np.array(energy)
        self.angmom = np.array(angmom)
        self.xt = self.x.reshape((len(self.tt), nbodies, 3))
        self.vt = self.v.reshape((len(self.tt), nbodies, 3))

        self.colors = colors

    def animate(self, ffwd=1, xyzlim=None, save=False, plot_legend=True):
        """

        ffwd 	  : speed factor/fast-forward. Factor by which to speed the 
                                animation up by
        xyzlim	  : custom x,y,z limits for the animation. List must have 
                                shape (3,) or (3,2)
        """

        tconv = 58.13199
        
        def update_graph(i):
            # x,y,z of all bodies at current time
            data = self.xt[int(ffwd*i), :, :]
            tnow = self.tt[int(ffwd*i)]
            physt = round(tnow * tconv, 1)  # days
            k = 0
            for body, graph in zip(data, graphs):  # update graphs
                graph.set_data(body[0], body[1])
                graph.set_3d_properties(body[2])
                if plot_legend:
                    graph.set_label(self.names[k])
                    k += 1
            title.set_text('time = {} days'.format(physt))
            if plot_legend:
                plt.legend()
            return graphs, title

        plt.style.use('dark_background')
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        title = ax.set_title('')
        ax.set_xlabel('x (AU)')
        ax.set_ylabel('y (AU)')
        ax.set_zlabel('z (AU)')

        xyzlim = np.array(xyzlim)
        if np.shape(xyzlim) == (3,):
            o = np.ones((3, 2))
            for i in range(3):
                o[i] *= xyzlim[i]
                o[i, 0] *= -1
            xyzlim = o
        if np.any(xyzlim) == None or np.shape(xyzlim) != (3, 2):
            bound = 1.2 * np.amax(self.xt[0, :, :].flatten())

            plt.xlim(-bound, bound)
            plt.ylim(-bound, bound)
            ax.set_zlim(-bound, bound)
            if np.any(xyzlim) != None and np.shape(xyzlim) != (3, 2):
                print('Cannot recognize xyz limits. Needs to be of shape (3,) or (3,2)')
        else:
            plt.xlim(xyzlim[0, 0], xyzlim[0, 1])
            plt.ylim(xyzlim[1, 0], xyzlim[1, 1])
            ax.set_zlim(xyzlim[2, 0], xyzlim[2, 1])

        graphs = []
        if len(self.colors) < self.nbodies:
            for i in range(self.nbodies - len(self.colors)):
                self.colors.append('blue')
        if len(self.ms) < self.nbodies:
            for i in range(self.ms - len(self.colors)):
                self.ms.append(3)
        for n in range(self.nbodies):
            graphs.append(ax.plot([], [], [], linestyle="", marker=".",
                                  markersize=self.ms[n], color=self.colors[n])[0])

        ax.grid(False)
        ax.w_xaxis.pane.fill = False
        ax.w_yaxis.pane.fill = False
        ax.w_zaxis.pane.fill = False

        ani = animation.FuncAnimation(fig, func=update_graph, frames=int(len(self.tt)/(ffwd)),
                                      interval=20, blit=False, repeat=True)
        
        plt.show()
        plt.close()
        if save:
            self.save_animation(ani)

        return ani

    def plot_curves(self, outdir, ncols=3):

        energy_frac = (self.energy - self.energy[0]) / self.energy[0]
        angmom_frac = (self.angmom - self.angmom[0]) / self.angmom[0]

        print("Max energy fractional error:", np.amax(energy_frac))
        
        plt.style.use('default')
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(211)
        ax1.plot(self.tt, energy_frac)
        ax1.set_xlabel('t')
        ax1.set_ylabel('$\\Delta E/E$')

        ax2 = fig1.add_subplot(212)
        ax2.plot(self.tt, angmom_frac)
        ax2.set_xlabel('t')
        ax2.set_ylabel('$\\Delta L/L$')

        plt.savefig(outdir + '/energy_angmom_curves.png', dpi=300)
        plt.close()
        
        nrows = int(np.ceil(self.nbodies / ncols))
        fig2, axes = plt.subplots(nrows=nrows, ncols=ncols)
        axes = axes.flatten()
        for i in range(self.nbodies):
            speed = []
            vt_i = self.vt[:, i, :]
            for vj in vt_i:
                speed.append(np.dot(vj, vj))
            speed = np.array(speed)
            axes[i].plot(self.tt, speed)
            if i >= self.nbodies - ncols:
                axes[i].set_xlabel('t')
            if i % ncols == 0:
                axes[i].set_ylabel('speed')
            axes[i].set_title(self.names[i])
        
        plt.tight_layout()
        plt.savefig(outdir + '/velocity_curves.png', dpi=300)
        plt.close()

        return

    def save_animation(self, ani, backend, outdir):
        """
        backend: ffmpeg for .mp4 or imagemagick for .gif
        """

        print("\nSaving animation. This may take a moment...")
        if backend == "ffmpeg":
            br = 1800
            ext = '.mp4'
        elif backend == "imagemagick":
            br = 800
            ext = '.gif'
        else:
            print("Backend not recognized.")
            return
        Writer = animation.writers[backend]
        writer = Writer(fps=24, bitrate=br)
        ani.save('{0}/animation{1}'.format(outdir, ext), writer=writer)
