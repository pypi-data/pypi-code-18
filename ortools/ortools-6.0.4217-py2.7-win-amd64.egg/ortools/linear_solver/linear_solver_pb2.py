# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ortools/linear_solver/linear_solver.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ortools/linear_solver/linear_solver.proto',
  package='operations_research',
  syntax='proto2',
  serialized_pb=_b('\n)ortools/linear_solver/linear_solver.proto\x12\x13operations_research\"\x93\x01\n\x0fMPVariableProto\x12\x19\n\x0blower_bound\x18\x01 \x01(\x01:\x04-inf\x12\x18\n\x0bupper_bound\x18\x02 \x01(\x01:\x03inf\x12 \n\x15objective_coefficient\x18\x03 \x01(\x01:\x01\x30\x12\x19\n\nis_integer\x18\x04 \x01(\x08:\x05\x66\x61lse\x12\x0e\n\x04name\x18\x05 \x01(\t:\x00\"\xa0\x01\n\x11MPConstraintProto\x12\x15\n\tvar_index\x18\x06 \x03(\x05\x42\x02\x10\x01\x12\x17\n\x0b\x63oefficient\x18\x07 \x03(\x01\x42\x02\x10\x01\x12\x19\n\x0blower_bound\x18\x02 \x01(\x01:\x04-inf\x12\x18\n\x0bupper_bound\x18\x03 \x01(\x01:\x03inf\x12\x0e\n\x04name\x18\x04 \x01(\t:\x00\x12\x16\n\x07is_lazy\x18\x05 \x01(\x08:\x05\x66\x61lse\"I\n\x19PartialVariableAssignment\x12\x15\n\tvar_index\x18\x01 \x03(\x05\x42\x02\x10\x01\x12\x15\n\tvar_value\x18\x02 \x03(\x01\x42\x02\x10\x01\"\x8f\x02\n\x0cMPModelProto\x12\x17\n\x08maximize\x18\x01 \x01(\x08:\x05\x66\x61lse\x12\x1b\n\x10objective_offset\x18\x02 \x01(\x01:\x01\x30\x12\x36\n\x08variable\x18\x03 \x03(\x0b\x32$.operations_research.MPVariableProto\x12:\n\nconstraint\x18\x04 \x03(\x0b\x32&.operations_research.MPConstraintProto\x12\x0e\n\x04name\x18\x05 \x01(\t:\x00\x12\x45\n\rsolution_hint\x18\x06 \x01(\x0b\x32..operations_research.PartialVariableAssignment\"\x1f\n\x0eOptionalDouble\x12\r\n\x05value\x18\x01 \x01(\x01\"\xbd\x04\n\x18MPSolverCommonParameters\x12=\n\x10relative_mip_gap\x18\x01 \x01(\x0b\x32#.operations_research.OptionalDouble\x12=\n\x10primal_tolerance\x18\x02 \x01(\x0b\x32#.operations_research.OptionalDouble\x12;\n\x0e\x64ual_tolerance\x18\x03 \x01(\x0b\x32#.operations_research.OptionalDouble\x12j\n\x0clp_algorithm\x18\x04 \x01(\x0e\x32?.operations_research.MPSolverCommonParameters.LPAlgorithmValues:\x13LP_ALGO_UNSPECIFIED\x12H\n\x08presolve\x18\x05 \x01(\x0e\x32$.operations_research.OptionalBoolean:\x10\x42OOL_UNSPECIFIED\x12G\n\x07scaling\x18\x07 \x01(\x0e\x32$.operations_research.OptionalBoolean:\x10\x42OOL_UNSPECIFIED\"g\n\x11LPAlgorithmValues\x12\x17\n\x13LP_ALGO_UNSPECIFIED\x10\x00\x12\x10\n\x0cLP_ALGO_DUAL\x10\x01\x12\x12\n\x0eLP_ALGO_PRIMAL\x10\x02\x12\x13\n\x0fLP_ALGO_BARRIER\x10\x03\"\x99\x05\n\x0eMPModelRequest\x12\x30\n\x05model\x18\x01 \x01(\x0b\x32!.operations_research.MPModelProto\x12\x43\n\x0bsolver_type\x18\x02 \x01(\x0e\x32..operations_research.MPModelRequest.SolverType\x12!\n\x19solver_time_limit_seconds\x18\x03 \x01(\x01\x12,\n\x1d\x65nable_internal_solver_output\x18\x04 \x01(\x08:\x05\x66\x61lse\x12\"\n\x1asolver_specific_parameters\x18\x05 \x01(\t\"\x9a\x03\n\nSolverType\x12\x1b\n\x17GLOP_LINEAR_PROGRAMMING\x10\x02\x12\x1a\n\x16\x43LP_LINEAR_PROGRAMMING\x10\x00\x12\x1b\n\x17GLPK_LINEAR_PROGRAMMING\x10\x01\x12\x1d\n\x19GUROBI_LINEAR_PROGRAMMING\x10\x06\x12\x1c\n\x18\x43PLEX_LINEAR_PROGRAMMING\x10\n\x12\"\n\x1eSCIP_MIXED_INTEGER_PROGRAMMING\x10\x03\x12\"\n\x1eGLPK_MIXED_INTEGER_PROGRAMMING\x10\x04\x12!\n\x1d\x43\x42\x43_MIXED_INTEGER_PROGRAMMING\x10\x05\x12$\n GUROBI_MIXED_INTEGER_PROGRAMMING\x10\x07\x12#\n\x1f\x43PLEX_MIXED_INTEGER_PROGRAMMING\x10\x0b\x12\x1b\n\x17\x42OP_INTEGER_PROGRAMMING\x10\x0c\x12&\n\"KNAPSACK_MIXED_INTEGER_PROGRAMMING\x10\r\"\xd5\x01\n\x12MPSolutionResponse\x12T\n\x06status\x18\x01 \x01(\x0e\x32+.operations_research.MPSolverResponseStatus:\x17MPSOLVER_UNKNOWN_STATUS\x12\x17\n\x0fobjective_value\x18\x02 \x01(\x01\x12\x1c\n\x14\x62\x65st_objective_bound\x18\x05 \x01(\x01\x12\x1a\n\x0evariable_value\x18\x03 \x03(\x01\x42\x02\x10\x01\x12\x16\n\ndual_value\x18\x04 \x03(\x01\x42\x02\x10\x01*F\n\x0fOptionalBoolean\x12\x14\n\x10\x42OOL_UNSPECIFIED\x10\x00\x12\x0e\n\nBOOL_FALSE\x10\x01\x12\r\n\tBOOL_TRUE\x10\x02*\xfa\x02\n\x16MPSolverResponseStatus\x12\x14\n\x10MPSOLVER_OPTIMAL\x10\x00\x12\x15\n\x11MPSOLVER_FEASIBLE\x10\x01\x12\x17\n\x13MPSOLVER_INFEASIBLE\x10\x02\x12\x16\n\x12MPSOLVER_UNBOUNDED\x10\x03\x12\x15\n\x11MPSOLVER_ABNORMAL\x10\x04\x12\x17\n\x13MPSOLVER_NOT_SOLVED\x10\x06\x12\x1b\n\x17MPSOLVER_MODEL_IS_VALID\x10\x61\x12\x1b\n\x17MPSOLVER_UNKNOWN_STATUS\x10\x63\x12\x1a\n\x16MPSOLVER_MODEL_INVALID\x10\x05\x12(\n$MPSOLVER_MODEL_INVALID_SOLUTION_HINT\x10T\x12,\n(MPSOLVER_MODEL_INVALID_SOLVER_PARAMETERS\x10U\x12$\n MPSOLVER_SOLVER_TYPE_UNAVAILABLE\x10\x07\x42#\n\x1f\x63om.google.ortools.linearsolverP\x01')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_OPTIONALBOOLEAN = _descriptor.EnumDescriptor(
  name='OptionalBoolean',
  full_name='operations_research.OptionalBoolean',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BOOL_UNSPECIFIED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BOOL_FALSE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BOOL_TRUE', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=2221,
  serialized_end=2291,
)
_sym_db.RegisterEnumDescriptor(_OPTIONALBOOLEAN)

