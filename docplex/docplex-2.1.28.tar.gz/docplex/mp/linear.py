# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2015, 2016
# --------------------------------------------------------------------------

# pylint: disable=too-many-lines
from __future__ import print_function

from six import iteritems

from docplex.mp.constants import ComparisonType, UpdateEvent, CplexScope
from docplex.mp.compat23 import unitext
from docplex.mp.basic import ModelingObject, Expr, ModelingObjectBase, _SubscriptionMixin, _BendersAnnotatedMixin
from docplex.mp.operand import LinearOperand
from docplex.mp.vartype import BinaryVarType, IntegerVarType, ContinuousVarType
from docplex.mp.utils import *


class DOCplexQuadraticArithException(Exception):
    # INTERNAL
    pass


# from docplex.mp.xcounter import ExprCounter


class Var(ModelingObject, LinearOperand, _BendersAnnotatedMixin):
    """Var()

    This class models decision variables.
    Decision variables are instantiated by :class:`docplex.mp.model.Model` methods such as :func:`docplex.mp.model.Model.var`.

    """

    __slots__ = ('_vartype', '_lb', '_ub')

    def __init__(self, model, vartype, name,
                 lb=None, ub=None,
                 container=None,
                 _safe_lb=False, _safe_ub=False):
        ModelingObject.__init__(self, model, name)
        self._vartype = vartype
        self._container = container

        if _safe_lb:
            self._lb = lb
        else:
            self._lb = vartype.compute_lb(lb)
        if _safe_ub:
            self._ub = ub
        else:
            self._ub = vartype.compute_ub(ub)

    def cplex_scope(self):
        return CplexScope.VAR_SCOPE

    # noinspection PyUnusedLocal
    def copy(self, new_model, var_mapping):
        return var_mapping[self]

    # linear operand api

    def as_variable(self):
        return self

    def iter_terms(self):
        yield self, 1

    iter_sorted_terms = iter_terms

    def number_of_terms(self):
        return 1

    def unchecked_get_coef(self, dvar):
        return 1 if dvar is self else 0

    def contains_var(self, dvar):
        return self is dvar

    def accept_initial_value(self, candidate_value):
        return self.vartype.accept_domain_value(candidate_value, lb=self._lb, ub=self._ub)

    def check_name(self, new_name):
        ModelingObject.check_name(self, new_name)
        if not is_string(new_name) or not new_name:
            self.fatal("Variable name accepts only non-empty strings, got: {0!s}", new_name)
        elif new_name.find(' ') >= 0:
            self.warning("Variable name contains blank space, var: {0!s}, name: \'{1!s}\'", self, new_name)

    def __hash__(self):
        return self._index

    def to_linear_expr(self):
        # INTERNAL
        return LinearExpr(model=self._model, e=self, safe=True, transient=True)
        # return MonomialExpr(self._get_model(), self, coeff=1)

    def set_name(self, new_name):
        # INTERNAL
        self.check_name(new_name)
        self.model.set_var_name(self, new_name)

    name = property(ModelingObjectBase.get_name, set_name)

    @property
    def lb(self):
        """ This property is used to get or set the lower bound of the variable.

        Possible values for the lower bound depend on the variable type. Binary variables
        accept only 0 or 1 as bounds. An integer variable will convert the lower bound value to the
        ceiling integer value of the argument.
        """
        return self._lb

    @lb.setter
    def lb(self, new_lb):
        self.set_lb(new_lb)

    def _get_lb(self):
        return self._lb

    def set_lb(self, lb):
        if lb != self._lb:
            self._model.set_var_lb(self, lb)
            return self._lb

    def _internal_set_lb(self, lb):
        # Internal, used only by the model
        self._lb = lb

    def _internal_set_ub(self, ub):
        # INTERNAL
        self._ub = ub

    @property
    def ub(self):
        """ This property is used to get or set the upper bound of the variable.

        Possible values for the upper bound depend on the variable type. Binary variables
        accept only 0 or 1 as bounds. An integer variable will convert the upper bound value to the
        floor integer value of the argument.

        To reset the upper bound to its default infinity value, use :func:`docplex.mp.model.Model.infinity`.
        """
        return self._ub

    @ub.setter
    def ub(self, new_ub):
        self.set_ub(new_ub)

    def set_ub(self, ub):
        if ub != self._ub:
            self._model.set_var_ub(self, ub)
            return self._ub

    def _get_ub(self):
        return self._ub

    def has_free_lb(self):
        return self.get_linear_factory().is_free_lb(self._lb)

    def has_free_ub(self):
        return self.get_linear_factory().is_free_ub(self._ub)

    def is_free(self):
        return self.has_free_lb() and self.has_free_ub()

    @property
    def vartype(self):
        """ This property returns the variable type, an instance of :class:`VarType`.

        """
        return self._vartype

    def get_vartype(self):
        return self._vartype

    def set_vartype(self, new_vartype):
        return self._model.set_var_type(self, new_vartype)

    def _set_vartype_internal(self, new_vartype):
        # INTERNAL
        self._vartype = new_vartype


    def has_type(self, vartype):
        # internal
        return type(self._vartype) == vartype

    def is_binary(self):
        """ Checks if the variable is binary.

        Returns:
            Boolean: True if the variable is of type Binary.
        """
        return self.has_type(BinaryVarType)

    def is_integer(self):
        """ Checks if the variable is integer.

        Returns:
            Boolean: True if the variable is of type Integer.
        """
        return self.has_type(IntegerVarType)

    def is_continuous(self):
        """ Checks if the variable is continuous.

        Returns:
            Boolean: True if the variable is of type Continuous.
        """
        return self.has_type(ContinuousVarType)

    def is_discrete(self):
        """  Checks if the variable is discrete.

        Returns:
            Boolean: True if the variable is of  type Binary or Integer.
        """
        return self._vartype.is_discrete()

    @property
    def float_precision(self):
        return 0 if self.is_discrete() else self._model.float_precision

    def get_value(self):
        # for compatibility only: use solution_value instead
        print("* get_value() is deprecated, use property solution_value instead")  # pragma: no cover
        return self.solution_value  # pragma: no cover

    @property
    def solution_value(self):
        """ This property returns the solution value of the variable.

        Raises:
            DOCplexException
                if the model has not been solved succesfully.

        """
        self._check_model_has_solution()
        return self._get_solution_value()

    @property
    def unchecked_solution_value(self):
        # INTERNAL
        return self._get_solution_value()

    def _get_solution_value(self, s=None):
        sol = s or  self._get_model()._get_solution()
        return sol.get_value(self)

    def get_container_index(self):
        ctn = self.get_container()
        return ctn.index if ctn else -1

    def get_key(self):
        self_container = self.get_container()
        return self_container.get_var_key(self) if self_container else None

    def __ne__(self, other):
        # INTERNAL: For now, not supported
        self.model.unsupported_neq_error(self, other)

    def __mul__(self, e):
        return self.times(e)

    def times(self, e):
        if is_number(e):
            if e:
                return MonomialExpr(self._model, self, e, checked_num=True)
            else:
                return self._model._lfactory.new_zero_expr()
        elif isinstance(e, ZeroExpr):
            return e
        elif isinstance(e, (Var, Expr)):
            return self._model._qfactory.new_var_product(self, e)
        else:
            return self.to_linear_expr().multiply(e)

    def __rmul__(self, e):
        return self.times(e)

    def __add__(self, e):
        return self.plus(e)

    def plus(self, e):
        if isinstance(e, Var):
            expr = self._make_linear_expr()
            expr._add_term(e)
            return expr

        elif is_number(e):
            return self._make_linear_expr(constant=e)
        elif e.is_quad_expr():
            return e.plus(self)
        else:
            return self.to_linear_expr().add(e)

    def _make_linear_expr(self, constant=0, safe=True):
        return LinearExpr(self._model, self, constant, None, safe, True)

    def __radd__(self, e):
        return self.plus(e)

    def __sub__(self, e):
        return self.minus(e)

    def minus(self, e):
        if isinstance(e, LinearOperand):
            return self.to_linear_expr().subtract(e)

        elif is_number(e):
            # v -k -> expression(v,-1) -k
            return self._make_linear_expr(constant=-e)

        elif isinstance(e, Expr) and e.is_quad_expr():
            return e.rminus(self)
        else:
            return self.to_linear_expr().subtract(e)

    def __rsub__(self, e):
        # e - self
        # if is_number(e):
        #     return self._make_linear_expr(e=(self, -1), constant=e, safe=True)
        # else:
        expr = self.get_linear_factory()._to_linear_expr(e, force_clone=True)  # makes a clone.
        return expr.subtract(self)

    def divide(self, e):
        return self.to_linear_expr().divide(e)

    def __div__(self, e):
        return self.divide(e)

    def __truediv__(self, e):
        # for py3
        # INTERNAL
        return self.divide(e)  # pragma: no cover

    def __rtruediv__(self, e):
        # for py3
        self.fatal("Variable {0!s} cannot be used as denominator of {1!s}", self, e)  # pragma: no cover

    def __rdiv__(self, e):
        self.fatal("Variable {0!s} cannot be used as denominator of {1!s}", self, e)

    def __pos__(self):
        # the "+e" unary plus is syntactic sugar
        return self

    def __neg__(self):
        # the "-e" unary minus returns a linear expression
        return MonomialExpr(self._model, dvar=self, coeff=-1, checked_num=True)

    def __pow__(self, power):
        # INTERNAL
        # power must be checke in {0, 1, 2}
        self.model.typecheck_as_power(self, power)
        if 0 == power:
            return 1
        elif 1 == power:
            return self
        else:
            return self.square()

    def square(self):
        return self._model._qfactory.new_var_square(self)

    def __int__(self):
        """ Converts a decision variable to a integer number.

        This is only possible for discrete variables,
        and when the model has been solved successfully.
        If the model has been solved, returns the variable's solution value.

        Returns:
            int: The variable's solution value.

        Raises:
            DOCplexException
                if the model has not been solved successfully.
            DOCplexException
                if the variable is not discrete.
        """

        if self.is_continuous():
            self.fatal("Cannot convert continuous variable value to int: {0!s}", self)
        return int(self.solution_value)

    def __float__(self):
        """ Converts a decision variable to a floating-point number.

        This is only possible when the model has been solved successfully,
        otherwise an exception is raised.
        If the model has been solved, it returns the variable's solution value.

        Returns:
            float: The variable's solution value.
        Raises:
            DOCplexException
                if the model has not been solved successfully.
        """
        return float(self.solution_value)

    def to_bool(self):
        """ Converts a variable value to True or False.

        This is only possible for discrete variables and assumes there is a solution.

        Raises:
            DOCplexException 
                if the model has not been solved successfully.
            DOCplexException 
                if the variable is not discrete.

        Returns:
            Boolean: True if the variable value is nonzero, else False.
        """
        if not self.is_discrete():
            self.fatal("boolean conversion only for discrete variables, type is {0!s}", self.vartype)
        value = self.solution_value  # this property checks for a solution.
        return value != 0

    # def __nonzero__(self):
    # return self.to_boolean(precision=1e-5)

    def __str__(self):
        """
        Returns:
            string: A string representation of the variable.

        """
        return self.to_string()

    def to_string(self):
        str_name = self.get_name() or ('_x%d' % (self.unchecked_index + 1))
        return str_name

    def print_name(self):
        # INTERNAL
        return self._name or self._model._var_scope.new_obj_symbol(self)

    def __repr__(self):
        self_vartype, self_lb, self_ub = self._vartype, self._lb, self._ub
        if self_vartype.is_default_lb(self_lb):
            repr_lb = ''
        else:
            repr_lb = ',lb={0:g}'.format(self_lb)
        if self_vartype.is_default_ub(self_ub):
            repr_ub = ''
        else:
            repr_ub = ',ub={0:g}'.format(self_ub)
        if self.has_name():
            repr_name = ",name='{0}'".format(self.name)
        else:
            repr_name = ''
        return "docplex.mp.linear.Var(type={0}{1}{2}{3})". \
            format(self_vartype.one_letter_symbol(), repr_name, repr_lb, repr_ub)

    @property
    def reduced_cost(self):
        """ Returns the reduced cost of the variable.

        Note:
            This method will raise an exception if the model has not been solved successfully as a LP.

        Returns:
            The reduced cost of the variable (a float value).
        """
        return self._model.reduced_costs(self)

    @property
    def benders_annotation(self):
        """
        This property is used to get or set the Benders annotation of a variable.
        The value of the annotation must be a positive integer

        """
        return self.get_benders_annotation()

    @benders_annotation.setter
    def benders_annotation(self, new_anno):
        self.set_benders_annotation(new_anno)





