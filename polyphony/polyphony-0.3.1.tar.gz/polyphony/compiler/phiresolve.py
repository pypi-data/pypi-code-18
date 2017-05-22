from .ir import *
from .irvisitor import IRVisitor
from logging import getLogger
logger = getLogger(__name__)


class PHICondResolver(object):
    def __init__(self):
        self.count = 0

    def process(self, scope):
        self.scope = scope

        self._collect_phi()
        phis = self.phis[:]
        for phi in phis:
            if phi.is_a(PHI) and not phi.var.symbol().typ.is_scalar():
                self._divide_phi_to_mv(phi)
                #pass
            elif phi.is_a(LPHI):
                self._divide_phi_to_mv(phi)
                #self._add_initial_mv(phi)

    def _collect_phi(self):
        self.phis = []
        for b in self.scope.traverse_blocks():
            for stm in b.stms:
                if stm.is_a([PHI, LPHI]):
                    #if stm.var.sym.is_memory():
                    #    continue
                    self.phis.append(stm)

    def _insert_mv(self, var, arg, blk):
        mv = MOVE(var, arg)
        mv.lineno = arg.lineno
        mv.iorder = arg.iorder
        mv.dst.lineno = arg.lineno
        assert mv.lineno > 0
        idx = self._find_stm_insetion_index(blk, mv)
        blk.insert_stm(idx, mv)
        logger.debug('PHI divide into ' + str(mv))

    def _divide_phi_to_mv(self, phi):
        #usedef = self.scope.usedef
        for arg, blk in zip(phi.args, phi.defblks):
            if not blk:
                continue
            if phi.var.symbol().typ.is_object():
                continue
            self._insert_mv(phi.var.clone(), arg, blk)
            #update usedef table
            # if arg.is_a(TEMP):
            #     usedef.remove_var_use(arg, phi)
            #     usedef.add_var_use(mv.src, mv)
            # elif arg.is_a(CONST):
            #     usedef.remove_const_use(arg, phi)
            #     usedef.add_const_use(mv.src, mv)

            # usedef.add_var_def(mv.dst, mv)

        # usedef.remove_var_def(phi.var, phi)
        phi.block.stms.remove(phi)
        self.phis.remove(phi)
        #assert len(usedef.get_def_stms_by_sym(phi.var.sym)) == len(phi.argv())

    def _find_stm_insetion_index(self, block, target_stm):
        for i, stm in enumerate(block.stms):
            if stm.iorder > target_stm.iorder:
                return i
        return -1

    def _add_initial_mv(self, lphi):
        assert lphi.ps[0].is_a(CONST) and lphi.ps[0].value
        # assert lphi.var.symbol().is_induction()
        self._insert_mv(lphi.var.clone(), lphi.args[0], lphi.defblks[0])
        cond_sym = self.scope.add_condition_sym()
        mv = MOVE(TEMP(cond_sym, Ctx.STORE), RELOP('Eq', lphi.var, lphi.args[0]))
        mv.block = lphi.block
        mv.lineno = lphi.args[0].lineno
        idx = lphi.block.stms.index(lphi)
        lphi.block.stms.insert(idx, mv)
        lphi.ps[0] = TEMP(cond_sym, Ctx.LOAD)
        lphi.args[0] = TEMP(lphi.var.symbol(), Ctx.LOAD)


class StmOrdering(IRVisitor):
    def visit(self, ir):
        method = 'visit_' + ir.__class__.__name__
        visitor = getattr(self, method, None)
        if ir.is_a(IRStm):
            ir.iorder = ir.block.stms.index(ir)
        else:
            ir.iorder = self.current_stm.iorder
        visitor(ir)
