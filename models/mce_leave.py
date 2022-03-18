# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class Leave(models.Model):
    _name = 'mce_hr.leave'
    _description = 'Leave'

    name = fields.Char(required=True, string="Display name")
    employee_id = fields.Many2one('mce_hr.employee', required=True)
    date_from = fields.Date(required=True, string="Start Date")
    date_to = fields.Date(required=True, string="End Date")
    duration = fields.Integer(compute='_compute_duration', string='Leave Duration', readonly=True)
    description = fields.Date(required=True, string="Description")

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