OptionalBoolean = enum_type_wrapper.EnumTypeWrapper(_OPTIONALBOOLEAN)
_MPSOLVERRESPONSESTATUS = _descriptor.EnumDescriptor(
  name='MPSolverResponseStatus',
  full_name='operations_research.MPSolverResponseStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MPSOLVER_OPTIMAL', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MPSOLVER_FEASIBLE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MPSOLVER_INFEASIBLE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MPSOLVER_UNBOUNDED', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MPSOLVER_ABNORMAL', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MPSOLVER_NOT_SOLVED', index=5, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MPSOLVER_MODEL_IS_VALID', index=6, number=97,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MPSOLVER_UNKNOWN_STATUS', index=7, number=99,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MPSOLVER_MODEL_INVALID', index=8, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MPSOLVER_MODEL_INVALID_SOLUTION_HINT', index=9, number=84,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MPSOLVER_MODEL_INVALID_SOLVER_PARAMETERS', index=10, number=85,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MPSOLVER_SOLVER_TYPE_UNAVAILABLE', index=11, number=7,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=2294,
  serialized_end=2672,
)
_sym_db.RegisterEnumDescriptor(_MPSOLVERRESPONSESTATUS)

MPSolverResponseStatus = enum_type_wrapper.EnumTypeWrapper(_MPSOLVERRESPONSESTATUS)
BOOL_UNSPECIFIED = 0
BOOL_FALSE = 1
BOOL_TRUE = 2
MPSOLVER_OPTIMAL = 0
MPSOLVER_FEASIBLE = 1
MPSOLVER_INFEASIBLE = 2
MPSOLVER_UNBOUNDED = 3
MPSOLVER_ABNORMAL = 4
MPSOLVER_NOT_SOLVED = 6
MPSOLVER_MODEL_IS_VALID = 97
MPSOLVER_UNKNOWN_STATUS = 99
MPSOLVER_MODEL_INVALID = 5
MPSOLVER_MODEL_INVALID_SOLUTION_HINT = 84
MPSOLVER_MODEL_INVALID_SOLVER_PARAMETERS = 85
MPSOLVER_SOLVER_TYPE_UNAVAILABLE = 7


