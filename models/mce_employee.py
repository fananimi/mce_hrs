# -*- coding: utf-8 -*-

from odoo import models, fields, api

ADDRESS_FIELDS = (
    'street', 'street2', 'zip', 'city', 'city_id', 'subdistrict_id', 'district_id', 'state_id', 'country_id'
)

class Employee(models.Model):
    _name = 'mce_hr.employee'
    _description = 'Employee'
    _order = 'name'

    name = fields.Char(string="Employee Name", required=True)
    register_id = fields.Char(string="Employee ID", required=True)
    birth_date = fields.Date(string="Birth date", required=True)
    joined_date = fields.Date(string="Joined date", required=True)

    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',
        required=True)
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
        domain="[('country_id', '=?', country_id)]", required=True)
    city_id = fields.Many2one("res.country.city", string='City', ondelete='restrict',
        required=True)
    district_id = fields.Many2one("res.country.district", string='District',
        ondelete='restrict', required=False)
    subdistrict_id = fields.Many2one("res.country.subdistrict", string='Sub District',
        ondelete='restrict', required=False)

    street = fields.Char(string="Address Line 1", required=True)
    street2 = fields.Char(string="Address Line 2", required=False)
    zip = fields.Char(change_default=True, required=False)
    city = fields.Char("City Name")
    contact_address = fields.Char(compute='_compute_contact_address', string='Complete Address')

    leave_ids = fields.One2many('mce_hr.leave', 'employee_id', string='Leave History',
        readonly=True, copy=True, auto_join=True, domain=[('state', '=', 'done')])
    leave_count = fields.Integer(readonly=True, store=True, compute='_compute_leave_count')
    leave_balance = fields.Integer(readonly=True, store=True, compute='_compute_leave_balance')

    @api.depends('leave_ids')
    def _compute_leave_count(self):
        for employee in self:
            employee.leave_count = sum(employee.leave_ids.mapped('duration'))

    def _compute_leave_balance(self):
        for employee in self:
            employee.leave_balance = self.env['mce_hr.leave'].get_remaining_leave(employee)

    def action_leave_balance(self):
        return True

    @api.depends(lambda self: self._display_address_depends())
    def _compute_contact_address(self):
        for employee in self:
            employee.contact_address = employee._display_address()

    def _display_address_depends(self):
        # field dependencies of method _display_address()
        return self._formatting_address_fields() + [
            'country_id', 'state_id',
        ]

    @api.model
    def _formatting_address_fields(self):
        """Returns the list of address fields usable to format addresses."""
        return self._address_fields()

    @api.onchange('country_id')
    def onchange_employee_country(self):
        domain = {'state_id': [], 'city_id': [], 'district_id': [], 'subdistrict_id': []}
        if self.country_id:
            list_domain = [('country_id', '=', self.country_id.id)]
            domain = {'state_id': list_domain, 'city_id': list_domain, 'district_id': list_domain,
                      'subdistrict_id': list_domain}
            if (self.state_id and self.state_id.country_id) and (self.state_id.country_id.id != self.country_id.id):
                self.state_id = False
            if (self.city_id and self.city_id.country_id) and (self.city_id.country_id.id != self.country_id.id):
                self.city_id = False
            if (self.district_id and self.district_id.country_id) and (
                    self.district_id.country_id.id != self.country_id.id):
                self.district_id = False
            if (self.subdistrict_id and self.subdistrict_id.country_id) and (
                    self.subdistrict_id.country_id.id != self.country_id.id):
                self.subdistrict_id = False
        return {'domain': domain}

    @api.onchange('state_id')
    def onchange_employee_state(self):
        domain = {'city_id': [], 'district_id': [], 'subdistrict_id': []}
        if self.state_id:
            list_domain = [('state_id', '=', self.state_id.id)]
            domain = {'city_id': list_domain, 'district_id': list_domain, 'subdistrict_id': list_domain}
            if (self.subdistrict_id and self.subdistrict_id.state_id) and (
                    self.subdistrict_id.state_id.id != self.state_id.id):
                self.subdistrict_id = False
            if (self.district_id and self.district_id.state_id) and (self.district_id.state_id.id != self.state_id.id):
                self.district_id = False
            if (self.city_id and self.city_id.state_id) and (self.city_id.state_id.id != self.state_id.id):
                self.city_id = False
            self.country_id = self.state_id.country_id
        return {'domain': domain}

    @api.onchange('city_id')
    def onchange_employee_city(self):
        domain = {'district_id': [], 'subdistrict_id': []}
        if self.city_id:
            list_domain = [('city_id', '=', self.city_id.id)]
            domain = {'district_id': list_domain, 'subdistrict_id': list_domain}
            if (self.district_id and self.district_id.city_id) and (self.district_id.city_id.id != self.city_id.id):
                self.district_id = False
            self.city = self.city_id.name
            self.state_id = self.city_id.state_id
            self.country_id = self.city_id.country_id

        return {'domain': domain}

    @api.onchange('district_id')
    def onchange_employee_district(self):
        domain = {'subdistrict_id': []}
        if self.district_id:
            list_domain = [('district_id', '=', self.district_id.id)]
            domain = {'subdistrict_id': list_domain}
            if (self.subdistrict_id and self.subdistrict_id.district_id) and (
                    self.subdistrict_id.district_id != self.district_id):
                self.subdistrict_id = False
            self.city_id = self.district_id.city_id
            self.state_id = self.district_id.state_id
            self.country_id = self.district_id.country_id
        return {'domain': domain}

    @api.onchange('subdistrict_id')
    def onchange_employee_subdistrict(self):
        if self.subdistrict_id:
            self.district_id = self.subdistrict_id.district_id
            self.city_id = self.subdistrict_id.city_id
            self.state_id = self.subdistrict_id.state_id
            self.country_id = self.subdistrict_id.country_id

    def _display_address(self):
        address_format_txt = '%(street)s\n%(street2)s\n%(subdistrict_name)s, %(district_name)s\n%(city_name)s - %(' \
                             'state_name)s\n%(country_name)s\n%(zip)s'
        address_format = address_format_txt or self.country_id.address_format
        args = {
            'country_code': self.country_id.code or '',
            'country_name': self.country_id.name or '',
            'state_code': self.state_id.code or '',
            'state_name': self.state_id.name or '',
            'city_name': self.city_id and self.city_id.name or self.city or '',
            'district_name': self.district_id.name or '',
            'subdistrict_name': self.subdistrict_id.name or ''
        }
        for field in self._address_fields():
            args[field] = getattr(self, field) or ''
        if not self.subdistrict_id or not self.district_id:
            address_format = address_format.replace(',', '')
        if not (self.city or self.city_id) or not self.state_id:
            address_format = address_format.replace('-', '')
        return address_format % args

    @api.model
    def _address_fields(self):
        """ Returns the list of address fields that are synced from the parent
        when the `use_parent_address` flag is set. """
        return list(ADDRESS_FIELDS)
