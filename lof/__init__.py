#!/usr/bin/python
# -*- coding: utf8 -*-
"""
lof
~~~~~~~~~~~~

This module implements the Local Outlier Factor algorithm.

:copyright: (c) 2013 by Damjan Kužnar.
:license: GNU GPL v2, see LICENSE for more details.

"""
from __future__ import division
import warnings

import numpy as np


class LOF:
    """Helper class for performing LOF computations and instances
    normalization."""

    def __init__(self, instances, normalize=True):
        self.instances = instances
        self.normalize = normalize
        if normalize:
            self.normalize_instances()

    def compute_instance_attribute_bounds(self):
        max_values = np.max(self.instances, axis=0)
        min_values = np.min(self.instances, axis=0)

        diff = max_values - min_values
        if not np.all(diff):
            problematic_dimensions = ", ".join(str(i + 1) for i, v
                                               in enumerate(diff) if v == 0)
            warnings.warn("No data variation in dimensions: %s. You should "
                          "check your data or disable normalization."
                          % problematic_dimensions)

        self.max_attribute_values = max_values
        self.min_attribute_values = min_values

    def normalize_instances(self):
        """Normalizes the instances and stores the infromation for rescaling new
         instances."""
        if not hasattr(self, "max_attribute_values"):
            self.compute_instance_attribute_bounds()
        self.instances = (self.instances - self.min_attribute_values) /\
            (self.max_attribute_values - self.min_attribute_values)
        self.instances[np.logical_not(np.isfinite(self.instances))] = 0


    def normalize_instance(self, instance):
        instance = (instance - self.min_attribute_values) /\
            (self.max_attribute_values - self.min_attribute_values)
        instance[np.logical_not(np.isfinite(instance))] = 0
        return instance

    def local_outlier_factor(self, min_pts, instance):
        """The (local) outlier factor of instance captures the degree to which
        we call instance an outlier. min_pts is a parameter that is specifying a
        minimum number of instances to consider for computing LOF value.
        Returns: local outlier factor
        Signature: (int, float[:,:]) -> float"""
        if self.normalize:
            instance = self.normalize_instance(instance)
        return local_outlier_factor(min_pts, instance, self.instances)


def k_distance(k, instance, instances):
    """Computes the k-distance of instance as defined in paper. It also gatheres
    the set of k-distance neighbors.
    Returns: (k-distance, k-distance neighbors)
    Signature: (int, float[:,:]) -> (float, float[:,:])"""

    # compute Euclidean distances
    distances = np.sqrt(np.sum(np.power(instances - instance, 2), axis=1))

    sort_permutation = np.argsort(distances)
    distances = distances[sort_permutation]
    instances = instances[sort_permutation]

    real_k = np.unique(distances)
    real_k = real_k[k - 1] if len(real_k) >= k else real_k[-1]
    neighbors = instances[distances <= real_k, :]

    k_distance_value = distances[
        k - 1] if len(distances) >= k else distances[-1]
    return k_distance_value, neighbors


def reachability_distance(k, instance1, instance2, instances):
    """The reachability distance of instance1 with respect to instance2.
    Returns: reachability distance
    Signature: (int, float[:], float[:], float[:,:]) -> float"""
    (k_distance_value, neighbors) = k_distance(k, instance2, instances)
    return max([k_distance_value,
                np.sqrt(np.sum(np.power(instance1 - instance2, 2)))])


def local_reachability_density(min_pts, instance, instances):  # , **kwargs):
    """Local reachability density of instance is the inverse of the average
    reachability distance based on the min_pts-nearest neighbors of instance.
    Returns: local reachability density
    Signature: (int, float[:], float[:,:]) -> float"""
    (k_distance_value, neighbors) = k_distance(min_pts, instance, instances)
    reachability_distances_array = [0] * len(neighbors)
    for i, neighbour in enumerate(neighbors):
        reachability_distances_array[i] = reachability_distance(min_pts,
                                                                instance,
                                                                neighbour,
                                                                instances)
    if not any(reachability_distances_array):
        warnings.warn("Instance %s (could be normalized) is identical to all "
                      "the neighbors. Setting local reachability density to "
                      "inf." % repr(instance))
        return float("inf")
    else:
        return len(neighbors) / sum(reachability_distances_array)


def local_outlier_factor(min_pts, instance, instances):
    """The (local) outlier factor of instance captures the degree to which we
    call instance an outlier. min_pts is a parameter that is specifying a
    minimum number of instances to consider for computing LOF value.
    Returns: local outlier factor
    Signature: (int, float[:], float[:,:]) -> float"""
    (k_distance_value, neighbors) = k_distance(min_pts, instance, instances)
    instance_lrd = local_reachability_density(min_pts, instance, instances)
    lrd_ratios_array = [0] * len(neighbors)
    for i, neighbour in enumerate(neighbors):
        instances_without_instance = \
            instances[(instances != neighbour).any(axis=1)]
        neighbour_lrd = local_reachability_density(min_pts, neighbour,
                                                   instances_without_instance)
        lrd_ratios_array[i] = neighbour_lrd / instance_lrd
    return sum(lrd_ratios_array) / len(neighbors)


def outliers(k, instances, normalize=True):
    """Simple procedure to identify outliers in the dataset."""
    instances_value_backup = np.copy(instances)
    outliers = []
    for i, instance in enumerate(instances_value_backup):
        instances = np.copy(instances_value_backup)
        instances = np.delete(instances, i, axis=0)
        l = LOF(instances, normalize=normalize)
        value = l.local_outlier_factor(k, instance)
        if value > 1:
            outliers.append({"lof": value, "instance": instance, "index": i})
    outliers.sort(key=lambda o: o["lof"], reverse=True)
    return outliers