_MPSOLVERCOMMONPARAMETERS_LPALGORITHMVALUES = _descriptor.EnumDescriptor(
  name='LPAlgorithmValues',
  full_name='operations_research.MPSolverCommonParameters.LPAlgorithmValues',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LP_ALGO_UNSPECIFIED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LP_ALGO_DUAL', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LP_ALGO_PRIMAL', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LP_ALGO_BARRIER', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1232,
  serialized_end=1335,
)
_sym_db.RegisterEnumDescriptor(_MPSOLVERCOMMONPARAMETERS_LPALGORITHMVALUES)

_MPMODELREQUEST_SOLVERTYPE = _descriptor.EnumDescriptor(
  name='SolverType',
  full_name='operations_research.MPModelRequest.SolverType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='GLOP_LINEAR_PROGRAMMING', index=0, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CLP_LINEAR_PROGRAMMING', index=1, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GLPK_LINEAR_PROGRAMMING', index=2, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GUROBI_LINEAR_PROGRAMMING', index=3, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CPLEX_LINEAR_PROGRAMMING', index=4, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SCIP_MIXED_INTEGER_PROGRAMMING', index=5, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GLPK_MIXED_INTEGER_PROGRAMMING', index=6, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CBC_MIXED_INTEGER_PROGRAMMING', index=7, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GUROBI_MIXED_INTEGER_PROGRAMMING', index=8, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CPLEX_MIXED_INTEGER_PROGRAMMING', index=9, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BOP_INTEGER_PROGRAMMING', index=10, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='KNAPSACK_MIXED_INTEGER_PROGRAMMING', index=11, number=13,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1593,
  serialized_end=2003,
)
_sym_db.RegisterEnumDescriptor(_MPMODELREQUEST_SOLVERTYPE)


