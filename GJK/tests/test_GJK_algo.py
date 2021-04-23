#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementation of GJK algorithm to detect intersection of convex shapes.

Uses the convexity of Minkowski differences to quickly detect 
intersection of convex shapes.

Extensible to any convex shape as long as a support function is defined for it.

Inspired from https://www.youtube.com/watch?v=ajv46BSqcK4
"""

__author__ = "Abhijit Kale"

from .context import gjk