# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from itertools import groupby
import json

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class RealEstateOrder(models.Model):
    _name = "real_estate.order"
    _description = "Real Estate Order"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "property_type_id desc"

    @api.model
    def default_get(self, fields):
        res = super(RealEstateOrder, self).default_get(fields)
        res['cancel_date'] = datetime.now() + timedelta(days=5)
        return res

    name = fields.Char(string='Name', default=lambda self: _('New'))
    description = fields.Text(string='Description', required=False)
    postcode = fields.Char(string='Postcode', required=False)
    date_availability = fields.Date(string='Available Date', required=False)
    cancel_date = fields.Date(string='Cancel Date', required=False)
    expected_price = fields.Float(string='Expected Price', required=False)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area(sqm)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], copy=False, index=True, tracking=3)
    property_type_id = fields.Many2one('property.type', string='Property Type')
    other_info = fields.Text(string='Other Info', required=False)
    salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    tag_id = fields.Many2many('property.tag', string='Property Tag')
    offer_ids = fields.One2many('property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(string='Total Area(sqm)', compute='_compute_total_area')
    best_offer = fields.Float(string='Best Price', compute='_compute_best_offer')
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string='Status', copy=False, default='new', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    active = fields.Boolean(default=True)
    sequence = fields.Char(string='Sequence', required=False)

    @api.model
    def update_property_state(self):
        change_state = self._search([
            ('state', 'in', 'new'),
            ('cancel_date', '=', fields.date.today())
        ])
        change_state.write({'state': 'canceled'})

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for rec in self:
            rec.best_offer = max(rec.offer_ids.mapped("price"), default=0)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.onchange("garden")
    def onchange_garden(self):
        for rec in self:
            if rec.garden == True:
                rec.garden_area = 10
                rec.garden_orientation = 'north'
            else:
                rec.garden_area = 0
                rec.garden_orientation = None

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                error = 'Canceled properties cannot be sold.'
                raise UserError(error)
            else:
                record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                error = 'Sold properties cannot be cancel.'
                raise UserError(error)
            else:
                record.state = "canceled"
        return True

    def action_reset(self):
        for rec in self:
            if rec.state == "canceled":
                return {
                     'type': 'ir.actions.act_window',
                     'view_mode': 'form',
                     'view_id': False,
                     'res_model': 'real_estate.order',
                     'domain': []
                 }

    def action_send_mail(self):
        template = self.env.ref('real_estate.property_mail_template')
        for rec in self:
            template.send_mail(rec.id)
        lang = self.env.context.get('lang')
        ctx = {
            'default_model': 'real_estate.order',
            'default_res_id': self.ids[0],
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    # _sql_constraints = [
    #     ('check_expected_price', 'CHECK(expected_price >= 0)',
    #      'The expected price must be strictly positive.'),
    #     ('check_selling_price', 'CHECK(selling_price >= 0)',
    #      'The selling price must be strictly positive.'),
    #     ('check_best_offer', 'CHECK(best_offer >= 0)',
    #      'The offer price must be strictly positive.')
    # ]

    @api.constrains('expected_price')
    def check_expected_price(self):
        for rec in self:
            if rec.expected_price and rec.expected_price <= 0:
                raise ValidationError(
                    _("A property expected price must be strictly positive"
                      ))

    @api.constrains('selling_price')
    def check_selling_price(self):
        for rec in self:
            if rec.selling_price and rec.selling_price <= 0:
                raise ValidationError(
                    _("A property selling price must be strictly positive"
                      ))

    @api.constrains('best_offer')
    def check_best_offer(self):
        for rec in self:
            if rec.best_offer and rec.best_offer <= 0:
                raise ValidationError(
                    _("A property best price must be strictly positive"
                      ))

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.9:
                raise ValidationError("The selling price must be at least 90% of expected price!")

    @api.ondelete(at_uninstall=False)
    def _check_state(self):
        for rec in self:
            if rec.state not in ['new', 'canceled']:
                raise ValidationError("Only new and canceled properties can be deleted.")

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('real_estate.order')
        return super().create(vals)

    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         name = rec.sequence + rec.buyer_id
    #         result.append(rec.id, name)
    #     return result