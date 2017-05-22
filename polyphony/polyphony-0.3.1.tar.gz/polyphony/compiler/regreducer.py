from .ahdl import *
from .ahdlvisitor import AHDLVisitor
from .ir import *
from .irvisitor import IRVisitor


class AliasVarDetector(IRVisitor):
    def process(self, scope):
        self.usedef = scope.usedef
        self.removes = []
        super().process(scope)

    def visit_MOVE(self, ir):
        assert ir.dst.is_a([TEMP, ATTR])
        sym = ir.dst.symbol()
        if sym.is_condition():
            sym.add_tag('alias')
            return
        if sym.typ.is_seq() or sym.is_induction() or sym.is_return() or sym.typ.is_port():
            return
        if ir.src.is_a([TEMP, ATTR]):
            src_sym = ir.src.symbol()
            if src_sym.is_param() or src_sym.typ.is_port():
                return
        elif ir.src.is_a(CALL):
            return
        elif ir.src.is_a(MREF):
            memnode = ir.src.mem.symbol().typ.get_memnode()
            if memnode.is_writable():
                return

        stms = self.usedef.get_stms_defining(sym)
        if len(stms) > 1:
            return
        # TODO: need more strict scheme
        uses = self.usedef.get_syms_used_at(ir)
        for u in uses:
            if u.is_induction():
                return

        sym.add_tag('alias')

    def visit_UPHI(self, ir):
        sym = ir.var.symbol()
        if sym.typ.is_seq() or sym.is_induction() or sym.is_return() or sym.typ.is_port():
            return
        sym.add_tag('alias')


class CopyRemover(AHDLVisitor):
    def process(self, scope):
        self.scope = scope
        if not scope.module_info:
            return
        self.usedef = scope.ahdlusedef
        self.copies = []
        self.collect_copy()
        for state, cp in self.copies:
            defstms = self.usedef.get_stms_defining(cp.src.sig)
            if len(defstms) > 1:
                continue
            for stm in defstms:
                print(cp.src, '{} => {}'.format(cp.dst.sig, stm.dst.sig), stm)
                stm.dst.sig = cp.dst.sig
            state.codes.remove(cp)
    def collect_copy(self):
        for fsm in self.scope.module_info.fsms.values():
            for stg in fsm.stgs:
                for state in stg.states:
                    self.current_state = state
                    for code in state.codes:
                        self.visit(code)

    def visit_AHDL_MOVE(self, ahdl):
        if ahdl.dst.is_a(AHDL_VAR) and ahdl.src.is_a(AHDL_VAR):
            if ahdl.src.sig.is_input():
                return
            self.copies.append((self.current_state, ahdl))


class InductionVarMerger(AHDLVisitor):
    def process(self, scope):
        #return
        self.scope = scope
        if not scope.module_info:
            return
        for fsm in scope.module_info.fsms.values():
            for stg in fsm.stgs:
                for state in stg.states:
                    self.current_state = state
                    self.removes = []
                    for code in state.codes:
                        self.visit(code)
                    for code in self.removes:
                        state.codes.remove(code)


    def visit_AHDL_VAR(self, ahdl):
        #return
        if ahdl.sig.is_induction():
            #print(self.current_stm, ahdl.sig.sym.root_sym())
            sig_prefix = ahdl.sig.prefix()
            name = sig_prefix + ahdl.sig.sym.root_sym().hdl_name()
            root_sig = self.scope.signal(name)
            if not root_sig:
                root_sig = self.scope.gen_sig(name, ahdl.sig.width, ahdl.sig.tags, ahdl.sig.sym)
                self.scope.module_info.add_internal_reg(root_sig)
            if ahdl.sig is not root_sig:
                self.scope.module_info.remove_signal_decl(ahdl.sig)
                ahdl.sig = root_sig

    def visit_AHDL_MOVE(self, ahdl):
        super().visit_AHDL_MOVE(ahdl)
        if ahdl.dst.is_a(AHDL_VAR) and ahdl.src.is_a(AHDL_VAR) and ahdl.dst.sig is ahdl.src.sig:
            self.removes.append(ahdl)
            return


class RegReducer(AHDLVisitor):
    # TODO
    pass
