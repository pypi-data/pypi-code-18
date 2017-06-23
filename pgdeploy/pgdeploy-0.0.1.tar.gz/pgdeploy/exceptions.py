# -*- coding: utf-8 -*-


class PGDeployException(Exception):
    pass


class NoMigrationsFoundException(PGDeployException):
    pass


class RollbackUnsupportedException(PGDeployException):
    pass
