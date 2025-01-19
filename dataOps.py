import pandas as pd

def getClass(category, u):
    # out = []
    # for i in category.count():
    #     curr = category.get(i)
    #     out.extend()
    # return out
    classes = pd.read_csv('ryc.csv')
    return classes.where(classes["Category"] == category).dropna(how='all')