import pandas as pd


d1 = pd.read_excel('DM_TermProj/temperature.xlsx')
d2 = pd.read_excel('DM_TermProj/heat_1.xlsx')

data=pd.merge(d1, d2, on="num")
del data['date_y']
del data['num']
del data['day']
del data['time']
del data['spot']
data.rename(columns={"date_x":"date"}, inplace = True)
#print(data.head())

data.to_excel("test.xlsx")

