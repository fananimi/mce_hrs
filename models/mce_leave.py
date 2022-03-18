# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class Leave(models.Model):
    _name = 'mce_hr.leave'
    _description = 'Leave'

    name = fields.Char(readonly=True, string="Display name", compute='_compute_name')
    employee_id = fields.Many2one('mce_hr.employee', required=True)
    employee_name = fields.Char(readonly=True, related="employee_id.name")
    employee_reg_id = fields.Char(readonly=True, related="employee_id.employee_id", string="Employee ID")
    date_from = fields.Date(required=True, string="Start Date")
    date_to = fields.Date(required=True, string="End Date")
    duration = fields.Integer(compute='_compute_duration', string='Leave Duration', readonly=True)
    description = fields.Text(required=True, string="Description")

    @api.depends('duration', 'description')
    def _compute_name(self):
        for leave in self:
            leave.name = "%d day(s) leave of %s for %s" % (leave.duration, leave.employee_id.name, leave.description)


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