_MPVARIABLEPROTO = _descriptor.Descriptor(
  name='MPVariableProto',
  full_name='operations_research.MPVariableProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lower_bound', full_name='operations_research.MPVariableProto.lower_bound', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=-1e10000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='upper_bound', full_name='operations_research.MPVariableProto.upper_bound', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=1e10000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='objective_coefficient', full_name='operations_research.MPVariableProto.objective_coefficient', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_integer', full_name='operations_research.MPVariableProto.is_integer', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='operations_research.MPVariableProto.name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=67,
  serialized_end=214,
)


_MPCONSTRAINTPROTO = _descriptor.Descriptor(
  name='MPConstraintProto',
  full_name='operations_research.MPConstraintProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='var_index', full_name='operations_research.MPConstraintProto.var_index', index=0,
      number=6, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='coefficient', full_name='operations_research.MPConstraintProto.coefficient', index=1,
      number=7, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='lower_bound', full_name='operations_research.MPConstraintProto.lower_bound', index=2,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=-1e10000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='upper_bound', full_name='operations_research.MPConstraintProto.upper_bound', index=3,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=1e10000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='operations_research.MPConstraintProto.name', index=4,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_lazy', full_name='operations_research.MPConstraintProto.is_lazy', index=5,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=217,
  serialized_end=377,
)


_PARTIALVARIABLEASSIGNMENT = _descriptor.Descriptor(
  name='PartialVariableAssignment',
  full_name='operations_research.PartialVariableAssignment',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='var_index', full_name='operations_research.PartialVariableAssignment.var_index', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='var_value', full_name='operations_research.PartialVariableAssignment.var_value', index=1,
      number=2, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=379,
  serialized_end=452,
)


_MPMODELPROTO = _descriptor.Descriptor(
  name='MPModelProto',
  full_name='operations_research.MPModelProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='maximize', full_name='operations_research.MPModelProto.maximize', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='objective_offset', full_name='operations_research.MPModelProto.objective_offset', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='variable', full_name='operations_research.MPModelProto.variable', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='constraint', full_name='operations_research.MPModelProto.constraint', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='operations_research.MPModelProto.name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='solution_hint', full_name='operations_research.MPModelProto.solution_hint', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=455,
  serialized_end=726,
)


_OPTIONALDOUBLE = _descriptor.Descriptor(
  name='OptionalDouble',
  full_name='operations_research.OptionalDouble',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='operations_research.OptionalDouble.value', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=728,
  serialized_end=759,
)


_MPSOLVERCOMMONPARAMETERS = _descriptor.Descriptor(
  name='MPSolverCommonParameters',
  full_name='operations_research.MPSolverCommonParameters',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='relative_mip_gap', full_name='operations_research.MPSolverCommonParameters.relative_mip_gap', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='primal_tolerance', full_name='operations_research.MPSolverCommonParameters.primal_tolerance', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dual_tolerance', full_name='operations_research.MPSolverCommonParameters.dual_tolerance', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lp_algorithm', full_name='operations_research.MPSolverCommonParameters.lp_algorithm', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='presolve', full_name='operations_research.MPSolverCommonParameters.presolve', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='scaling', full_name='operations_research.MPSolverCommonParameters.scaling', index=5,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MPSOLVERCOMMONPARAMETERS_LPALGORITHMVALUES,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=762,
  serialized_end=1335,
)


