from ucimlrepo import fetch_ucirepo
from aq import Example, AQ
import numpy as np
from sklearn.model_selection import train_test_split


def main():
    id = 19  # mushrooms: 73, cars: 19
    dataSet = fetch_ucirepo(id=id)

    X = dataSet.data.features
    y = dataSet.data.targets

    print(dataSet.variables["name"])

    target_position = next(
        (i for i, role in enumerate(dataSet.variables["role"]) if role == "Target"),
        None,
    )

    xnLabels = {}
    data = []

    for i, column in enumerate(dataSet.variables["name"]):
        if dataSet.variables["role"][i] == "Feature":
            xnLabels[str(column)] = X[str(column)].unique().tolist()

    X_train, X_test, Y_train, Y_test = train_test_split(
        X.iloc[0:].values, y.iloc[0:].values, test_size=0.5
    )

    for feature, target in zip(X_train, Y_train):
        if target_position < 1:
            featureDict = {
                column: feature[i]
                for i, column in enumerate(dataSet.variables["name"][1:])
            }
        else:
            featureDict = {
                column: feature[i]
                for i, column in enumerate(dataSet.variables["name"][:-1])
            }
        data.append(Example(xnLabels, featureDict, target))

    testData = []
    for feature, target in zip(X_test, Y_test):
        if target_position < 1:
            featureDict = {
                column: feature[i]
                for i, column in enumerate(dataSet.variables["name"][1:])
            }
        else:
            featureDict = {
                column: feature[i]
                for i, column in enumerate(dataSet.variables["name"][:-1])
            }
        testData.append(Example(xnLabels, featureDict, target))

    print("Algorithm Start")
    modified = False
    aq = AQ(data, xnLabels, 1, "ordered", testData, modified)
    aq.run()
    i = 0
    count = 0
    for example in data:
        if aq.validate(example) != example.result:
            i = i + 1
        count += 1

    print(f"Train set error rate: {i / count}")

    i = 0
    count = 0
    for example in testData:
        if aq.validate(example) != example.result:
            i = i + 1
        count += 1

    print(f"Test set error rate: {i / count}")
    # [print(rule) for rule in aq.rules]


if __name__ == "__main__":
    main()
