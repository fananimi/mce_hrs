# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Leave(models.Model):
    _name = 'mce_hr.leave'
    _description = 'Leave'

    name = fields.Char(required=True)
    employee_id = fields.Many2one('mce_hr.employee', required=True)
    # address = fields.Float(compute="_value_pc", store=True)
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    duration = fields.Integer()
    description = fields.Date(required=True)
