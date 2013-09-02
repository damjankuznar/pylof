#!/usr/bin/python
# -*- coding: utf8 -*-
"""
lof
~~~~~~~~~~~~

This module implements the Local Outlier Factor algorithm.

:copyright: (c) 2013 by Damjan Kužnar.
:license: GNU GPL v2, see LICENSE for more details.

"""

import numpy as n

def distance_euclidean(instance1, instance2):
    """Computes the distance between two instances. Instances should be tuples of equal length.
    Returns: Euclidean distance
    Signature: ((attr_1_1, attr_1_2, ...), (attr_2_1, attr_2_2, ...)) -> float"""
    def detect_value_type(attribute):
        """Detects the value type (number or non-number).
        Returns: (value type, value casted as detected type)
        Signature: value -> (str or float type, str or float value)"""
        from numbers import Number
        attribute_type = None
        if isinstance(attribute, Number):
            attribute_type = float
            attribute = float(attribute)
        else:
            attribute_type = str
            attribute = str(attribute)
        return attribute_type, attribute
    # check if instances are of same length
    if len(instance1) != len(instance2):
        raise AttributeError("Instances have different number of arguments.")
    # init differences vector
    differences = n.zeros(len(instance1)) # [0] * len(instance1)
    # compute difference for each attribute and store it to differences vector
    for i, (attr1, attr2) in enumerate(zip(instance1, instance2)):
        type1, attr1 = detect_value_type(attr1)
        type2, attr2 = detect_value_type(attr2)
        # raise error is attributes are not of same data type.
        if type1 != type2:
            raise AttributeError("Instances have different data types.")
        if type1 is float:
            # compute difference for float
            differences[i] = attr1 - attr2
        else:
            # compute difference for string
            if attr1 == attr2:
                differences[i] = 0
            else:
                differences[i] = 1
    # compute RMSE (root mean squared error)
    rmse = n.sqrt(n.sum(n.power(differences, 2)) / len(differences))
    return rmse

class LOF:
    def __init__(self, instances, normalize=True, distance_function=distance_euclidean):
        self.instances = instances
        self.normalize = normalize
        self.distance_function = distance_function
        if normalize:
            self.__normalize_instances()
            
    def __normalize_instances(self):
        """Normalizes the instances and stores the infromation for rescaling new instances."""
        min_values = n.ones(len(self.instances[0])) * n.inf 
        max_values = n.ones(len(self.instances[0])) * -1 * n.inf
        for instance in self.instances:
            min_values = n.minimum(min_values, instance)
            max_values = n.maximum(max_values, instance)
        new_instances = []
        for i, instance in enumerate(self.instances):
            new_instances.append(tuple((instance - min_values) / (max_values - min_values)))
        self.instances = new_instances
        self.max_attribute_values = max_values
        self.min_attribute_values = min_values
        
    def k_distance(self, k, instance, instances):
        #TODO: implement caching
        """Computes the k-distance of instance as defined in paper. It also gatheres the set of k-distance neighbours.
        Returns: (k-distance, k-distance neighbours)
        Signature: (int, (attr1, attr2, ...), ((attr_1_1, ...),(attr_2_1, ...), ...)) -> (float, ((attr_j_1, ...),(attr_k_1, ...), ...))"""
        distances = {}
        for instance2 in instances:
            distance_value = self.distance_function(instance, instance2)
            if distances.has_key(distance_value):
                distances[distance_value].append(instance2)
            else:
                distances[distance_value] = [instance2]
        distances = sorted(distances.items())
        neighbours = []
        [neighbours.extend(n[1]) for n in distances[:k]]
        return distances[k - 1][0], neighbours
    
    def reachability_distance(self, k, instance1, instance2, instances):
        """The reachability distance of instance1 with respect to instance2.
        Returns: reachability distance
        Signature: (int, (attr_1_1, ...),(attr_2_1, ...)) -> float"""
        (k_distance_value, neighbours) = self.k_distance(k, instance2, instances)
        return n.max([k_distance_value, self.distance_function(instance1, instance2)])
    
    def local_reachability_density(self, min_pts, instance, instances):
        """Local reachability density of instance is the inverse of the average reachability 
        distance based on the min_pts-nearest neighbors of instance.
        Returns: local reachability density
        Signature: (int, (attr1, attr2, ...), ((attr_1_1, ...),(attr_2_1, ...), ...)) -> float"""
        (k_distance_value, neighbours) = self.k_distance(min_pts, instance, instances)
        reachability_distances_array = n.zeros(len(neighbours))
        for i, neighbour in enumerate(neighbours):
            reachability_distances_array[i] = self.reachability_distance(min_pts, instance, neighbour, instances) 
        return len(neighbours) / n.sum(reachability_distances_array)
    
    def local_outlier_factor(self, min_pts, instance):
        """The (local) outlier factor of instance captures the degree to which we call instance an outlier.
        min_pts is a parameter that is specifying a minimum number of instances to consider for computing LOF value.
        Returns: local outlier factor
        Signature: (int, (attr1, attr2, ...), ((attr_1_1, ...),(attr_2_1, ...), ...)) -> float"""
        if self.normalize:
            instance = tuple((instance - self.min_attribute_values) / (self.max_attribute_values - self.min_attribute_values))
        (k_distance_value, neighbours) = self.k_distance(min_pts, instance, self.instances)
        instance_lrd = self.local_reachability_density(min_pts, instance, self.instances)
        lrd_ratios_array = n.zeros(len(neighbours))
        for i, neighbour in enumerate(neighbours):
            instances_without_instance = set(self.instances)
            instances_without_instance.discard(neighbour)
            neighbour_lrd = self.local_reachability_density(min_pts, neighbour, instances_without_instance)
            lrd_ratios_array[i] = neighbour_lrd / instance_lrd
        return n.sum(lrd_ratios_array) / len(neighbours)
    
def outliers(k, instances, **kwargs):
    """Simple procedure to identify outliers in the dataset."""
    instances_value_backup = instances
    outliers = []
    for i, instance in enumerate(instances_value_backup):
        instances = list(instances_value_backup)
        instances.remove(instance)
        lof = LOF(instances, **kwargs)
        value = lof.local_outlier_factor(k, instance)
        if value > 1:
            outliers.append({"lof": value, "instance": instance, "index": i})
    outliers.sort(key=lambda o: o["lof"], reverse=True)
    return outliers