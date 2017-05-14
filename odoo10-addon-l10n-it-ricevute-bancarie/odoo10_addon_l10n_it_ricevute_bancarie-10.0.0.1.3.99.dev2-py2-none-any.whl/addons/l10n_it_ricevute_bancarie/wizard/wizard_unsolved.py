# -*- coding: utf-8 -*-
# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _, api
from odoo.exceptions import UserError


class RibaUnsolved(models.TransientModel):

    @api.model
    def _get_unsolved_journal_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list_line('unsolved_journal_id')

    @api.model
    def _get_effects_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list_line('acceptance_account_id')

    @api.model
    def _get_effects_amount(self):
        if not self.env.context.get('active_id', False):
            return False
        return self.env[
            'riba.distinta.line'
        ].browse(self.env.context['active_id']).amount

    @api.model
    def _get_riba_bank_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list_line('accreditation_account_id')

    @api.model
    def _get_overdue_effects_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list_line('overdue_effects_account_id')

    @api.model
    def _get_bank_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list_line('bank_account_id')

    @api.model
    def _get_bank_expense_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list_line('protest_charge_account_id')

    _name = "riba.unsolved"
    unsolved_journal_id = fields.Many2one(
        'account.journal', 'Unsolved journal', domain=[('type', '=', 'bank')],
        default=_get_unsolved_journal_id)
    effects_account_id = fields.Many2one(
        'account.account', 'Effects account',
        domain=[('internal_type', '=', 'receivable')],
        default=_get_effects_account_id)
    effects_amount = fields.Float(
        'Effects amount', default=_get_effects_amount)
    riba_bank_account_id = fields.Many2one(
        'account.account', 'Ri.Ba. bank account',
        default=_get_riba_bank_account_id)
    riba_bank_amount = fields.Float(
        'Ri.Ba. bank amount', default=_get_effects_amount)
    overdue_effects_account_id = fields.Many2one(
        'account.account', 'Overdue Effects account',
        domain=[('internal_type', '=', 'receivable')],
        default=_get_overdue_effects_account_id)
    overdue_effects_amount = fields.Float(
        'Overdue Effects amount', default=_get_effects_amount)
    bank_account_id = fields.Many2one(
        'account.account', 'Bank account', domain=[(
            'internal_type', '=', 'liquidity')],
        default=_get_bank_account_id)
    bank_amount = fields.Float('Taken amount')
    bank_expense_account_id = fields.Many2one(
        'account.account', 'Bank Expenses account',
        default=_get_bank_expense_account_id)
    expense_amount = fields.Float('Expenses amount')

    def skip(self):
        active_id = self.env.context.get('active_id')
        if not active_id:
            raise UserError(_('No active ID found'))
        line_model = self.env['riba.distinta.line']
        line = line_model.browse(active_id)
        line.state = 'unsolved'
        line.distinta_id.signal_workflow('unsolved')
        return {'type': 'ir.actions.act_window_close'}

    def create_move(self):
        active_id = self.env.context.get('active_id', False)
        if not active_id:
            raise UserError(_('No active ID found'))
        move_model = self.env['account.move']
        invoice_model = self.env['account.invoice']
        move_line_model = self.env['account.move.line']
        distinta_line = self.env['riba.distinta.line'].browse(active_id)
        wizard = self
        if (
            not wizard.unsolved_journal_id or
            not wizard.effects_account_id or
            not wizard.riba_bank_account_id or
            not wizard.overdue_effects_account_id or
            not wizard.bank_account_id or
            not wizard.bank_expense_account_id
        ):
            raise UserError(_('Every account is mandatory'))
        move_vals = {
            'ref': _('Unsolved Ri.Ba. %s - line %s') % (
                distinta_line.distinta_id.name, distinta_line.sequence),
            'journal_id': wizard.unsolved_journal_id.id,
            'line_ids': [
                (0, 0, {
                    'name':  _('Effects'),
                    'account_id': wizard.effects_account_id.id,
                    'partner_id': distinta_line.partner_id.id,
                    'credit': wizard.effects_amount,
                    'debit': 0.0,
                }),
                (0, 0, {
                    'name':  _('Ri.Ba. Bank'),
                    'account_id': wizard.riba_bank_account_id.id,
                    'debit': wizard.riba_bank_amount,
                    'credit': 0.0,
                }),
                (0, 0, {
                    'name':  _('Overdue Effects'),
                    'account_id': wizard.overdue_effects_account_id.id,
                    'debit': wizard.overdue_effects_amount,
                    'credit': 0.0,
                    'partner_id': distinta_line.partner_id.id,
                    'date_maturity': distinta_line.due_date,
                }),
                (0, 0, {
                    'name':  _('Bank'),
                    'account_id': wizard.bank_account_id.id,
                    'credit': wizard.bank_amount,
                    'debit': 0.0,
                }),
                (0, 0, {
                    'name':  _('Expenses'),
                    'account_id': wizard.bank_expense_account_id.id,
                    'debit': wizard.expense_amount,
                    'credit': 0.0,
                }),
            ]
        }
        move = move_model.create(move_vals)

        to_be_reconciled = []
        for move_line in move.line_ids:
            if move_line.account_id.id == wizard.overdue_effects_account_id.id:
                for riba_move_line in distinta_line.move_line_ids:
                    invoice_ids = []
                    if riba_move_line.move_line_id.invoice_id:
                        invoice_ids = [
                            riba_move_line.move_line_id.invoice_id.id
                        ]
                    elif riba_move_line.move_line_id.unsolved_invoice_ids:
                        invoice_ids = [
                            i.id for i in
                            riba_move_line.move_line_id.unsolved_invoice_ids
                        ]
                    invoice_model.browse(invoice_ids).write({
                        'unsolved_move_line_ids': [(4, move_line.id)],
                    })
            if move_line.account_id.id == wizard.effects_account_id.id:
                to_be_reconciled.append(move_line.id)
        for acceptance_move_line in distinta_line.acceptance_move_id.line_ids:
            if (
                acceptance_move_line.account_id.id ==
                wizard.effects_account_id.id
            ):
                to_be_reconciled.append(acceptance_move_line.id)

        distinta_line.write({
            'unsolved_move_id': move.id,
            'state': 'unsolved',
        })
        to_be_reconciled_lines = move_line_model.with_context(
            {'unsolved_reconciliation': True}).browse(to_be_reconciled)
        to_be_reconciled_lines.reconcile()
        distinta_line.distinta_id.signal_workflow('unsolved')
        return {
            'name': _('Unsolved Entry'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': move.id or False,
        }
