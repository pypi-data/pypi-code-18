# -*- coding: utf-8 -*-
import urllib2,json,os,xml.dom.minidom,time,datetime,re,gzip
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class date_calculate:
    def __init__(self,begin_date,end_date):
        self.begin_date = begin_date
        self.end_date = end_date
        self.date_start = datetime.datetime.strptime(self.begin_date, '%Y-%m-%d')
        self.date_end = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')
        self.date_cursor = self.date_start
        self.prev_date_cursor = self.date_cursor
        self.year_day_list = {'year':[],'month':[],'week':[],'day':[]}


    def month_calc(self,year_days, month):
        index = int(month) - 1
        if year_days == 366:
            month_list = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        else:
            month_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return month_list[index]

    def year_clac(self,year_start):
        '''计算闰年'''
        if year_start % 100 == 0:  # 整百年
            if year_start % 400 == 0:
                year_days = 366
            else:
                year_days = 365
        else:
            if year_start % 4 == 0:  # 非整百年
                year_days = 366
            else:
                year_days = 365
        return year_days

    def year_delta(self):
        self.prev_date_cursor = self.date_cursor
        if self.days_interval >= self.year_days:  # 相差一年及以上
            self.prev_date_cursor = self.date_cursor
            while self.date_cursor <= self.date_end:
                if self.date_cursor.year < self.date_end.year:
                    self.year_day_list['year'].append(self.date_cursor.year)
                self.prev_date_cursor = self.date_cursor
                self.date_cursor = self.date_cursor + datetime.timedelta(days=self.year_days)
                self.year_days = self.year_clac(self.date_cursor.year)  # 更新yeardays
            self.date_cursor = self.prev_date_cursor
            self.days_interval = int((self.date_end - self.date_cursor).days)
        if self.days_interval == (self.year_days - 1):#是相差一整年就直接返回
            self.year_day_list['year'].append(self.date_cursor.year)
            return 0
        if self.days_interval == 0 and self.date_cursor.day == 1 and self.date_cursor.month == 1:  # 是0就直接返回，非1月1号到期的情况不存在
            day_str = self.date_cursor.strftime('%Y%m%d')
            self.year_day_list['day'].append(day_str)
            return 0
        return 1

    def month_delata(self):
        month = self.date_cursor.month
        month_days = self.month_calc(self.year_days, month)
        if self.days_interval > month_days:
            self.prev_date_cursor = self.date_cursor
            month_str = str(self.date_cursor.year) + str(self.date_cursor.month).zfill(2)
            while self.date_cursor <= self.date_end:
                month = self.date_cursor.month
                month_days = self.month_calc(self.year_days, month)  # 更新该月天数
                if int((self.date_end - self.date_cursor).days) >= month_days:  # 非最后一次迭代
                    self.year_day_list['month'].append(month_str)
                self.prev_date_cursor = self.date_cursor
                self.date_cursor = self.date_cursor + datetime.timedelta(days=month_days)
                self.year_days = self.year_clac(self.date_cursor.year)  # 更新yeardays
                month_str = str(self.date_cursor.year) + str(self.date_cursor.month).zfill(2)
            self.date_cursor = self.prev_date_cursor
            self.days_interval = int((self.date_end - self.date_cursor).days)
        if self.days_interval == 0 and self.date_cursor.day == 1:  # 整好一年零一个月，非1号到期的情况不存在
            day_str = self.date_cursor.strftime('%Y%m%d')
            self.year_day_list['day'].append(day_str)
            return 0
        if self.date_end.day == month_days:  # 此时差额差额已经不足一个月，如果日期终止整好是该月最后一天，直接
            month_str = str(self.date_cursor.year) + str(self.date_cursor.month).zfill(2)
            self.year_day_list['month'].append(month_str)
            return 0
        self.date_cursor = self.date_cursor - datetime.timedelta(days=(self.date_cursor.day - 1))  # 月算完后把游标调到当前月第一天
        return 1

    def week_delta_first(self):
        self.prev_date_cursor = self.date_cursor
        week_day = self.date_cursor.weekday()
        week_interval = 6 - week_day
        self.date_cursor = self.date_cursor + datetime.timedelta(days=week_interval)
        first_week_interval = int((self.date_cursor - self.prev_date_cursor).days)
        if self.date_cursor <= self.date_end:  # 这个是必须判定的条件，不能超出，这个是为了判断剩下的时间是否已经不足一周
            if first_week_interval == 6 :#整一周
                day_str = self.date_cursor.strftime('%Y%m%d')
                self.year_day_list['week'].append(day_str)
            else:
                self.date_cursor = self.prev_date_cursor
                day_str = self.date_cursor.strftime('%Y%m%d')
                self.year_day_list['week'].append(day_str)
                #day_str = date_cursor.strftime('%Y-%m-%d')
                for i in range(1, first_week_interval + 1):
                    self.date_cursor = self.date_cursor + datetime.timedelta(days=1)
                    day_str = self.date_cursor.strftime('%Y%m%d')
                    self.year_day_list['week'].append(day_str)
        else:
            self.date_cursor = self.prev_date_cursor
        self.days_interval = int((self.date_end - self.date_cursor).days)
        return 1

    def week_delta(self):
        if self.days_interval > 6:  # 相差一周以上
            self.date_cursor = self.date_cursor + datetime.timedelta(days=7)  # 调整到下一个周末，上一个日期游标必然是周末
            day_str = self.date_cursor.strftime('%Y%m%d')
            while self.date_cursor <= self.date_end:
                self.year_day_list['week'].append(day_str)
                self.prev_date_cursor = self.date_cursor
                self.date_cursor = self.date_cursor + datetime.timedelta(days=7)
                day_str = self.date_cursor.strftime('%Y%m%d')
            self.date_cursor = self.prev_date_cursor + datetime.timedelta(days=1)
            self.days_interval = int((self.date_end - self.date_cursor).days)
        if self.days_interval < 0:
            return 0
        return 1

    def day_delta(self):
        day_str = self.date_cursor.strftime('%Y%m%d')
        week_day = self.date_cursor.weekday()
        week_interval = 6 - week_day
        weekend_date = self.date_cursor + datetime.timedelta(days=week_interval)
        self.year_day_list['day'].append(day_str)
        for i in range(1, self.days_interval + 1):
            self.date_cursor = self.date_cursor + datetime.timedelta(days=1)
            if self.date_cursor < weekend_date:
                day_str = self.date_cursor.strftime('%Y%m%d')
                self.year_day_list['day'].append(day_str)
            else:
                break

    def week_delta_first_same_month(self):
        cur_month = self.date_cursor.month#不能跨月
        self.prev_date_cursor = self.date_cursor
        week_day = self.date_cursor.weekday()
        week_interval = 6 - week_day
        self.date_cursor = self.date_cursor + datetime.timedelta(days=week_interval)
        first_week_interval = int((self.date_cursor - self.prev_date_cursor).days)
        if self.date_cursor <= self.date_end and self.date_cursor.month == cur_month:  # 这个是必须判定的条件，不能超出并且不能跨月，这个是为了判断剩下的时间是否已经不足一周
            if first_week_interval == 6 :#整一周
                day_str = self.date_cursor.strftime('%Y%m%d')
                self.year_day_list['week'].append(day_str)
            else:
                self.date_cursor = self.prev_date_cursor
                day_str = self.date_cursor.strftime('%Y%m%d')
                self.year_day_list['day'].append(day_str)
                #day_str = date_cursor.strftime('%Y-%m-%d')
                for i in range(1, first_week_interval + 1):
                    self.date_cursor = self.date_cursor + datetime.timedelta(days=1)
                    if self.date_cursor.month == cur_month:  # 不能跨月
                        day_str = self.date_cursor.strftime('%Y%m%d')
                        self.year_day_list['day'].append(day_str)
                    else:
                        break
        else:
            self.date_cursor = self.prev_date_cursor
        self.days_interval = int((self.date_end - self.date_cursor).days)
        return 1

    def week_delta_same_month(self):
        self.prev_date_cursor = self.date_cursor#先更新这个，防止因为没有进入循环导致错误
        cur_month = self.date_cursor.month#不能跨月
        if self.days_interval > 6:  # 相差一周以上
            self.date_cursor = self.date_cursor + datetime.timedelta(days=7)  # 调整到下一个周末，上一个日期游标必然是周末
            day_str = self.date_cursor.strftime('%Y%m%d')
            while self.date_cursor <= self.date_end:
                if self.date_cursor.month == cur_month:#不能跨月
                    self.year_day_list['week'].append(day_str)
                    self.prev_date_cursor = self.date_cursor
                    self.date_cursor = self.date_cursor + datetime.timedelta(days=7)
                    day_str = self.date_cursor.strftime('%Y%m%d')
                else:
                    break
            self.date_cursor = self.prev_date_cursor + datetime.timedelta(days=1)
            self.days_interval = int((self.date_end - self.date_cursor).days)
        if self.days_interval < 0:
            return 0
        return 1

    def day_delta_same_month(self):
        cur_month = self.date_cursor.month  # 不能跨月
        day_str = self.date_cursor.strftime('%Y%m%d')
        week_day = self.date_cursor.weekday()
        week_interval = 6 - week_day
        weekend_date = self.date_cursor + datetime.timedelta(days=week_interval)
        self.year_day_list['day'].append(day_str)
        for i in range(1, self.days_interval + 1):
            self.date_cursor = self.date_cursor + datetime.timedelta(days=1)
            if self.date_cursor.month == cur_month:  # 不能跨月
                if self.date_cursor < weekend_date:
                    #print "day_str", day_str
                    day_str = self.date_cursor.strftime('%Y%m%d')
                    self.year_day_list['day'].append(day_str)
                else:
                    break
            else:
                break
        #print "day_str", day_str

    def year_start(self):
        # 年
        flag_year = self.year_delta()
        if flag_year == 0:
            return 0
        # 月
        flag_month = self.month_delata()
        if flag_month == 0:
            return 0
        # 周，先把日期游标调整到第一个周末
        flag_week_first = self.week_delta_first()
        if flag_week_first == 0:
            return 0
        # 周
        flag_week = self.week_delta()
        if flag_week == 0:
            return 0
        # 日
        self.day_delta()
        return 1

    def month_start(self):
        # 月
        flag_month = self.month_delata()
        if flag_month == 0:
            return 0
        # 周，先把日期游标调整到第一个周末
        flag_week_first = self.week_delta_first()
        if flag_week_first == 0:
            return 0
        # 周
        flag_week = self.week_delta()
        if flag_week == 0:
            return 0
        # 日
        self.day_delta()
        return 1

    def multi_year(self):
        year_interval = self.date_end.year - self.date_cursor.year
        prev_date_end = self.date_end#先修改date_end，最后改回来
        first_year_end = datetime.datetime(self.date_cursor.year,12,31,0,0)#第一年最后一天
        self.date_end = first_year_end
        #第一年
        if self.date_cursor.month ==1 and self.date_cursor.day ==1:#起始日期是1月1日
            self.year_start()

        elif self.date_cursor.day ==1:#起始日期是非1月的1日
            self.month_start()

        else:#普通日子
            self.common_day()

        #第二年
        for year_plus in range(1,year_interval):
            new_year = self.date_cursor.year+year_plus
            self.date_cursor = datetime.datetime(new_year,1,1,0,0)#一月一号
            self.date_end = datetime.datetime(new_year,12,31,0,0)#一月一号
            self.days_interval = int((self.date_end-self.date_cursor).days)
            self.year_days = self.year_clac(self.date_cursor.year)  # 当前年的天数
            self.year_delta()
        #最后一年
        self.date_end = prev_date_end
        self.date_cursor = datetime.datetime(self.date_cursor.year + 1, 1, 1, 0, 0)  # 一月一号
        self.days_interval = int((self.date_end - self.date_cursor).days)
        year_start_flag = self.year_start()
        if year_start_flag == 0:
            return 0
        return 1


    def common_day(self):
        if self.date_cursor.month != (self.date_cursor + datetime.timedelta(days=1)).month:  # 月末年末
            self.day_delta_same_month()
        else:
            # 周，先把日期游标调整到第一个周末
            flag_week_first = self.week_delta_first_same_month()
            if flag_week_first == 0:
                return 0
            # 周
            flag_week = self.week_delta_same_month()
            if flag_week == 0:
                return 0
            if self.date_cursor.day != 1:  # 如果是下一个月的第一天，就直接跳过
                # 日
                self.day_delta_same_month()
                self.date_cursor = self.date_cursor + datetime.timedelta(days=1)  # 跨月
        # 月
        flag_month = self.month_delata()
        if flag_month == 0:
            return 0
        # 周，先把日期游标调整到第一个周末
        flag_week_first = self.week_delta_first()
        if flag_week_first == 0:
            return 0
        # 周
        flag_week = self.week_delta()
        if flag_week == 0:
            return 0
        # 日
        self.day_delta()
        return 1

    def Main(self):
        # 计算日期和闰年
        self.days_interval = int((self.date_end - self.date_start).days)
        year_start = self.date_start.year
        self.year_days = self.year_clac(year_start)#当前年的天数
        #先判断起始日期
        if self.date_cursor.month ==1 and self.date_cursor.day ==1:#起始日期是1月1日
            year_start_flag = self.year_start()
            if year_start_flag == 0:
                return self.year_day_list

        elif self.date_cursor.day ==1:#起始日期是非1月的1日
            month_start_flag = self.month_start()
            if month_start_flag == 0:
                return self.year_day_list

        elif self.date_end.year - self.date_cursor.year >1:#相差一年以上
            multi_year_flag = self.multi_year()
            if multi_year_flag == 0:
                return self.year_day_list

        else:#普通日子
            commonday_flag = self.common_day()
            if commonday_flag == 0:
                return self.year_day_list

        return self.year_day_list