class PID:
    """
    PID Controller
    """

    def __init__(self, timestamp=0, k_p=0.2, t_i=0.0, t_d=0.0, maximum=100.0, set_point=25):

        self.SetPoint = set_point

        self.Kp = k_p
        self.Ti = t_i
        self.Td = t_d

        # Windup Guard
        self.Guard = maximum

        # Remember last time and last error for next calculation
        self.last_timestamp = timestamp
        self.last_error = 0
        self.last_integral = 0

    def clear(self, timestamp):
        """Clears PID computations."""
        self.last_timestamp = timestamp
        self.last_error = 0
        self.last_integral = 0

    def update(self, feedback_value, timestamp):
        """
        Computes PID value for given reference feedback and timestamp.
        
                 /             t                  \
                 |            /                   |
                 |        1  |               de(t)|
        PID = Kp |e(t) + --  | e(t) dt + Td ------|
                 |       Ti  |               dt   |
                 |          /                     |
                 \           0                    /
        
        """
        # Compute e(t).
        error = self.SetPoint - feedback_value
        # Compute dt.
        delta_time = timestamp - self.last_timestamp

        # Proportionnal value.
        p = error

        # Integral value.
        i = (error + self.last_error) * delta_time / 2
        if self.Ti != 0:
            i /= self.Ti
        i += self.last_integral

        # Derivative value.
        d = (error - self.last_error) * self.Td
        if delta_time != 0:
            d /= delta_time

        # Sum PID values.
        pid = self.Kp * (p + i + d)

        # Check if value is bigger than maximum output.
        if abs(pid) > self.Guard:
            pid = self.Guard if pid > 0 else -self.Guard
            # Limit integral while output is at maximum.
            i = pid / self.Kp - (p + d)

        # Remember last timestamp, error and integral for next calculation.
        self.last_timestamp = timestamp
        self.last_error = error
        self.last_integral = i

        # Return output.
        return pid

    def set_point(self, set_p):
        """Changes the PID setpoint value."""
        self.SetPoint = set_p

    def set_kp(self, proportional_gain):
        """Changes the PID proportionnal constant."""
        self.Kp = proportional_gain

    def set_ti(self, integral_gain):
        """Changes the PID integration time constant."""
        self.Ti = integral_gain

    def set_td(self, derivative_gain):
        """Changes the PID derivative time constant."""
        self.Td = derivative_gain

    def set_guard(self, maximum):
        """Changes the PID maximum output value."""
        self.Guard = maximum
