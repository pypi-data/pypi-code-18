from __future__ import print_function
import easyaccess as ea
import pandas as pd
import numpy as np
import ephem
from Orbit import Orbit
from calendar import monthrange
from MPCRecord import MPCToTNO


class Connect:
    """
    Interacts with TNO database on DESOPER.
    
    """

    def __init__(self):
        # connect to desoper and destest once
        self.desoper = ea.connect(section='desoper')
        self.destest = ea.connect(section='destest')

    def add_candidate_from_csv(self, csv_file, season=None, name="", prepend_cand_info=True):
        """
        Adds candidate to database from csv file.
        
        Args:
            csv_file (str): File path for csv file containing at minimum columns 'date', 'ra', 'dec'.
                Other recognized column names include 'objid', 'expnum', 'exptime', 'band', 'ccd', 'mag',
                'ml_score', 'fakeid', and 'designation'.
            season (int): specifies season of candidate
            name (str): Specifies name of candidate. Defaults to the csv filename
            prepend_cand_info (bool): specifies whether canid will have an informational prefix attached to the
                beginning of it. Ex: "S1Y1NF_"
            
        """
        can_table = pd.read_csv(csv_file)
        if not name:
            name = csv_file.split('/')[-1]
            name = name.split('.')[0]

        return self.add_candidate(can_table, season=season,
                                  name=name, prepend_cand_info=prepend_cand_info)

    def add_candidate_from_mpc(self, file_path, canid):
        """
        Adds object to database from an text file with observations in mpc format.
        
        Args:
            file_path (str): file path for text file with mpc observations. Can be absolute or relative
            canid (str): candidate id to go into database

        """
        mpc_file = open(file_path, "r")
        obj = MPCToTNO(mpc_file.read())
        desig = obj.observations['designation'][0]
        self.add_candidate(obj.observations, name=canid, designation=desig, prepend_cand_info=False)

    def add_candidate(self, can_table, season=None, name="", designation="", prepend_cand_info=True):
        """
        Adds candidate to database if candidate is unique.

        Args:
            can_table (pd.DataFrame): DataFrame that represents a single candidate. The table should have columns 
                date, ra, dec.
            season (int): specifies season of candidate
            name (str): Name of candidate
            designation (str): Optional designation of candidate
            prepend_cand_info (bool): specifies whether canid will have an informational prefix attached to the
                beginning of it. Ex: "S1Y1NF_"

        """
        try:
            cursor = self.desoper.cursor()

            if 'objid' not in can_table.columns:
                can_table = can_table.assign(objid=pd.Series(data=self.__create_obj_ids(len(can_table.index))))

            if 'fakeid' not in can_table.columns:
                # assume if no fakeid that object is real
                can_table = can_table.assign(fakeid=pd.Series(np.zeros(len(can_table.index))))

            index = []

            objid_index = []
            for i, row in can_table.iterrows():

                if not (self.__comment(row) or self.__duplicate_obs(row)):
                    index.append(i)

                    if not self.__valid_obj_id(row['objid']):
                        objid_index.append(i)

            new_obj_ids = self.__create_obj_ids(len(objid_index))

            # loop through can_table indices that need new objids
            j = 0
            for i in objid_index:
                can_table['objid'][i] = new_obj_ids[j]
                j += 1

            canid = self.__find_canid(can_table, season, name, prepend_cand_info)
            orbid = self.__create_orbit_id()

            orbcmd = self.__write_orb(can_table, canid, orbid, designation=designation)

            linkcmds = self.__write_linker(canid, can_table, orbid)

            objcmds = self.__write_obs(index, can_table)

            if not designation:
                statcmd = ("INSERT INTO LZULLO.TNOSTAT(ID, EXTENDED, VISUAL, ACCEPT, QUAL_FLAG, INSPECT_TIME, ANALYST, "
                           "ANALYST_COMMENT) VALUES ('" + canid + "', '0', '0','0', '0' ,'UNINSPECTED', "
                           "'LZULLO', 'NONE')")
            else:
                statcmd = ("INSERT INTO LZULLO.TNOSTAT(ID, EXTENDED, VISUAL, ACCEPT, QUAL_FLAG, INSPECT_TIME, ANALYST, "
                           "ANALYST_COMMENT) VALUES ('" + designation + "', '0', '0','1', '0' , 'UNINSPECTED', "
                           "'LZULLO', 'KNOWN_OBJECT')")
            # cursor.execute(candcmd)

            try:
                cursor.execute(orbcmd)
            except:
                raise RuntimeError("Orbit Command Failure\n" + orbcmd)

            for l in linkcmds:
                try:
                    cursor.execute(l)
                except:
                    raise RuntimeError("Link Command Failure\n" + l)

            for o in objcmds:
                try:
                    cursor.execute(o)
                except:
                    raise RuntimeError("Object Command Failure\n" + o)
            try:
                cursor.execute(statcmd)
            except:
                raise RuntimeError("Stat Command Failure\n" + statcmd)

        except RuntimeError:
            raise

    # def update_observation(self, observation, objid=None, overwrite=None):
    #     """
    #
    #     Args:
    #         observation (pd.Series): data series representing new info to be merged in
    #         objid (int): if given, overrides default behavior of merging on observation['objid']
    #             and instead merges with observation with given objid. Note that objid may change
    #             to observation['objid'] depending on overwrite.
    #         overwrite (str): 'n' -> when conflicts occur, overwrite old values with new values
    #
    #             'o' -> when conflicts occur, keep old values
    #
    #             default -> when conflicts occur, prompt for user input
    #
    #     Returns:
    #
    #     """
    #     if not objid:
    #         objid = observation['objid']
    #     query = "SELECT * FROM LZULLO.TNOBS WHERE LZULLO.TNOBS.OBJID = " + str(objid)
    #
    #     output_obs = pd.Series(observation)
    #     matching_obs_df = pd.read_sql(query, self.desoper)
    #     if matching_obs_df.empty:
    #         raise RuntimeError("No observation in tnobs matches objid")
    #
    #     matching_obs = pd.Series(matching_obs_df[0])
    #
    #     matching_destest = self.__access_destest(observation['objid'])
    #     if not matching_destest.empty:
    #         matching_destest = pd.Series(matching_destest[0])
    #         for i in matching_destest.index:
    #             output_obs[i] = matching_destest[i]
    #
    #     for i in matching_obs.index:
    #         if matching_obs[i]:
    #             if i in output_obs.index:
    #                 if output_obs[i]:
    #                     if
    #

    def get_values(self, table, column, value):
        """
        Gets values from table with column = value. Equivalent to 
            'SELECT * FROM LZULLO.[table] WHERE [column] = [value]'
        Args:
            table (str): table to get values from
            column: column for condition
            value: value of condition

        Returns:
            pd.DataFrame: Table of matching values

        """
        cmd = "SELECT * FROM LZULLO." + str(table) + " WHERE " + str(column) + "=" + str(value)
        return pd.read_sql(cmd, self.desoper)

    def rm_cand(self, canid):
        """
        Removes candidate from TNORBIT, TNOLINK, TNOSTAT
        
        Args:
            canid (str): canid of object to be removed

        """
        cursor = self.desoper.cursor()

        orbcmd = "DELETE FROM LZULLO.TNORBIT WHERE ID=" + str(canid)
        linkcmd = "DELETE FROM LZULLO.TNOLINK WHERE ID=" + str(canid)
        statcmd = "DELETE FROM LZULLO.TNOSTAT WHERE ID=" + str(canid)

        try:
            cursor.execute(orbcmd)
            cursor.execute(linkcmd)
            cursor.execute(statcmd)
            print(str(canid) + " DELETED")
        except:
            raise RuntimeError("No orbit named " + str(canid) + "\n")

    def execute(self, cmd):
        """
        Execute command and return results (if command begins with 'SELECT')
        
        Args:
            cmd: Command to be executed

        Returns:
            pd.DataFrame: DataFrame of matching values for 'SELECT', otherwise returns nothing.
        """
        if cmd.upper().startswith("SELECT"):
            return pd.read_sql(cmd, self.desoper)
        else:
            cursor = self.desoper.cursor()
            cursor.execute(cmd)

    # private helper methods
    # -------------------------

    def __write_linker(self, canid, can_table, orbid):
        """
        
        Args: 
            canid (str): Candidate ID as a string
            can_table (pd.DataFrame):  A dataframe of observations
            orbid (str): Unique orbit ID that corresponds to a set of observations in the linker

        Returns: 
            A list of commands to be run by the cursor.  Populates linker with object IDs and corresponding object IDs

        """

        linkcmds = []
        for index, row in can_table.iterrows():
            if not self.__comment(row):
                linkcmds += ["INSERT INTO LZULLO.TNOLINK (ID, OBJID, ORBID) \
                VALUES ('" + canid + "', " + str(can_table['objid'][index]) + ", " + orbid + ")"]

        return linkcmds

    def __write_obs(self, index, can_table):
        """
        
        Args:
            index: A dataframe of new observations not in LZULLO.TNOBS
            can_table: Dataframe of candidate observations

        Returns:
            List of commands that insert a new observation into TNOBS
        """
        objcmds = []

        if 'date' not in can_table.columns:
            raise RuntimeError("Candidate table must have column 'date'")

        if 'ra' not in can_table.columns:
            raise RuntimeError("Candidate table must have column 'ra'")

        if 'dec' not in can_table.columns:
            raise RuntimeError("Candidate table must have column 'dec'")

        if 'objid' not in can_table.columns:
            raise RuntimeError("Candidate table must have column 'objid'")

        for i in index:
            # Insertion formatting
            date_obs = "'" + str(can_table['date'][i]) + "'"
            ra = "'" + str(can_table['ra'][i]) + "'"
            dec = "'" + str(can_table['dec'][i]) + "'"

            expnum = str(can_table['expnum'][i]) if 'expnum' in can_table.columns else "NULL"

            exptime = str(can_table['exptime'][i]) if 'exptime' in can_table.columns else "NULL"

            band = "'" + str(can_table['band'][i]) + "'" if 'band' in can_table.columns else "NULL"

            ccd = str(can_table['ccd'][i]) if 'ccd' in can_table.columns else "NULL"
            mag = str(can_table['mag'][i]) if 'mag' in can_table.columns else "NULL"

            ml_score = str(can_table['ml_score'][i]) if 'ml_score' in can_table.columns else "NULL"

            # Fix for non float values in ml_score table
            if not ml_score.replace('.', '', 1).isdigit():
                ml_score = "NULL"

            # These vars specifically for known objects
            pixelx = str(can_table['pixelx'][i]) if 'pixelx' in can_table.columns else "NULL"
            pixely = str(can_table['pixely'][i]) if 'pixely' in can_table.columns else "NULL"
            fwhm = str(can_table['fwhm'][i]) if 'fwhm' in can_table.columns else "NULL"

            # Fix for non float values in fwhm
            if not fwhm.replace('.', '', 1).isdigit():
                fwhm = "NULL"

            objid = str(can_table['objid'][i])

            year = self.__find_year(can_table['date'][i])

            # DESTEST information
            destest_list = self.__access_destest(objid)

            if len(destest_list) > 0:
                nite = destest_list.iloc[0]['NITE']
                flux = destest_list.iloc[0]['FLUX']
                flux_err = destest_list.iloc[0]['FLUX_ERR']
                season = destest_list.iloc[0]['SEASON']
            else:
                nite = "NULL"
                flux = "NULL"
                flux_err = "NULL"
                season = "NULL"

            if not str(can_table['fakeid'][i]).replace('.', '', 1).isdigit():
                fakeid = "NULL"
            elif not (can_table['fakeid'][i] == 0 or can_table['fakeid'][i] > 1):
                raise RuntimeError("fakeid must be 0 or a positive value")
            else:
                fakeid = can_table['fakeid'][i]

            objcmds += ["INSERT INTO lzullo.TNOBS (DATE_OBS, RA, DEC, EXPNUM, EXPTIME, BAND, CCD, MAG , ML_SCORE, "
                        "OBJID, FAKEID, NITE, FLUX, FLUX_ERR, SEASON, YEAR, PIXELX, PIXELY, FWHM ) VALUES (" + date_obs
                        + "," + ra + "," + dec + "," + expnum + "," + exptime + "," + band + "," + ccd + "," + mag + ","
                        + ml_score + "," + objid + "," + str(fakeid) + "," + nite + "," + str(flux) + "," +
                        str(flux_err) + "," + str(season) + "," + str(year) + "," + pixelx + "," + pixely
                        + "," + fwhm + ")"]
        return objcmds

    def __write_orb(self, can_table, canid, orbid, designation=""):
        """
        
        Args:
            can_table: Dataframe of candidate observations
            canid: Candidate ID that corresponds to candidate (string)
            orbid: Unique randomly generated integer value that indicates a unique orbit
            designation: MPC designation
        Returns:
            A string command that writes the orbit to TNORBIT
        """

        df = can_table
        orb = self.__fit_orbit(df)

        # Not necessary if already connected to desoper

        # cursor = self.desoper.cursor()
        orbitdf = orb.orbit2df()

        # barycentric distance value only found via method

        # baryc = orb.barycentric_distance()
        # baryc_dist = str(baryc[0])
        # baryc_error = str(baryc[1])

        # defining all vars for easy object manipulation

        chisq = orbitdf.iloc[0]['chisq']
        ndof = orbitdf.iloc[0]['ndof']
        a = orbitdf.iloc[0]['a']
        e = orbitdf.iloc[0]['e']
        inc = orbitdf.iloc[0]['inc']
        aop = orbitdf.iloc[0]['aop']
        node = orbitdf.iloc[0]['node']
        peri_jd = orbitdf.iloc[0]['peri_jd']
        peri_date = orbitdf.iloc[0]['peri_date']
        epoch_jd = orbitdf.iloc[0]['epoch_jd']
        mean_anomaly = orbitdf.iloc[0]['mean_anomaly']
        period = orbitdf.iloc[0]['period']
        period_err = orbitdf.iloc[0]['period_err']
        a_err = orbitdf.iloc[0]['a_err']
        e_err = orbitdf.iloc[0]['e_err']
        inc_err = orbitdf.iloc[0]['inc_err']
        aop_err = orbitdf.iloc[0]['aop_err']
        node_err = orbitdf.iloc[0]['node_err']
        peri_err = orbitdf.iloc[0]['peri_err']
        latO = orbitdf.iloc[0]['lat0']
        lonO = orbitdf.iloc[0]['lon0']
        xbary = orbitdf.iloc[0]['xbary']
        ybary = orbitdf.iloc[0]['ybary']
        zbary = orbitdf.iloc[0]['zbary']
        abg_a = orbitdf.iloc[0]['abg_a']
        abg_b = orbitdf.iloc[0]['abg_b']
        abg_g = orbitdf.iloc[0]['abg_g']
        abg_adot = orbitdf.iloc[0]['abg_adot']
        abg_bdot = orbitdf.iloc[0]['abg_bdot']
        abg_gdot = orbitdf.iloc[0]['abg_gdot']
        abg_a_err = orbitdf.iloc[0]['abg_a_err']
        abg_b_err = orbitdf.iloc[0]['abg_b_err']
        abg_g_err = orbitdf.iloc[0]['abg_g_err']
        abg_adot_err = orbitdf.iloc[0]['abg_adot_err']
        abg_bdot_err = orbitdf.iloc[0]['abg_bdot_err']
        abg_gdot_err = orbitdf.iloc[0]['abg_gdot_err']

        designation = designation if designation else "NULL"

        duplicate_orbid = self.__duplicate_orbit(a, e, inc)
        if duplicate_orbid:
            raise RuntimeError("This orbit already exists. It has orbid " + str(duplicate_orbid) + "\n")

        c = ("INSERT INTO LZULLO.TNORBIT (ID, CHISQ , NDOF , A, E, INC, AOP, NODE, PERI_JD, PERI_DATE, EPOCH_JD, "
             "MEAN_ANOMALY, PERIOD, A_ERR,E_ERR, INC_ERR, AOP_ERR, NODE_ERR, PERI_ERR, PERIOD_ERR, LAT0, LON0, XBARY, "
             "YBARY, ZBARY, ABG_A, ABG_B, ABG_G, ABG_ADOT, ABG_BDOT, ABG_GDOT, ABG_A_ERR, ABG_B_ERR, ABG_G_ERR, "
             "ABG_ADOT_ERR, ABG_BDOT_ERR, ABG_GDOT_ERR, ORBID, DESIGNATION) VALUES ('" + canid + "','" + chisq + "','" +
             ndof + "','" + a + "','" + e + "','" + inc + "','" + aop + "','" + node + "', '" + peri_jd + "', '" +
             peri_date + "', '" + epoch_jd + "', '" + mean_anomaly + "', '" + period + "','" + a_err + "','" + e_err +
             "','" + inc_err + "','" + aop_err + "','" + node_err + "','" + peri_err + "','" + period_err + "','" +
             latO + "','" + lonO + "','" + xbary + "','" + ybary + "','" + zbary + "','" + abg_a + "','" + abg_b + "','"
             + abg_g + "','" + abg_adot + "','" + abg_bdot + "','" + abg_gdot + "','" + abg_a_err + "','" + abg_b_err +
             "','" + abg_g_err + "','" + abg_adot_err + "','" + abg_bdot_err + "','" + abg_gdot_err + "'," + orbid +
             ",'" + designation + "')")

        return c

    def __duplicate_obs(self, observation):
        """

        Args:
            observation (pd.Series): Series representing observation 

        Returns:
            bool: True if observation is already in table (by ra, dec, and date_obs), false otherwise

        """

        query = "SELECT * FROM LZULLO.TNOBS WHERE LZULLO.TNOBS.DATE_OBS = '" + str(observation['date']) + \
                "' AND LZULLO.TNOBS.RA = '" + str(observation['ra']) + \
                "' AND LZULLO.TNOBS.DEC = '" + str(observation['dec']) + "'"

        results = pd.read_sql(query, self.desoper)
        return not results.empty

    def __duplicate_orbit(self, a, e, inc):
        """
        
        Args:
            a (str): Semimajor axis
            e (str): Eccentricity
            inc (str): Inclination

        Returns:
            Checks to see if orbit is already in TNORBIT. Compares given a, e, and inc to orbits in TNORBIT.  If there
            is a duplication, then returns orbid of duplicate. Else returns False
        """
        query = ("SELECT * FROM LZULLO.TNORBIT WHERE LZULLO.TNORBIT.A = '" + a + "'AND LZULLO.TNORBIT.E = '" + e +
                 "'AND LZULLO.TNORBIT.INC = '" + inc + "'")
        results = pd.read_sql(query, self.desoper)
        if results.empty:
            return False
        else:
            return results['ORBID'][0]

    @staticmethod
    def __comment(observation):
        """
        
        Args:
            observation: Single observation from CSV file

        Returns:
            Disregards comment lines
        """
        return observation['date'].startswith('#')

    # Returns a Dataframe of necessary information from DESTEST
    def __access_destest(self, objid):
        """
        
        Args:
            objid: Unique object ID

        Returns:
            Finds all the necessary information for a given observation from DESTEST 
        """
        query = "SELECT NITE, SEASON, FLUX, FLUX_ERR  FROM WSDIFF.SNOBS WHERE SNOBJID =" + objid
        data_list = pd.read_sql(query, self.destest)

        return data_list

    @staticmethod
    def __fit_orbit(df_obs):
        """
        
        Args:
            df_obs (pd.DataFrame): Dataframe of observations

        Returns:
            Uses pyOrbfit code to create an orbit
        """
        df_obs = df_obs.ix[['#' not in row['date'] for ind, row in df_obs.iterrows()]]  # filter comment lines
        nobs = len(df_obs)
        ralist = [ephem.hours(r) for r in df_obs['ra'].values]
        declist = [ephem.degrees(r) for r in df_obs['dec'].values]
        datelist = [ephem.date(d) for d in df_obs['date'].values]
        obscode = np.ones(nobs, dtype=int) * 807
        orbit = Orbit(dates=datelist, ra=ralist, dec=declist, obscode=obscode, err=0.15)
        # print orbit.chisq
        return orbit

    def __find_year(self, date):
        """
        
        Args:
            date: String in format yyyy/mm/dd hh:mm:ss

        Returns:
            Finds year.  Returns -1 if year is not in DES operating years
        """
        if not self.__date_format_check(date):
            raise RuntimeError("Dates must be in format yyyy/mm/dd hh:mm:ss")

        date_obj = ephem.date(date)
        years = []
        for i in range(0, 5):
            years.append({'start': ephem.date((2013 + i, 8, 1)), 'end': ephem.date((2014 + i, 2, 20)), 'year': i + 1})
        yr = -1
        for y in years:
            if y['start'] < date_obj < y['end']:
                yr = y['year']
        return yr

    def __find_canid(self, can_table, season, name, cand_info):

        canid = name
        if cand_info:
            canid = "NONE_GENERATED"
            for date in can_table['date']:
                if not date.startswith('#'):
                    yr = self.__find_year(date)

                    if yr == -1:
                        raise RuntimeError("Observations must be within DES operating years")

                    if can_table['fakeid'][0]:
                        canid = "S" + str(season) + "Y" + str(yr) + "FO_" + name
                    else:
                        canid = "S" + str(season) + "Y" + str(yr) + "NF_" + name

        return canid

    def __create_orbit_id(self):
        """
        
        Returns:
            creates and returns a unique 7 digit orbit id
        """
        while True:
            num = np.random.randint(1000000, 9999999)
            query = "SELECT ORBID FROM LZULLO.TNORBIT WHERE ORBID = " + str(num)
            df = pd.read_sql(query, self.desoper)
            if df.empty:
                return str(num)

    def __create_obj_ids(self, size):
        """
        Returns a list of size unique 12 digit obj_ids

        Args:
            size (int): Number of obj_ids needed

        Returns:
            list: A list of unique obj_ids
        """
        num_list = []
        while len(num_list) != size:
            num = np.random.randint(100000000000, 999999999999)
            query = "SELECT OBJID FROM LZULLO.TNOBS WHERE OBJID = " + str(num)
            df = pd.read_sql(query, self.desoper)
            if df.empty and str(num) not in num_list:
                num_list.append(str(num))

        return num_list

    # noinspection PyBroadException
    @staticmethod
    def __date_format_check(date):
        """
        Checks to see if date is in form yyyy/mm/dd hh:mm:ss
        
        Args:
            date: Takes in date string

        Returns:
            bool: True if date in correct format, false otherwise
        """

        year, month, datetime = date.split('/')
        if len(year) != 4 or (year[0:2] != '20' and year[0:2] != '19'):
            return False

        if len(month) != 1 and len(month) != 2:
            return False

        if int(month) <= 0 or int(month) > 12:
            return False

        date, time = datetime.split() if len(datetime) > 2 else (datetime, "")

        day_range = monthrange(int(year), int(month))  # day_range[1] num days in month
        if int(date) <= 0 or int(date) > day_range[1]:
            return False

        if len(date) != 2 and len(date) != 1:
            return False

        if time == "":
            return True
        try:
            hour, minute, second = time.split(':', 3)
        except Exception:
            try:
                hour, minute = time.split(':', 2)
                second = ""
            except Exception:
                hour, minute, second = time, "", ""

        if len(hour) != 2 and len(hour) != 1:
            return False

        if int(hour) < 0 or int(hour) > 24:
            return False

        if minute == "":
            return True

        if len(minute) != 2 and len(minute) != 1:
            return False

        if int(minute) < 0 or int(minute) >= 60:
            return False

        if second == "":
            return True

        if len(second) != 2 and len(second) != 1:
            return False

        if int(second) < 0 or int(second) >= 60:
            return False

        return True

    @staticmethod
    def __valid_obj_id(objid):
        objid = str(objid)
        if not objid.replace('.', '', 1).isdigit() or int(float(objid)) == 0:
            return False

        return True

    def __del__(self):
        self.desoper.close()
        self.destest.close()
