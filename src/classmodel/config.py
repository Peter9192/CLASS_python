"""Class configuration."""

from dataclasses import dataclass


@dataclass
class ModelInput:
    """Class for storing mixed-layer model input data."""

    # general model variables
    runtime = None  # duration of model run [s]
    dt = None  # time step [s]

    # mixed-layer variables
    sw_ml = None  # mixed-layer model switch
    sw_shearwe = None  # Shear growth ABL switch
    sw_fixft = None  # Fix the free-troposphere switch
    h = None  # initial ABL height [m]
    Ps = None  # surface pressure [Pa]
    divU = None  # horizontal large-scale divergence of wind [s-1]
    fc = None  # Coriolis parameter [s-1]

    theta = None  # initial mixed-layer potential temperature [K]
    dtheta = None  # initial temperature jump at h [K]
    gammatheta = None  # free atmosphere potential temperature lapse rate [K m-1]
    advtheta = None  # advection of heat [K s-1]
    beta = None  # entrainment ratio for virtual heat [-]
    wtheta = None  # surface kinematic heat flux [K m s-1]

    q = None  # initial mixed-layer specific humidity [kg kg-1]
    dq = None  # initial specific humidity jump at h [kg kg-1]
    gammaq = None  # free atmosphere specific humidity lapse rate [kg kg-1 m-1]
    advq = None  # advection of moisture [kg kg-1 s-1]
    wq = None  # surface kinematic moisture flux [kg kg-1 m s-1]

    CO2 = None  # initial mixed-layer potential temperature [K]
    dCO2 = None  # initial temperature jump at h [K]
    gammaCO2 = None  # free atmosphere potential temperature lapse rate [K m-1]
    advCO2 = None  # advection of heat [K s-1]
    wCO2 = None  # surface kinematic heat flux [K m s-1]

    sw_wind = None  # prognostic wind switch
    u = None  # initial mixed-layer u-wind speed [m s-1]
    du = None  # initial u-wind jump at h [m s-1]
    gammau = None  # free atmosphere u-wind speed lapse rate [s-1]
    advu = None  # advection of u-wind [m s-2]

    v = None  # initial mixed-layer u-wind speed [m s-1]
    dv = None  # initial u-wind jump at h [m s-1]
    gammav = None  # free atmosphere v-wind speed lapse rate [s-1]
    advv = None  # advection of v-wind [m s-2]

    # surface layer variables
    sw_sl = None  # surface layer switch
    ustar = None  # surface friction velocity [m s-1]
    z0m = None  # roughness length for momentum [m]
    z0h = None  # roughness length for scalars [m]
    Cm = None  # drag coefficient for momentum [-]
    Cs = None  # drag coefficient for scalars [-]
    L = None  # Obukhov length [-]
    Rib = None  # bulk Richardson number [-]

    # radiation parameters
    sw_rad = None  # radiation switch
    lat = None  # latitude [deg]
    lon = None  # longitude [deg]
    doy = None  # day of the year [-]
    tstart = None  # time of the day [h UTC]
    cc = None  # cloud cover fraction [-]
    Q = None  # net radiation [W m-2]
    dFz = None  # cloud top radiative divergence [W m-2]

    # land surface parameters
    sw_ls = None  # land surface switch
    ls_type = None  # land-surface parameterization ('js' for Jarvis-Stewart or 'ags' for A-Gs)
    wg = None  # volumetric water content top soil layer [m3 m-3]
    w2 = None  # volumetric water content deeper soil layer [m3 m-3]
    Tsoil = None  # temperature top soil layer [K]
    T2 = None  # temperature deeper soil layer [K]

    a = None  # Clapp and Hornberger retention curve parameter a
    b = None  # Clapp and Hornberger retention curve parameter b
    p = None  # Clapp and Hornberger retention curve parameter p
    CGsat = None  # saturated soil conductivity for heat

    wsat = None  # saturated volumetric water content ECMWF config [-]
    wfc = None  # volumetric water content field capacity [-]
    wwilt = None  # volumetric water content wilting point [-]

    C1sat = None
    C2ref = None

    c_beta = None  # Curvatur plant water-stress factor (0..1) [-]

    LAI = None  # leaf area index [-]
    gD = None  # correction factor transpiration for VPD [-]
    rsmin = None  # minimum resistance transpiration [s m-1]
    rssoilmin = None  # minimum resistance soil evaporation [s m-1]
    alpha = None  # surface albedo [-]

    Ts = None  # initial surface temperature [K]

    cveg = None  # vegetation fraction [-]
    Wmax = None  # thickness of water layer on wet vegetation [m]
    Wl = None  # equivalent water layer depth for wet vegetation [m]

    Lambda = None  # thermal diffusivity skin layer [-]

    # A-Gs parameters
    c3c4 = None  # Plant type ('c3' or 'c4')

    # Cumulus parameters
    sw_cu = None  # Cumulus parameterization switch
    dz_h = None  # Transition layer thickness [m]
