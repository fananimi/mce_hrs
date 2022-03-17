# -*- coding: utf-8 -*-
# from odoo import http


# class MceHr(http.Controller):
#     @http.route('/mce_hr/mce_hr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mce_hr/mce_hr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mce_hr.listing', {
#             'root': '/mce_hr/mce_hr',
#             'objects': http.request.env['mce_hr.mce_hr'].search([]),
#         })

#     @http.route('/mce_hr/mce_hr/objects/<model("mce_hr.mce_hr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mce_hr.object', {
#             'object': obj
#         })
