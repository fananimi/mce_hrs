# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Employee(models.Model):
    _name = 'mce_hr.employee'
    _description = 'Employee'

    name = fields.Char(required=True)
    employee_id = fields.Char(required=True)
    # address = fields.Float(compute="_value_pc", store=True)
    birt_date = fields.Date(required=True)
    joined_date = fields.Date(required=True)
