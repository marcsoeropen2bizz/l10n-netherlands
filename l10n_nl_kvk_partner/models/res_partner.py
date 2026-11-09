# Copyright 2025 360ERP (<https://www.360erp.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models

KVK_SCHEME_ID = "0106"


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_nl_kvk = fields.Char(
        "KvK Number",
        help="Dutch Chamber of Commerce number",
        compute="_compute_l10n_nl_kvk",
        inverse="_inverse_l10n_nl_kvk",
        search="_search_l10n_nl_kvk",
    )

    @api.depends("routing_endpoint", "routing_scheme", "additional_identifiers")
    def _compute_l10n_nl_kvk(self):
        """Reflect the Peppol/Routing Endpoint as the KvK Number"""
        for partner in self:
            if partner.routing_scheme == KVK_SCHEME_ID and partner.routing_endpoint:
                partner.l10n_nl_kvk = partner.routing_endpoint
            else:
                partner.l10n_nl_kvk = (
                    partner._get_additional_identifier("NL_KVK")
                    if hasattr(partner, "_get_additional_identifier")
                    else False
                )

    def _inverse_l10n_nl_kvk(self):
        """Store the KvK number as the Peppol/Routing Endpoint and Scheme"""
        for partner in self:
            if not partner.l10n_nl_kvk and partner.routing_scheme == KVK_SCHEME_ID:
                partner.routing_endpoint = False
                partner.routing_scheme = False
                if hasattr(partner, "_set_additional_identifier"):
                    partner._set_additional_identifier("NL_KVK", False)
            elif partner.l10n_nl_kvk:
                partner.routing_endpoint = partner.l10n_nl_kvk
                partner.routing_scheme = KVK_SCHEME_ID
                if hasattr(partner, "_set_additional_identifier"):
                    partner._set_additional_identifier("NL_KVK", partner.l10n_nl_kvk)

    def _search_l10n_nl_kvk(self, operator, value):
        """Translate to a search on Peppol/Routing attributes"""
        return [
            ("routing_scheme", "=", KVK_SCHEME_ID),
            ("routing_endpoint", operator, value),
        ]
