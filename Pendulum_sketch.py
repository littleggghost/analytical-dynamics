import numpy as np
import pathlib
import plotly.offline as py
import plotly.graph_objs as go

length = 1.5 # (m)
g = 9.81

theta = 0
x = length * np.cos(theta)
y = length * np.sin(theta)
X = np.array([[x, y]]).T

theta_d = 0
x_d = theta_d * length * -np.sin(theta)
y_d = theta_d * length * np.cos(theta)
X_d = np.array([[x_d, y_d]]).T

time = 0
dt = 0.0001

f_e = np.array([[0, g]]).T

x_plot = []
y_plot = []
t_plot = []
for ix in range(100000):
    x_d = X_d[0]
    y_d = X_d[1]
    x = X[0][0]
    y = X[1][0]

    x_plot.append(x)   
    y_plot.append(y) 
    t_plot.append(time)

    # Solution to fundamental dynamics equation
    X_dd = f_e - (np.power(x_d, 2) + np.power(y_d, 2) + g * y) / (np.power(x, 2) + np.power(y, 2)) * X
    
    # Euler integration
    time += dt
    X_d += dt * X_dd
    X += dt * X_d

t_plot = np.array(t_plot)
x_plot = np.array(x_plot)
y_plot = np.array(y_plot)
data_x = go.Scatter(x=t_plot, y=x_plot)
data_y = go.Scatter(x=t_plot, y=y_plot)
data = [data_x, data_y]

pathlib.Path('./Media').mkdir(parents=True, exist_ok=True) 
py.plot(data, filename='./Media/SinglePendulum.html')