_MPMODELREQUEST = _descriptor.Descriptor(
  name='MPModelRequest',
  full_name='operations_research.MPModelRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='model', full_name='operations_research.MPModelRequest.model', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='solver_type', full_name='operations_research.MPModelRequest.solver_type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=2,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='solver_time_limit_seconds', full_name='operations_research.MPModelRequest.solver_time_limit_seconds', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='enable_internal_solver_output', full_name='operations_research.MPModelRequest.enable_internal_solver_output', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='solver_specific_parameters', full_name='operations_research.MPModelRequest.solver_specific_parameters', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MPMODELREQUEST_SOLVERTYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1338,
  serialized_end=2003,
)


_MPSOLUTIONRESPONSE = _descriptor.Descriptor(
  name='MPSolutionResponse',
  full_name='operations_research.MPSolutionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='operations_research.MPSolutionResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=99,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='objective_value', full_name='operations_research.MPSolutionResponse.objective_value', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='best_objective_bound', full_name='operations_research.MPSolutionResponse.best_objective_bound', index=2,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='variable_value', full_name='operations_research.MPSolutionResponse.variable_value', index=3,
      number=3, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='dual_value', full_name='operations_research.MPSolutionResponse.dual_value', index=4,
      number=4, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=2006,
  serialized_end=2219,
)

_MPMODELPROTO.fields_by_name['variable'].message_type = _MPVARIABLEPROTO
_MPMODELPROTO.fields_by_name['constraint'].message_type = _MPCONSTRAINTPROTO
_MPMODELPROTO.fields_by_name['solution_hint'].message_type = _PARTIALVARIABLEASSIGNMENT
_MPSOLVERCOMMONPARAMETERS.fields_by_name['relative_mip_gap'].message_type = _OPTIONALDOUBLE
_MPSOLVERCOMMONPARAMETERS.fields_by_name['primal_tolerance'].message_type = _OPTIONALDOUBLE
_MPSOLVERCOMMONPARAMETERS.fields_by_name['dual_tolerance'].message_type = _OPTIONALDOUBLE
_MPSOLVERCOMMONPARAMETERS.fields_by_name['lp_algorithm'].enum_type = _MPSOLVERCOMMONPARAMETERS_LPALGORITHMVALUES
_MPSOLVERCOMMONPARAMETERS.fields_by_name['presolve'].enum_type = _OPTIONALBOOLEAN
_MPSOLVERCOMMONPARAMETERS.fields_by_name['scaling'].enum_type = _OPTIONALBOOLEAN
_MPSOLVERCOMMONPARAMETERS_LPALGORITHMVALUES.containing_type = _MPSOLVERCOMMONPARAMETERS
_MPMODELREQUEST.fields_by_name['model'].message_type = _MPMODELPROTO
_MPMODELREQUEST.fields_by_name['solver_type'].enum_type = _MPMODELREQUEST_SOLVERTYPE
_MPMODELREQUEST_SOLVERTYPE.containing_type = _MPMODELREQUEST
_MPSOLUTIONRESPONSE.fields_by_name['status'].enum_type = _MPSOLVERRESPONSESTATUS
DESCRIPTOR.message_types_by_name['MPVariableProto'] = _MPVARIABLEPROTO
DESCRIPTOR.message_types_by_name['MPConstraintProto'] = _MPCONSTRAINTPROTO
DESCRIPTOR.message_types_by_name['PartialVariableAssignment'] = _PARTIALVARIABLEASSIGNMENT
DESCRIPTOR.message_types_by_name['MPModelProto'] = _MPMODELPROTO
DESCRIPTOR.message_types_by_name['OptionalDouble'] = _OPTIONALDOUBLE
DESCRIPTOR.message_types_by_name['MPSolverCommonParameters'] = _MPSOLVERCOMMONPARAMETERS
DESCRIPTOR.message_types_by_name['MPModelRequest'] = _MPMODELREQUEST
DESCRIPTOR.message_types_by_name['MPSolutionResponse'] = _MPSOLUTIONRESPONSE
DESCRIPTOR.enum_types_by_name['OptionalBoolean'] = _OPTIONALBOOLEAN
DESCRIPTOR.enum_types_by_name['MPSolverResponseStatus'] = _MPSOLVERRESPONSESTATUS

