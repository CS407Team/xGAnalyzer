from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_blobs
import app

X1 = app.getXgDataYellow("../includes/arsenal-tottenham.png", 1.6, 1490, 90)
X2 = app.getXgDataYellow("../includes/chelsea-tottenham.png", 1.2, 1500, 90)
X3 = app.getXgDataYellow("../includes/leicester-tottenham.png", 4.5, 1500, 90)
X4 = app.getXgDataYellow("../includes/southampton-tottenham.png", 3.0, 1440, 90)
X5 = app.getXgDataYellow("../includes/westham-tottenham.png", 1.8, 1490, 90)
X6 = app.getXgDataBlue("../includes/tottenham-brentford.png", 2.5, 1480, 90)
X7 = app.getXgDataBlue("../includes/tottenham-crystalpalace.png", 3.0, 1490, 90)
X8 = app.getXgDataBlue("../includes/tottenham-liverpool.png", 3, 1500, 90)
X9 = app.getXgDataBlue("../includes/tottenham-southampton.png", 1.8, 1500, 90)
X10 = app.getXgDataBlue("../includes/tottenham-watford.png", 1, 1490, 90)
X11 = app.getXgDataBlue("../includes/arsenal-tottenham.png", 1.6, 1490, 90)
X12 = app.getXgDataBlue("../includes/chelsea-tottenham.png", 1.2, 1500, 90)
X13 = app.getXgDataBlue("../includes/leicester-tottenham.png", 4.5, 1500, 90)
X14 = app.getXgDataBlue("../includes/southampton-tottenham.png", 3.0, 1440, 90)
X15 = app.getXgDataBlue("../includes/westham-tottenham.png", 1.8, 1490, 90)
X16 = app.getXgDataYellow("../includes/tottenham-brentford.png", 2.5, 1480, 90)
X17 = app.getXgDataYellow("../includes/tottenham-crystalpalace.png", 3.0, 1490, 90)
X18 = app.getXgDataYellow("../includes/tottenham-liverpool.png", 3, 1500, 90)
X19 = app.getXgDataYellow("../includes/tottenham-southampton.png", 1.8, 1500, 90)
X20 = app.getXgDataYellow("../includes/tottenham-watford.png", 1, 1490, 90)
x = [X1, X2, X3, X4, X5, X6, X7, X9, X10]
y = [1, 0, 3, 1, 0, 2, 3, 2, 1]
model = LogisticRegression(solver='lbfgs')
model.fit(x, y)
new_input = [X8]
new_output = model.predict(new_input)
X = [X11, X12, X3, X14, X15, X16, X17, X19, X20]
Y = [3, 2, 2, 1, 1, 0, 0, 3, 0]
mod = LogisticRegression(solver='lbfgs')
mod.fit(X, Y)
inp = [X18]
output = mod.predict(inp)

if __name__ == '__main__':
    print("Tottenham: " + str(new_output[0]) + " Liverpool: " + str(output[0]))
