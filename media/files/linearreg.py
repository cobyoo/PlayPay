import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import model_selection
from sklearn import metrics
from mpl_toolkits.mplot3d import Axes3D


data = pd.read_excel('train_data.xlsx')
data2 = pd.read_excel('test_data.xlsx')
dfX = pd.DataFrame(data, columns=["temp", "humid"])
dfy = pd.DataFrame(data, columns=["Gcal"])
df = pd.concat([dfX, dfy], axis=1)


testx = pd.DataFrame(data2, columns=["temp", "humid"])
testy = pd.DataFrame(data2, columns=["Gcal"])

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111, projection='3d')
cols = ["temp", "humid", "Gcal"]

ax.scatter(df["temp"],df["humid"], df["Gcal"])

model = smf.ols(formula = 'Gcal ~ temp + humid', data = data)
result = model.fit()
#print(result.summary())  #-----변수 별 관계성 수치표현

#plt.show()  # plotting function


#x_train, x_test, y_train, y_test = model_selection.train_test_split(dfX, dfy, test_size=0.3)

model = LinearRegression()
model.fit(dfX, dfy)
#print(model.coef_, model.intercept_)

#y_predict = boston_model.predict(x_train) 
#score = metrics.r2_score(y_train, y_predict)
#print(score) #1.0

y_predict = model.predict(testx) 
score = metrics.r2_score(testy, y_predict)
print(score) #1.0

temp = input()
humid = input()
result = int(model.intercept_[0]) + int(model.coef_[0][0])*float(temp) + int(model.coef_[0][1])*float(humid)
print(result)