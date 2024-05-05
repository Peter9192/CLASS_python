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

from classmodel.constants import CONSTANTS
from classmodel.output import ModelOutput


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
        self.sw_wind = self.input.sw_wind  # prognostic wind switch
        self.sw_sl = self.input.sw_sl  # surface layer switch
        self.Q = self.input.Q0
        self.sw_ls = self.input.sw_ls  # land surface switch
        self.ls_type = self.input.ls_type  # land surface paramaterization (js or ags)
        self.sw_cu = self.input.sw_cu  # cumulus parameterization switch

        # initialize mixed-layer
        self.h = self.input.h  # initial ABL height [m]
        self.Ps = self.input.Ps  # surface pressure [Pa]
        self.divU = self.input.divU  # horizontal large-scale divergence of wind [s-1]
        self.ws = None  # large-scale vertical velocity [m s-1]
        self.wf = None  # mixed-layer growth due to radiative divergence [m s-1]
        self.fc = self.input.fc  # coriolis parameter [s-1]
        self.we = -1.0  # entrainment velocity [m s-1]

        # Temperature
        self.theta = self.input.theta  # initial mixed-layer potential temperature [K]
        self.dtheta = self.input.dtheta  # initial temperature jump at h [K]
        self.gammatheta = self.input.gammatheta  # free atmosphere potential temperature lapse rate [K m-1]
        self.advtheta = self.input.advtheta  # advection of heat [K s-1]
        self.beta = self.input.beta  # entrainment ratio for virtual heat [-]
        self.wtheta = self.input.wtheta  # surface kinematic heat flux [K m s-1]
        self.wthetae = None  # entrainment kinematic heat flux [K m s-1]

        self.wstar = 0.0  # convective velocity scale [m s-1]

        # 2m diagnostic variables
        self.T2m = None  # 2m temperature [K]
        self.q2m = None  # 2m specific humidity [kg kg-1]
        self.e2m = None  # 2m vapor pressure [Pa]
        self.esat2m = None  # 2m saturated vapor pressure [Pa]
        self.u2m = None  # 2m u-wind [m s-1]
        self.v2m = None  # 2m v-wind [m s-1]

        # Surface variables
        self.thetasurf = self.input.theta  # surface potential temperature [K]
        self.thetavsurf = None  # surface virtual potential temperature [K]
        self.qsurf = None  # surface specific humidity [g kg-1]

        # Mixed-layer top variables
        self.P_h = None  # Mixed-layer top pressure [pa]
        self.T_h = None  # Mixed-layer top absolute temperature [K]
        self.q2_h = None  # Mixed-layer top specific humidity variance [kg2 kg-2]
        self.CO22_h = None  # Mixed-layer top CO2 variance [ppm2]
        self.RH_h = None  # Mixed-layer top relavtive humidity [-]
        self.dz_h = None  # Transition layer thickness [-]
        self.lcl = None  # Lifting condensation level [m]

        # Virtual temperatures and fluxes
        self.thetav = None  # initial mixed-layer potential temperature [K]
        self.dthetav = None  # initial virtual temperature jump at h [K]
        self.wthetav = None  # surface kinematic virtual heat flux [K m s-1]
        self.wthetave = None  # entrainment kinematic virtual heat flux [K m s-1]

        # Moisture
        self.q = self.input.q  # initial mixed-layer specific humidity [kg kg-1]
        self.dq = self.input.dq  # initial specific humidity jump at h [kg kg-1]
        self.gammaq = self.input.gammaq  # free atmosphere specific humidity lapse rate [kg kg-1 m-1]
        self.advq = self.input.advq  # advection of moisture [kg kg-1 s-1]
        self.wq = self.input.wq  # surface kinematic moisture flux [kg kg-1 m s-1]
        self.wqe = None  # entrainment moisture flux [kg kg-1 m s-1]
        self.wqM = None  # moisture cumulus mass flux [kg kg-1 m s-1]

        self.qsat = None  # mixed-layer saturated specific humidity [kg kg-1]
        self.esat = None  # mixed-layer saturated vapor pressure [Pa]
        self.e = None  # mixed-layer vapor pressure [Pa]
        self.qsatsurf = None  # surface saturated specific humidity [g kg-1]
        self.dqsatdT = None  # slope saturated specific humidity curve [g kg-1 K-1]

        # CO2
        fac = CONSTANTS.mair / (CONSTANTS.rho * CONSTANTS.mco2)  # Conversion factor mgC m-2 s-1 to ppm m s-1
        self.CO2 = self.input.CO2  # initial mixed-layer CO2 [ppm]
        self.dCO2 = self.input.dCO2  # initial CO2 jump at h [ppm]
        self.gammaCO2 = self.input.gammaCO2  # free atmosphere CO2 lapse rate [ppm m-1]
        self.advCO2 = self.input.advCO2  # advection of CO2 [ppm s-1]
        self.wCO2 = self.input.wCO2 * fac  # surface kinematic CO2 flux [ppm m s-1]
        self.wCO2A = 0  # surface assimulation CO2 flux [ppm m s-1]
        self.wCO2R = 0  # surface respiration CO2 flux [ppm m s-1]
        self.wCO2e = None  # entrainment CO2 flux [ppm m s-1]
        self.wCO2M = 0  # CO2 mass flux [ppm m s-1]

        # Wind
        self.u = self.input.u  # initial mixed-layer u-wind speed [m s-1]
        self.du = self.input.du  # initial u-wind jump at h [m s-1]
        self.gammau = self.input.gammau  # free atmosphere u-wind speed lapse rate [s-1]
        self.advu = self.input.advu  # advection of u-wind [m s-2]

        self.v = self.input.v  # initial mixed-layer u-wind speed [m s-1]
        self.dv = self.input.dv  # initial u-wind jump at h [m s-1]
        self.gammav = self.input.gammav  # free atmosphere v-wind speed lapse rate [s-1]
        self.advv = self.input.advv  # advection of v-wind [m s-2]

        # Tendencies
        self.htend = None  # tendency of CBL [m s-1]
        self.thetatend = None  # tendency of mixed-layer potential temperature [K s-1]
        self.dthetatend = None  # tendency of potential temperature jump at h [K s-1]
        self.qtend = None  # tendency of mixed-layer specific humidity [kg kg-1 s-1]
        self.dqtend = None  # tendency of specific humidity jump at h [kg kg-1 s-1]
        self.CO2tend = None  # tendency of CO2 humidity [ppm]
        self.dCO2tend = None  # tendency of CO2 jump at h [ppm s-1]
        self.utend = None  # tendency of u-wind [m s-1 s-1]
        self.dutend = None  # tendency of u-wind jump at h [m s-1 s-1]
        self.vtend = None  # tendency of v-wind [m s-1 s-1]
        self.dvtend = None  # tendency of v-wind jump at h [m s-1 s-1]
        self.dztend = None  # tendency of transition layer thickness [m s-1]

        # initialize surface layer
        self.ustar = self.input.ustar  # surface friction velocity [m s-1]
        self.uw = None  # surface momentum flux in u-direction [m2 s-2]
        self.vw = None  # surface momentum flux in v-direction [m2 s-2]
        self.z0m = self.input.z0m  # roughness length for momentum [m]
        self.z0h = self.input.z0h  # roughness length for scalars [m]
        self.Cm = 1e12  # drag coefficient for momentum [-]
        self.Cs = 1e12  # drag coefficient for scalars [-]
        self.L = None  # Obukhov length [m]
        self.Rib = None  # bulk Richardson number [-]
        self.ra = None  # aerodynamic resistance [s m-1]

        self.tstart = self.input.tstart  # time of the day [-]
        self.dFz = self.input.dFz  # cloud top radiative divergence [W m-2]

        # initialize land surface
        self.wg = self.input.wg  # volumetric water content top soil layer [m3 m-3]
        self.w2 = self.input.w2  # volumetric water content deeper soil layer [m3 m-3]
        self.Tsoil = self.input.Tsoil  # temperature top soil layer [K]
        self.T2 = self.input.T2  # temperature deeper soil layer [K]

        self.a = self.input.a  # Clapp and Hornberger retention curve parameter a [-]
        self.b = self.input.b  # Clapp and Hornberger retention curve parameter b [-]
        self.p = self.input.p  # Clapp and Hornberger retention curve parameter p [-]
        self.CGsat = self.input.CGsat  # saturated soil conductivity for heat

        self.wsat = self.input.wsat  # saturated volumetric water content ECMWF config [-]
        self.wfc = self.input.wfc  # volumetric water content field capacity [-]
        self.wwilt = self.input.wwilt  # volumetric water content wilting point [-]

        self.C1sat = self.input.C1sat
        self.C2ref = self.input.C2ref

        self.c_beta = self.input.c_beta  # Curvature plant water-stress factor (0..1) [-]

        self.LAI = self.input.LAI  # leaf area index [-]
        self.gD = self.input.gD  # correction factor transpiration for VPD [-]
        self.rsmin = self.input.rsmin  # minimum resistance transpiration [s m-1]
        self.rssoilmin = self.input.rssoilmin  # minimum resistance soil evaporation [s m-1]
        self.alpha = self.input.alpha  # surface albedo [-]  # TODO constant; only used in radiation

        self.rs = 1.0e6  # resistance transpiration [s m-1]
        self.rssoil = 1.0e6  # resistance soil [s m-1]

        self.Ts = self.input.Ts  # surface temperature [K]

        self.cveg = self.input.cveg  # vegetation fraction [-]
        self.Wmax = self.input.Wmax  # thickness of water layer on wet vegetation [m]
        self.Wl = self.input.Wl  # equivalent water layer depth for wet vegetation [m]
        self.cliq = None  # wet fraction [-]

        self.Lambda = self.input.Lambda  # thermal diffusivity skin layer [-]

        self.Tsoiltend = None  # soil temperature tendency [K s-1]
        self.wgtend = None  # soil moisture tendency [m3 m-3 s-1]
        self.Wltend = None  # equivalent liquid water tendency [m s-1]

        self.H = None  # sensible heat flux [W m-2]
        self.LE = None  # evapotranspiration [W m-2]
        self.LEliq = None  # open water evaporation [W m-2]
        self.LEveg = None  # transpiration [W m-2]
        self.LEsoil = None  # soil evaporation [W m-2]
        self.LEpot = None  # potential evaporation [W m-2]
        self.LEref = None  # reference evaporation using rs = rsmin / LAI [W m-2]
        self.G = None  # ground heat flux [W m-2]

        # initialize A-Gs surface scheme
        self.c3c4 = self.input.c3c4  # plant type ('c3' or 'c4')

        # initialize cumulus parameterization
        self.sw_cu = self.input.sw_cu  # Cumulus parameterization switch
        self.dz_h = self.input.dz_h  # Transition layer thickness [m]
        self.ac = 0.0  # Cloud core fraction [-]
        self.M = 0.0  # Cloud core mass flux [m s-1]
        self.wqM = 0.0  # Cloud core moisture flux [kg kg-1 m s-1]

        # initialize time variables
        self.tsteps = int(np.floor(self.input.runtime / self.input.dt))
        self.dt = self.input.dt
        self.t = 0

        # Some sanity checks for valid input
        if self.c_beta is None:
            self.c_beta = 0  # Zero curvature; linear response
        assert self.c_beta >= 0 or self.c_beta <= 1

        # initialize output
        self.out = ModelOutput(self.tsteps)

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

    def statistics(self):
        # Calculate virtual temperatures
        self.thetav = self.theta + 0.61 * self.theta * self.q
        self.wthetav = self.wtheta + 0.61 * self.theta * self.wq
        self.dthetav = (self.theta + self.dtheta) * (1.0 + 0.61 * (self.q + self.dq)) - self.theta * (
            1.0 + 0.61 * self.q
        )

        # Mixed-layer top properties
        self.P_h = self.Ps - CONSTANTS.rho * CONSTANTS.g * self.h
        self.T_h = self.theta - CONSTANTS.g / CONSTANTS.cp * self.h

        # self.P_h    = self.Ps / np.exp((CONSTANTS.g * self.h)/(CONSTANTS.Rd * self.theta))
        # self.T_h    = self.theta / (self.Ps / self.P_h)**(CONSTANTS.Rd/CONSTANTS.cp)

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
            p_lcl = self.Ps - CONSTANTS.rho * CONSTANTS.g * self.lcl
            T_lcl = self.theta - CONSTANTS.g / CONSTANTS.cp * self.lcl
            RHlcl = self.q / qsat(T_lcl, p_lcl)
            it += 1

        if it == itmax:
            print("LCL calculation not converged!!")
            print(f"RHlcl = {RHlcl:f}, zlcl={self.lcl:f}")

    def run_mixed_layer(self):
        if not self.sw_sl:
            # PK todo: treat these two lines as a "very simple surface layer scheme"?
            # decompose ustar along the wind components
            self.uw = -np.sign(self.u) * (self.ustar**4.0 / (self.v**2.0 / self.u**2.0 + 1.0)) ** (0.5)
            self.vw = -np.sign(self.v) * (self.ustar**4.0 / (self.u**2.0 / self.v**2.0 + 1.0)) ** (0.5)

        # calculate large-scale vertical velocity (subsidence)
        self.ws = -self.divU * self.h

        # calculate compensation to fix the free troposphere in case of subsidence
        if self.sw_fixft:
            w_th_ft = self.gammatheta * self.ws
            w_q_ft = self.gammaq * self.ws
            w_CO2_ft = self.gammaCO2 * self.ws
        else:
            w_th_ft = 0.0
            w_q_ft = 0.0
            w_CO2_ft = 0.0

        # calculate mixed-layer growth due to cloud top radiative divergence
        self.wf = self.dFz / (CONSTANTS.rho * CONSTANTS.cp * self.dtheta)

        # calculate convective velocity scale w*
        if self.wthetav > 0.0:
            self.wstar = ((CONSTANTS.g * self.h * self.wthetav) / self.thetav) ** (1.0 / 3.0)
        else:
            self.wstar = 1e-6

        # Virtual heat entrainment flux
        self.wthetave = -self.beta * self.wthetav

        # compute mixed-layer tendencies
        if self.sw_shearwe:
            self.we = (-self.wthetave + 5.0 * self.ustar**3.0 * self.thetav / (CONSTANTS.g * self.h)) / self.dthetav
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

        self.thetatend = (self.wtheta - self.wthetae) / self.h + self.advtheta
        self.qtend = (self.wq - self.wqe - self.wqM) / self.h + self.advq
        self.CO2tend = (self.wCO2 - self.wCO2e - self.wCO2M) / self.h + self.advCO2

        self.dthetatend = self.gammatheta * (self.we + self.wf - self.M) - self.thetatend + w_th_ft
        self.dqtend = self.gammaq * (self.we + self.wf - self.M) - self.qtend + w_q_ft
        self.dCO2tend = self.gammaCO2 * (self.we + self.wf - self.M) - self.CO2tend + w_CO2_ft

        # assume u + du = ug, so ug - u = du
        if self.sw_wind:
            self.utend = -self.fc * self.dv + (self.uw + self.we * self.du) / self.h + self.advu
            self.vtend = self.fc * self.du + (self.vw + self.we * self.dv) / self.h + self.advv

            self.dutend = self.gammau * (self.we + self.wf - self.M) - self.utend
            self.dvtend = self.gammav * (self.we + self.wf - self.M) - self.vtend

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

        if self.sw_wind:
            self.u += self.dt * self.utend
            self.du += self.dt * self.dutend
            self.v += self.dt * self.vtend
            self.dv += self.dt * self.dvtend

    # store model output
    def store(self):
        t = self.t
        self.out.t[t] = t * self.dt / 3600.0 + self.tstart
        self.out.h[t] = self.h

        self.out.theta[t] = self.theta
        self.out.thetav[t] = self.thetav
        self.out.dtheta[t] = self.dtheta
        self.out.dthetav[t] = self.dthetav
        self.out.wtheta[t] = self.wtheta
        self.out.wthetav[t] = self.wthetav
        self.out.wthetae[t] = self.wthetae
        self.out.wthetave[t] = self.wthetave

        self.out.q[t] = self.q
        self.out.dq[t] = self.dq
        self.out.wq[t] = self.wq
        self.out.wqe[t] = self.wqe
        self.out.wqM[t] = self.wqM

        self.out.qsat[t] = self.qsat
        self.out.e[t] = self.e
        self.out.esat[t] = self.esat

        fac = (CONSTANTS.rho * CONSTANTS.mco2) / CONSTANTS.mair
        self.out.CO2[t] = self.CO2
        self.out.dCO2[t] = self.dCO2
        self.out.wCO2[t] = self.wCO2 * fac
        self.out.wCO2e[t] = self.wCO2e * fac
        self.out.wCO2R[t] = self.wCO2R * fac
        self.out.wCO2A[t] = self.wCO2A * fac

        self.out.u[t] = self.u
        self.out.du[t] = self.du
        self.out.uw[t] = self.uw

        self.out.v[t] = self.v
        self.out.dv[t] = self.dv
        self.out.vw[t] = self.vw

        self.out.T2m[t] = self.T2m
        self.out.q2m[t] = self.q2m
        self.out.u2m[t] = self.u2m
        self.out.v2m[t] = self.v2m
        self.out.e2m[t] = self.e2m
        self.out.esat2m[t] = self.esat2m

        self.out.thetasurf[t] = self.thetasurf
        self.out.thetavsurf[t] = self.thetavsurf
        self.out.qsurf[t] = self.qsurf
        self.out.ustar[t] = self.ustar
        self.out.Cm[t] = self.Cm
        self.out.Cs[t] = self.Cs
        self.out.L[t] = self.L
        self.out.Rib[t] = self.Rib

        self.out.Swin[t] = None  # Set by radiation scheme
        self.out.Swout[t] = None
        self.out.Lwin[t] = None
        self.out.Lwout[t] = None
        self.out.Q[t] = self.Q

        self.out.ra[t] = self.ra
        self.out.rs[t] = self.rs
        self.out.H[t] = self.H
        self.out.LE[t] = self.LE
        self.out.LEliq[t] = self.LEliq
        self.out.LEveg[t] = self.LEveg
        self.out.LEsoil[t] = self.LEsoil
        self.out.LEpot[t] = self.LEpot
        self.out.LEref[t] = self.LEref
        self.out.G[t] = self.G

        self.out.zlcl[t] = self.lcl
        self.out.RH_h[t] = self.RH_h

        self.out.ac[t] = self.ac
        self.out.M[t] = self.M
        self.out.dz[t] = self.dz_h