# noinspection PyAbstractClass
class AbstractLinearExpr(Expr, LinearOperand):
    __slots__ = ()

    def get_coef(self, dvar):
        """ Returns the coefficient of a variable in the expression.

        Note:
            If the variable is not present in the expression, the function returns 0.

        :param dvar: The variable for which the coefficient is being queried.

        :return: A floating-point number.
        """
        self.model.typecheck_var(dvar)
        return self.unchecked_get_coef(dvar)

    def __getitem__(self, dvar):
        # direct access to a variable coef x[var]
        return self.unchecked_get_coef(dvar)

    def __iter__(self):
        # INTERNAL: this is necessary to prevent expr from being an iterable.
        # as it follows getitem protocol, it can mistakenly be interpreted as an iterable
        # but this would make sum loop forever.
        raise TypeError

class MonomialExpr( _SubscriptionMixin, AbstractLinearExpr):
    # INTERNAL

    def _get_solution_value(self, s=None):
        raw = self.coef * self._dvar._get_solution_value(s)
        return self._round_if_discrete(raw)

    # INTERNAL class
    __slots__ = ('_dvar', '_coef', '_subscribers')

    # noinspection PyMissingConstructor
    def __init__(self, model, dvar, coeff, checked_num=False, safe=False):
        self._model = model  # faster than to call recursively init methods...
        self._name = None
        self._dvar = dvar
        self._subscribers = []
        # check perf on that
        if safe:
            self._coef = coeff
        else:
            validfn = model._checker.get_number_validation_fn()
            self._coef = validfn(coeff) if validfn else coeff

    def number_of_variables(self):
        return 1

    @property
    def var(self):
        return self._dvar

    @property
    def coef(self):
        return self._coef

    @property
    def constant(self):
        # for compatibility
        return 0

    def as_variable(self):
        # INTERNAL
        return self._dvar if 1 == self._coef else None

    def clone(self):
        return MonomialExpr(self.model, self._dvar, self._coef, safe=True)

    def copy(self, target_model, var_mapping):
        copy_var = var_mapping[self._dvar]
        return MonomialExpr(target_model, dvar=copy_var, coeff=self._coef, safe=True)


    def iter_terms(self):
        yield self._dvar, self._coef

    iter_sorted_terms = iter_terms

    def unchecked_get_coef(self, dvar):
        return self._coef if dvar is self._dvar else 0

    def contains_var(self, dvar):
        return self._dvar is dvar

    def is_normalized(self):
        # INTERNAL
        return self._coef != 0  # pragma: no cover

    def is_discrete(self):
        return self._dvar.is_discrete() and is_int(self._coef)

    # arithmetics
    def negate(self):
        self._coef = - self._coef
        self.notify_modified(event=UpdateEvent.LinExprCoef)
        return self

    def plus(self, e):
        if isinstance(e, LinearOperand) or is_number(e):
            return self.to_linear_expr().add(e)
        else:
            return e.plus(self)

    def minus(self, e):
        if isinstance(e, LinearOperand) or is_number(e):
            expr = self.to_linear_expr()
            expr.subtract(e)
            return expr
        else:
            return e.rminus(self)

    def times(self, e):
        if is_number(e):
            # e might be a fancy numpy type
            if 1 == e:
                return self
            elif 0 == e:
                return self.get_linear_factory().new_zero_expr()
            else:
                # return a fresh instance
                return MonomialExpr(self._model, self._dvar, self._coef * e, checked_num=True)
        elif isinstance(e, LinearExpr):
            return e.times(self)
        elif isinstance(e, Var):
            return self.model._qfactory.new_var_product(e, self)
        elif isinstance(e, MonomialExpr):
            return self.model._qfactory.new_monomial_product(self, e)
        else:
            expr = self.to_linear_expr()
            return expr.multiply(e)

    def square(self):
        return self.model._qfactory.new_monomial_product(self, self)

    def quotient(self, e):
        self.model.typecheck_as_denominator(e, self)
        inverse = 1.0 / float(e)
        return MonomialExpr(self._model, self._dvar, self._coef * inverse, checked_num=True)

    def __add__(self, e):
        return self.plus(e)

    def __radd__(self, e):
        return self.__add__(e)

    def __sub__(self, e):
        return self.minus(e)

    def __rsub__(self, e):
        return self.model._to_linear_expr(e, force_clone=True).minus(self)

    def __neg__(self):
        opposite = self.clone()
        return opposite.negate()

    def __mul__(self, e):
        return self.times(e)

    def __rmul__(self, e):
        return self.times(e)

    def __div__(self, e):
        return self.quotient(e)

    def __truediv__(self, e):
        # for py3
        # INTERNAL
        return self.__div__(e)  # pragma: no cover

    def __rtruediv__(self, e):
        # for py3
        self.model.cannot_be_used_as_denominator_error(self, e)  # pragma: no cover

    def __rdiv__(self, e):
        self.model.cannot_be_used_as_denominator_error(self, e)

    subtract = minus
    divide = quotient
    multiply = times
    add = plus

    # -- arithmetic to self
    def __iadd__(self, other):
        if isinstance(other, LinearOperand) or is_number(other):
            added = self.to_linear_expr().add(other)
        else:
            added = other.plus(self)
        self.notify_replaced(added)
        return added

    def __isub__(self, other):
        if isinstance(other, LinearOperand) or is_number(other):
            expr = self.to_linear_expr()
            expr.subtract(other)
            subtracted = expr
        else:
            subtracted = other.rminus(self)
        self.notify_replaced(subtracted)
        return subtracted

    def __imul__(self, e):
        if is_number(e):
            # e might be a fancy numpy type
            if 1 == e:
                # fast exit, no replacement
                return self
            elif 0 == e:
                product = self.get_linear_factory().new_zero_expr()
            else:
                # return a fresh instance
                self._coef *= e
                self.notify_modified(event=UpdateEvent.LinExprCoef)
                # fast exit
                return self
        elif isinstance(e, LinearExpr):
            product =  e.times(self)
        elif isinstance(e, Var):
            product = self.model._qfactory.new_var_product(e, self)
        elif isinstance(e, MonomialExpr):
            product = self.model._qfactory.new_monomial_product(self, e)
        elif isinstance(e, Expr) and e.is_quad_expr():
            if e.has_quadratic_term():
                self.fatal('Cannot multiply non-constant expression {0!s} with quadratic expression {1!s}',
                           self, e)
            else:
                product = self.model._qfactory.new_monomial_product(self, e.linear_part)
        else:
            product = self.to_linear_expr().multiply(e)
            self.notify_replaced(product)
        return product

    def __idiv__(self, other):
        return self.divide(other)

    def __itruediv__(self, other):   # pragma: no cover
        # for py3
        return self.divide(other)

    def divide(self, other):
        self.model.typecheck_as_denominator(other, self)
        inverse = 1.0 / float(other)
        self._coef *= inverse
        self.notify_modified(event=UpdateEvent.LinExprCoef)
        return self


    def equals_expr(self, other):
        if isinstance(other, MonomialExpr):
            return self.var is other.var and self.coef == other.coef
        elif isinstance(other, LinearExpr):
            expr = other
            if expr.constant == 0 and expr.number_of_variables() == 1:
                (v, k) = next(other.iter_terms())
                return self.var is v and self.coef == k
        else:
            return False

    # conversion
    def to_linear_expr(self):
        #terms = self._model._lfactory.term_dict_type([(self._dvar, self._coef)])
        e = LinearExpr(self._model, e=(self._dvar, self._coef), safe=True, transient=True)
        return e

    def to_stringio(self, oss, nb_digits, use_space, var_namer=lambda v: v.print_name()):
        self_coef = self._coef
        if self_coef != 1:
            if self_coef < 0:
                oss.write(u'-')
                self_coef = - self_coef
            if self_coef != 1:
                self._num_to_stringio(oss, num=self_coef, ndigits=nb_digits)
            if use_space:
                oss.write(u' ')
        oss.write(unitext(var_namer(self._dvar)))

    def __repr__(self):
        return "docplex.mp.MonomialExpr(%s)" % self.to_string()


