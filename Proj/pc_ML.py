import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#데이터 불러오기
df = pd.read_excel("survey.xlsx", encoding="UTF-8")

#컬럼 명 재정의 및 필요없는 컬럼 삭제
df.columns = ['timestamp', 'sex', 'age', 'region', 'avg_time', 'food_choice', 'what_food', 'f_con1', 'f_con2', 'f_con']
df.drop(['timestamp', 'what_food', 'f_con'], axis='columns', inplace=True)
df_1 = df.drop(['age'], axis='columns', inplace=False)
data = df[['age']]
#print(type(data))

cols = ['sex', 'age', 'region', 'avg_time', 'food_choice', 'f_con1', 'f_con2',]

# 결측치 확인
#print(df.isnull().values.sum())

#OrdinalEncoder
from sklearn.preprocessing import OrdinalEncoder
enc=OrdinalEncoder()
enc_cols = ['sex', 'region', 'avg_time', 'food_choice', 'f_con1', 'f_con2'] #일부 컬럼에 대해서만 인코더 적용
out_enc=enc.fit_transform(df_1[enc_cols])
df=pd.DataFrame(out_enc, columns=df_1.columns)
df = pd.concat([df, data], axis=1)
#print(df)

#이상치 제거
data = df[(df['age'] >= 30) | (df['age'] < 19)].index
df.drop(data, inplace=True)
#print(df)

#상관 계수
"""
cor=df.corr()
cor_target=abs(cor['f_con2'])
#상관 계수가 0.6이상인 데이터 필터링
#selected_cols=cor_target[cor_target>0.6]
#df_sel=df[selected_cols.index]
print(cor_target)
"""

#데이터 스플릿
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(df.loc[:, df.columns != 'f_con2'], df['f_con2'], test_size=0.2)

#랜덤 포레스트 학습(분류)
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
#n_estimators=트리의 개수, max_features=참고할 속성의 개수
clf=RandomForestClassifier(max_depth=7, n_estimators=4, max_features='sqrt')
clf.fit(x_train, y_train)

#print(y_train.head())
y_pred=clf.predict(x_test)
x_test.to_excel('x_test.xlsx', index=False)
#모델 유효성 검사
#print(y_pred)
score=f1_score(y_test, y_pred, average='micro')
print('f1 score is = '+ str(score))


#생성된 모델 .pkl파일로 저장
"""
import joblib
result_file = 'object_01.pkl'
joblib.dump(clf, result_file)
"""