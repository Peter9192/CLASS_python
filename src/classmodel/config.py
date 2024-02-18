# class for storing mixed-layer model input data
class ModelInput:
    def __init__(self):
        # general model variables
        self.runtime = None  # duration of model run [s]
        self.dt = None  # time step [s]

        # mixed-layer variables
        self.sw_ml = None  # mixed-layer model switch
        self.sw_shearwe = None  # Shear growth ABL switch
        self.sw_fixft = None  # Fix the free-troposphere switch
        self.h = None  # initial ABL height [m]
        self.Ps = None  # surface pressure [Pa]
        self.divU = None  # horizontal large-scale divergence of wind [s-1]
        self.fc = None  # Coriolis parameter [s-1]

        self.theta = None  # initial mixed-layer potential temperature [K]
        self.dtheta = None  # initial temperature jump at h [K]
        self.gammatheta = (
            None  # free atmosphere potential temperature lapse rate [K m-1]
        )
        self.advtheta = None  # advection of heat [K s-1]
        self.beta = None  # entrainment ratio for virtual heat [-]
        self.wtheta = None  # surface kinematic heat flux [K m s-1]

        self.q = None  # initial mixed-layer specific humidity [kg kg-1]
        self.dq = None  # initial specific humidity jump at h [kg kg-1]
        self.gammaq = None  # free atmosphere specific humidity lapse rate [kg kg-1 m-1]
        self.advq = None  # advection of moisture [kg kg-1 s-1]
        self.wq = None  # surface kinematic moisture flux [kg kg-1 m s-1]

        self.CO2 = None  # initial mixed-layer potential temperature [K]
        self.dCO2 = None  # initial temperature jump at h [K]
        self.gammaCO2 = None  # free atmosphere potential temperature lapse rate [K m-1]
        self.advCO2 = None  # advection of heat [K s-1]
        self.wCO2 = None  # surface kinematic heat flux [K m s-1]

        self.sw_wind = None  # prognostic wind switch
        self.u = None  # initial mixed-layer u-wind speed [m s-1]
        self.du = None  # initial u-wind jump at h [m s-1]
        self.gammau = None  # free atmosphere u-wind speed lapse rate [s-1]
        self.advu = None  # advection of u-wind [m s-2]

        self.v = None  # initial mixed-layer u-wind speed [m s-1]
        self.dv = None  # initial u-wind jump at h [m s-1]
        self.gammav = None  # free atmosphere v-wind speed lapse rate [s-1]
        self.advv = None  # advection of v-wind [m s-2]

        # surface layer variables
        self.sw_sl = None  # surface layer switch
        self.ustar = None  # surface friction velocity [m s-1]
        self.z0m = None  # roughness length for momentum [m]
        self.z0h = None  # roughness length for scalars [m]
        self.Cm = None  # drag coefficient for momentum [-]
        self.Cs = None  # drag coefficient for scalars [-]
        self.L = None  # Obukhov length [-]
        self.Rib = None  # bulk Richardson number [-]

        # radiation parameters
        self.sw_rad = None  # radiation switch
        self.lat = None  # latitude [deg]
        self.lon = None  # longitude [deg]
        self.doy = None  # day of the year [-]
        self.tstart = None  # time of the day [h UTC]
        self.cc = None  # cloud cover fraction [-]
        self.Q = None  # net radiation [W m-2]
        self.dFz = None  # cloud top radiative divergence [W m-2]

        # land surface parameters
        self.sw_ls = None  # land surface switch
        self.ls_type = None  # land-surface parameterization ('js' for Jarvis-Stewart or 'ags' for A-Gs)
        self.wg = None  # volumetric water content top soil layer [m3 m-3]
        self.w2 = None  # volumetric water content deeper soil layer [m3 m-3]
        self.Tsoil = None  # temperature top soil layer [K]
        self.T2 = None  # temperature deeper soil layer [K]

        self.a = None  # Clapp and Hornberger retention curve parameter a
        self.b = None  # Clapp and Hornberger retention curve parameter b
        self.p = None  # Clapp and Hornberger retention curve parameter p
        self.CGsat = None  # saturated soil conductivity for heat

        self.wsat = None  # saturated volumetric water content ECMWF config [-]
        self.wfc = None  # volumetric water content field capacity [-]
        self.wwilt = None  # volumetric water content wilting point [-]

        self.C1sat = None
        self.C2ref = None

        self.c_beta = None  # Curvatur plant water-stress factor (0..1) [-]

        self.LAI = None  # leaf area index [-]
        self.gD = None  # correction factor transpiration for VPD [-]
        self.rsmin = None  # minimum resistance transpiration [s m-1]
        self.rssoilmin = None  # minimum resistance soil evaporation [s m-1]
        self.alpha = None  # surface albedo [-]

        self.Ts = None  # initial surface temperature [K]

        self.cveg = None  # vegetation fraction [-]
        self.Wmax = None  # thickness of water layer on wet vegetation [m]
        self.Wl = None  # equivalent water layer depth for wet vegetation [m]

        self.Lambda = None  # thermal diffusivity skin layer [-]

        # A-Gs parameters
        self.c3c4 = None  # Plant type ('c3' or 'c4')

        # Cumulus parameters
        self.sw_cu = None  # Cumulus parameterization switch
        self.dz_h = None  # Transition layer thickness [m]
