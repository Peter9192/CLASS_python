import numpy as np
import pandas as pd


# class for storing mixed-layer model output data
class ModelOutput:
    def __init__(self, tsteps):
        self.t = np.zeros(tsteps)  # time [s]

        # mixed-layer variables
        self.h = np.zeros(tsteps)  # ABL height [m]

        self.theta = np.zeros(tsteps)  # initial mixed-layer potential temperature [K]
        self.thetav = np.zeros(
            tsteps
        )  # initial mixed-layer virtual potential temperature [K]
        self.dtheta = np.zeros(tsteps)  # initial potential temperature jump at h [K]
        self.dthetav = np.zeros(
            tsteps
        )  # initial virtual potential temperature jump at h [K]
        self.wtheta = np.zeros(tsteps)  # surface kinematic heat flux [K m s-1]
        self.wthetav = np.zeros(tsteps)  # surface kinematic virtual heat flux [K m s-1]
        self.wthetae = np.zeros(tsteps)  # entrainment kinematic heat flux [K m s-1]
        self.wthetave = np.zeros(
            tsteps
        )  # entrainment kinematic virtual heat flux [K m s-1]

        self.q = np.zeros(tsteps)  # mixed-layer specific humidity [kg kg-1]
        self.dq = np.zeros(tsteps)  # initial specific humidity jump at h [kg kg-1]
        self.wq = np.zeros(tsteps)  # surface kinematic moisture flux [kg kg-1 m s-1]
        self.wqe = np.zeros(
            tsteps
        )  # entrainment kinematic moisture flux [kg kg-1 m s-1]
        self.wqM = np.zeros(
            tsteps
        )  # cumulus mass-flux kinematic moisture flux [kg kg-1 m s-1]

        self.qsat = np.zeros(
            tsteps
        )  # mixed-layer saturated specific humidity [kg kg-1]
        self.e = np.zeros(tsteps)  # mixed-layer vapor pressure [Pa]
        self.esat = np.zeros(tsteps)  # mixed-layer saturated vapor pressure [Pa]

        self.CO2 = np.zeros(tsteps)  # mixed-layer CO2 [ppm]
        self.dCO2 = np.zeros(tsteps)  # initial CO2 jump at h [ppm]
        self.wCO2 = np.zeros(tsteps)  # surface total CO2 flux [mgC m-2 s-1]
        self.wCO2A = np.zeros(tsteps)  # surface assimilation CO2 flux [mgC m-2 s-1]
        self.wCO2R = np.zeros(tsteps)  # surface respiration CO2 flux [mgC m-2 s-1]
        self.wCO2e = np.zeros(tsteps)  # entrainment CO2 flux [mgC m-2 s-1]
        self.wCO2M = np.zeros(tsteps)  # CO2 mass flux [mgC m-2 s-1]

        self.u = np.zeros(tsteps)  # initial mixed-layer u-wind speed [m s-1]
        self.du = np.zeros(tsteps)  # initial u-wind jump at h [m s-1]
        self.uw = np.zeros(tsteps)  # surface momentum flux u [m2 s-2]

        self.v = np.zeros(tsteps)  # initial mixed-layer u-wind speed [m s-1]
        self.dv = np.zeros(tsteps)  # initial u-wind jump at h [m s-1]
        self.vw = np.zeros(tsteps)  # surface momentum flux v [m2 s-2]

        # diagnostic meteorological variables
        self.T2m = np.zeros(tsteps)  # 2m temperature [K]
        self.q2m = np.zeros(tsteps)  # 2m specific humidity [kg kg-1]
        self.u2m = np.zeros(tsteps)  # 2m u-wind [m s-1]
        self.v2m = np.zeros(tsteps)  # 2m v-wind [m s-1]
        self.e2m = np.zeros(tsteps)  # 2m vapor pressure [Pa]
        self.esat2m = np.zeros(tsteps)  # 2m saturated vapor pressure [Pa]

        # surface-layer variables
        self.thetasurf = np.zeros(tsteps)  # surface potential temperature [K]
        self.thetavsurf = np.zeros(tsteps)  # surface virtual potential temperature [K]
        self.qsurf = np.zeros(tsteps)  # surface specific humidity [kg kg-1]
        self.ustar = np.zeros(tsteps)  # surface friction velocity [m s-1]
        self.z0m = np.zeros(tsteps)  # roughness length for momentum [m]
        self.z0h = np.zeros(tsteps)  # roughness length for scalars [m]
        self.Cm = np.zeros(tsteps)  # drag coefficient for momentum []
        self.Cs = np.zeros(tsteps)  # drag coefficient for scalars []
        self.L = np.zeros(tsteps)  # Obukhov length [m]
        self.Rib = np.zeros(tsteps)  # bulk Richardson number [-]

        # radiation variables
        self.Swin = np.zeros(tsteps)  # incoming short wave radiation [W m-2]
        self.Swout = np.zeros(tsteps)  # outgoing short wave radiation [W m-2]
        self.Lwin = np.zeros(tsteps)  # incoming long wave radiation [W m-2]
        self.Lwout = np.zeros(tsteps)  # outgoing long wave radiation [W m-2]
        self.Q = np.zeros(tsteps)  # net radiation [W m-2]

        # land surface variables
        self.ra = np.zeros(tsteps)  # aerodynamic resistance [s m-1]
        self.rs = np.zeros(tsteps)  # surface resistance [s m-1]
        self.H = np.zeros(tsteps)  # sensible heat flux [W m-2]
        self.LE = np.zeros(tsteps)  # evapotranspiration [W m-2]
        self.LEliq = np.zeros(tsteps)  # open water evaporation [W m-2]
        self.LEveg = np.zeros(tsteps)  # transpiration [W m-2]
        self.LEsoil = np.zeros(tsteps)  # soil evaporation [W m-2]
        self.LEpot = np.zeros(tsteps)  # potential evaporation [W m-2]
        self.LEref = np.zeros(
            tsteps
        )  # reference evaporation at rs = rsmin / LAI [W m-2]
        self.G = np.zeros(tsteps)  # ground heat flux [W m-2]

        # Mixed-layer top variables
        self.zlcl = np.zeros(tsteps)  # lifting condensation level [m]
        self.RH_h = np.zeros(tsteps)  # mixed-layer top relative humidity [-]

        # cumulus variables
        self.ac = np.zeros(tsteps)  # cloud core fraction [-]
        self.M = np.zeros(tsteps)  # cloud core mass flux [m s-1]
        self.dz = np.zeros(tsteps)  # transition layer thickness [m]

    def to_pandas(self):
        df = pd.DataFrame(self.__dict__)
        return df
