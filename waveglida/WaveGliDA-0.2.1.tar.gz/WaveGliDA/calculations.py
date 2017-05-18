# -*- coding: utf-8 -*-
"""

created: Sun Jan 19 10:06:25 2014
author:  Luke Gregor
"""

span_ref = 436.68


def do_calculations(df):
    from seawater import satO2, dens0

    # this step has been commented until we can figure out the dataframe
    # df = licor_raw_calcs(df, **co2_kwargs)

    # preparing variables
    ctd_cond = df["CTD_Conductivity"].values
    sst_degC = df["CTD_Temp"].values
    pres_kPa = df["EQ_Press_Ave"].values
    oxyg_mLL = df['O2_Calculated'].values
    sea_xco2 = df['Ocean_CO2_Ave'].values
    atm_xco2 = df['Atmosphere_CO2_Ave'].values
    dates = df.index.values
    lat = df['Latitude']
    lon = df['Longitude']

    # Calculate salinity
    salt_psu = prawler_salinity(ctd_cond, sst_degC, pres_kPa)

    # Calculate oxygen concentration and saturation percentage
    dens_kgL = dens0(salt_psu, sst_degC) / 1000.  # kg/L
    # mL/L * molL/mL / kg/L  -  check this dimension analysis
    oxy_satr_uMkg = satO2(salt_psu, sst_degC) * 44.661 / dens_kgL
    oxy_meas_uMkg = oxyg_mLL * 44.661 / dens_kgL * 0.7
    oxy_prct = oxy_meas_uMkg / oxy_satr_uMkg * 100

    # Calculate ATM pressure with a pH2O correction
    ph2o_atm = water_vapour_pressure(salt_psu, sst_degC)
    # pressure is in kPa - convert to ATM first and subtract pH2O
    pres_atm = (pres_kPa / 101.325) - ph2o_atm
    # temperature correction
    temp_cor = temperature_correction(sst_degC, sst_degC)
    # pCO2 is simply ATM pressure * mole fraction of CO2 * temperature correction
    sea_pco2 = sea_xco2 * pres_atm * temp_cor
    atm_pco2 = atm_xco2 * pres_atm * temp_cor

    # Calculate fugacity of CO2 from partial pressure
    ve = virial_expansion(sst_degC, pres_kPa)
    sea_fco2 = sea_pco2 * ve
    atm_fco2 = atm_pco2 * ve

    # Calculate Delta fCO2
    dta_fco2 = sea_fco2 - atm_fco2

    # Ship speed is calculated using lat, lon with Haversin function
    ship_spd = calculate_speed(dates, lat, lon)

    # assign functions to the dataframe
    df['CTD_Salt'] = salt_psu
    df['O2_Meas_umolkg'] = oxy_meas_uMkg
    df['O2_Sat_umolkg'] = oxy_satr_uMkg
    df['O2_SatPct'] = oxy_prct
    df['Ocean_xCO2'] = sea_xco2
    df['Atmos_xCO2'] = atm_xco2
    df['Ocean_pCO2'] = sea_pco2
    df['Atmos_pCO2'] = atm_pco2
    df['Ocean_fCO2'] = sea_fco2
    df['Atmos_fCO2'] = atm_fco2
    df['Delta_fCO2'] = dta_fco2
    df['Ship_speed'] = ship_spd

    return df


def licor_raw_calcs(df, verbose=True, span_threshold=0.0001):
    from numpy import nanmax

    zr_raw1 = df['Zero_Raw_1']
    zr_raw2 = df['Zero_Raw_2']
    zero = (zr_raw2 / zr_raw1).ffill().bfill().values
    df['Zero_K_est'] = zero

    df['Span_K_est'] = .71  # df.Span_Cal_K  # a first estimate
    span = df['Span_K_est'].ffill().bfill().values
    sp_raw1 = df['Span_Post_Raw_1'].ffill().bfill().values
    sp_raw2 = df['Span_Post_Raw_2'].ffill().bfill().values
    sp_pres = df['Span_Post_Press_Ave'].ffill().bfill().values
    sp_temp = df['Span_Post_Temp_Ave'].ffill().bfill().values

    # Calculate the span coefficient using an iterative approach
    # TODO: I'm not sure this completely matches the method of the LICOR in the manual
    i = 0
    diff = df['Span_K_est'].values
    while nanmax(abs(diff)) > span_threshold:
        span_est = LI820_raw(sp_raw1, sp_raw2, sp_temp, sp_pres, zero, span)
        diff = span_est - span_ref
        span -= diff * 0.0012  # 0.0012 is empirically selected learning rate
        i += 1
    if verbose:
        print('Span coefficient solved in {} iterations'.format(i))

    eq_raw1 = df['EQ_Raw_1'].values
    eq_raw2 = df['EQ_Raw_2'].values
    eq_temp = df['EQ_Temp_Ave'].values
    eq_pres = df['EQ_Press_Ave'].values

    at_raw1 = df['Air_Raw_1'].values
    at_raw2 = df['Air_Raw_2'].values
    at_temp = df['Air_Temp_Ave'].values
    at_pres = df['Air_Press_Ave'].values

    df['Ocean_xCO2'] = LI820_raw(eq_raw1, eq_raw2, eq_temp, eq_pres, zero, span)
    df['Atmos_xCO2'] = LI820_raw(at_raw1, at_raw2, at_temp, at_pres, zero, span)

    return df


