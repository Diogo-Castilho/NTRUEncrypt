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
    
    end = Polynomial([0])
    round = 1
    while r[round] != end:
        print(r[round-1].coefs)
        print(r[round].coefs)
        quotientRemainder = r[round - 1] // r[round]
        print("Quotient")
        quotient = quotientRemainder[0]
        print(quotient.coefs)
        print("Reminder")
        remainder = quotientRemainder[1]
        remainder.reduce()
        print(remainder.coefs)
        r.append(remainder)
        print(r[round + 1].coefs)
        new_s = s[round - 1] - quotient * s[round]
        #new_s.reduce()
        s.append(new_s)
        print(s[round + 1].coefs)
        new_t = t[round - 1] - quotient * t[round]
        #new_t.reduce()
        t.append(new_t)
        print(t[round + 1].coefs)
        round += 1
    result = []
    print(r[round -2].coefs)
    result.extend((r[round - 2], s[round - 2], t[round - 2]))
    return result


def testGCD(poly_a: Polynomial, poly_b: Polynomial):
    prevx, x = Polynomial([1]), Polynomial([0])
    prevy, y = Polynomial([0]), Polynomial([1])
    end = Polynomial([0])
    while poly_b != end:
        print("a and b")
        print(poly_a.coefs)
        print(poly_b.coefs)
        quotient_remainder = poly_a // poly_b
        quotient = quotient_remainder[0]
        x, prevx = prevx - quotient * x, x
        print(x.coefs)
        print(prevx.coefs)
        y, prevy = prevy - quotient * y, y
        print(y.coefs)
        print(prevy.coefs)
        poly_a, poly_b = poly_b, quotient_remainder[1]
        poly_a.reduce()
    return [poly_a, prevx, prevy]