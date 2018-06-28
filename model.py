#import numpy as np
#import pandas as pd

#from pandas import Series, DataFrame
#from scipy.stats import spearmanr

#from pylab import rcParams
#import seaborn as sb
#import matplotlib.pyplot as plt

#import sklearn
#from sklearn.preprocessing import scale
#from sklearn.linear_model import LinearRegression
#from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import sklearn

from pandas import Series, DataFrame
from pylab import rcParams
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics 
from sklearn.metrics import classification_report

# load dataset
address = 'vectors.tsv'
bias = pd.read_table(address)
bias.columns = ['word','lemma','pos','pos-1','pos-2','pos+1','pos+2','position','hedge','h_conext','factive','f_context','assertive','a_context','implicative','imp_context','report','rep_context','entailement','ent_context','st_subjective','st_sub_context','wk_subjective','wk_sub_context','polarity','positive','positive_context','negative','negative_context','result']

X = bias.ix[:,1:].values
y = bias.ix[:,-1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .3, random_state=25)

LogReg = LogisticRegression()

LogReg.fit(X_train, y_train)



y_pred = LogReg.predict(X_test)

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)

print(classification_report(y_test, y_pred))

