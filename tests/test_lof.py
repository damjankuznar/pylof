import lof
import numpy as np

instances = np.array((
    (1, 1, 1, 1),
    (2, 2, 2, 2),
    (3, 3, 3, 3),
    (2, 1, 1, 1),
    (1, 2, 1, 1),
    (13, 13, 13, 13)
))
instance = np.array((1, 1, 1, 2))


def test_LOF_normalize_instances():
    l = lof.LOF(np.array(((1, 1), (2, 2))), normalize=True)
    assert np.allclose(l.instances, np.array([(0.0, 0.0), (1.0, 1.0)]))
    l = lof.LOF(np.array(((1, 1), (2, 2), (3, 3))), normalize=True)
    assert np.allclose(l.instances, np.array(
        [(0.0, 0.0), (0.5, 0.5), (1.0, 1.0)]))


def test_k_distance():
    instances = np.array(((1, 1), (2, 2), (3, 3)))
    d = lof.k_distance(1, (2, 2), instances)
    assert np.allclose(d[0], 0.0)
    assert np.allclose(d[1], np.array([(2, 2)]))

    d = lof.k_distance(1, (2.2, 2.2), instances)
    assert np.allclose(d[0], 0.28284271247461928)
    assert np.allclose(d[1], np.array([(2, 2)]))

    d = lof.k_distance(1, (2.5, 2.5), instances)
    assert np.allclose(d[0], 0.70710678118654757)
    assert np.allclose(d[1], np.array([(2, 2), (3, 3)]))

    d = lof.k_distance(5, (2.2, 2.2), instances)
    assert np.allclose(d[0], 1.6970562748477143)
    assert np.allclose(d[1], np.array([(2, 2), (3, 3), (1, 1)]))


def test_reachability_distance():
    instances = np.array(((1, 1), (2, 2), (3, 3)))
    print lof.reachability_distance(1, np.array((1, 1)), np.array((2, 2)),
                                    instances)

def test_outliers():
    lof.outliers(1, instances)

def test_normalization_problems():
    # see issue https://github.com/damjankuznar/pylof/issues/7
    instances = [(1.,2.,3.),(2.,3.,4.),(1.,2.,4.),(1.,2.,1.)]
    l = lof.outliers(1, instances)

def test_duplicate_instances():
    instances = (
        (1, 1, 1, 1),
        (2, 2, 2, 2),
        (3, 3, 3, 3),
        (2, 1, 1, 1),
        (1, 2, 1, 1),
        (2, 2, 2, 2),
        (2, 2, 2, 2),
        (1, 1, 1, 1),
        (1, 1, 1, 1),
        (13, 13, 13, 13)
        )
    lof.outliers(1, instances)

if __name__ == "__main__":
    print("Running tests, nothing more should appear if everything goes well.")
    test_LOF_normalize_instances()
    test_distance()
    test_k_distance()
    test_reachability_distance()
    test_outliers()
    test_normalization_problems()
