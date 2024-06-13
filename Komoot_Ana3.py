#--------Komoot Analyze Ver 1.3 02/02/22------#
#--- Preperation to work together with GUI ---#
import pandas as pd
from source_scraper import K_statistics as Stat
from datetime import datetime as dt
from Comments import Comments

class K_Analize():
    def __init__(self, conf):
        '''
        conf:
        #0 - date
        #1 - per week
        #2 - daily
        #3 - from day one
        #4 - from beginning of this year
        #5 - from date
        #6 - with comments
        '''
        self.conf = conf
        self.summary = []
        date = dt.strptime(conf[0], "%Y-%m-%d")
        self.start_date = date.strftime("%m/%d/%Y")
        self.conf = conf
        self.data = self.fill_data

    @property
    def fill_data(self):
        k_stat = Stat()
        if self.conf[6]:
            Comments.merge_comments(self)
            try:
                self.komoot_tours = pd.read_csv('united.csv', parse_dates=[1])
                pandas_daily_table_w_comments = k_stat.detailed_rides_from_date_DF_with_comments(self.komoot_tours, self.conf)
                data = self.print_2_screen_DF_w_comments(pandas_daily_table_w_comments)  # daily information w comments to be  present
            except IOError:
                raise Exception('united comments does not exist')
        else:
            try:
                self.komoot_tours = pd.read_csv('main.csv', parse_dates=[1])
                if self.conf[1]:
                    pandas_weekly_table = k_stat.weekly_rides_seperator_DF(self.komoot_tours,  self.conf)
                    data = self.print_2_screen_DF(pandas_weekly_table)  # weekly information to be  present
                if self.conf[2]:
                    pandas_daily_table = k_stat.detailed_rides_from_date_DF(self.komoot_tours, self.conf)
                    data = self.print_2_screen_DF(pandas_daily_table)    # daily information to be  present
            except IOError:
                raise Exception('main does not exist')
        return data

    #----------print summary to screen------------#

    def print_2_screen_DF(self, prepared_table):
        s_list = prepared_table
        s_list = s_list.sort_values(by="Date", ascending=False)
        data = []
        for n in range(len(s_list)):
            line =[]
            line.append(str(s_list.Date.iloc[n])[:10])
            line.append(str(round((s_list.Duration.iloc[n]),2)))
            line.append(str(round((s_list.Distance.iloc[n]),2)))
            line.append(str(round((s_list.UpHill.iloc[n]),2)))
            line.append(str(round((s_list.Count.iloc[n]), 2)))
            data.append(line)

        self.summary.append(str(round(s_list.Duration.sum(), 2)))
        self.summary.append(str(round(s_list.Distance.sum(), 2)))
        self.summary.append(s_list.Count.sum())
        return data

        # ----------print to screen with comments------------#

    def print_2_screen_DF_w_comments(self, prepared_table):
        s_list = prepared_table
        s_list = s_list.sort_values(by="Date", ascending=False)
        data = []
        for n in range(len(s_list)):
            line = []
            line.append(str(s_list.Date.iloc[n])[:10])
            line.append(str(round((s_list.Duration.iloc[n]), 2)))
            line.append(str(round((s_list.Distance.iloc[n]), 2)))
            # line.append(str(round((s_list.Count.iloc[n]), 2)))
            line.append(str(round((s_list.A_Duration.iloc[n]), 2)))
            line.append(str(round((s_list.A_Distance.iloc[n]), 2)))
            line.append((s_list.A_Comment.iloc[n]))
            data.append(line)

        self.summary.append(str(round(s_list.Duration.sum(), 2)))
        self.summary.append(str(round(s_list.Distance.sum(), 2)))
        self.summary.append(s_list.Count.sum())
        return data













