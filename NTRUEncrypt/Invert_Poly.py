from Polynomial import Polynomial


def invert_poly(poly, modulus):
    extendedGCD(poly, [])
    return poly


def extendedGCD(poly_a: Polynomial, poly_b: Polynomial):
    r = []
    s = []
    t = []
    r.extend((poly_a, poly_b))
    s.extend((Polynomial([1]), Polynomial([0])))
    t.extend((Polynomial([0]), Polynomial([1])))
    
    end = [0] * len(poly_a.coefs)
    round = 1
    while [round] != end:
        print(r[round-1].coefs)
        print(r[round].coefs)
        quotient = r[round - 1] // r[round]
        print("Quotient")
        print(quotient.coefs)
        print("Reminder")
        remainder = r[round - 1] - quotient * r[round]
        remainder.reduce()
        print(remainder.coefs)
        r.append(remainder)
        print(r[round + 1].coefs)
        new_s = s[round - 1] - quotient * s[round]
        new_s.reduce()
        s.append(new_s)
        print(s[round + 1].coefs)
        new_t = t[round - 1] - quotient * t[round]
        new_t.reduce()
        t.append(new_t)
        print(t[round + 1].coefs)
        round += 1
    result = []
    result.extend((r[round - 1], s[round - 1], t[round - 1]))
    return result

