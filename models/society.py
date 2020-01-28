from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Society(models.Model):
    _name = 'society.society'
    _description = 'Society details'

    name = fields.Char(string='Society Name')
    registration_number = fields.Char(string='Registration Number')
    address = fields.Text(string='Society Address')
    society_type = fields.Selection([
        ('cooperative', 'cooperative'),
    ])
    _sql_constraints = [
        ('registration_number_uniq', 'unique(registration_number)',
         'registration number is Not Valid!')
    ]

    @api.model
    def create(self, vals):
        print(vals['name'])
        return super(Society, self).create(vals)



class Member(models.Model):
    _name = 'member.member'
    _description = 'Member details'

    name = fields.Char(string='Member Name')
    society_id = fields.Many2one(
        comodel_name='society.society', ondelete='cascade')
    house_no = fields.Char(string='House Number')
    ph_no = fields.Char(string='Phon Number')
    email = fields.Char(string='Email-Id')
    user_type = fields.Selection([
        ('Secretary', 'Secratery'),
        ('member', 'Member')
    ])

    @api.constrains('ph_no')
    def _check_ph_no(self):
        for numb in self:
            if numb.ph_no and len(str(numb.ph_no)) != 10:
                raise ValidationError(
                    "Your phon number is wrong: %s" % numb.ph_no)

    _sql_constraints = [
        ('ph_no_uniq', 'unique(ph_no)', 'Phone Number number is Already register!'),
        ('email_uniq', 'unique(email)', 'email is Already register!')
    ]


class Complaint(models.Model):
    _name = 'complaint.complaint'
    _description = 'Complaint details'
    _rec_name = 'complaint_details'

    complaint_details = fields.Selection([
        ('water', 'Water Problem'),
        ('commonplot', 'Common Plot'),
        ('security', 'Security')
    ])
    complaint_date = fields.Date(string='Complaint Date')
    member_ids = fields.Many2one(comodel_name='member.member')
    state = fields.Selection([
        ('pending', 'pending'),
        ('inprogress', 'inprogress'),
        ('completed', 'completed')
    ], default='pending')

    def action_pending(self):
        self.write({'state': 'pending'})
        return True

    def action_inprogress(self):
        self.write({'state': 'inprogress'})
        return True

    def action_completed(self):
        self.write({'state' : 'completed'})
        return True





class Notic_Board(models.Model):
    _name = 'noticboard.noticboard'
    _description = 'Activity Details'

    name = fields.Char(string='Notice Name')
    notic_type = fields.Selection([
        ('meeting', 'Meeting'),
        ('cultural', 'Cultural Activity'),
        ('program', 'Program')
    ])
    date = fields.Date(string='Date')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    description = fields.Text(string='Details')
    society_ids = fields.Many2one(comodel_name='society.society')

    def unlink(self):
        print("confirm")
        return super(Notic_Board, self).unlink()


class Account(models.Model):
    _name = 'balance.balance'
    _description = 'society balance sheet'

    name = fields.Many2one(string='Member Name', comodel_name='member.member')
    amount = fields.Integer(string='Amount')
    details = fields.Char(string='Details')
    provide = fields.Selection([
        ('recipt', 'Recipt'),
        ('vouchar', 'Vouchar')
    ])
    balance = fields.Integer()

    @api.constrains('amount')
    def _check_ph_no(self):
        balancesheet = self.env['balance.balance'].search([])
        total_balance = 0
        i = 0
        if balancesheet:
            for i in balancesheet:
                if i.provide == 'recipt':
                    total_balance += i.amount
                else:
                    total_balance -= i.amount
        for r in self:
            if total_balance < r.amount and r.provide == 'vouchar':
                raise ValidationError(
                    "Invalid Amount Avilable balance is : %s" % (total_balance +r.amount))
            else:
                r.balance=total_balance    
