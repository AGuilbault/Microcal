#!/usr/bin/python
#
# This file is part of IvPID.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# IvPID is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IvPID is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# title           :PID.py
# description     :python pid controller
# author          :Caner Durmusoglu
# date            :20151218
# version         :0.1
# notes           :
# python_version  :2.7
# ==============================================================================

"""Ivmech PID Controller is simple implementation of a Proportional-Integral-Derivative (PID) Controller in the Python
Programming Language. More information about PID Controller: http://en.wikipedia.org/wiki/PID_controller
"""


class PID:
    """PID Controller"""

    def __init__(self, timestamp, k_p=0.2, t_i=0.0, t_d=0.0, max_out=100.0):

        self.SetPoint = 0.0

        self.Kp = k_p
        self.Ti = t_i
        self.Td = t_d

        # Windup Guard
        self.windup_guard = max_out

        # Remember last time and last error for next calculation
        self.last_time = timestamp
        self.last_error = 0
        self.last_i = 0

    def clear(self, timestamp):
        """Clears PID computations and coefficients"""
        self.last_time = timestamp
        self.last_error = 0
        self.last_i = 0

    def update(self, feedback_value, timestamp):
        """Calculates PID value for given reference feedback"""
        error = self.SetPoint - feedback_value
        delta_error = error - self.last_error

        delta_time = timestamp - self.last_time

        p = error

        i = self.last_i + (error + self.last_error) * delta_time / (2 * self.Ti)

        d = error - self.last_error
        if delta_time > 0:
            d = delta_error * self.Td / delta_time

        pid = self.Kp * (p + i + d)
        if pid > self.windup_guard:
            pid = self.windup_guard
            i = pid - p - d
        elif pid < -self.windup_guard:
            pid = -self.windup_guard
            i = pid - p - d

        # Remember last time and last error for next calculation
        self.last_time = timestamp
        self.last_error = error
        self.last_i = i

        return pid

    def set_kp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.Kp = proportional_gain

    def set_ti(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.Ti = integral_gain

    def set_td(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.Td = derivative_gain
