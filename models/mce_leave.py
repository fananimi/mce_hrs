# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class Leave(models.Model):
    _name = 'mce_hr.leave'
    _description = 'Leave'
    _order = 'date_from DESC'

    name = fields.Char(readonly=True, string="Display name", compute='_compute_name')
    employee_id = fields.Many2one('mce_hr.employee', required=True)
    employee_name = fields.Char(readonly=True, related="employee_id.name")
    employee_reg_id = fields.Char(readonly=True, related="employee_id.register_id", string="Employee ID")
    date_from = fields.Date(required=True, string="Start Date")
    date_to = fields.Date(required=True, string="End Date")
    date_to_cal = fields.Date(required=False, string="End Date for Calendar", compute='_compute_date_to_cal', store=True)
    duration = fields.Integer(compute='_compute_duration', string='Leave Duration', readonly=True)
    remaining_leave = fields.Integer(compute='_compute_remaining_leave',
        string='Remaining Leave', readonly=True)
    description = fields.Text(required=True, string="Description")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting to Approve'),
        ('done', 'Approved')
        ], string='Status', readonly=True, copy=False, index=True, default='draft')

    def action_approve(self):
        for leave in self:
            duration = leave.duration
            remaining_leave = leave.remaining_leave
            if duration > remaining_leave:
                raise ValidationError(_('The remaining leave is less than the requested duration!'))
            leave.state = "done"

    def action_submit(self):
        for leave in self:
            duration = leave.duration
            remaining_leave = leave.remaining_leave
            if duration > remaining_leave:
                raise ValidationError(_('The remaining leave is less than the requested duration!'))
            leave.state = "waiting"

    @api.depends('duration', 'description')
    def _compute_name(self):
        for leave in self:
            leave.name = "%d day(s) leave of %s for %s" % (leave.duration, leave.employee_id.name, leave.description)

    @api.depends('employee_id')
    def _compute_remaining_leave(self):
        for leave in self:
            if leave.employee_id:
                remaining_leave = self.env['mce_hr.leave'].\
                    get_remaining_leave(leave.employee_id)
                self.remaining_leave = remaining_leave
            else:
                self.remaining_leave = 0

    @api.model
    def get_remaining_leave(self, employee_id):
        if not employee_id.joined_date:
            return 0

        today = datetime.now().date()
        joined_date = employee_id.joined_date
        max_leave = relativedelta(today, joined_date).years * 12
        domain = [
            ('employee_id', '=', employee_id.id),
            ('state', '=', 'done')
        ]
        leave_history = self.search(domain).mapped('duration')
        leave_taken = sum(leave_history)
        return (max_leave - leave_taken)

    @api.depends('date_from', 'date_to')
    def _compute_duration(self):
        for leave in self:
            start = leave.date_from
            end = leave.date_to
            if all([start, end]):
                duration = (end - start).days + 1
                if duration > 0:
                    leave.duration = duration
                else:
                    raise ValidationError(_('Incorrect End date!'))
            else:
                self.duration = 0

    @api.depends('date_to')
    def _compute_date_to_cal(self):
        for leave in self:
            end_cal = leave.date_to + timedelta(days=1)
            leave.date_to_cal = end_cal
