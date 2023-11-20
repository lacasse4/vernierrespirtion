class Peak():
    '''
    This class represents a peak in a one dimension signal
    Various function are provided:
    - self.erase(): resets a peak to a 'not found' state
    - find_peak():  creates a peak object and find the highest peak within the given signal index range
    - find_peak_precise(): creates a peak object and find the highest peak with precise location
                           and precise value within the given signal index range
    - find_peak_with_unit(): creates a peak object and find the highest peak with precise location
                             and precise value within the given range provided in units as defined
                             by the user.
    '''
    
    def __init__(self):
        self.erase()
        
    def erase(self):
        self.position = -1           # peak index in signal array (-1 if peak was not found)
        self.value = 0.0             # signal value where its peak was found
        self.precise_position = 0.0  # peak index with increased precision
        self.precise_value = 0.0     # signal value with increased precision
        self.scaled_position = 0.0   # precise position scaled to unit

    def __str__(self):  
        return str(vars(self))

    def get_accurate_peak(self, signal: list):
        # find peak accuratly
        i = self.position
        delta = (signal[i-1] - signal[i+1]) * 0.5 / (signal[i-1] - (2.0 * signal[i]) + signal[i+1])
        self.precise_position = i + delta
        self.precise_value = (signal[i-1] + (2.0 * signal[i]) + signal[i+1]) / 4
        return self


def find_peak(signal: list, start_index: int, stop_index: int) -> Peak:
    # create a Peak object and populate it with the highest signal value within range 
    peak = Peak()
    not_found = Peak()

    # check input parameters
    if start_index < 0:           return not_found
    if stop_index >= len(signal): return not_found

    # find max peak in specified range
    position = start_index
    value = signal[start_index]
    for i in range(start_index, stop_index+1): 
        if value < signal[i]:
            value = signal[i]
            position = i

    # a peak can not be at a boundary value
    if position == start_index: return not_found
    if position == stop_index:  return not_found

    # return result
    peak.position = position
    peak.value = value
    return peak

def find_peak_precise(signal: list, start_index: int, stop_index: int) -> Peak:
    # find peak precisely within range start_index to stop_index
    peak = find_peak(signal, start_index, stop_index)
    if peak.position == -1: return peak
    return peak.get_accurate_peak(signal)

def find_peak_with_unit(signal: list, from_unit: float, to_unit: float, samples_per_unit: float) -> Peak:
    # find peak precisely within from-to range using units provided 
    start_index = round(from_unit * samples_per_unit)
    stop_index  = round(to_unit   * samples_per_unit)
    peak = find_peak_precise(signal, start_index, stop_index)
    peak.scaled_position = peak.precise_position / samples_per_unit
    return peak