class LinearExpr(_SubscriptionMixin, AbstractLinearExpr):
    """LinearExpr()

    This class models linear expressions.
    This class is not intended to be instantiated. Expressions are built
    either using operators or using `Model.linear_expr()`.
    """

    def _new_terms_dict(self, model, *args, **kwargs):
        return model._term_dict_type(*args, **kwargs)

    def _new_empty_terms_dict(self, model):
        return model._term_dict_type()


    def to_linear_expr(self):
        return self

    def _get_terms_dict(self):
        # INTERNAL
        return self.__terms

    def __typecheck_terms_dict(self, terms):  #  pragma: no cover
        """
        INTERNAL: check a given dictionary of terms for (var, float)
        :param terms:
        :return:
        """
        if not isinstance(terms, dict):
            self.fatal("expecting expression terms as python dict, got: {0!s}", terms)
        self_model = self.model
        for (v, k) in iteritems(terms):
            self_model.typecheck_var(v)
            self_model.typecheck_num(k, 'LinearExpr:importTerms')

    def _assign_terms(self, terms, is_safe=False, assume_normalized=False):  # pragma: no cover
        if not is_safe:
            self.__typecheck_terms_dict(terms)
        if assume_normalized:
            self.__terms = terms
        else:
            # must put back to normal form
            self.__terms = self._new_terms_dict(self._model,
                                                [(k, v) for k, v in iteritems(terms) if v != 0])
        return self

    __slots__ = ('_constant', '__terms', '_transient', '_subscribers')

    #@profile
    def __init__(self, model, e=None, constant=0, name=None, safe=False, transient=False):
        ModelingObjectBase.__init__(self, model, name)
        # a global counter for performance measurement
        #model._linexpr_instance_counter += 1
        # "calling LinearExpr ctor, k=%d" % LinearExpr.InstanceCounter)
        if not safe and constant:
            model.typecheck_num(constant, 'LinearExpr()')
        self._constant = constant
        self._transient = transient
        self._subscribers = []


        if isinstance(e, dict):
            if safe:
                self.__terms = e
            else:
                self_terms = model._term_dict_type()
                for (v, k) in iteritems(e):
                    model.typecheck_var(v)
                    model.typecheck_num(k, 'LinearExpr')
                    if k != 0:
                        self_terms[v] = k
                self.__terms = self_terms
            return
        else:
            self.__terms = model._term_dict_type()

        if e is None:
            pass
        elif isinstance(e, Var):
            self.__terms[e] = 1

        elif isinstance(e, MonomialExpr):
            self._add_term(e.var, e.coef)

        elif isinstance(e, LinearExpr):
            # note that transient is not kept.
            self._constant = e.constant
            self.__terms = self._new_terms_dict(model, e._get_terms_dict())  # make a copy

        elif is_number(e):
            self._constant += e

        elif isinstance(e, tuple):
            v, k = e
            self.__terms[v] = k

        else:
            self.fatal("Cannot convert this to docplex.mp.LinearExpr, {0!r}", e)

    def keep(self):
        self._transient = False

    def is_kept(self):
        # INTERNAL
        return not self._transient

    def is_transient(self):  # pragma: no cover
        # INTERNAL
        return self._transient

    def clone_if_necessary(self):
        #  INTERNAL
        if self._transient and not self._model._keep_all_exprs and not self.is_in_use():
            return self
        else:
            return self.clone()

    def set_name(self, name):
        Expr.set_name(self, name)
        # an expression with a name is not transient any more
        if name:
            self.keep()

    def _get_name(self):
        return self._name

    name = property(_get_name, set_name)

    def clone(self):
        """
        Returns:
            A copy of the expression on the same model.
        """
        self._model._linexpr_clone_counter += 1
        cloned_terms = self._new_terms_dict(self._model, self.__terms)  # faster than copy() on OrderedDict()
        cloned = LinearExpr(model=self._model, e=cloned_terms, constant=self._constant, safe=True)
        return cloned

    def copy(self, target_model, var_mapping):
        # INTERNAL
        copied_terms = self._new_terms_dict(target_model)
        for v, k in self.iter_sorted_terms():
            copied_terms[var_mapping[v]] = k
        copied_expr = LinearExpr(model=target_model, e=copied_terms, constant=self.constant, safe=True)
        return copied_expr

    def negate(self):
        """ Takes the negation of an expression.

        Changes the expression by replacing each variable coefficient and the constant term
        by its opposite.

        Note:
            This method does not create any new expression but modifies the `self` instance.

        Returns:
            The modified self.

        """
        self._constant = - self._constant
        self_terms = self.__terms
        for v, k in iteritems(self_terms):
            self_terms[v] = -k
        self.notify_modified(event=UpdateEvent.LinExprGlobal)
        return self

    def _clear(self):
        """ Clears the expression.

        All variables and coefficients are removed and the constant term is set to zero.
        """
        #self._check_mutable()
        self._constant = 0
        self.__terms.clear()

    def equals_constant(self, scalar):
        """ Checks if the expression equals a constant term.

        Args:
            scalar (float): A floating-point number.
        Returns:
            Boolean: True if the expression equals this constant term.
        """
        return self.is_constant() and (scalar == self._constant)

    def is_zero(self):
        return self.equals_constant(0)

    def is_one(self):
        return self.equals_constant(1)

    def is_constant(self):
        """
        Checks if the expression is a constant.

        Returns:
            Boolean: True if the expression consists of only a constant term.
        """
        return not self.__terms


    def _has_nonzero_var_term(self):
        for dv, k in self.iter_terms():
            if k:
                return True
        else:
            return False


    def as_variable(self):
        # INTERNAL: returns True if expression is in fact a variable (1*x)
        if 0 == self.constant and 1 == len(self.__terms):
            for v, k in self.iter_terms():
                if k == 1:
                    return v
        return None

    def is_normalized(self):
        # INTERNAL
        for _, k in self.iter_terms():
            if not k:
                return False  # pragma: no cover
        return True

    def normalize(self):
        # modifies self
        doomed = [dv for dv, k in self.iter_terms() if not k]
        lterms = self.__terms
        for d in doomed:
            del lterms[d]

    def normalized(self):
        if self.is_normalized():
            return self
        else:
            cloned = self.clone()
            cloned.normalize()
            return cloned


    def number_of_variables(self):
        return len(self.__terms)

    def unchecked_get_coef(self, dvar):
        # INTERNAL
        return self.__terms.get(dvar, 0)

    def add_term(self, dvar, coeff):
        """
        Adds a term (variable and coefficient) to the expression.

        Args:
            dvar (:class:`Var`): A decision variable.
            coeff (float): A floating-point number.

        Returns:
            The modified expression itself.
        """
        if coeff:
            #self._check_mutable()
            self._model.typecheck_var(dvar)
            self._model.typecheck_num(coeff)
            self._add_term(dvar, coeff)
            self.notify_modified(event=UpdateEvent.LinExprCoef)
        return self

    def _add_term(self, dvar, coef=1):
        # INTERNAL
        self_terms = self.__terms
        if coef or dvar in self_terms:
            self_terms[dvar] = self_terms.get(dvar, 0) + coef

    def set_coefficient(self, dvar, coeff):
        #self._check_mutable()
        self._model.typecheck_var(dvar)
        self._model.typecheck_num(coeff)
        self._set_coefficient(dvar, coeff)

    def _set_coefficient_internal(self, dvar, coeff):
        self_terms = self.__terms
        if coeff or dvar in self_terms:
            self_terms[dvar] = coeff
            return True
        else:
            return False

    def _set_coefficient(self, dvar, coeff):
        if self._set_coefficient_internal(dvar, coeff):
            self.notify_modified(event=UpdateEvent.LinExprCoef)

    def set_coefficients(self, var_coef_seq):
        #self._check_mutable()
        # TODO: typecheck
        self._set_coefficients(var_coef_seq)

    #@profile
    def _set_coefficients(self, var_coef_seq):
        nb_changes = 0
        for dv, k in var_coef_seq:
            if self._set_coefficient_internal(dv, k):
                nb_changes += 1
        if nb_changes:
            self.notify_modified(event=UpdateEvent.LinExprCoef)

    def remove_term(self, dvar):
        """ Removes a term associated with a variable from the expression.

        Args:
            dvar (:class:`Var`): A decision variable.

        Returns:
            The modified expression.

        """
        self.set_coefficient(dvar, 0)

    @property
    def constant(self):
        """
        This property is used to get or set the constant term of the expression.
        """
        return self._constant

    @constant.setter
    def constant(self, new_constant):
        self._set_constant(new_constant)

    def get_constant(self):
        return self._constant

    def _set_constant(self, new_constant):
        if new_constant != self._constant:
            #self._check_mutable()
            self._constant = new_constant
            self.notify_modified(event=UpdateEvent.ExprConstant)


    # def iter_variables(self):
    #     """  Iterates over all variables mentioned in the linear expression.
    #
    #     Returns:
    #         An iterator object.
    #     """
    #     # return iter(self.__terms.keys())

    def contains_var(self, dvar):
        """ Checks whether a decision variable is part of an expression.

        Args:
            dvar (:class:`Var`): A decision variable.

        Returns:
            Boolean: True if `dvar` is mentioned in the expression with a nonzero coefficient.
        """
        return dvar in self.__terms

    def equals_expr(self, other):
        if is_number(other):
            return self.is_constant() and other == self.constant
        elif isinstance(other, LinearExpr):
            if self.constant != other.constant:
                return False
            if self.number_of_variables() != other.number_of_variables():
                return False
            for dv, k in self.iter_terms():
                if k != other[dv]:
                    return False
            else:
                return True
        else:
            return False

    # noinspection PyPep8
    def to_stringio(self, oss, nb_digits, use_space, var_namer=lambda v: v.print_name()):
        # INTERNAL
        # Writes unicode repsentation of self
        c = 0
        # noinspection PyPep8Naming
        SP = u' '

        for v, coeff in self.iter_sorted_terms():
            if not coeff:
                continue  #  pragma: no cover

            # 1 separator
            if use_space and c > 0:
                oss.write(SP)

            # ---
            # sign is printed if  non-first OR negative
            # at the end of this block coeff is positive
            if coeff < 0 or c > 0:
                oss.write(u'-' if coeff < 0 else u'+')
                if coeff < 0:
                    coeff = -coeff
                if use_space and c > 0:
                    oss.write(SP)
            # ---

            if 1 != coeff:
                self._num_to_stringio(oss, coeff, nb_digits)
                if use_space:
                    oss.write(SP)

            varname = var_namer(v)
            oss.write(unitext(varname))
            c += 1

        k = self.constant
        if c == 0:
            self._num_to_stringio(oss, k, nb_digits)
        elif k != 0:
            if k < 0:
                sign = u'-'
                k = -k
            else:
                sign = u'+'
            if use_space: oss.write(SP)
            oss.write(sign)
            if use_space: oss.write(SP)
            self._num_to_stringio(oss, k, nb_digits)

    def _add_expr(self, other_expr):
        # INTERNAL
        #self._check_mutable()
        self._constant += other_expr._constant
        # merge term dictionaries
        for v, k in other_expr.iter_terms():
            # use unchecked version
            self._add_term(v, k)

    def _add_expr_scaled(self, expr, factor):
        # INTERNAL: used by quadratic
        if factor:
            self._constant += expr.get_constant() * factor
            for v, k in expr.iter_terms():
                # use unchecked version
                self._add_term(v, k * factor)

    # --- algebra methods always modify self.
    def add(self, e):
        """ Adds an expression to self.

        Note:
            This method does not create an new expression but modifies the `self` instance.

        Args:
            e: The expression to be added. Can be a variable, an expression, or a number.

        Returns:
            The modified self.

        See Also:
            The method :func:`plus` to compute a sum without modifying the self instance.
        """
        event = UpdateEvent.LinExprGlobal
        if isinstance(e, Var):
            self._add_term(e, coef=1)
        elif isinstance(e, LinearExpr):
            self._add_expr(e)
        elif isinstance(e, MonomialExpr):
            self._add_term(e._dvar, e._coef)
        elif isinstance(e, ZeroExpr):
            event = None
        elif is_number(e):
            self._constant += e
            event = UpdateEvent.ExprConstant
        elif isinstance(e, Expr) and e.is_quad_expr():
            raise DOCplexQuadraticArithException
        else:
            try:
                self.add(e.to_linear_expr())
            except AttributeError:
                self._unsupported_binary_operation(self, "+", e)

        self.notify_modified(event=event)
        return self

    def iter_terms(self):
        """ Iterates over the terms in the expression.

        Returns:
            An iterator over the (variable, coefficient) pairs in the expression.
        """
        return iteritems(self.__terms)

    def number_of_terms(self):
        return len(self.__terms)

    def subtract(self, e):
        """ Subtracts an expression from this expression.
        Note:
            This method does not create a new expression but modifies the `self` instance.

        Args:
            e: The expression to be subtracted. Can be either a variable, an expression, or a number.

        Returns:
            The modified self.

        See Also:
            The method :func:`minus` to compute a difference without modifying the `self` instance.
        """
        event = UpdateEvent.LinExprCoef
        if isinstance(e, Var):
            self._add_term(e, -1)
        elif is_number(e):
            self._constant -= e
            event = UpdateEvent.ExprConstant
        elif isinstance(e, LinearExpr):
            if e.is_constant() and 0 == e.get_constant():
                return self
            else:
                # 1. decr constant
                self.constant -= e.constant
                # merge term dictionaries 
                for v, k in e.iter_terms():
                    self._add_term(v, -k)
        elif isinstance(e, MonomialExpr):
            self._add_term(e.var, -e.coef)
        elif isinstance(e, ZeroExpr):
            event = None
        elif isinstance(e, Expr) and e.is_quad_expr():
            raise DOCplexQuadraticArithException
        else:
            try:
                self.subtract(e.to_linear_expr())
            except AttributeError:
                self._unsupported_binary_operation(self, "-", e)
        self.notify_modified(event)
        return self

    def _scale(self, factor):
        # INTERNAL: used my multiply
        # this method modifies self.
        #self._check_mutable()
        if 0 == factor:
            self._clear()
        elif factor != 1:
            self._constant *= factor
            self_terms = self.__terms
            for v, k in iteritems(self_terms):
                self_terms[v] = k * factor

    def multiply(self, e):
        """ Multiplies this expression by an expression.

        Note:
            This method does not create a new expression but modifies the `self` instance.

        Args:
            e: The expression that is used to multiply `self`.

        Returns:
            The modified `self`.

        See Also:
            The method :func:`times` to compute a multiplication without modifying the `self` instance.
        """
        mul_res = self
        event = UpdateEvent.LinExprGlobal
        self_constant = self.get_constant()
        if is_number(e):
            self._scale(factor=e)

        elif isinstance(e, LinearOperand):
            if e.is_constant():
                # simple scaling
                self._scale(factor=e.get_constant())
            elif self.is_constant():
                # self is constant: import other terms , scaled.
                # set constant to zero.
                if self_constant:
                    for lv, lk in e.iter_terms():
                        self.set_coefficient(dvar=lv, coeff=lk * self_constant)
                    self._constant *= e.get_constant()
            else:
                # yields a quadratic
                mul_res = self.model._qfactory.new_linexpr_product(self, e)
                event = UpdateEvent.LinExprPromotedToQuad

        elif isinstance(e, ZeroExpr):
            self._scale(factor=0)

        elif isinstance(e, Expr) and e.is_quad_expr():
            if not e.number_of_quadratic_terms:
                return self.multiply(e.linear_part)
            else:
                self.fatal("Multiply expects variable, expr or number, got: {0!s}", e)

        else:
            self.fatal("Multiply expects variable, expr or number, got: {0!s}", e)

        self.notify_modified(event=event)

        return mul_res

    def square(self):
        return self.model._qfactory.new_linexpr_product(self, self)

    def divide(self, e):
        """ Divides this expression by an operand.

        Args:
            e: The operand by which the self expression is divided. Only nonzero numbers are permitted.

        Note:
            This method does not create a new expression but modifies the `self` instance.

        Returns:
            The modified `self`.
        """
        self.model.typecheck_as_denominator(e, numerator=self)
        inverse = 1.0 / float(e)
        return self.multiply(inverse)

    # operator-based API
    def opposite(self):
        cloned = self.clone_if_necessary()
        cloned.negate()
        return cloned

    def plus(self, e):
        """ Computes the sum of the expression and some operand.

        Args:
            e: the expression to add to self. Can be either a variable, an expression or a number.

        Returns:
            a new expression equal to the sum of the self expression and `e`

        Note:
            This method doe snot modify self.
        """
        cloned = self.clone_if_necessary()
        try:
            return cloned.add(e)
        except DOCplexQuadraticArithException:
            return e.plus(self)

    def minus(self, e):
        cloned = self.clone_if_necessary()
        try:
            return cloned.subtract(e)
        except DOCplexQuadraticArithException:
            return e.rminus(self)

    def times(self, e):
        """ Computes the multiplication of this expression with an operand.

        Note:
            This method does not modify the `self` instance but returns a new expression instance.

        Args:
            e: The expression that is used to multiply `self`.

        Returns:
            A new instance of expression.
        """
        cloned = self.clone_if_necessary()
        return cloned.multiply(e)

    def quotient(self, e):
        """ Computes the division of this expression with an operand.

        Note:
            This method does not modify the `self` instance but returns a new expression instance.

        Args:
            e: The expression that is used to modify `self`. Only nonzero numbers are permitted.

        Returns:
            A new instance of expression.
        """
        cloned = self.clone_if_necessary()
        cloned.divide(e)
        return cloned

    def __add__(self, e):
        return self.plus(e)

    def __radd__(self, e):
        return self.plus(e)

    def __iadd__(self, e):
        try:
            self.add(e)
            return self
        except DOCplexQuadraticArithException:
            # modify self
            r = e + self
            #self = r
            return r

    def __sub__(self, e):
        return self.minus(e)

    def __rsub__(self, e):
        cloned = self.clone_if_necessary()
        cloned.subtract(e)
        cloned.negate()
        return cloned

    def __isub__(self, e):
        try:
            return self.subtract(e)
        except DOCplexQuadraticArithException:
            r = -e + self
            return r

    def __neg__(self):
        return self.opposite()

    def __mul__(self, e):
        return self.times(e)

    def __rmul__(self, e):
        return self.times(e)

    def __imul__(self, e):
        return self.multiply(e)

    def __div__(self, e):
        return self.quotient(e)

    def __idiv__(self, other):
        return self.divide(other)

    def __itruediv__(self, other):
        # this is for Python 3.z
        return self.divide(other)  # pragma: no cover

    def __truediv__(self, e):
        return self.__div__(e)  # pragma: no cover

    def __rtruediv__(self, e):
        self.fatal("Expression {0!s} cannot be used as divider of {1!s}", self, e)  # pragma: no cover



    @property
    def solution_value(self):
        """ This property returns the solution value of the variable.

        Raises:
            DOCplexException
                if the model has not been solved.
        """
        self._check_model_has_solution()
        return self._get_solution_value()

    def _get_solution_value(self, s=None):
        # INTERNAL: no checks
        val = self._constant
        for var, koef in self.iter_terms():
            val += koef * var._get_solution_value(s)
        return self._round_if_discrete(val)

    def is_discrete(self):
        """ Checks if the expression contains only discrete variables and coefficients.

        Example:
            If X is an integer variable, X, X+1, 2X+3 are discrete
            but X+0.3, 1.5X, 2X + 0.7 are not.

        Returns:
            Boolean: True if the expression contains only discrete variables and coefficients.
        """
        self_cst = self._constant
        if self_cst != int(self_cst):
            return False

        for v, k in self.iter_terms():
            if not v.is_discrete() or not is_int(k):
                return False
        else:
            return True

    def __repr__(self):
        return "docplex.mp.LinearExpr({0})".format(self.truncated_str())

    def _iter_sorted_terms(self):
        # internal
        self_terms = self.__terms
        for dv in sorted(self_terms.keys(), key=lambda v: v._index):
            yield dv, self_terms[dv]

    def iter_sorted_terms(self):
        if self.is_model_ordered():
            return self.iter_terms()
        else:
            return self._iter_sorted_terms()