def water_vapour_pressure(salt, tempC_sea):
    from numpy import exp, log

    """Calculate pCO2 (calc_pco2)
    --------------------------
    This script is based on the CO2SYS script originally by Lewis and
    Wallace 1998. Weiss and Price (1980) in Marine Chemistry referenced
    by CO2SYS. If you'd like to calculate pCO2 from any xCO2 (not
    necessarily dry) it is the product of the pressure in the measureing
    chamber and xCO2.
    """

    Tk = tempC_sea + 273.15
    S = salt

    # Equation from Weiss and Price (1980)
    pH2O = exp(24.4543 -
               67.4509 * (100. / Tk) -
               4.8489 * log(Tk / 100.) -
               0.000544 * S)

    return pH2O


def temperature_correction(equ_degC, sst_degC):
    """
    pCO2 is corrected for equilibrator vs seawater temperatures
    using the relationship determined in Takahashi (1993).
    Here the Prawler CTD temperature is used in conjunction with
    the Licor equilibrator temperature.
    """
    from numpy import exp

    delta_temp = sst_degC - equ_degC
    temp_correct_factor = exp(0.0423 * delta_temp)

    return temp_correct_factor


def virial_expansion(sst_degC, pres_kPa):
    from numpy import exp

    """
    This script calculates the virial expansion coefficient. It is based on the
    Fugacity Factor calculation in the CO2SYS script originally by Lewis
    and Wallace 1998. Requires pCO2 and temperature in degC for inputs.

    The fugacity of CO2 is calculatied by finding the Fugacity Factor.
    This is based on Weiss, R. F., Marine Chemistry 2:203-215, 1974.

    This assumes that the pressure is at one atmosphere, or close to it.
    Otherwise, the Pres term in the exponent affects the results.
          Weiss, R. F., Marine Chemistry 2:203-215, 1974.
          Delta and B in cm3/mol
    """

    pres_atm = pres_kPa / 101.325
    Tk = sst_degC + 273.15
    R = 83.1451

    # d is the cross virial Coefficient B12 for interaction between gases 1 and 2
    # minus the mean of B11 and B22 for 2 our gases
    Delta = (57.7 - 0.118 * Tk)

    # B is the Virial Coefficient for CO2 and can be calculated using Weiss's power series
    B = -1636.75 + 12.0408 * Tk - 0.0327957 * Tk**2 + 3.16528 * 0.00001 * Tk**3

    # For a mixture of CO2 and air at 1 atm (at low CO2 concentrations)
    ve = exp(pres_atm * (B + 2 * Delta) / (R * Tk))

    return ve


def prawler_salinity(cond, temp, pres_kPa):
    from numpy import arange, array

    T_90 = temp
    P = pres_kPa.copy()

    A1, A2, A3 = 0.0000207, -0.000000000637, 3.989E-15
    B1, B2, B3, B4 = 0.03426, 0.0004464, 0.4215, 0.003107
    C0, C1, C2, C3, C4 = 0.676609, 0.0200564, 1.104259e-4, 6.9698e-7, 1.0031e-9

    a = array([0.008, -0.1692, 25.3851, 14.0941, -7.0261, 2.7081], ndmin=2)
    b = array([0.0005, -0.0056, -0.0066, -0.0375, 0.0636, -0.0144], ndmin=2)
    r = arange(6)[None] / 2.

    # convert Siemens/meter to mmhos/cm
    C = cond * 10.

    # Convert its-90 to its-68
    # ITS68 = ITS90 * 1.00024
    t = T_90 * 1.00024
    R = C / 42.914
    val = 1. + (B1 * t) + (B2 * t * t) + (B3 * R) + (B4 * R * t)

    RP = 1 + ((P * (A1 + P * (A2 + P * A3))) / val)
    val = RP * (C0 + (t * (C1 + t * (C2 + t * (C3 + t * C4)))))

    RT = R / val
    RT[RT <= 0] = 0.000001
    RT = RT[:, None]

    sum1 = (RT**r * a).sum(1)
    sum2 = (RT**r * b).sum(1)

    val = 1 + (0.0162 * (t - 15))

    salinity = sum1 + (sum2 * (t - 15.) / val)

    return salinity


