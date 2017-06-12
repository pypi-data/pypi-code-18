# -*- coding: utf-8 -*-
import GeoFunctions as geo
import DataFunctions as data
import os
import pandas as pd
import numpy as np
import pytz
reload(data)
reload(geo)

"""
Since NOAA's API changed and the LCD API is under development, this module will
be re-implemented with LCD and TMY export classes in expors.py
"""


def get_historical_weather(input_dir, output_dir, idy, zipcode,
                           start_date, end_date, w):
    """
       """
    # Download Historical Data
    output = output_dir
    stations_file = input_dir + '\\stations.csv'
    options_file = input_dir + '\\options.csv'
    if not os.path.exists(output):
        print "Output directory not found as relative path"
        if os.path.exists(os.path.abspath(output)):
            print "Found output directory as absolute path"
            output = os.path.abspath(output)
        else:
            print "Output directory not found as absolute path"
            print "Creating output directory: %s" % output
            os.makedirs(output)
    all_stations = geo.import_station_df(stations_file)
    x = np.nan
    addresses = pd.DataFrame(data=[[idy, x, x, x, x, x, x, zipcode, x,
                                    x, start_date, end_date, 'hourly', x]],
                             columns=['Site ID', 'Unformatted Address',
                                      'Street Address', 'City', 'State',
                                      'ZIP', 'ZIP+4', 'Lookup Address',
                                      'Lat', 'Lon', 'Start Date', 'End Date',
                                      'Data Period', 'Preferred Station WBAN'])
    addresses['Start Date'] = pd.to_datetime(
        addresses['Start Date']).dt.tz_localize('US/Eastern')
    addresses['End Date'] = pd.to_datetime(
        addresses['End Date']).dt.tz_localize('US/Eastern')
    options = pd.read_csv(
        options_file, dtype={'Station Type': str, 'Include': bool})
    options.index = options['Station Type']
    del options['Station Type']
    options = options.iloc[0:6]['Include'].to_dict()
    # Initialize the geocoder
    geocoder = geo.initiate_geolocator()
    # Geocode the addresses and match to nearest station
    coded_addresses = geo.geocode_addresses(addresses, geocoder)
    match_stations = geo.get_eligible_stations(all_stations, options)
    coded_addresses = geo.find_stations(coded_addresses, match_stations)
    return coded_addresses['TMY3 USAF ID'].iloc[0], coded_addresses['Matched WBAN'].iloc[0]
    # Group by station and export data
    wgrp2 = coded_addresses.groupby(['Matched WBAN', 'Data Period'])
    # TODO: Adapt to new API, this call is not broken
    # data.export_data_for_addresses(
    #     coded_addresses, wgrp2, match_stations, output)
    # Process Historical Data
    summary_path = output_dir + '\\summary.csv'
    summary_df = pd.read_csv(summary_path, dtype=str)
    idy_row = summary_df[summary_df['Site ID'] == idy]
    wban = str(idy_row.iloc[0]['Matched WBAN'])
    df = pd.read_csv(output_dir + '\\' +
                     wban + '.csv', dtype=str,

                     error_bad_lines=False)
    for column_id in df.columns:
        keep = ['Date', 'Time', 'DryBulbFarenheit', 'RelativeHumidity',
                'WindSpeed']
        # keep = ['Date', 'Time', 'WetBulbFarenheit', 'RelativeHumidity']
        if column_id not in keep:
            del df[column_id]
    df['Date'] = df['Date'].astype(str)
    df['Date'] = (df['Date'].str[0:4] + '/' + df['Date'].str[4:6] +
                  '/' + df['Date'].str[6:])
    df['Time'] = df['Time'].astype(str)
    df['Time'] = df['Time'].str[0:-2] + ':' + df['Time'].str[-2:]
    df['Time'][df['Time'].str[0] == ':'] = '0' + df['Time']
    df.index = df['Date'] + ' ' + df['Time']
    del df['Date'], df['Time']
    df.columns = ['Tdb [deg F]', 'RH [%]', 'Wind Speed [mi/h]']
    # df.columns = ['Twb [deg F]', 'RH [%]']
    df.index = pd.to_datetime(df.index, format='%Y/%m/%d %H:%M')
    df.index = df.index.tz_localize(
        pytz.FixedOffset(-5 * 60)).tz_convert('UTC')
    df.replace('M', np.nan, inplace=True)
    df.replace('  ', np.nan, inplace=True)
    df = df.astype(float)
    df = df.resample(w).mean()
    inter_lim = 61
    df.interpolate(inplace=True,
                   limit=inter_lim, limit_direction='both')
    df = df.ix[start_date:end_date]
    hist_t = df['Tdb [deg F]']
    # hist_t = df['Twb [deg F]']
    hist_rh = df['RH [%]']
    hist_ws = df['Wind Speed [mi/h]']
    return hist_t, hist_rh, hist_ws


def get_normal_weather(usaf, start_date, end_date, w):
    """
       """
    # def get_normal_weather(idy, start_date, end_date, input_dir, w):
    # Download and process normal data
    # summary_path = input_dir + '\\summary.csv'
    # summary_df = pd.read_csv(summary_path, dtype=str)
    # idy_row = summary_df[summary_df['Site ID'] == idy]
    # usaf = str(idy_row.iloc[0]['TMY3 USAF ID'])
    usaf_ids = usaf
    usaf_ids = usaf_ids + 'TY.csv'
    tmy_path = r'\\cadmusgroup.org\energy\weather$\TMY3\station files'
    for station_id in os.listdir(tmy_path):
        if station_id == usaf_ids:
            df = pd.read_csv(tmy_path + '\\' + station_id,
                             low_memory=False,
                             header=1)
            for column_id in df.columns:
                keep = ['Date (MM/DD/YYYY)', 'Time (HH:MM)',
                        'Dry-bulb (C)', 'RHum (%)', 'Wspd (m/s)']
                if column_id not in keep:
                    del df[column_id]
            df['Time (HH:MM)'][
                df['Time (HH:MM)'] == '24:00'] = '00:00'
            frames = list()
            start_year = int(start_date.split('/')[2])
            end_year = int(end_date.split('/')[2])
            for i in np.arange(start_year, end_year + 1, 1):
                temp_df = df.copy()
                temp_df['Date (MM/DD/YYYY)'] = temp_df[
                    'Date (MM/DD/YYYY)'].str[0:6] + str(i)
                frames.append(temp_df)
            df = pd.concat(frames)
            df.index = df['Date (MM/DD/YYYY)'] + ' ' + df[
                'Time (HH:MM)']
            del df['Date (MM/DD/YYYY)'], df['Time (HH:MM)']
            df.index = pd.to_datetime(
                df.index, format='%m/%d/%Y %H:%M')
            df.index = df.index.tz_localize(
                pytz.FixedOffset(-5 * 60)).tz_convert('UTC')
            df = df.astype(float)
            df = df.resample(w).mean()
            inter_lim = 61
            df.interpolate(inplace=True,
                           limit=inter_lim, limit_direction='both')
            df = df.ix[start_date:end_date]
            df['Dry-bulb (C)'] = df['Dry-bulb (C)'] * 9 / 5. + 32.
            df['Wspd (m/s)'] = df['Wspd (m/s)'] * 2.237
            df.columns = ['Tdb [deg F]', 'RH [%]', 'Wind Speed [mi/h]']
            norm_t = df['Tdb [deg F]']
            norm_rh = df['RH [%]']
            norm_ws = df['Wind Speed [mi/h]']
            return norm_t, norm_rh, norm_ws
