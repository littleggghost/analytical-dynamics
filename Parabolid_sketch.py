import numpy as np
import pathlib
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

a = 1.5 # (m)
b = 2.0

g = 9.81

x = -10.0
y = 0.0
z = x**2 / a**2 + y**2 / b**2

X = np.array([[x, y, z]]).T

x_max = 10
y_max = 10
z_max = x_max**2 / a**2 + y_max**2 / b**2
z_max = np.ceil(z_max/10)*10

x_d = 0.0
y_d = 5.0
z_d = 0.0
X_d = np.array([[x_d, y_d, z_d]]).T

time = 0
dt = 0.001

f_e = np.array([[0.0, 0.0, -g]]).T

x_plot = []
y_plot = []
z_plot = []
t_plot = []

steps = 30000
for ix in range(steps):
    x_d = X_d[0]
    y_d = X_d[1]
    z_d = X_d[2]

    x = X[0][0]
    y = X[1][0]
    z = X[2][0]

    x_plot.append(x)   
    y_plot.append(y)
    z_plot.append(z)
    t_plot.append(time)

    # Solution to fundamental dynamics equation
    MP_A = (
        1 / (4 * x**2 / a**4 + 4 * y**2 / b**4 + 1) * 
        np.array([[2 * x / a**2, 2 * y / b**2, -1]]).T
    )
    X_dd = f_e + MP_A * (-(2 * x_d**2 / a**2 + 2 * y_d**2 / b**2) - g)
    
    # Euler integration
    time += dt
    X_d += dt * X_dd
    X += dt * X_d

Nx = 20
Ny = 20
xs = np.linspace(-10, 10, Nx)
ys = np.linspace(-10, 10, Ny)
zs = np.zeros((Ny, Nx))
for ix, x in enumerate(xs):
    for iy, y in enumerate(ys):
        zs[iy, ix] = x**2 / a**2 + y**2 / b**2
xs, ys = np.meshgrid(xs, ys)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d([-10.0, 10.0])
ax.set_xlabel('X')
ax.set_ylim3d([-10.0, 10.0])
ax.set_ylabel('Y')
ax.set_zlim3d([0.0, z_max])
ax.set_zlabel('Z')

surf1 = ax.plot_surface(X=xs, Y=ys, Z=zs)
lines = ax.plot_wireframe(X=xs, Y=ys, Z=zs)
surf1.set_facecolor((0.0, 0.0, 0.0, 0.1))

particle, = ax.plot([0.0], [0.0], [0.0], linestyle="", marker="o", color="#ff9400")

def animate(i, x_plot, y_plot, z_plot):
    particle.set_data(x_plot[i], y_plot[i])
    particle.set_3d_properties(z_plot[i])
    return particle

fps = 30
a_step = np.floor(1/fps/dt)
plot_ix = np.arange(0, steps, a_step).astype(int)
ix_range = plot_ix.shape[0]
x_plot = np.array(x_plot)[plot_ix]
y_plot = np.array(y_plot)[plot_ix]
z_plot = np.array(z_plot)[plot_ix]

ani = animation.FuncAnimation(fig, animate, ix_range,
                              interval=20, blit=False, fargs=(x_plot, y_plot, z_plot))

pathlib.Path('./Media').mkdir(parents=True, exist_ok=True) 
ani.save('./Media/ParabolidMovie.mp4', fps=fps)