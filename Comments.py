import pandas as pd
from datetime import datetime as dt


class Comments:
    def __init__(self):
        self.main = pd.read_csv('main.csv')

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

    def add_comment_to_csv(self, date, comment = 'A_Comment', duraion=0, distance=0 ):
        try:
            comments = pd.read_csv('comments.csv')

            init_line = ['Date', 'A_Comment', duraion, distance]
            data_to_add = [[date, comment, 0, 0]]

            comments_line_to_add = pd.DataFrame(data_to_add, columns=init_line)
            print(comments_line_to_add)
            # print(self.main.head(7))
            comments_line_to_add = comments_line_to_add.reset_index()
            comments = comments.reset_index()
            comments = pd.concat([comments_line_to_add, comments], ignore_index=True)
            comments.to_csv('comments.csv')
        except IOError:
            raise Comments("file does not exist")

        finally:
            print(comments.head(5))
            print(self.main.head(7))
            united = pd.merge(self.main, comments, on='Date', how='outer')
            united.to_csv('united.csv')




if __name__ == '__main__':
    get_comments = Comments()
    # get_comments.fetch_comments()
    get_comments.add_comment_to_csv('2022-04-18', 'Cycling with MTesting', 0, 0)
