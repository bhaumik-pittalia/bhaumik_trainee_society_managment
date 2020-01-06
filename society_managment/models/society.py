from odoo import api,fields,models
from odoo.exceptions import ValidationError

class Society(models.Model):
	_name = 'society.society'
	_description = 'Society details'

	name = fields.Char(string='Society Name')
	registration_number = fields.Char(string='Registration number')
	address = fields.Text(string='Society Address')
	society_type = fields.Selection([
             ('co-oprativ', 'co-oprativ-housing'),
             ])
	_sql_constraints = [
		('registration_number_uniq','unique(registration_number)','registration number is wrong!')
	]

class Member(models.Model):
	_name = 'member.member'
	_description = 'Member details'

	name = fields.Char(string='Member name')
	society_id = fields.Many2one(comodel_name='society.society')
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
				raise ValidationError("Your phon number is wrong: %s" % numb.ph_no)

	_sql_constraints = [
		('ph_no_uniq','unique(ph_no)','Phone Number number is Already register!'),
		('email_uniq','unique(email)','email is Already register!')
	]



class Complaint(models.Model):
	_name = 'complaint.complaint'
	_description = 'Complaint details'
	_rec_name ='complaint_details'

	complaint_details = fields.Selection([
             ('water', 'Water Problem'),
             ('common plot', 'Common Plot'),
             ('security', 'Security')
             ])
	complaint_date = fields.Date(string='Complaint Date')
	member_ids = fields.Many2one(comodel_name='member.member')


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
	description = fields.Text(string='Details')
	society_ids = fields.Many2one(comodel_name='society.society')