def calculate_speed(time, lat, lon):
    from pandas import Series
    from numpy import nan, append

    lat, lon = lat.values.copy(), lon.values.copy()

    mask = (lat == 0) | (lon == 0)
    lat[mask] = nan
    lon[mask] = nan

    time = Series(time.copy())
    locs = list(zip(lat, lon))
    loc1, loc2 = locs[:-1], locs[1:]

    dT = time.diff()[1:].astype('timedelta64[s]').values
    dT[dT == 0] = nan
    dist = haversine(loc1, loc2) * 1000

    speed = dist / dT

    speed = append(nan, speed)

    return speed


def haversine(location1, location2):
    from numpy import deg2rad, sin, cos, arctan2, sqrt, array

    location1 = array(location1, ndmin=2)
    location2 = array(location2, ndmin=2)

    # using combination inds to get lats and lons
    lat1, lon1 = location1.T
    lat2, lon2 = location2.T

    # setting up variables for haversine
    R = 6371.
    dLat = deg2rad(lat2 - lat1)
    dLon = deg2rad(lon2 - lon1)
    lat1 = deg2rad(lat1)
    lat2 = deg2rad(lat2)

    # haversine formula
    a = sin(dLat / 2) * sin(dLat / 2) + \
        sin(dLon / 2) * sin(dLon / 2) * \
        cos(lat1) * cos(lat2)
    c = 2 * arctan2(sqrt(a), sqrt(1 - a))
    d = R * c

    return d


def LI820_raw(raw1, raw2, temp, pres_kPa, coeff_zero, coeff_span):
    from numpy import ndarray, NaN

    """xCO2 from raw voltages (calc_xco2_raw)
    --------------------------------------
    Calculates the mole fraction of CO2 (xCO2) from the raw voltage
    measurements made by the Wave Glider's Licor unit.
    This script has been modelled on the equations in the LI-820
    manual.

    For more details see:
    https://www.licor.com/documents/srqy9vep2nocnnei7ksb
    """

    xCO2 = ndarray(pres_kPa.shape)
    xCO2[pres_kPa == 0] = NaN

    # absroptance without pressure correction
    v = raw1
    vo = raw2
    Z = coeff_zero
    S = coeff_span
    a_c = (1. - ((v / vo) * Z)) * S

    # Pressure correction of absroptance
    p1 = pres_kPa  # p1 is the measured pressure
    p0 = 99.  # std pressure, po = 99
    # P is the ratio of the std pressure and measured press
    P = ndarray(pres_kPa.shape)
    P[p1 < p0] = p0 / p1[p1 < p0]
    P[p1 > p0] = p1[p1 > p0] / p0
    P[p1 == p0] = p1[p1 == p0]

    # g is the empirical correction function and is a function of
    # absorptance and pressure
    b1 = 1.10158
    b2 = -0.00612178
    b3 = -0.266278
    b4 = 3.69895
    b5 = 0.49609938
    x_1 = (1. / (b1 * (P - 1.)))
    x_2 = (1. / (b5 - a_c)) - (1. / b5)
    x_3 = 1. / (1. / (b2 + (b3 * P)) + b4)
    X = 1. + (1. / (x_1 + (x_2 / x_3)))

    # pressure correction function refered to as: g_{c}(a_{c}, P)
    g = ndarray(pres_kPa.shape)
    g[p1 == p0] = 1.
    g[p1 < p0] = X[p1 < p0]
    g[p1 > p0] = 1. / X[p1 > p0]

    # s is the pressure corrected absorptance and
    # equal absorptance(absp) * correction (g)
    # refered to as \alpha_{pc} in the manual
    a_pc = a_c * g

    # COMPUTING MOLE FRACTION
    # empirically derived coefficients
    a1 = 0.3989974
    a2 = 5897.2804
    a3 = 0.097101982
    a4 = 596.49981

    A = a2 - a4
    B = 2. * A * ((a1 * a4) - (a2 * a3))
    D = (a3 * a2) + (a1 * a4)
    # CO2 mole fraction is represented by C
    # C = f_c (\alpha_{pc}) (tempK / temp0K)
    # where f_c is the co2 calibration function
    c_1 = D - ((a2 + a4) * a_pc)
    c_2 = (A**2 * a_pc**2) + ((B * a_pc) + D**2)
    c_3 = a_pc - a1 - a3
    C = (c_1 - c_2**0.5) / (2. * c_3) * ((temp + 273.15) / (50. + 273.15))

    return C


if __name__ == "__main__":

    pass
