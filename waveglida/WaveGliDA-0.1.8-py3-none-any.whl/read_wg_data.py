#!/usr/bin/env python

"""
This script reads the output from txt files produced by the CSIR waveglider.
This is the data that has already been processed by Clinton's script.
"""


def main():
    from glob import glob
    # from matplotlib.pylab import show
    from calculations import do_calculations

    flist = glob('../test_data/STS_sensor/txt/*.txt')
    df = read_wg_flist(flist)

    print (do_calculations(df))


# This is a dictionary of functions associated with the length of a batch.
# The aim of the functions is to make the length of the lines 123 columns.
# If a new sensor is added, these will have to be modified
# NOTE: This is very specific to this WG setup.
# This will have to be changed for each set based on the input columns
# see cols for more info
# TODO: This could be moved into a config file eventually. Documentation then needs to be good
reshape_funcs = {
    # system restart creates cols to skip in beginning - thus slice starts at 7
    130: lambda x: x[slice(7, len(x))],  # calibration with system restart
    123: lambda x: x[slice(0, len(x))],  # calibration
    # calibration occupies 46 cols after the 10 meta data columns
    77: lambda x: x[slice(0, 10)] + ["NaN"] * 46 + x[slice(10, len(x))],  # no calibration
    84: lambda x: x[slice(7, 17)] + ["NaN"] * 46 + x[slice(17, len(x))],  # no calibration with system restart
}

# Column headers. This list is NB: incorrect length and it will fail.
# The reshape_funcs are very dependent on this list.
cols = [
    # metadata columns = 10L
    "Date", "Time",
    "Latitude", "Longitude",
    "Status_Flags",
    "Enclosure_Press_Ave",
    "Enclosure_Temp_Ave",
    "Enclosure_RH_Ave",
    "PCB_Temp_Ave",

    "SENSOR_CO2",
    # Calibration columns = 46L
    "Zero_Temp_Ave", "Zero_Temp_SD",
    "Zero_Press_Ave", "Zero_Press_SD",
    "Zero_CO2_Ave", "Zero_CO2_SD",
    "Zero_RH_Ave", "Zero_RH_SD",
    "Zero_RH_Temp_Ave", "Zero_RH_Temp_SD",
    "Zero_Raw_1", "Zero_Raw_2",
    "Span_Pump_On_Temp_Ave", "Span_Pump_On_Temp_SD",
    "Span_Pump_On_Press_Ave", "Span_Pump_On_Press_SD",
    "Span_Pump_On_CO2_Ave", "Span_Pump_On_CO2_SD",
    "Span_Pump_On_RH_Ave", "Span_Pump_On_RH_SD",
    "Span_Pump_On_RH_Temp_Ave", "Span_Pump_On_RH_Temp_SD",
    "Span_Pre_Temp_Ave", "Span_Pre_Temp_SD",
    "Span_Pre_Press_Ave", "Span_Pre_Press_SD",
    "Span_Pre_CO2_Ave", "Span_Pre_CO2_SD",
    "Span_Pre_RH_Ave", "Span_Pre_RH_SD",
    "Span_Pre_RH_Temp_Ave", "Span_Pre_RH_Temp_SD",
    "Span_Pre_Raw_1", "Span_Pre_Raw_2",
    "Span_Post_Temp_Ave", "Span_Post_Temp_SD",
    "Span_Post_Press_Ave", "Span_Post_Press_SD",
    "Span_Post_CO2_Ave", "Span_Post_CO2_SD",
    "Span_Post_RH_Ave", "Span_Post_RH_SD",
    "Span_Post_RH_Temp_Ave", "Span_Post_RH_Temp_SD",
    "Span_Post_Raw_1", "Span_Post_Raw_2",
    # measurement columns = 50L
    "EQ_Pump_On_Temp_Ave", "EQ_Pump_On_Temp_SD",
    "EQ_Pump_On_Press_Ave", "EQ_Pump_On_Press_SD",
    "EQ_Pump_On_CO2_Ave", "EQ_Pump_On_CO2_SD",
    "EQ_Pump_On_RH_Ave", "EQ_Pump_On_RH_SD",
    "EQ_Pump_On_RH_Temp_Ave", "EQ_Pump_On_RH_Temp_SD",
    "EQ_Temp_Ave", "EQ_Temp_SD",
    "EQ_Press_Ave", "EQ_Press_SD",
    "EQ_CO2_Ave", "EQ_CO2_SD",
    "EQ_RH_Ave", "EQ_RH_SD",
    "EQ_RH_Temp_Ave", "EQ_RH_Temp_SD",
    "EQ_Raw_1", "EQ_Raw_2",
    "Air_Pump_On_Temp_Ave", "Air_Pump_On_Temp_SD",
    "Air_Pump_On_Press_Ave", "Air_Pump_On_Press_SD",
    "Air_Pump_On_CO2_Ave", "Air_Pump_On_CO2_SD",
    "Air_Pump_On_RH_Ave", "Air_Pump_On_RH_SD",
    "Air_Pump_On_RH_Temp_Ave", "Air_Pump_On_RH_Temp_SD",
    "Air_Temp_Ave", "Air_Temp_SD",
    "Air_Press_Ave", "Air_Press_SD",
    "Air_CO2_Ave", "Air_CO2_SD",
    "Air_RH_Ave", "Air_RH_SD",
    "Air_RH_Temp_Ave", "Air_RH_Temp_SD",
    "Air_Raw_1", "Air_Raw_2",
    "Zero_Cal_K", "Span_Cal_K",
    "Ocean_CO2_Ave", "Atmosphere_CO2_Ave",

    "SENSOR_PH",
    # PH columns = 11L
    "PH_Int", "PH_Ext", "FET_Temp",
    "FET_Voltage_Int", "FET_Voltage_Ext",
    "Voltage_Thermistor", "Supply_Voltage",
    "Supply_Current", "Enclosure_RH", "SeaFET_Status",

    "SENSOR_CTD",
    # CTD columns = 2L
    "CTD_Temp", "CTD_Conductivity",

    "SENSOR_O2",
    # O2 columns = 4L
    "O2_Phase_Delay", "O2_Therm_Voltage", "O2_Calculated", "O2_Temp",
]


