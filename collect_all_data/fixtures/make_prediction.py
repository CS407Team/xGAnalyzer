import pandas
from sklearn import linear_model



df = pandas.read_csv("file.csv")
X = df[['RoundNum','HalftimeHome','HalftimeAway','FulltimeHome','FulltimeAway']]
Y = df['Winner']
