###   SGP30   ###m,
import seeed_sgp30
from grove.i2c import Bus

sgp30 = seeed_sgp30.grove_sgp30(Bus())

#functions to read measurements from the sensors
def sgp30_get_voc():
    data = sgp30.read_measurements()
    tvoc_ppb, co2_eq_ppm =data.data
    tvoc_ppb=round((tvoc_ppb),2)
    tvoc_ppb=str(tvoc_ppb)
    return(tvoc_ppb)

def sgp30_get_eco2():
    data = sgp30.read_measurements()
    tvoc_ppb, co2_eq_ppm=data.data
    co2_eq_ppm=round((co2_eq_ppm),2)
    co2_eq_ppm=str(co2_eq_ppm)
    return (co2_eq_ppm)