def read_wg_flist(flist, verbose=False):
    """
    Reads a list of waveglider files and returns a pandas.DataFrame.
    The function, flatten_wg_file, reads a wg.txt and reshapes each batch
    onto one line, creating a ndarray with dims: batches, 123
    The ndarrays are concatenated and made into a pandas.DataFrame.
    """

    from re import split
    from numpy import ndarray, delete, concatenate
    from pandas import DataFrame, to_datetime

    def flatten_wg_file(fname):
        """
        1. seperate batches (\n\n)
        2. split batches and transform using reshape_funcs (potential API)
        3. put standard batch in ndarray and delete skipped batches
        """
        txt = open(fname).read()

        # split the batches if a blank line occurs
        batches = split('\n\n', txt, flags=16)  # 16 is re.DOTALL

        # premade ndarray with a standard size (n, cols)
        # much quicker than using lists (have checked this)
        strung_file = ndarray([len(batches), len(cols)], dtype='|U25')

        skipped = []  # for deleting
        for c, batch in enumerate(batches):
            # put everything on one line and split it by spaces
            line = batch.replace('\n', ' ').split()
            L = len(line)

            # reshape_funcs is a dict of expected lengths with functions
            # of what to do when that length is found. Skip the line if
            # it is not found in the dictionary
            if L not in reshape_funcs:
                skipped += c,
                if verbose == 2:
                    print (line)
                continue

            func = reshape_funcs[L]
            strung_file[c, :] = func(line)
        strung_file = delete(strung_file, skipped, axis=0)

        return strung_file

    # append the ndarrays and concatenate them
    list_of_flat_files = []
    for fname in flist:
        if verbose:
            print (fname)
        list_of_flat_files += flatten_wg_file(fname),
    ndarr_of_flat_files = concatenate(list_of_flat_files, axis=0)

    # Create Dataframe
    df = DataFrame(ndarr_of_flat_files, columns=cols)

    # Make numeric columns float32
    df = df.apply(lambda x: x.astype(float, raise_on_error=False), axis=0)

    # Create a datetime array which will become the index
    df['space'] = ' '
    datetime = df.ix[:, ['Date', 'space', 'Time']].sum(axis=1)
    df['Datetime'] = to_datetime(datetime, errors='coerce')
    df = df.set_index('Datetime').sort_index()

    # Drop columns that are not needed - these include sensor names
    drop_cols = df.filter(regex='SENSOR*|space|Date$|Time', axis=1).columns
    df = df.drop(drop_cols, axis=1)

    # Fix coordinates (DDMM.dec)
    df.Latitude /= 100.
    df.Longitude /= 100.
    ydeg = df.Latitude // 1
    xdeg = df.Longitude // 1
    ymin = (df.Latitude - ydeg) / .6
    xmin = (df.Longitude - xdeg) / .6
    df['Latitude'] = ydeg + ymin
    df['Longitude'] = xdeg + xmin

    return df


if __name__ == '__main__':
    main()
