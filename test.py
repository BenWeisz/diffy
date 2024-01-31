from diffy import DiffyConst, DiffyVar, DiffyE, DiffyPI, DiffyNode, DiffyNodeType

if __name__ == "__main__":
    x = DiffyVar("x")
    # c = x * x
    # e = DiffyE()
    d = DiffyConst("10")

    # a = e ** (c)

    # b = x ** d
    a = d + x
    ap = a.diffy()
    ap = ap.simp()

    print(ap)
    # print(b.diffy())