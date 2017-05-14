from pyomo.core import *
from pyomo.pysp.annotations import (PySP_ConstraintStageAnnotation,
                                    PySP_StochasticRHSAnnotation,
                                    PySP_StochasticMatrixAnnotation,
                                    PySP_StochasticObjectiveAnnotation)

def pysp_scenario_tree_model_callback():
    from pyomo.pysp.scenariotree.tree_structure_model \
        import CreateConcreteTwoStageScenarioTreeModel

    st_model = CreateConcreteTwoStageScenarioTreeModel(3)

    first_stage = st_model.Stages.first()
    second_stage = st_model.Stages.last()

    # First Stage
    st_model.StageCost[first_stage] = 'StageCost[1]'
    st_model.StageVariables[first_stage].add('x')
    st_model.StageDerivedVariables[first_stage].add('y')
    st_model.StageDerivedVariables[first_stage].add('fx')

    # Second Stage
    st_model.StageCost[second_stage] = 'StageCost[2]'
    st_model.StageVariables[second_stage].add('z')
    st_model.StageDerivedVariables[second_stage].add('q')
    st_model.StageDerivedVariables[second_stage].add('fz')
    st_model.StageDerivedVariables[second_stage].add('r')

    return st_model

d = {}
d['Scenario1'] = 0
d['Scenario2'] = 1
d['Scenario3'] = 2
def create_instance(scenario_name):
    cnt = d[scenario_name]

    model = ConcreteModel()
    # first stage
    model.x = Var(bounds=(0,10))
    # first stage derived
    model.y = Expression(expr=model.x + 1)
    model.fx = Var()
    # second stage
    model.z = Var(bounds=(-10, 10))
    # second stage derived
    model.q = Expression(expr=model.z**2)
    model.fz = Var()
    model.r = Var()
    # stage costs
    model.StageCost = Expression([1,2])
    model.StageCost.add(1, model.fx)
    model.StageCost.add(2, -model.fz + model.r - cnt)
    model.o = Objective(expr=summation(model.StageCost))

    model.ZERO = Param(initialize=0, mutable=True)
    if cnt == 0:
        cnt = model.ZERO

    model.c_first_stage = Constraint(expr= model.x >= 0)

    # test our handling of intermediate variables that
    # are created by Piecewise but can not necessarily
    # be declared on the scenario tree
    model.p_first_stage = Piecewise(model.fx, model.x,
                                    pw_pts=[0.,2.,5.,7.,10.],
                                    pw_constr_type='EQ',
                                    pw_repn='INC',
                                    f_rule=[10.,10.,9.,10.,10.],
                                    force_pw=True)

    model.c_second_stage = Constraint(expr= model.x + model.r * cnt >= -100)
    model.r_second_stage = Constraint(expr= -cnt <= model.r <= 0)
    # exercise more of the code by making this an indexed
    # block
    model.p_second_stage = Piecewise([1], model.fz, model.z,
                                     pw_pts=[-10,-5.,0.,5.,10.],
                                     pw_constr_type='EQ',
                                     pw_repn='INC',
                                     f_rule=[0.,0.,-1.,2.+cnt,1.],
                                     force_pw=True)
    return model

def pysp_instance_creation_callback(scenario_name, node_names):

    model = create_instance(scenario_name)

    #
    # SMPS Related Annotations
    #

    model.constraint_stage = PySP_ConstraintStageAnnotation()
    model.constraint_stage.declare(model.c_first_stage, 1)
    model.constraint_stage.declare(model.p_first_stage, 1)
    model.constraint_stage.declare(model.c_second_stage, 2)
    model.constraint_stage.declare(model.r_second_stage, 2)
    model.constraint_stage.declare(model.p_second_stage, 2)

    # The difficulty with Piecewise is that it hides the
    # structure of the underlying constraints (there may be
    # more than one). It doesn't seem possible to direct a
    # modeler on how to go about tagging specific
    # constraints.  For this reason, we allow the
    # PySP_StochasticRHS and PySP_StochasticMatrix suffixes
    # to contain entries for entire blocks, where we
    # interpret this as meaning all rhs and constraint
    # matrix entries should be treated as stochastic.
    model.stoch_rhs = PySP_StochasticRHSAnnotation()
    model.stoch_rhs.declare(model.p_second_stage)
    model.stoch_rhs.declare(model.r_second_stage)
    model.stoch_matrix = PySP_StochasticMatrixAnnotation()
    # exercise more of the code by testing this with an
    # indexed block and a single block
    model.stoch_matrix.declare(model.c_second_stage, variables=[model.r])
    model.stoch_matrix.declare(model.p_second_stage[1])
    model.stoch_objective = PySP_StochasticObjectiveAnnotation()

    return model
