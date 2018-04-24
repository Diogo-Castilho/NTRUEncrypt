from Polynomial import Polynomial


def invert_poly(poly, modulus):
    extendedGCD(poly, [])
    return poly


def extendedGCD(poly_a: Polynomial, poly_b: Polynomial):
    r = []
    s = []
    t = []
    r.extend((poly_a, poly_b))
    s.extend((1, 0))
    t.extend((0, 1))
    
    end = [0] * len(poly_a.coefs)
    round = 1
    while [round] != end:
        print(round)
        print(r[round - 1].coefs)
        print(r[round].coefs)
        quotient = r[round] // (r[round - 1])
        print(quotient.coefs)
        r.append(r[round - 1] - quotient * r[round])
        s.append(s[round - 1] - quotient * s[round])
        t.append(t[round - 1] - quotient * t[round])
        round += 1
    result = []
    result.extend((r[round - 1], s[round - 1], t[round - 1]))
    return result

