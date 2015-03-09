import lof

instances = (
    (1, 1, 1, 1),
    (2, 2, 2, 2),
    (3, 3, 3, 3),
    (2, 1, 1, 1),
    (1, 2, 1, 1),
    (13, 13, 13, 13)
    )
instance = (1, 1, 1, 2)

def test_LOF_normalize_instances():
    l = lof.LOF(((1,1),(2,2)), normalize=True)
    assert l.instances == [(0.0,0.0),(1.0,1.0)]
    l = lof.LOF(((1,1),(2,2),(3,3)), normalize=True)
    assert l.instances == [(0.0,0.0),(0.5,0.5),(1.0,1.0)]

def test_distance():
    assert 1 == lof.distance_euclidean((1,1), (2,2))

def test_k_distance():
    instances = ((1,1),(2,2),(3,3))
    d = lof.k_distance(1,(2,2),instances)
    assert d == (0.0, [(2,2)])
    d = lof.k_distance(1,(2.2,2.2),instances)
    assert d == (0.20000000000000018, [(2,2)])
    d = lof.k_distance(1,(2.5,2.5),instances)
    assert d == (0.5, [(2,2),(3,3)])

def test_reachability_distance():
    instances = ((1,1),(2,2),(3,3))
    lof.reachability_distance(1, (1,1), (2,2), instances)

def test_outliers():
    lof.outliers(1, instances)

if __name__ == "__main__":
    print("Running tests, nothing more should appear if everything goes well.")
    test_LOF_normalize_instances()
    test_distance()
    test_k_distance()
    test_reachability_distance()
    test_outliers()
