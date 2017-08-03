class PID:
    """PID Controller"""

    def __init__(self, timestamp=0, k_p=0.2, t_i=0.0, t_d=0.0, max_out=100.0, set_point=25):

        self.SetPoint = set_point

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
        """ Clears PID computations """
        self.last_time = timestamp
        self.last_error = 0
        self.last_i = 0

    def update(self, feedback_value, timestamp):
        """ Calculates PID value for given reference feedback """
        error = self.SetPoint - feedback_value

        delta_time = timestamp - self.last_time

        p = error
        i = self.last_i + (error + self.last_error) * delta_time / 2
        if self.Ti != 0:
            i /= self.Ti
        d = (error - self.last_error) * self.Td
        if delta_time != 0:
            d /= delta_time

        pid = self.Kp * (p + i + d)

        # Windup guard.
        if pid > self.windup_guard:
            pid = self.windup_guard
            i = pid / self.Kp - (p + d)
        elif pid < -self.windup_guard:
            pid = -self.windup_guard
            i = pid / self.Kp - (p + d)

        # Remember last time and last error for next calculation
        self.last_time = timestamp
        self.last_error = error
        self.last_i = i

        return pid

    def set_point(self, set_p):
        self.SetPoint = set_p

    def set_kp(self, proportional_gain):
        self.Kp = proportional_gain

    def set_ti(self, integral_gain):
        self.Ti = integral_gain

    def set_td(self, derivative_gain):
        self.Td = derivative_gain
