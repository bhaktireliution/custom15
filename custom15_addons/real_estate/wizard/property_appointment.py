#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from itertools import groupby
import json

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class PropertyAppointment(models.TransientModel):
    _name = "property.appointment"
    _description = "Property Appointment"

    # property_type_id = fields.Many2one('property.type', string='Property Type')
    # name = fields.Char(string="Name")
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    date_availability = fields.Date(string='Available Date', required=False)
    tag_id = fields.Many2many('property.tag', string='Property Tag')
    # offer_ids = fields.One2many('property.offer', 'property_id', string='Offers')
    # property_id = fields.Many2one('real_estate.order', string='Property')
    # postcode = fields.Char(string='Postcode')

    def create_appointment(self):
        active_id = self._context.get('active_id')
        upd_var = self.env['real_estate.order'].browse(active_id)
        tag_lst = []
        for vals in self.tag_id:
            tag_lst.append(vals.id)
        # lst2 = []
        # for vals2 in self.offer_ids:
        #     lst2.append((0,0,{
        #         'price': vals2.price,
        #         'partner_id': vals2.partner_id.id,
        #         'status': vals2.status,
        #         'validity': vals2.validity,
        #         'date_deadline': vals2.date_deadline,
        #         'property_id': vals2.property_id
        #     }))
        vals = {
            'buyer_id': self.buyer_id.id,
            'date_availability': self.date_availability,
            'tag_id': [(6,0,tag_lst)],
            # 'offer_ids': lst2
        }
        upd_var.update(vals)
