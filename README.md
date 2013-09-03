pylof
=====
[![Build Status](https://travis-ci.org/damjankuznar/pylof.png?branch=master)](https://travis-ci.org/damjankuznar/pylof)

Python implementation of Local Outlier Factor algorithm by [Markus M. Breunig](http://www.dbs.ifi.lmu.de/Publikationen/Papers/LOF.pdf).

Tests
-----
Travis CI tests fails on Python 3.2 and 3.3, however the tests work on my development computer.
```bash
(virt_env_python3)damjan@########:~/workspace/pylof$ python --version
Python 3.2.3
(virt_env_python3)damjan@########:~/workspace/pylof$ nosetests -v
test_lof.test_LOF_normalize_instances ... ok
test_lof.test_distance ... ok
test_lof.test_k_distance ... ok
test_lof.test_reachability_distance ... ok
test_lof.test_outliers ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.007s

OK
```

TODO
-----
 * Increase the unit test coverage
 * Determine why Travis CI nosetests are failing on Python 3.2 and 3.3
