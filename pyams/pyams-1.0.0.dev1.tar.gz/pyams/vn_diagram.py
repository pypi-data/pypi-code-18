"""
Python Aerospace Mechanic & Structures (PyAMS)

V-N Diagram Generator
"""

import numpy as np
import matplotlib.pyplot as plt

# Gust Alleviation Factor (Kg)
def calcGustAlleviationFactor_Kg(c, dCL_dalpha, rho, S, W):
    g = 9.81
    mu_g = 2*(W/g)/rho/S/c/dCL_dalpha
    Kg = 0.88*mu_g / (5.3+mu_g)
    return Kg

# Plot Gust Envelope
def plotDiagram_Gust(c, dCL_dalpha, S, W, rho, V_cruise, V_dive):
    x_cruise = np.linspace(0, V_cruise, 1000)
    x_dive = np.linspace(0, V_dive, 1000)

    # Gust Velocity (U) = 50 ft/sec
    U = 15.25
    rho = 1.225
    Kg = calcGustAlleviationFactor_Kg(c, dCL_dalpha, rho, S, W)
    n_pos_cruise = 1 + (Kg * (rho*U*S/W*dCL_dalpha/2) * x_cruise)
    n_neg_cruise = 1 - (Kg * (rho*U*S/W*dCL_dalpha/2) * x_cruise)
    print(Kg, U, dCL_dalpha, rho, S, 2, W/9.81, 9.81)
    print(Kg * (rho*U*S/W*dCL_dalpha/2))
    plt.plot(x_cruise, n_pos_cruise, 'g--')
    plt.plot(x_cruise, n_neg_cruise, 'g--')

    # Gust Velocity (U) = 25 ft/sec
    U = 7.5
    rho = 0.9
    Kg = calcGustAlleviationFactor_Kg(c, dCL_dalpha, rho, S, W)
    n_pos_dive = 1 + (Kg * (rho*U*S/W*dCL_dalpha/2) * x_dive)
    n_neg_dive = 1 - (Kg * (rho*U*S/W*dCL_dalpha/2) * x_dive)
    print(Kg, U, dCL_dalpha, rho, S, 2, W/9.81, 9.81)
    print(Kg * (rho*U*S/W*dCL_dalpha/2))
    plt.plot(x_dive, n_pos_dive, 'g--')
    plt.plot(x_dive, n_neg_dive, 'g--')

    # Gust Velocity (U) = 0 ft/sec
    plt.plot(np.linspace(0, V_dive*1.5, 1000), np.ones(1000), 'g--')

# Plot V-N Diagram
def plotDiagram_VN(V_stall_dirty, V_stall_clean, V_cruise, V_dive, V_flutter, n_p, n_n):
    # Plot Positive Stall Curve
    n = np.arange(0., n_p, 0.01)
    plt.plot(n**(1/2)*V_stall_clean, n, 'b')

    # Plot Positive Stall Curve (Flaps Down)
    n = np.arange(0., n_p, 0.01)
    plt.plot(n**(1/2)*V_stall_dirty, n, 'b--')

    # Plot Negative Stall Curve
    n = np.arange(0., n_n, -0.01)
    plt.plot((-n)**(1/2)*V_stall_clean, n, 'b')

    # Plot Max Line
    n = np.arange(n_p**(1/2)*V_stall_clean, V_dive, 0.01)
    plt.plot(n, np.ones(n.size)*n_p, 'b')

    # Plot Min Line
    n = np.arange((-n_n)**(1/2)*V_stall_clean, V_cruise, 0.01)
    plt.plot(n, np.ones(n.size)*n_n, 'b')

    # Plot Dive Line
    n = np.arange(0., n_p, 0.01)
    plt.plot(np.ones(n.size)*V_dive, n, 'b')

    # Plot Flutter Line
    n = np.arange(n_n, n_p, 0.01)
    plt.plot(np.ones(n.size)*V_flutter, n, 'b')

    # Plot Cruise-Dive Line
    x = np.linspace(V_cruise, V_dive, 1000)
    y = np.linspace(n_n, 0., 1000)
    plt.plot(x, y, 'b')

    # Legend & Axes Labels
    plt.title('V-N Diagram')
    plt.xlabel(r'Velocity, V $(kts)$')
    plt.ylabel('Load Factor, n')

    # # Set Axes Limits
    # axes = plt.gca()
    # axes.set_xlim([0, V_flutter*1.05])
    # axes.set_ylim([n_n-0.5, n_p+0.5])

    # Show Plot
    plt.grid()
    plt.show()

# Initiate Variables from User Input or Specs File
def initiateVar():
    # User Input : aircraft type
    try:
        aircraft_type = float(input("Enter Type of Aircraft < 1:normal / 2:utility / 3:acrobatic> (default=normal): "))
        if aircraft_type!=1 and aircraft_type!=2 and aircraft_type!=3:
            print('Error: Aircraft type is not valid!')
            quit()
    except ValueError:
        aircraft_type = 1
    # Positive Load Factor (n_p)
    if aircraft_type == 1:
        # User Input: weight of aircraft
        try:
            W = float(input("Enter Weight of Aircraft [lbs] (default = 2300lb): "))
        except ValueError:
            W = 2300*9.81
        n_p = 2.1 + (24000 / (W + 10000))
    elif aircraft_type == 2:
        n_p = 4.4
    elif aircraft_type == 3:
        n_p = 6.0
    # Negative Load Factor (n_n)
    if aircraft_type == 1:
        n_n = -1.52
    elif aircraft_type == 2:
        n_n = -1.80
    elif aircraft_type == 3:
        n_n = -3.00
    # Stall Velocity (V_stall)
    V_stall_dirty = 60                      # dummy value (units: mph)
    V_stall_clean = 60                      # dummy value (units: mph)
    # Cruise Velocity (V_cruise)
    V_cruise = 310                          # dummy value (units: mph)
    # Dive Velocity (V_dive)
    if aircraft_type == 1:
        V_dive = 1.40 * V_cruise
    elif aircraft_type == 2:
        V_dive = 1.50 * V_cruise
    elif aircraft_type == 3:
        V_dive = 1.55 * V_cruise
    # Flutter Velocity (V_flutter)
    V_flutter = 1.2 * V_dive
    return V_stall_dirty, V_stall_clean, V_cruise, V_dive, V_flutter, n_p, n_n

if __name__ == '__main__':
    # temp data
    c = 1.66                                # m
    dCL_dalpha = 6.3                        # 1/rad
    S = 19.33                               # m^2
    W = 2300*9.81                           # N
    rho = 1.225                             # N/m^3
    # temp data
    V_stall_dirty, V_stall_clean, V_cruise, V_dive, V_flutter, n_p, n_n = initiateVar()
    plotDiagram_Gust(c, dCL_dalpha, S, W, rho, V_cruise, V_dive)
    plotDiagram_VN(V_stall_dirty, V_stall_clean, V_cruise, V_dive, V_flutter, n_p, n_n)
    print(V_dive)
