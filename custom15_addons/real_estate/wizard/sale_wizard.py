# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from itertools import groupby
import json

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def action_confirm(self):
        x = {
            'user_id': self.user_id.id,
            'team_id': self.team_id.id,
            'partner_id': self.partner_id
        }
        self.env['sale.order'].create(x)

