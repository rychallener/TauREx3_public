"""Includes some useful definitions and enums"""
from enum import Enum


class OutputSize(Enum):
    """
    This enum describes how heavy the final output will be
    """

    heavy = 5
    """Output everything native and binned (large file size)"""
    light = 3
    """Output everything but only keep binned optical depths"""
    lighter = 1
    """Do not output optical depths"""
