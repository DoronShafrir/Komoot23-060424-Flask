import pandas as pd
from datetime import datetime as dt


class Comments:
    def __init__(self):
       pass

    @staticmethod
    def merge_comments(self):
        try:
            comments = pd.read_csv('comments.csv')


        except IOError:
            raise Exception('comments file does not exist')
            init_line = ['Date', 'A_Comment', 'A_Duration', 'A_Distance']
            comments = pd.Dataframe(columns=init_line)


        finally:
            main = pd.read_csv('main.csv')
            united = pd.merge(main, comments, on='Date', how='outer')
            columns_to_delete = [col for col in united.columns if col.startswith('Unnamed')]
            united.drop(columns=columns_to_delete, inplace=True)
            united.drop_duplicates(subset='Date', keep='first', inplace=True)
            united.to_csv('united.csv')

    # def show_comments(self):
    #     try:
    #         comments = pd.read_csv("comments.csv")
    #         s_list = comments.sort_values(by="Date", ascending=False)
    #         data = []
    #         for n in range(len(s_list)):
    #             line = []
    #             line.append(str(s_list.Date.iloc[n])[:10])
    #             line.append(s_list.A_Comment.iloc[n])
    #             line.append(str(round((s_list.A_Duration.iloc[n]), 2)))
    #             line.append(str(round((s_list.A_Distance.iloc[n]), 2)))
    #             data.append(line)
    #     except IOError:
    #         raise Exception("comments.csv does not exist")
    #     return data

    #------------the function gets the data to be insert into the comments.csv and save it ----------#
    @staticmethod
    def add_comment_to_csv(date, comment, duration, distance):

        main = pd.read_csv('main.csv', parse_dates=[1])
        try:
            comments = pd.read_csv('comments.csv', parse_dates=[0])
        except IOError:
            init_line = ['Date', 'A_Comment', 'A_Duration', 'A_Distance']
            comments = pd.DataFrame(columns=init_line)
            raise Comments("file does not exist")
        finally:
            init_line = ['Date', 'A_Comment', 'A_Duration', 'A_Distance']
            date = dt.strptime(date[0], "%Y-%m-%d")
            if comment[0] != "":
                data_to_add = [[date, comment[0], duration[0], distance[0]]]
                comments_line_to_add = pd.DataFrame(data_to_add, columns=init_line)
                print(comments_line_to_add)
                comments = pd.concat([comments, comments_line_to_add], ignore_index=False, axis=0)
                comments.drop_duplicates(subset='Date', keep='last', inplace=True)
                comments.to_csv('comments.csv', index=False, encoding='utf-8-sig')
                united = pd.merge(main, comments, on='Date', how='outer')
                columns_to_delete = [col for col in united.columns if col.startswith('Unnamed')]
                united.drop(columns=columns_to_delete, inplace=True)
                united.drop_duplicates(subset='Date', keep='first', inplace=True)
                united.to_csv('united.csv', index=False, encoding='iso-8859-8')
                return "success"


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
    get_comments.get_list_of_dates_to_change()
