# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Employee(models.Model):
    _name = 'mce_hr.employee'
    _description = 'Employee'

    name = fields.Char()
    employee_id = fields.Char()
    # address = fields.Float(compute="_value_pc", store=True)
    birt_date = fields.Date()
    joined_date = fields.Date()
