# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from itertools import groupby
import json

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty

from odoo.addons.payment import utils as payment_utils


class RealEstateTags(models.Model):
    _name = "real.estate.tags"
    _description = "Real Estate Tags "
    _order = " name desc"

    name = fields.Char(string='Name', required=False)
    color = fields.Integer(string="Color")
    color2 = fields.Char(string="Color2")

    _sql_constraints = [
        ('unique_tag_name', 'unique (name)', 'property tag must be unique.')
    ]
