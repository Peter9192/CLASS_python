import numpy as np

from classmodel.constants import CONSTANTS


class Radiation:
    def __init__(self, config):
        """Copy fixed parameters from config."""
        self.lat = config.lat  # latitude [deg]
        self.lon = config.lon  # longitude [deg]
        self.doy = config.doy  # day of the year [-]
        self.tstart = config.tstart  # time of the day [-]
        self.cc = config.cc  # cloud cover fraction [-]
        self.Q0 = config.Q0  # net radiation [W m-2]

    def initialize(self):
        """Initialize state variables."""
        self.Q = self.Q0
        self.Swin = None  # incoming short wave radiation [W m-2]
        self.Swout = None  # outgoing short wave radiation [W m-2]
        self.Lwin = None  # incoming long wave radiation [W m-2]
        self.Lwout = None  # outgoing long wave radiation [W m-2]
        self.run_radiation()

    def run_radiation(self, t, dt, theta, Ps, h, alpha, Ts):
        """Update state variables."""
        sda = 0.409 * np.cos(2.0 * np.pi * (self.doy - 173.0) / 365.0)
        sinlea = np.sin(2.0 * np.pi * self.lat / 360.0) * np.sin(sda) - np.cos(2.0 * np.pi * self.lat / 360.0) * np.cos(
            sda
        ) * np.cos(2.0 * np.pi * (t * dt + self.tstart * 3600.0) / 86400.0 + 2.0 * np.pi * self.lon / 360.0)
        sinlea = max(sinlea, 0.0001)

        Ta = theta * ((Ps - 0.1 * h * CONSTANTS.rho * CONSTANTS.g) / Ps) ** (CONSTANTS.Rd / CONSTANTS.cp)

        Tr = (0.6 + 0.2 * sinlea) * (1.0 - 0.4 * self.cc)

        self.Swin = CONSTANTS.S0 * Tr * sinlea
        self.Swout = alpha * CONSTANTS.S0 * Tr * sinlea
        self.Lwin = 0.8 * CONSTANTS.bolz * Ta**4.0
        self.Lwout = CONSTANTS.bolz * Ts**4.0

        self.Q = self.Swin - self.Swout + self.Lwin - self.Lwout
