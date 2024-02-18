"""Regression test for output consistency.

To update reference data, run:

python test_model.py update-reference
"""

import sys
import pandas as pd
from model import model_input, model


def default_config():
    config = model_input()
    config.dt = 60.0  # time step [s]
    config.runtime = 12 * 3600  # total run time [s]

    # mixed-layer input
    config.sw_ml = True  # mixed-layer model switch
    config.sw_shearwe = False  # shear growth mixed-layer switch
    config.sw_fixft = False  # Fix the free-troposphere switch
    config.h = 200.0  # initial ABL height [m]
    config.Ps = 101300.0  # surface pressure [Pa]
    config.divU = 0.0  # horizontal large-scale divergence of wind [s-1]
    config.fc = 1.0e-4  # Coriolis parameter [m s-1]

    config.theta = 288.0  # initial mixed-layer potential temperature [K]
    config.dtheta = 1.0  # initial temperature jump at h [K]
    config.gammatheta = (
        0.006  # free atmosphere potential temperature lapse rate [K m-1]
    )
    config.advtheta = 0.0  # advection of heat [K s-1]
    config.beta = 0.2  # entrainment ratio for virtual heat [-]
    config.wtheta = 0.1  # surface kinematic heat flux [K m s-1]

    config.q = 0.008  # initial mixed-layer specific humidity [kg kg-1]
    config.dq = -0.001  # initial specific humidity jump at h [kg kg-1]
    config.gammaq = 0.0  # free atmosphere specific humidity lapse rate [kg kg-1 m-1]
    config.advq = 0.0  # advection of moisture [kg kg-1 s-1]
    config.wq = 0.1e-3  # surface kinematic moisture flux [kg kg-1 m s-1]

    config.CO2 = 422.0  # initial mixed-layer CO2 [ppm]
    config.dCO2 = -44.0  # initial CO2 jump at h [ppm]
    config.gammaCO2 = 0.0  # free atmosphere CO2 lapse rate [ppm m-1]
    config.advCO2 = 0.0  # advection of CO2 [ppm s-1]
    config.wCO2 = 0.0  # surface kinematic CO2 flux [ppm m s-1]

    config.sw_wind = False  # prognostic wind switch
    config.u = 6.0  # initial mixed-layer u-wind speed [m s-1]
    config.du = 4.0  # initial u-wind jump at h [m s-1]
    config.gammau = 0.0  # free atmosphere u-wind speed lapse rate [s-1]
    config.advu = 0.0  # advection of u-wind [m s-2]

    config.v = -4.0  # initial mixed-layer u-wind speed [m s-1]
    config.dv = 4.0  # initial u-wind jump at h [m s-1]
    config.gammav = 0.0  # free atmosphere v-wind speed lapse rate [s-1]
    config.advv = 0.0  # advection of v-wind [m s-2]

    config.sw_sl = False  # surface layer switch
    config.ustar = 0.3  # surface friction velocity [m s-1]
    config.z0m = 0.02  # roughness length for momentum [m]
    config.z0h = 0.002  # roughness length for scalars [m]

    config.sw_rad = False  # radiation switch
    config.lat = 51.97  # latitude [deg]
    config.lon = -4.93  # longitude [deg]
    config.doy = 268.0  # day of the year [-]
    config.tstart = 6.8  # time of the day [h UTC]
    config.cc = 0.0  # cloud cover fraction [-]
    config.Q = 400.0  # net radiation [W m-2]
    config.dFz = 0.0  # cloud top radiative divergence [W m-2]

    config.sw_ls = False  # land surface switch
    config.ls_type = "js"  # land-surface parameterization ('js' for Jarvis-Stewart or 'ags' for A-Gs)
    config.wg = 0.21  # volumetric water content top soil layer [m3 m-3]
    config.w2 = 0.21  # volumetric water content deeper soil layer [m3 m-3]
    config.cveg = 0.85  # vegetation fraction [-]
    config.Tsoil = 285.0  # temperature top soil layer [K]
    config.T2 = 286.0  # temperature deeper soil layer [K]
    config.a = 0.219  # Clapp and Hornberger retention curve parameter a
    config.b = 4.90  # Clapp and Hornberger retention curve parameter b
    config.p = 4.0  # Clapp and Hornberger retention curve parameter c
    config.CGsat = 3.56e-6  # saturated soil conductivity for heat

    config.wsat = 0.472  # saturated volumetric water content ECMWF config [-]
    config.wfc = 0.323  # volumetric water content field capacity [-]
    config.wwilt = 0.171  # volumetric water content wilting point [-]

    config.C1sat = 0.132
    config.C2ref = 1.8

    config.LAI = 2.0  # leaf area index [-]
    config.gD = 0.0  # correction factor transpiration for VPD [-]
    config.rsmin = 110.0  # minimum resistance transpiration [s m-1]
    config.rssoilmin = 50.0  # minimun resistance soil evaporation [s m-1]
    config.alpha = 0.25  # surface albedo [-]

    config.Ts = 290.0  # initial surface temperature [K]

    config.Wmax = 0.0002  # thickness of water layer on wet vegetation [m]
    config.Wl = 0.0000  # equivalent water layer depth for wet vegetation [m]

    config.Lambda = 5.9  # thermal diffusivity skin layer [-]

    config.c3c4 = "c3"  # Plant type ('c3' or 'c4')

    config.sw_cu = False  # Cumulus parameterization switch
    config.dz_h = 150.0  # Transition layer thickness [m]
    return config


def update_reference_data():
    """(Re)Generate data for regression test.

    Should be run only once when the expected output changes.
    """
    config = default_config()
    r1 = model(config)
    r1.run()
    output = r1.out.to_pandas()
    output.to_csv("test_output.csv")


def test_model():
    """Verify that model with default config reproduces previous result."""
    config = default_config()
    r1 = model(config)
    r1.run()
    output = r1.out.to_pandas()
    expected_output = pd.read_csv("test_output.csv", index_col=0)

    pd.testing.assert_frame_equal(output, expected_output)


if __name__ == "__main__":
    if len(sys.argv == 0):
        print("Use `pytest` to run test")
        print("Use `python test_model update-reference` to update reference data")

    if sys.argv[1] == "update-reference":
        print("Updating reference data")
        update_reference_data()
