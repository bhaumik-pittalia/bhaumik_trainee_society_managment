# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models



from odoo import fields,api,models

class Wizard(models.TransientModel):
    _name = 'member.wizard'
    _description = "Wizard: Quick Registration of member"

    def _default_session(self):
        return self.env['member.member'].browse(self._context.get('active_id'))

    session_id = fields.Many2one('member.member',string="Session", required=True, default=_default_session)
    member_ids = fields.Many2many('member.member', string="member")

    def subscribe(self,vals):
        self.session_id.member_ids |= self.member_ids
        return {self.member_ids}
