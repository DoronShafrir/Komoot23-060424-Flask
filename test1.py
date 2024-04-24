import pandas as pd

init_line = ['Date', 'A_Comment', duraion, distance]
data_to_add = [[date, comment, 0, 0]]

comments_line_to_add = pd.DataFrame(data_to_add, columns=init_line)
print(comments_line_to_add)
# Reset the index of comments_line_to_add
comments_line_to_add.reset_index(drop=True, inplace=True)
comments.reset_index(drop=True, inplace=True)
comments = pd.concat([comments,comments_line_to_add ], ignore_index=True, axis=0)