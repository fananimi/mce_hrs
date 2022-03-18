# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    city_ids = fields.One2many('res.country.city', 'state_id', "Cities", required=False,
                               help="List of cities in this country state")


class ResCountryCity(models.Model):
    _name = 'res.country.city'
    _description = 'Cities'
    _order = 'name'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code')
    state_id = fields.Many2one('res.country.state', string='State', required=True)
    country_id = fields.Many2one('res.country', related='state_id.country_id', store=True, readonly=True)
    district_ids = fields.One2many('res.country.district', inverse_name='city_id', string="Districts",
                                   help="List of districts in this city")

class ResCountryDistrict(models.Model):
    _name = 'res.country.district'
    _description = 'Districts'
    _order = 'name'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code')
    city_id = fields.Many2one('res.country.city', 'City', required=True)
    state_id = fields.Many2one('res.country.state', related='city_id.state_id', store=True, readonly=True)
    country_id = fields.Many2one('res.country', related='state_id.country_id', store=True, readonly=True)
    subdistrict_ids = fields.One2many('res.country.subdistrict', inverse_name='district_id', string="Sub Districts",
                                      help="List of sub districts in this district")


class ResCountrySubDistrict(models.Model):
    _name = 'res.country.subdistrict'
    _description = 'Sub-districts'
    _order = 'name'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code')
    district_id = fields.Many2one('res.country.district', 'District', required=True)
    city_id = fields.Many2one('res.country.city', related='district_id.city_id', store=True, readonly=True)
    state_id = fields.Many2one('res.country.state', related='city_id.state_id', store=True, readonly=True)
    country_id = fields.Many2one('res.country', related='state_id.country_id', store=True, readonly=True)
