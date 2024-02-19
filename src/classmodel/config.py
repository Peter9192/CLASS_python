"""Class configuration."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class CLASSConfig:
    """Class for storing mixed-layer model input data."""

    # general model variables
    runtime: int = 12 * 3600  # total run time [s]
    dt: float = 60.0  # time step [s]

    # mixed-layer variables
    sw_ml: bool = True  # mixed-layer model switch
    sw_shearwe: bool = False  # Shear growth ABL switch
    sw_fixft: bool = False  # Fix the free-troposphere switch
    h: float = 200.0  # initial ABL height [m]
    Ps: float = 101300.0  # surface pressure [Pa]
    divU: float = 0.0  # horizontal large-scale divergence of wind [s-1]
    fc: float = 1.0e-4  # Coriolis parameter [s-1]

    theta: float = 288.0  # initial mixed-layer potential temperature [K]
    dtheta: float = 1.0  # initial temperature jump at h [K]
    gammatheta: float = 0.006  # free atmosphere potential temperature lapse rate [K m-1]
    advtheta: float = 0.0  # advection of heat [K s-1]
    beta: float = 0.2  # entrainment ratio for virtual heat [-]
    wtheta: float = 0.1  # surface kinematic heat flux [K m s-1]

    q: float = 0.008  # initial mixed-layer specific humidity [kg kg-1]
    dq: float = -0.001  # initial specific humidity jump at h [kg kg-1]
    gammaq: float = 0.0  # free atmosphere specific humidity lapse rate [kg kg-1 m-1]
    advq: float = 0.0  # advection of moisture [kg kg-1 s-1]
    wq: float = 0.1e-3  # surface kinematic moisture flux [kg kg-1 m s-1]

    CO2: float = 422.0  # initial mixed-layer potential temperature [K]
    dCO2: float = -44.0  # initial temperature jump at h [K]
    gammaCO2: float = 0.0  # free atmosphere potential temperature lapse rate [K m-1]
    advCO2: float = 0.0  # advection of heat [K s-1]
    wCO2: float = 0.0  # surface kinematic heat flux [K m s-1]

    sw_wind: bool = False  # prognostic wind switch
    u: float = 6.0  # initial mixed-layer u-wind speed [m s-1]
    du: float = 4.0  # initial u-wind jump at h [m s-1]
    gammau: float = 0.0  # free atmosphere u-wind speed lapse rate [s-1]
    advu: float = 0.0  # advection of u-wind [m s-2]

    v: float = -4.0  # initial mixed-layer u-wind speed [m s-1]
    dv: float = 4.0  # initial u-wind jump at h [m s-1]
    gammav: float = 0.0  # free atmosphere v-wind speed lapse rate [s-1]
    advv: float = 0.0  # advection of v-wind [m s-2]

    # surface layer variables
    sw_sl: bool = False  # surface layer switch
    ustar: float = 0.3  # surface friction velocity [m s-1]
    z0m: float = 0.02  # roughness length for momentum [m]
    z0h: float = 0.002  # roughness length for scalars [m]
    Cm: float | None = None  # drag coefficient for momentum [-]
    Cs: float | None = None  # drag coefficient for scalars [-]
    L: float | None = None  # Obukhov length [-]
    Rib: float | None = None  # bulk Richardson number [-]

    # radiation parameters
    sw_rad: bool = False  # radiation switch
    lat: float = 51.97  # latitude [deg]
    lon: float = -4.93  # longitude [deg]
    doy: float = 268.0  # day of the year [-]
    tstart: float = 6.8  # time of the day [h UTC]
    cc: float = 0.0  # cloud cover fraction [-]
    Q: float = 400.0  # net radiation [W m-2]
    dFz: float = 0.0  # cloud top radiative divergence [W m-2]

    # land surface parameters
    sw_ls: bool = False  # land surface switch
    ls_type: Literal["js", "ags"] = "js"  # land-surface parameterization ('js' for Jarvis-Stewart or 'ags' for A-Gs)
    wg: float = 0.21  # volumetric water content top soil layer [m3 m-3]
    w2: float = 0.21  # volumetric water content deeper soil layer [m3 m-3]
    Tsoil: float = 285.0  # temperature top soil layer [K]
    T2: float = 286.0  # temperature deeper soil layer [K]

    a: float = 0.219  # Clapp and Hornberger retention curve parameter a
    b: float = 4.90  # Clapp and Hornberger retention curve parameter b
    p: float = 4.0  # Clapp and Hornberger retention curve parameter c
    CGsat: float = 3.56e-6  # saturated soil conductivity for heat

    wsat: float = 0.472  # saturated volumetric water content ECMWF config [-]
    wfc: float = 0.323  # volumetric water content field capacity [-]
    wwilt: float = 0.171  # volumetric water content wilting point [-]

    C1sat: float = 0.132
    C2ref: float = 1.8

    c_beta: float | None = None  # Curvatur plant water-stress factor (0..1) [-]

    LAI: float = 2.0  # leaf area index [-]
    gD: float = 0.0  # correction factor transpiration for VPD [-]
    rsmin: float = 110.0  # minimum resistance transpiration [s m-1]
    rssoilmin: float = 50.0  # minimun resistance soil evaporation [s m-1]
    alpha: float = 0.25  # surface albedo [-]

    Ts: float = 290.0  # initial surface temperature [K]

    cveg: float = 0.85  # vegetation fraction [-]
    Wmax: float = 0.0002  # thickness of water layer on wet vegetation [m]
    Wl: float = 0.0000  # equivalent water layer depth for wet vegetation [m]

    Lambda: float = 5.9  # thermal diffusivity skin layer [-]

    # A-Gs parameters
    c3c4: Literal["C3", "C4"] = "c3"  # Plant type ('c3' or 'c4')

    # Cumulus parameters
    sw_cu: bool = False  # Cumulus parameterization switch
    dz_h: float = 150.0  # Transition layer thickness [m]
