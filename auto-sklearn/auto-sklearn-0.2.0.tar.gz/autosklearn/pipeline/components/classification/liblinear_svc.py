from ConfigSpace.configuration_space import ConfigurationSpace
from ConfigSpace.hyperparameters import UniformFloatHyperparameter, \
    CategoricalHyperparameter, Constant
from ConfigSpace.forbidden import ForbiddenEqualsClause, \
    ForbiddenAndConjunction

from autosklearn.pipeline.components.base import AutoSklearnClassificationAlgorithm
from autosklearn.pipeline.implementations.util import softmax
from autosklearn.pipeline.constants import *


class LibLinear_SVC(AutoSklearnClassificationAlgorithm):
    # Liblinear is not deterministic as it uses a RNG inside
    def __init__(self, penalty, loss, dual, tol, C, multi_class,
                 fit_intercept, intercept_scaling, class_weight=None,
                 random_state=None):
        self.penalty = penalty
        self.loss = loss
        self.dual = dual
        self.tol = tol
        self.C = C
        self.multi_class = multi_class
        self.fit_intercept = fit_intercept
        self.intercept_scaling = intercept_scaling
        self.class_weight = class_weight
        self.random_state = random_state
        self.estimator = None

    def fit(self, X, Y):
        import sklearn.svm
        import sklearn.multiclass

        self.C = float(self.C)
        self.tol = float(self.tol)

        self.dual = self.dual == 'True'
        self.fit_intercept = self.fit_intercept == 'True'
        self.intercept_scaling = float(self.intercept_scaling)

        if self.class_weight == "None":
            self.class_weight = None

        estimator = sklearn.svm.LinearSVC(penalty=self.penalty,
                                          loss=self.loss,
                                          dual=self.dual,
                                          tol=self.tol,
                                          C=self.C,
                                          class_weight=self.class_weight,
                                          fit_intercept=self.fit_intercept,
                                          intercept_scaling=self.intercept_scaling,
                                          multi_class=self.multi_class,
                                          random_state=self.random_state)

        if len(Y.shape) == 2 and Y.shape[1] > 1:
            self.estimator = sklearn.multiclass.OneVsRestClassifier(estimator, n_jobs=1)
        else:
            self.estimator = estimator

        self.estimator.fit(X, Y)
        return self

    def predict(self, X):
        if self.estimator is None:
            raise NotImplementedError()
        return self.estimator.predict(X)

    def predict_proba(self, X):
        if self.estimator is None:
            raise NotImplementedError()

        df = self.estimator.decision_function(X)
        return softmax(df)

    @staticmethod
    def get_properties(dataset_properties=None):
        return {'shortname': 'Liblinear-SVC',
                'name': 'Liblinear Support Vector Classification',
                'handles_regression': False,
                'handles_classification': True,
                'handles_multiclass': True,
                'handles_multilabel': True,
                'is_deterministic': False,
                'input': (SPARSE, DENSE, UNSIGNED_DATA),
                'output': (PREDICTIONS,)}

    @staticmethod
    def get_hyperparameter_search_space(dataset_properties=None):
        cs = ConfigurationSpace()

        penalty = CategoricalHyperparameter(
            "penalty", ["l1", "l2"], default="l2")
        loss = CategoricalHyperparameter(
            "loss", ["hinge", "squared_hinge"], default="squared_hinge")
        dual = Constant("dual", "False")
        # This is set ad-hoc
        tol = UniformFloatHyperparameter(
            "tol", 1e-5, 1e-1, default=1e-4, log=True)
        C = UniformFloatHyperparameter(
            "C", 0.03125, 32768, log=True, default=1.0)
        multi_class = Constant("multi_class", "ovr")
        # These are set ad-hoc
        fit_intercept = Constant("fit_intercept", "True")
        intercept_scaling = Constant("intercept_scaling", 1)
        cs.add_hyperparameters([penalty, loss, dual, tol, C, multi_class,
                                fit_intercept, intercept_scaling])

        penalty_and_loss = ForbiddenAndConjunction(
            ForbiddenEqualsClause(penalty, "l1"),
            ForbiddenEqualsClause(loss, "hinge")
        )
        constant_penalty_and_loss = ForbiddenAndConjunction(
            ForbiddenEqualsClause(dual, "False"),
            ForbiddenEqualsClause(penalty, "l2"),
            ForbiddenEqualsClause(loss, "hinge")
        )
        penalty_and_dual = ForbiddenAndConjunction(
            ForbiddenEqualsClause(dual, "False"),
            ForbiddenEqualsClause(penalty, "l1")
        )
        cs.add_forbidden_clause(penalty_and_loss)
        cs.add_forbidden_clause(constant_penalty_and_loss)
        cs.add_forbidden_clause(penalty_and_dual)
        return cs
