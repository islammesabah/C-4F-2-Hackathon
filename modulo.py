def mod(u, m):
    return (u % m + m) % m


def power_mod(a, e, m):
    result = 1
    while e > 0:
        if e % 2 == 0:
            e = e // 2
            a = (a * a) % m
        else:
            e = e - 1
            result = (result * a) % m
            e = e // 2
            a = (a * a) % m
    return result


def update_egcd(r0, r1, q):
    tmp = r0 - q * r1
    r0 = r1
    r1 = tmp
    return r0, r1


def egcd(r0, r1):
    x1 = y0 = 0
    y1 = x0 = 1
    while r1:
        q = r0 // r1
        r0, r1 = update_egcd(r0, r1, q)
        x0, x1 = update_egcd(x0, x1, q)
        y0, y1 = update_egcd(y0, y1, q)
    return r0, x0, y0


def inverse_mod(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        return -1
    else:
        return (x % m + m) % m


def solve_lde(a, b, c):
    g, x, y = egcd(a, b)
    m = c // g
    x *= m
    y *= m
    success = (c - m * g) == 0
    return g, x, y, success


def crt(rs, ms):
    R = rs[0]
    M = ms[0]
    for i in range(1, len(rs)):
        g, v, u, success = solve_lde(M, -ms[i], rs[i] - R)
        if not success:
            return -1, -1
        g = abs(g)
        v = mod(v, ms[i] / g)
        R = M * v + R
        M = M // g * ms[i]
        R %= M
    return R, M


if __name__ == '__main__':
    n = 26
    for i in range(1, n):
        inv = inverse_mod(i, n)
        print(f"{i} x {inv} = {(i * inv) % n}")
