

def project_query_1(qry, cfg, opt_prefix=None, loader=defaultload):
    """
    BFSs through config tree modifying query

    opt_prefix is a path from the root of up to the child we are about
    to modify.
    """
    def add_to_opt_prefix(old_prefix, new_name):
        if old_prefix:
            new_prefix = getattr(old_prefix, loader.__name__)(new_name)
        else:
            new_prefix = loader(new_name)
        return new_prefix

    def project_current_depth(qry, cfg, opt_prefix):
        load_only_opt = cfg['load_only']
        noload_opt = cfg['noload']
        reload_opt = cfg['reload']

        # defer all
        if opt_prefix:
            qry = qry.options(opt_prefix.defer('*'))
        else:
            qry = qry.options(defer('*'))

        # noload all
        if opt_prefix:
            qry = qry.options(opt_prefix.noload('*'))
        else:
            qry = qry.options(noload('*'))

        if opt_prefix:
            # qry = qry.options(opt_prefix.load_only(*load_only_opt))
            qry = qry.options(opt_prefix.undefer(*load_only_opt))
        else:
            log.debug('load_only_opt', load_only_opt)
            qry = qry.options(undefer(*load_only_opt))

        # for name in noload_opt:
        #     if opt_prefix:
        #         qry = qry.options(opt_prefix.noload(name))
        #     else:
        #         qry = qry.options(noload(name))

        for name in reload_opt:
            reload_expr = add_to_opt_prefix(opt_prefix, name)
            qry = qry.options(reload_expr)

        return qry

    projected_qry = qry

    for name, child_cfg in cfg['childs'].items():
        child_opt_prefix = add_to_opt_prefix(opt_prefix, name)
        projected_qry = project_query(projected_qry,
                                      child_cfg,
                                      child_opt_prefix)

    log.debug(opt_prefix)
    projected_qry = project_current_depth(projected_qry, cfg, opt_prefix)
    return projected_qry


def cfg_current_level(cfg):
    cfg1 = cfg.copy()
    del cfg1['childs']
    return cfg1
