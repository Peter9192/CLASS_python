"""Class configuration."""

from dataclasses import dataclass


@dataclass
class CLASSConfig:
    """Class for storing mixed-layer model input data."""

    # general model variables
    runtime = 12 * 3600  # total run time [s]
    dt = 60.0  # time step [s]

    # mixed-layer variables
    sw_ml = True  # mixed-layer model switch
    sw_shearwe = False  # Shear growth ABL switch
    sw_fixft = False  # Fix the free-troposphere switch
    h = 200.0  # initial ABL height [m]
    Ps = 101300.0  # surface pressure [Pa]
    divU = 0.0  # horizontal large-scale divergence of wind [s-1]
    fc = 1.0e-4  # Coriolis parameter [s-1]

    theta = 288.0  # initial mixed-layer potential temperature [K]
    dtheta = 1.0  # initial temperature jump at h [K]
    gammatheta = 0.006  # free atmosphere potential temperature lapse rate [K m-1]
    advtheta = 0.0  # advection of heat [K s-1]
    beta = 0.2  # entrainment ratio for virtual heat [-]
    wtheta = 0.1  # surface kinematic heat flux [K m s-1]

    q = 0.008  # initial mixed-layer specific humidity [kg kg-1]
    dq = -0.001  # initial specific humidity jump at h [kg kg-1]
    gammaq = 0.0  # free atmosphere specific humidity lapse rate [kg kg-1 m-1]
    advq = 0.0  # advection of moisture [kg kg-1 s-1]
    wq = 0.1e-3  # surface kinematic moisture flux [kg kg-1 m s-1]

    CO2 = 422.0  # initial mixed-layer potential temperature [K]
    dCO2 = -44.0  # initial temperature jump at h [K]
    gammaCO2 = 0.0  # free atmosphere potential temperature lapse rate [K m-1]
    advCO2 = 0.0  # advection of heat [K s-1]
    wCO2 = 0.0  # surface kinematic heat flux [K m s-1]

    sw_wind = False  # prognostic wind switch
    u = 6.0  # initial mixed-layer u-wind speed [m s-1]
    du = 4.0  # initial u-wind jump at h [m s-1]
    gammau = 0.0  # free atmosphere u-wind speed lapse rate [s-1]
    advu = 0.0  # advection of u-wind [m s-2]

    v = -4.0  # initial mixed-layer u-wind speed [m s-1]
    dv = 4.0  # initial u-wind jump at h [m s-1]
    gammav = 0.0  # free atmosphere v-wind speed lapse rate [s-1]
    advv = 0.0  # advection of v-wind [m s-2]

    # surface layer variables
    sw_sl = False  # surface layer switch
    ustar = 0.3  # surface friction velocity [m s-1]
    z0m = 0.02  # roughness length for momentum [m]
    z0h = 0.002  # roughness length for scalars [m]
    Cm = None  # drag coefficient for momentum [-]
    Cs = None  # drag coefficient for scalars [-]
    L = None  # Obukhov length [-]
    Rib = None  # bulk Richardson number [-]

    # radiation parameters
    sw_rad = False  # radiation switch
    lat = 51.97  # latitude [deg]
    lon = -4.93  # longitude [deg]
    doy = 268.0  # day of the year [-]
    tstart = 6.8  # time of the day [h UTC]
    cc = 0.0  # cloud cover fraction [-]
    Q = 400.0  # net radiation [W m-2]
    dFz = 0.0  # cloud top radiative divergence [W m-2]

    # land surface parameters
    sw_ls = False  # land surface switch
    ls_type = "js"  # land-surface parameterization ('js' for Jarvis-Stewart or 'ags' for A-Gs)
    wg = 0.21  # volumetric water content top soil layer [m3 m-3]
    w2 = 0.21  # volumetric water content deeper soil layer [m3 m-3]
    Tsoil = 285.0  # temperature top soil layer [K]
    T2 = 286.0  # temperature deeper soil layer [K]

    a = 0.219  # Clapp and Hornberger retention curve parameter a
    b = 4.90  # Clapp and Hornberger retention curve parameter b
    p = 4.0  # Clapp and Hornberger retention curve parameter c
    CGsat = 3.56e-6  # saturated soil conductivity for heat

    wsat = 0.472  # saturated volumetric water content ECMWF config [-]
    wfc = 0.323  # volumetric water content field capacity [-]
    wwilt = 0.171  # volumetric water content wilting point [-]

    C1sat = 0.132
    C2ref = 1.8

    c_beta = None  # Curvatur plant water-stress factor (0..1) [-]

    LAI = 2.0  # leaf area index [-]
    gD = 0.0  # correction factor transpiration for VPD [-]
    rsmin = 110.0  # minimum resistance transpiration [s m-1]
    rssoilmin = 50.0  # minimun resistance soil evaporation [s m-1]
    alpha = 0.25  # surface albedo [-]

    Ts = 290.0  # initial surface temperature [K]

    cveg = 0.85  # vegetation fraction [-]
    Wmax = 0.0002  # thickness of water layer on wet vegetation [m]
    Wl = 0.0000  # equivalent water layer depth for wet vegetation [m]

    Lambda = 5.9  # thermal diffusivity skin layer [-]

    # A-Gs parameters
    c3c4 = "c3"  # Plant type ('c3' or 'c4')

    # Cumulus parameters
    sw_cu = False  # Cumulus parameterization switch
    dz_h = 150.0  # Transition layer thickness [m]
