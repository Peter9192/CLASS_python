"""CLASS.

Copyright (c) 2010-2015 Meteorology and Air Quality section, Wageningen University and Research centre
Copyright (c) 2011-2015 Jordi Vila-Guerau de Arellano
Copyright (c) 2011-2015 Chiel van Heerwaarden
Copyright (c) 2011-2015 Bart van Stratum
Copyright (c) 2011-2015 Kees van den Dries

This file is part of CLASS

CLASS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CLASS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CLASS.  If not, see <http://www.gnu.org/licenses/>.
"""

import copy as cp

import numpy as np
import pandas as pd

from classmodel import constants


def esat(T):
    return 0.611e3 * np.exp(17.2694 * (T - 273.16) / (T - 35.86))


def qsat(T, p):
    return 0.622 * esat(T) / p


class Model:
    def __init__(self, model_input):
        """Ïnitialize the different components of the model."""
        self.input = cp.deepcopy(model_input)

    def run(self):
        """Run model from start to finish."""
        # initialize model variables
        self.init()

        # time integrate model
        for t in range(self.tsteps):
            self.t = t
            # time integrate components
            self.timestep()

    def init(self):
        """Assign variables from input data."""
        # Read switches
        self.sw_ml = self.input.sw_ml  # mixed-layer model switch
        self.sw_shearwe = self.input.sw_shearwe  # shear growth ABL switch
        self.sw_fixft = self.input.sw_fixft  # Fix the free-troposphere switch
        self.sw_sl = self.input.sw_sl  # surface layer switch

        # State variables (they are initialized/updated prognostically)
        self.h = self.input.h  # initial ABL height [m]
        self.theta = self.input.theta  # initial mixed-layer potential temperature [K]
        self.dtheta = self.input.dtheta  # initial temperature jump at h [K]
        self.dz_h = self.input.dz_h  # Transition layer thickness [-]
        self.q = self.input.q  # initial mixed-layer specific humidity [kg kg-1]
        self.dq = self.input.dq  # initial specific humidity jump at h [kg kg-1]
        self.CO2 = self.input.CO2  # initial mixed-layer CO2 [ppm]
        self.dCO2 = self.input.dCO2  # initial CO2 jump at h [ppm]

        # Computed properties (they are set diagnostically)?
        self.ws = None  # large-scale vertical velocity [m s-1]
        self.wf = None  # mixed-layer growth due to radiative divergence [m s-1]
        self.we = -1.0  # entrainment velocity [m s-1]
        self.wthetae = None  # entrainment kinematic heat flux [K m s-1]
        self.thetav = None  # initial mixed-layer potential temperature [K]
        self.wstar = 0.0  # convective velocity scale [m s-1]
        self.P_h = None  # Mixed-layer top pressure [pa]
        self.T_h = None  # Mixed-layer top absolute temperature [K]
        self.RH_h = None  # Mixed-layer top relavtive humidity [-]
        self.lcl = None  # Lifting condensation level [m]  # PK: may want to cache it
        self.dthetav = None  # initial virtual temperature jump at h [K]
        self.wthetav = None  # surface kinematic virtual heat flux [K m s-1]
        self.wthetave = None  # entrainment kinematic virtual heat flux [K m s-1]
        self.wCO2e = None  # entrainment CO2 flux [ppm m s-1]
        self.wqe = None  # entrainment moisture flux [kg kg-1 m s-1]
        # Tendencies
        self.htend = None  # tendency of CBL [m s-1]
        self.thetatend = None  # tendency of mixed-layer potential temperature [K s-1]
        self.dthetatend = None  # tendency of potential temperature jump at h [K s-1]
        self.qtend = None  # tendency of mixed-layer specific humidity [kg kg-1 s-1]
        self.dqtend = None  # tendency of specific humidity jump at h [kg kg-1 s-1]
        self.CO2tend = None  # tendency of CO2 humidity [ppm]
        self.dCO2tend = None  # tendency of CO2 jump at h [ppm s-1]
        self.dztend = None  # tendency of transition layer thickness [m s-1]
        self.uw = None  # surface momentum flux in u-direction [m2 s-2]
        self.vw = None  # surface momentum flux in v-direction [m2 s-2]

        # Constants
        self.ac = 0.0  # Cloud core fraction [-]
        self.M = 0.0  # Cloud core mass flux [m s-1]
        self.wqM = 0.0  # Cloud core moisture flux [kg kg-1 m s-1]
        self.wCO2M = 0  # CO2 mass flux [ppm m s-1]

        # initialize time variables
        self.tsteps = int(np.floor(self.input.runtime / self.input.dt))
        self.dt = self.input.dt
        self.t = 0

        # initialize output
        self.out = pd.DataFrame(columns=self.OUTPUT_VAR_NAMES, index=np.arange(self.tsteps), dtype=float)

        self.statistics()

        if self.sw_ml:
            self.run_mixed_layer()

    def timestep(self):
        self.statistics()

        # run mixed-layer model
        if self.sw_ml:
            self.run_mixed_layer()

        # store output before time integration
        self.store()

        # time integrate mixed-layer model
        if self.sw_ml:
            self.integrate_mixed_layer()

    def store(self):
        for var in self.OUTPUT_VAR_NAMES:
            value = getattr(self, var, None)  # TODO: raise if not exist?

            # Special cases
            if var == "t":
                value = self.t * self.dt / 3600.0 + self.input.tstart
            if var in ["wCO2", "wCO2e", "wCO2R", "wCO2A"]:
                fac = (constants.rho * constants.mco2) / constants.mair
                value = getattr(self, var, 0) * fac
            if var == "dz":
                value = getattr(self, "dz_h", None)
            if var == "zlcl":
                value = getattr(self, "lcl", None)
            if var in ["Swin", "Swout", "Lwin", "Lwout"]:
                value = None
            if var in ["z0m", "z0h"]:
                # Was initialized but never updated
                value = 0

            # Unused (TODO: remove)
            if var in ["du", "dv", "wtheta", "wq", "u", "v", "ustar"]:
                value = getattr(self.input, var)
            if var in ["thetasurf"]:
                value = self.input.theta
            if var in ["Q"]:
                value = self.input.Q0
            if var in ["Cm", "Cs"]:
                value = 1e12
            if var in ["rs"]:
                value = 1.0e6

            self.out.loc[self.t, var] = value

    def statistics(self):
        # Calculate virtual temperatures
        self.thetav = self.theta + 0.61 * self.theta * self.q
        self.wthetav = self.input.wtheta + 0.61 * self.theta * self.input.wq
        self.dthetav = (self.theta + self.dtheta) * (1.0 + 0.61 * (self.q + self.dq)) - self.theta * (
            1.0 + 0.61 * self.q
        )

        # Mixed-layer top properties
        self.P_h = self.input.Ps - constants.rho * constants.g * self.h
        self.T_h = self.theta - constants.g / constants.cp * self.h

        # self.P_h    = self.input.Ps / np.exp((constants.g * self.h)/(constants.Rd * self.theta))
        # self.T_h    = self.theta / (self.input.Ps / self.P_h)**(constants.Rd/constants.cp)

        self.RH_h = self.q / qsat(self.T_h, self.P_h)

        # Find lifting condensation level iteratively
        if self.t == 0:
            self.lcl = self.h
            RHlcl = 0.5
        else:
            RHlcl = 0.9998

        itmax = 30
        it = 0
        while ((RHlcl <= 0.9999) or (RHlcl >= 1.0001)) and it < itmax:
            self.lcl += (1.0 - RHlcl) * 1000.0
            p_lcl = self.input.Ps - constants.rho * constants.g * self.lcl
            T_lcl = self.theta - constants.g / constants.cp * self.lcl
            RHlcl = self.q / qsat(T_lcl, p_lcl)
            it += 1

        if it == itmax:
            print("LCL calculation not converged!!")
            print(f"RHlcl = {RHlcl:f}, zlcl={self.lcl:f}")

    def run_mixed_layer(self):
        if not self.sw_sl:
            # PK todo: treat these two lines as a "very simple surface layer scheme"?
            # decompose ustar along the wind components
            self.uw = -np.sign(self.input.u) * (
                self.input.ustar**4.0 / (self.input.v**2.0 / self.input.u**2.0 + 1.0)
            ) ** (0.5)
            self.vw = -np.sign(self.input.v) * (
                self.input.ustar**4.0 / (self.input.u**2.0 / self.input.v**2.0 + 1.0)
            ) ** (0.5)

        # calculate large-scale vertical velocity (subsidence)
        self.ws = -self.input.divU * self.h

        # calculate compensation to fix the free troposphere in case of subsidence
        if self.sw_fixft:
            w_th_ft = self.input.gammatheta * self.ws
            w_q_ft = self.input.gammaq * self.ws
            w_CO2_ft = self.input.gammaCO2 * self.ws
        else:
            w_th_ft = 0.0
            w_q_ft = 0.0
            w_CO2_ft = 0.0

        # calculate mixed-layer growth due to cloud top radiative divergence
        self.wf = self.input.dFz / (constants.rho * constants.cp * self.dtheta)

        # calculate convective velocity scale w*
        if self.wthetav > 0.0:
            self.wstar = ((constants.g * self.h * self.wthetav) / self.thetav) ** (1.0 / 3.0)
        else:
            self.wstar = 1e-6

        # Virtual heat entrainment flux
        self.wthetave = -self.input.beta * self.wthetav

        # compute mixed-layer tendencies
        if self.sw_shearwe:
            self.we = (
                -self.wthetave + 5.0 * self.input.ustar**3.0 * self.thetav / (constants.g * self.h)
            ) / self.dthetav
        else:
            self.we = -self.wthetave / self.dthetav

        # Don't allow boundary layer shrinking if wtheta < 0
        if self.we < 0:
            self.we = 0.0

        # Calculate entrainment fluxes
        self.wthetae = -self.we * self.dtheta
        self.wqe = -self.we * self.dq
        self.wCO2e = -self.we * self.dCO2

        self.htend = self.we + self.ws + self.wf - self.M

        fac = constants.mair / (constants.rho * constants.mco2)  # Conversion factor mgC m-2 s-1 to ppm m s-1
        self.thetatend = (self.input.wtheta - self.wthetae) / self.h + self.input.advtheta
        self.qtend = (self.input.wq - self.wqe - self.wqM) / self.h + self.input.advq
        self.CO2tend = (self.input.wCO2 * fac - self.wCO2e - self.wCO2M) / self.h + self.input.advCO2

        self.dthetatend = self.input.gammatheta * (self.we + self.wf - self.M) - self.thetatend + w_th_ft
        self.dqtend = self.input.gammaq * (self.we + self.wf - self.M) - self.qtend + w_q_ft
        self.dCO2tend = self.input.gammaCO2 * (self.we + self.wf - self.M) - self.CO2tend + w_CO2_ft

        # tendency of the transition layer thickness
        if self.ac > 0 or self.lcl - self.h < 300:
            self.dztend = ((self.lcl - self.h) - self.dz_h) / 7200.0
        else:
            self.dztend = 0.0

    def integrate_mixed_layer(self):
        # integrate mixed-layer equations
        self.h += self.dt * self.htend
        self.theta += self.dt * self.thetatend
        self.dtheta += self.dt * self.dthetatend
        self.q += self.dt * self.qtend
        self.dq += self.dt * self.dqtend
        self.CO2 += self.dt * self.CO2tend
        self.dCO2 += self.dt * self.dCO2tend
        self.dz_h += self.dt * self.dztend

        # Limit dz to minimal value
        dz0 = 50
        if self.dz_h < dz0:
            self.dz_h = dz0

    OUTPUT_VAR_NAMES = [
        "t",  # time [s]
        #
        # mixed-layer variables
        "h",  # ABL height [m]
        #
        "theta",  # initial mixed-layer potential temperature [K]
        "thetav",  # initial mixed-layer virtual potential temperature [K]
        "dtheta",  # initial potential temperature jump at h [K]
        "dthetav",  # initial virtual potential temperature jump at h [K]
        "wtheta",  # surface kinematic heat flux [K m s-1]
        "wthetav",  # surface kinematic virtual heat flux [K m s-1]
        "wthetae",  # entrainment kinematic heat flux [K m s-1]
        "wthetave",  # entrainment kinematic virtual heat flux [K m s-1]
        #
        "q",  # mixed-layer specific humidity [kg kg-1]
        "dq",  # initial specific humidity jump at h [kg kg-1]
        "wq",  # surface kinematic moisture flux [kg kg-1 m s-1]
        "wqe",  # entrainment kinematic moisture flux [kg kg-1 m s-1]
        "wqM",  # cumulus mass-flux kinematic moisture flux [kg kg-1 m s-1]
        #
        "qsat",  # mixed-layer saturated specific humidity [kg kg-1]
        "e",  # mixed-layer vapor pressure [Pa]
        "esat",  # mixed-layer saturated vapor pressure [Pa]
        #
        "CO2",  # mixed-layer CO2 [ppm]
        "dCO2",  # initial CO2 jump at h [ppm]
        "wCO2",  # surface total CO2 flux [mgC m-2 s-1]
        "wCO2A",  # surface assimilation CO2 flux [mgC m-2 s-1]
        "wCO2R",  # surface respiration CO2 flux [mgC m-2 s-1]
        "wCO2e",  # entrainment CO2 flux [mgC m-2 s-1]
        "wCO2M",  # CO2 mass flux [mgC m-2 s-1]
        #
        "u",  # initial mixed-layer u-wind speed [m s-1]
        "du",  # initial u-wind jump at h [m s-1]
        "uw",  # surface momentum flux u [m2 s-2]
        #
        "v",  # initial mixed-layer u-wind speed [m s-1]
        "dv",  # initial u-wind jump at h [m s-1]
        "vw",  # surface momentum flux v [m2 s-2]
        #
        # diagnostic meteorological variables
        "T2m",  # 2m temperature [K]
        "q2m",  # 2m specific humidity [kg kg-1]
        "u2m",  # 2m u-wind [m s-1]
        "v2m",  # 2m v-wind [m s-1]
        "e2m",  # 2m vapor pressure [Pa]
        "esat2m",  # 2m saturated vapor pressure [Pa]
        #
        # surface-layer variables
        "thetasurf",  # surface potential temperature [K]
        "thetavsurf",  # surface virtual potential temperature [K]
        "qsurf",  # surface specific humidity [kg kg-1]
        "ustar",  # surface friction velocity [m s-1]
        "z0m",  # roughness length for momentum [m]
        "z0h",  # roughness length for scalars [m]
        "Cm",  # drag coefficient for momentum []
        "Cs",  # drag coefficient for scalars []
        "L",  # Obukhov length [m]
        "Rib",  # bulk Richardson number [-]
        #
        # radiation variables
        "Swin",  # incoming short wave radiation [W m-2]
        "Swout",  # outgoing short wave radiation [W m-2]
        "Lwin",  # incoming long wave radiation [W m-2]
        "Lwout",  # outgoing long wave radiation [W m-2]
        "Q",  # net radiation [W m-2]
        #
        # land surface variables
        "ra",  # aerodynamic resistance [s m-1]
        "rs",  # surface resistance [s m-1]
        "H",  # sensible heat flux [W m-2]
        "LE",  # evapotranspiration [W m-2]
        "LEliq",  # open water evaporation [W m-2]
        "LEveg",  # transpiration [W m-2]
        "LEsoil",  # soil evaporation [W m-2]
        "LEpot",  # potential evaporation [W m-2]
        "LEref",  # reference evaporation at rs = rsmin / LAI [W m-2]
        "G",  # ground heat flux [W m-2]
        # Mixed-layer top variables
        "zlcl",  # lifting condensation level [m]
        "RH_h",  # mixed-layer top relative humidity [-]
        # cumulus variables
        "ac",  # cloud core fraction [-]
        "M",  # cloud core mass flux [m s-1]
        "dz",  # transition layer thickness [m]
    ]
    """List of model variables availabe for output."""
