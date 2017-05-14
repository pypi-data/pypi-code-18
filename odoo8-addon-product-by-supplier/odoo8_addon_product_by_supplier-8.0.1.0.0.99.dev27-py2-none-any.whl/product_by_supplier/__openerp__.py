# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2013 Elico Corp.
#    Author: LIN Yu <lin.yu@elico-corp.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Product by supplier info',
    'version': '8.0.1.0.0',
    'category': 'purchase',
    'summary': 'Show products grouped by suppliers',
    'author': "Elico Corp,"
              "Odoo Community Association (OCA)",
    'website': 'http://www.elico-corp.com',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'purchase',
    ],
    'data': [
        'views/product_supplierinfo_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