LinearConstraintType = ComparisonType


class ZeroExpr(_SubscriptionMixin, AbstractLinearExpr):
    def _get_solution_value(self, s=None):
        return 0

    def is_zero(self):
        return True



    # INTERNAL
    __slots__ = ('_subscribers')

    def __init__(self, model):
        ModelingObjectBase.__init__(self, model)
        self._subscribers = []

    def clone(self):
        return self  # this is not cloned.

    def copy(self, target_model, var_map):
        return ZeroExpr(target_model)

    def to_linear_expr(self):
        return self  # this is a linear expr.

    def number_of_variables(self):
        return 0

    def number_of_terms(self):
        return 0

    def iter_terms(self):
        return iter_emptyset()

    def is_constant(self):
        return True

    def is_discrete(self):
        return True

    def unchecked_get_coef(self, dvar):
        return 0

    def contains_var(self, dvar):
        return False

    @property
    def constant(self):
        # for compatibility
        return 0

    def negate(self):
        return self

    # noinspection PyMethodMayBeStatic
    def plus(self, e):
        return e

    def times(self, _):
        return self

    # noinspection PyMethodMayBeStatic
    def minus(self, e):
        return -e

    def to_string(self, nb_digits=None, use_space=False):
        return '0'

    def to_stringio(self, oss, nb_digits, use_space, var_namer=lambda v: v.name):
        oss.write(self.to_string())

    # arithmetic
    def __sub__(self, e):
        return self.minus(e)

    def __rsub__(self, e):
        # e - 0 = e !
        return e

    def __neg__(self):
        return self

    def __add__(self, other):
        return other

    def __radd__(self, other):
        return other

    def __mul__(self, other):
        return self

    def __rmul__(self, other):
        return self

    def __div__(self, other):
        return self._divide(other)

    def __truediv__(self, e):
        # for py3
        # INTERNAL
        return self.__div__(e)  # pragma: no cover

    def _divide(self, other):
        self.model.typecheck_as_denominator(numerator=self, denominator=other)
        return self

    def __repr__(self):
        return "docplex.mp.linear.ZeroExpr()"

    def equals_expr(self, other):
        return isinstance(other, ZeroExpr)

    def square(self):
        return self

    # arithmetci to self
    add = plus
    subtract = minus
    multiply = times

    def __iadd__(self, other):
        self.notify_replaced(other)
        return other

    def __isub__(self, other):
        linear_other = self.get_linear_factory()._to_linear_expr(other, force_clone=True)
        linear_other.negate()
        self.notify_replaced(linear_other)
        return linear_other
