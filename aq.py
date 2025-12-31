import time, copy, random


class Example:
    def __init__(self, labels, data: dict, result):
        self.labels = labels
        self.result = result
        self.data = data

    def __str__(self):
        print(self.data)


class Rule:
    def __init__(self, conditions: dict, result):
        self.conditions = conditions
        self.result = result

    def __mul__(self, other):
        resultConditions = {}
        for label in self.conditions.keys():
            commonConditions = set()
            if self.conditions[label] == True:
                commonConditions = other.conditions[label]
            else:
                for el in self.conditions[label]:
                    if other.conditions[label] == True or el in other.conditions[label]:
                        commonConditions.add(el)
            if commonConditions != True and len(commonConditions) == 0:
                return None
            resultConditions[label] = commonConditions
        result = self.result
        return Rule(resultConditions, result)

    def __eq__(self, other):
        return self.conditions == other.conditions

    def includesIn(self, other):
        """Is Rule more precise than the other
        Args:
            other (Rule): Other rule to check
        Returns:
            bool: True if self is more precise
        """
        for label in self.conditions.keys():
            if self.conditions[label] == True and other.conditions[label] != True:
                return False
            if self.conditions[label] == True:
                continue
            for el in self.conditions[label]:
                if (
                    other.conditions[label] != True
                    and el not in other.conditions[label]
                ):
                    return False
        return True

    def coversExample(self, example: Example):
        """Does example fit the Rule
        Args:
            example (Example): Example to check by rule
        Returns:
            bool: True if example does fit the Rule
        """
        # czy przyklad spelnia regule
        if example.result != self.result:
            return False
        for label in example.data.keys():
            if (
                self.conditions[label] == True
                or example.data[label] in self.conditions[label]
            ):
                continue
            return False
        return True

    def __str__(self):
        return str(self.conditions) + " -> " + str(self.result)


def generateStar(seed: Example, negativeSeed: Example):
    """Generate Star algorithm
    Args:
        seed (Example): Seed for algorithm
        negativeSeed (Example): Negative seed for algorithm
    Returns:
        list of Rules: List of Rules computed by algorithm
    """
    rules = []
    for label in seed.data.keys():
        newRuleConditions = {}
        for label2 in seed.data.keys():
            if label == label2:
                if seed.data[label2] != negativeSeed.data[label2]:
                    newRuleConditions[label2] = {
                        ex
                        for ex in seed.labels[label2]
                        if ex != negativeSeed.data[label2]
                    }
                else:
                    newRuleConditions[label2] = True
            else:
                newRuleConditions[label2] = True
        for key in newRuleConditions.keys():
            if newRuleConditions[key] != True:
                rules.append(Rule(conditions=newRuleConditions, result=seed.result))
                break
    return rules


class AQ:
    def __init__(self, data: list, labels, m, mode, testData: list, modified, unitTesting = False):
        self.data = data
        self.testData = testData
        self.labels = labels
        self.m = m
        self.mode = mode
        self.modified = modified
        self.unitTesting = unitTesting

    def getMostGeneralComplex(self, result):
        """
        Args:
            result (Result): Result which will be covered by most general rule
        Returns:
            Rule: Most general rule
        """
        conditions = {}
        for label in self.labels.keys():
            conditions[label] = True
        return Rule(conditions, result)

    def countCoveredExamples(self, rule: Rule, data):
        """
        Args:
            rule (Rule): Rule which function check
            data : Checked set

        Returns:
            int: Number of examples from self.data which are covered by rule
        """
        counter = 0
        for example in data:
            if rule.coversExample(example):
                counter += 1
        return counter

    def run(self):
        """
        Main algorithm
        Appends rules to self.rules based on given attributes for object
        """
        self.rules = []
        coveredExamples = []
        uncoveredExamples = copy.deepcopy(self.data)
        stopAlgorithm = False
        while not stopAlgorithm:
            testSetForRule = random.sample(self.testData, int(len(self.testData) / 40))
            xs = 0  # first of uncovered rules
            if self.mode == "unordered":
                negativeLabelIndexes = [
                    i
                    for i, x in enumerate(self.data)
                    if x.result != uncoveredExamples[xs].result
                ]
            else:
                negativeLabelIndexes = [
                    i
                    for i, x in enumerate(uncoveredExamples)
                    if x.result != uncoveredExamples[xs].result
                ]
            S = [self.getMostGeneralComplex(uncoveredExamples[xs].result)]
            for xn in negativeLabelIndexes:
                if self.mode == "unordered":
                    star = generateStar(uncoveredExamples[xs], self.data[xn])
                else:
                    star = generateStar(uncoveredExamples[xs], uncoveredExamples[xn])
                complexProduct = []
                for rule1 in star:
                    for rule2 in S:
                        complexProduct.append(rule1 * rule2)
                # leaving most general complexes
                mostGeneralComplexSet = []
                for i, rule1 in enumerate(complexProduct):
                    coveredFlag = False
                    for j, rule2 in enumerate(complexProduct):
                        if rule1.includesIn(rule2) and not rule2.includesIn(rule1):
                            coveredFlag = True
                    if not coveredFlag and rule1 not in mostGeneralComplexSet:
                        mostGeneralComplexSet.append(rule1)
                # selecting m best complexes
                mostGeneralComplexSetIndexes = [
                    i for i, x in enumerate(mostGeneralComplexSet)
                ]
                if not self.modified:
                    # classic AQ algorithm - evaluation of rules based on number of covered examples from training set
                    mostGeneralComplexSetIndexes.sort(
                        key=lambda i: self.countCoveredExamples(
                            mostGeneralComplexSet[i], uncoveredExamples
                        ),
                        reverse=True,
                    )
                    # unit testing - additional rule that in case of complexes with the same quality chooses the one that
                    # appears last in the star
                    if self.unitTesting:
                        mostGeneralComplexSetIndexes.sort(
                            key=lambda i: (self.countCoveredExamples(
                                mostGeneralComplexSet[i], uncoveredExamples
                            ), i),
                            reverse=True,
                        )

                else:
                    # modified AQ algorithm - evaluation of rules based on number of covered examples from separate validation set
                    mostGeneralComplexSetIndexes.sort(
                        key=lambda i: self.countCoveredExamples(
                            mostGeneralComplexSet[i], testSetForRule
                        ),
                        reverse=True,
                    )
                S = [
                    x
                    for i, x in enumerate(mostGeneralComplexSet)
                    if i
                    in mostGeneralComplexSetIndexes[
                        0 : (self.m if xn != negativeLabelIndexes[-1] else 1)
                    ]
                ]
            newRule = S[0]
            self.rules.append(newRule)
            coveredExamples.extend([x for x in self.data if newRule.coversExample(x)])
            uncoveredExamples = [
                x for x in uncoveredExamples if not newRule.coversExample(x)
            ]
            # all examples are covered, stop algorithm
            if len(uncoveredExamples) == 0:
                stopAlgorithm = True
                self.evaluatedRules = self.rules

    def validate(self, example: Example):
        """Predicts class of example
        Args:
            example (Example): Example to validate
        Returns:
            type(example.result): Predicted value by algorithm
        """
        for rule in self.rules:
            for label in example.data.keys():
                if (
                    rule.conditions[label] == True
                    or example.data[label] in rule.conditions[label]
                ):
                    isCovered = True
                    continue
                isCovered = False
                break
            if isCovered:
                return rule.result
