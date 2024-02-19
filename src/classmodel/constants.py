from dataclasses import dataclass


@dataclass(frozen=True)
class _Constants:
    # initialize constants
    Lv = 2.5e6  # heat of vaporization [J kg-1]
    cp = 1005.0  # specific heat of dry air [J kg-1 K-1]
    rho = 1.2  # density of air [kg m-3]
    k = 0.4  # Von Karman constant [-]
    g = 9.81  # gravity acceleration [m s-2]
    Rd = 287.0  # gas constant for dry air [J kg-1 K-1]
    Rv = 461.5  # gas constant for moist air [J kg-1 K-1]
    bolz = 5.67e-8  # Bolzman constant [-]
    rhow = 1000.0  # density of water [kg m-3]
    S0 = 1368.0  # solar constant [W m-2]


CONSTANTS = _Constants()
