import pandas
from sklearn import linear_model
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import os

def validate_data(winner):
    start = winner[0]

    for val in winner:
        if val != start:
            return True
            break

    return False


def generate_odds():
    df = pandas.read_csv("fixture_data.csv",converters={"RoundNum":int})
 
    X = df[['RoundNum','HalftimeHome','HalftimeAway','FulltimeHome','FulltimeAway']]
    y = df['Winner']
    if(len(y) == 0):
        os.remove("fixture_data.csv")
        return {"Error": -1}
    
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=0)

    if(validate_data(y) == False):
        os.remove("fixture_data.csv")
        return {"Winner":int(y[0])}
    
    home_id = int(df.HomeId[0])
    away_id = int(df.AwayId[0])

    # col_name =['RoundNum','HalftimeHome','HalftimeAway','FulltimeHome','FulltimeAway', 'Winner']
    # df = pandas.read_csv("file.csv")
    # df = pandas.read_csv("file.csv", header=None, names=col_name, convertors={"RoundNum":float})
    # features = ['RoundNum','HalftimeHome','HalftimeAway','FulltimeHome','FulltimeAway']
    # df.RoundNum = df.RoundNum.astype(float)
    # print(df.RoundNum)

    # X = df[features]
    # y = df.Winner
    # X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=0)

    logreg = LogisticRegression()
    logreg.max_iter = 1000000
    logreg.fit(X_train,y_train)
    y_pred=logreg.predict(X_test)
    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    # print(y_pred)
    home_freq = 0
    away_freq = 0
    tie_freq = 0

    for val in y_pred:
        if val == home_id:
            home_freq = home_freq +1
        elif val == away_id:
            away_freq = away_freq +1
        else:
            tie_freq = tie_freq +1

    os.remove("fixture_data.csv")
    return {"home":home_freq, "away":away_freq,"tie":tie_freq}






# x_train, x_test, y_train, y_test = train_test_split(X,Y, test_size = 0.2, random_state = 0)


# regressor = LinearRegression()
# regressor.fit(X, Y)
# prediction = regressor.predict([[31,1,1,1,1]])
# print(prediction)
# # regressor.fit(x_train, y_train)
# # y_pred = regressor.predict(x_test)
