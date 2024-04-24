import pandas as pd
from datetime import datetime as dt


class Comments:
    def __init__(self):
       pass

    def fetch_comments(self):
        try:
            comments = pd.read_csv('comments.csv')

        except IOError:

            init_line = ['Date', 'A_Comment', 'A_Duration', 'A_Distance']
            data = [['2023-12-16', 'Cycling with Mali to Kfar Gvirol and Mrar', 0, 0],
                    ['2018-06-01', 'buy new w Ghost', 0, 0],
                    ['2023-12-05', 'Replace rear tier', 1, 10.5],
                    ['2023-12-23', 'Arad Masada Tour', 4, 31]]
            comments = pd.DataFrame(data, columns=init_line)

            # line = pd.DataFrame([[date, additinal_comments, corrected_duration, corrected_distance]],columns=init_line)
            # comments = comments.append(line, ignore_index=True)
            print(comments.head(5))
            print(self.main.head(7))
            comments.to_csv('comments.csv')

        finally:
            print(comments.head(5))
            print(self.main.head(7))
            united = pd.merge(self.main, comments, on='Date', how='outer')
            united.to_csv('united.csv')

    def show_comments(self):
        try:
            comments = pd.read_csv("comments.csv")
            s_list = comments.sort_values(by="Date", ascending=False)
            data = []
            for n in range(len(s_list)):
                line = []
                line.append(str(s_list.Date.iloc[n])[:10])
                line.append(s_list.A_Comment.iloc[n])
                line.append(str(round((s_list.A_Duration.iloc[n]), 2)))
                line.append(str(round((s_list.A_Distance.iloc[n]), 2)))
                data.append(line)
        except IOError:
            raise Exception("comments.cse does not exist")
        return data

    #------------the function gets the data to be insert into the comments.csv and save it ----------#
    @staticmethod
    def add_comment_to_csv(date, comment='A_Comment', duration=0, distance=0):

        main = pd.read_csv('main.csv', parse_dates=[1])
        try:
            comments = pd.read_csv('comments.csv', parse_dates=[0])
            init_line = ['Date', 'A_Comment', 'A_Duration', 'A_Distance']
            date = dt.strptime(date[0], "%Y-%m-%d")
            data_to_add = [[date, comment[0], duration[0], distance[0]]]

            comments_line_to_add = pd.DataFrame(data_to_add, columns=init_line)
            print(comments_line_to_add)

            comments = pd.concat([comments, comments_line_to_add], ignore_index=False, axis=0)
            comments.drop_duplicates(subset='Date', keep='last', inplace=True)
            comments.to_csv('comments.csv', index=False)
        except IOError:
            raise Comments("file does not exist")

        finally:
            # print(comments.head(5))
            # print(self.main.head(7))

            united = pd.merge(main, comments, on='Date', how='outer')
            columns_to_delete = [col for col in united.columns if col.startswith('Unnamed')]
            united.drop(columns=columns_to_delete, inplace=True)
            united.drop_duplicates(subset='Date', keep='first', inplace=True)
            united.to_csv('united.csv', index=False)

    @staticmethod
    def get_list_of_dates_to_change():
        try:
            main = pd.read_csv('main.csv')
            dates_list = main['Date'].tolist()
            return dates_list
        except IOError:
            raise Exception("Main is not exist")







if __name__ == '__main__':
    get_comments = Comments()
    # get_comments.fetch_comments()
    # get_comments.add_comment_to_csv('2024-04-18', 'Cycling with MT8', 3, 100)
    get_comments.get_list_of_dates_to_change()
