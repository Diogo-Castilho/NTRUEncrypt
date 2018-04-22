from Polynomial import Polynomial


def invert_poly(poly, modulus):
    extendedGCD(poly, [])
    return poly


def extendedGCD(poly_a, poly_b):
    r_old = poly_a
    r_new = poly_b
    s_old = 1
    s_new = 0
    t_old = 0
    t_new = 1
    
    end = [0] * poly_a.coefs.size
    while r_new != end:
        quotient = r_old.divide(r_new)
        