MPVariableProto = _reflection.GeneratedProtocolMessageType('MPVariableProto', (_message.Message,), dict(
  DESCRIPTOR = _MPVARIABLEPROTO,
  __module__ = 'ortools.linear_solver.linear_solver_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.MPVariableProto)
  ))
_sym_db.RegisterMessage(MPVariableProto)

MPConstraintProto = _reflection.GeneratedProtocolMessageType('MPConstraintProto', (_message.Message,), dict(
  DESCRIPTOR = _MPCONSTRAINTPROTO,
  __module__ = 'ortools.linear_solver.linear_solver_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.MPConstraintProto)
  ))
_sym_db.RegisterMessage(MPConstraintProto)

PartialVariableAssignment = _reflection.GeneratedProtocolMessageType('PartialVariableAssignment', (_message.Message,), dict(
  DESCRIPTOR = _PARTIALVARIABLEASSIGNMENT,
  __module__ = 'ortools.linear_solver.linear_solver_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.PartialVariableAssignment)
  ))
_sym_db.RegisterMessage(PartialVariableAssignment)

MPModelProto = _reflection.GeneratedProtocolMessageType('MPModelProto', (_message.Message,), dict(
  DESCRIPTOR = _MPMODELPROTO,
  __module__ = 'ortools.linear_solver.linear_solver_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.MPModelProto)
  ))
_sym_db.RegisterMessage(MPModelProto)

OptionalDouble = _reflection.GeneratedProtocolMessageType('OptionalDouble', (_message.Message,), dict(
  DESCRIPTOR = _OPTIONALDOUBLE,
  __module__ = 'ortools.linear_solver.linear_solver_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.OptionalDouble)
  ))
_sym_db.RegisterMessage(OptionalDouble)

MPSolverCommonParameters = _reflection.GeneratedProtocolMessageType('MPSolverCommonParameters', (_message.Message,), dict(
  DESCRIPTOR = _MPSOLVERCOMMONPARAMETERS,
  __module__ = 'ortools.linear_solver.linear_solver_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.MPSolverCommonParameters)
  ))
_sym_db.RegisterMessage(MPSolverCommonParameters)

MPModelRequest = _reflection.GeneratedProtocolMessageType('MPModelRequest', (_message.Message,), dict(
  DESCRIPTOR = _MPMODELREQUEST,
  __module__ = 'ortools.linear_solver.linear_solver_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.MPModelRequest)
  ))
_sym_db.RegisterMessage(MPModelRequest)

MPSolutionResponse = _reflection.GeneratedProtocolMessageType('MPSolutionResponse', (_message.Message,), dict(
  DESCRIPTOR = _MPSOLUTIONRESPONSE,
  __module__ = 'ortools.linear_solver.linear_solver_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.MPSolutionResponse)
  ))
_sym_db.RegisterMessage(MPSolutionResponse)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\037com.google.ortools.linearsolverP\001'))
_MPCONSTRAINTPROTO.fields_by_name['var_index'].has_options = True
_MPCONSTRAINTPROTO.fields_by_name['var_index']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_MPCONSTRAINTPROTO.fields_by_name['coefficient'].has_options = True
_MPCONSTRAINTPROTO.fields_by_name['coefficient']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_PARTIALVARIABLEASSIGNMENT.fields_by_name['var_index'].has_options = True
_PARTIALVARIABLEASSIGNMENT.fields_by_name['var_index']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_PARTIALVARIABLEASSIGNMENT.fields_by_name['var_value'].has_options = True
_PARTIALVARIABLEASSIGNMENT.fields_by_name['var_value']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_MPSOLUTIONRESPONSE.fields_by_name['variable_value'].has_options = True
_MPSOLUTIONRESPONSE.fields_by_name['variable_value']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_MPSOLUTIONRESPONSE.fields_by_name['dual_value'].has_options = True
_MPSOLUTIONRESPONSE.fields_by_name['dual_value']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
# @@protoc_insertion_point(module_scope)
