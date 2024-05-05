def ribtol(Rib, zsl, z0m, z0h):
    if Rib > 0.0:
        L = 1.0
        L0 = 2.0
    else:
        L = -1.0
        L0 = -2.0

    while abs(L - L0) > 0.001:
        L0 = L
        fx = (
            Rib
            - zsl
            / L
            * (np.log(zsl / z0h) - psih(zsl / L) + psih(z0h / L))
            / (np.log(zsl / z0m) - psim(zsl / L) + psim(z0m / L)) ** 2.0
        )
        Lstart = L - 0.001 * L
        Lend = L + 0.001 * L
        fxdif = (
            (
                -zsl
                / Lstart
                * (np.log(zsl / z0h) - psih(zsl / Lstart) + psih(z0h / Lstart))
                / (np.log(zsl / z0m) - psim(zsl / Lstart) + psim(z0m / Lstart)) ** 2.0
            )
            - (
                -zsl
                / Lend
                * (np.log(zsl / z0h) - psih(zsl / Lend) + psih(z0h / Lend))
                / (np.log(zsl / z0m) - psim(zsl / Lend) + psim(z0m / Lend)) ** 2.0
            )
        ) / (Lstart - Lend)
        L = L - fx / fxdif

        if abs(L) > 1e15:
            break

    return L


def psim(zeta):
    if zeta <= 0:
        x = (1.0 - 16.0 * zeta) ** (0.25)
        psim = 3.14159265 / 2.0 - 2.0 * np.arctan(x) + np.log((1.0 + x) ** 2.0 * (1.0 + x**2.0) / 8.0)
        # x     = (1. + 3.6 * abs(zeta) ** (2./3.)) ** (-0.5)
        # psim = 3. * np.log( (1. + 1. / x) / 2.)
    else:
        psim = -2.0 / 3.0 * (zeta - 5.0 / 0.35) * np.exp(-0.35 * zeta) - zeta - (10.0 / 3.0) / 0.35
    return psim


def psih(zeta):
    if zeta <= 0:
        x = (1.0 - 16.0 * zeta) ** (0.25)
        psih = 2.0 * np.log((1.0 + x * x) / 2.0)
        # x     = (1. + 7.9 * abs(zeta) ** (2./3.)) ** (-0.5)
        # psih  = 3. * np.log( (1. + 1. / x) / 2.)
    else:
        psih = (
            -2.0 / 3.0 * (zeta - 5.0 / 0.35) * np.exp(-0.35 * zeta)
            - (1.0 + (2.0 / 3.0) * zeta) ** (1.5)
            - (10.0 / 3.0) / 0.35
            + 1.0
        )
    return psih


def factorial(k):
    factorial = 1
    for n in range(2, k + 1):
        factorial = factorial * float(n)
    return factorial


def E1(x):
    E1sum = 0
    for k in range(1, 100):
        E1sum += pow((-1.0), (k + 0.0)) * pow(x, (k + 0.0)) / ((k + 0.0) * factorial(k))
    return -0.57721566490153286060 - np.log(x) - E1sum
