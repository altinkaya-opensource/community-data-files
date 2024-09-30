# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nace_id = fields.Many2one(
        comodel_name="res.partner.nace", string="Main NACE", index=True
    )
    secondary_nace_ids = fields.Many2many(
        comodel_name="res.partner.nace", string="Secondary NACE"
    )
    nace_product_categ_ids = fields.Many2many('product.category', string="NACE Target Product Category",
                                              compute="_compute_nace_product_categ")

    @api.multi
    def _compute_nace_product_categ(self):
        for partner in self:
            lst = self.env['product.category']
            if partner.nace_id:
                lst = lst | partner.nace_id.product_categ_ids
            for nace in partner.secondary_nace_ids:
                lst = lst | nace.product_categ_ids
            partner.nace_product_categ_ids = lst
