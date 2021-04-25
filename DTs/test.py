import os
import pydotplus
from sklearn.datasets import load_iris
from sklearn import tree
X = [[0, 0], [1, 1], [2, 2], [3, 3]]
Y = [0, 1, 2, 3]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
r1 = clf.predict([[2., 2.]])
r1 = clf.predict([[2., 2.]])
print(r1)
r2 = clf.predict_proba([[2., 2.]])
print(r2)
r3 = clf.predict_proba([[2, 2], [3, 2]])
print(r3)


iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)
# print(iris.data, iris.target)
with open("iris.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f,
                             feature_names=iris.feature_names,
                             class_names=iris.target_names,
                             filled=True, rounded=True,
                             special_characters=True)

# os.unlink('iris.dot')

# dot_data = tree.export_graphviz(clf, out_file=None)
# graph = pydotplus.graph_from_dot_data(dot_data)
# graph.write_pdf("iris.pdf")

r1 = clf.predict(iris.data[:1, :])
print(r1)
r2 = clf.predict_proba(iris.data[:1, :])
print(r2)
