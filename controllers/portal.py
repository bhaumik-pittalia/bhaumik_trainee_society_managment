from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
from datetime import date

class Home(Home):
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('society_managment.group_manager'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if  request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
            return '/yourhomepage'
        return super(Member, self)._login_redirect(uid, redirect=redirect)

class Member(http.Controller):

    @http.route('/member/', auth="public", type="http", csrf=False)
    def custmoer_register(self, **kw):
        currency = http.request.env['res.currency'].sudo().search([])
        return http.request.render('society_managment.member', {'currency': currency})

    @http.route('/yourhomepage', auth="public", type="http", csrf=False)
    def society_society(self, **kw):
        sm = request.env['member.member'].sudo().search([('res_user','=',request.session.uid)])
        notice = http.request.env['noticboard.noticboard'].sudo().search([('company_id','=',sm.company_id.id)])
        return http.request.render('society_managment.user_form', {
            'notice': notice
            })
    @http.route('/complaint', auth="public", type="http", csrf=False)
    def society_complaint(self, **kw):
        sm = request.env['member.member'].sudo().search([('res_user','=',request.session.uid)])
        complaint = request.env['complaint.complaint'].sudo().search([('company_id','=',sm.company_id.id)])
        member = request.env['member.member'].sudo().search([('company_id','=',sm.company_id.id)])
        return http.request.render('society_managment.complaint_form', {
            'complaint': complaint
            })
    @http.route('/members', auth="public", type="http", csrf=False)
    def society_member(self, **kw):
        sm = request.env['member.member'].sudo().search([('res_user','=',request.session.uid)])
        member = request.env['member.member'].sudo().search([('company_id','=',sm.company_id.id)])
        return http.request.render('society_managment.member_form', {
            'member' : member
            })

    @http.route('/complaintForm/', auth="public", type="http", csrf=False)
    def complaintForm(self):
        # cm = http.render.env['complaint.complaint']
        return http.request.render('society_managment.complaintform')

    @http.route('/complaint/form', auth="public", type="http", csrf=False, website=True)
    def complaint_form(self, **post):
        sm = request.env['member.member'].sudo().search([('res_user','=',request.session.uid)])
        http.request.env['complaint.complaint'].sudo().create([{
                    'complaint_details' : post.get('complaint_details'),
                    'complaint_date': date.today(),
                    'member_ids' : sm.id,
                    }])
        return http.request.redirect('/complaint')

    @http.route('/member/form/', auth="public", type="http", csrf=False)
    def member_register(self, **post):
        if post.get('manager_group') == 'service_provider':
            groups_id_name = [(6, 0, [request.env.ref('society_managment.group_manager').id])]
            currency_name = post.get('currency')
            currency = request.env['res.currency'].sudo().search([('name','=',currency_name)],limit=1)
            partner = request.env['res.partner'].sudo().create({
                'name': post.get('name'),
                'email': post.get('email')
            })
            company = request.env['res.company'].sudo().create({
                'name': post.get('companyname'),
                'partner_id': partner.id,
                'currency_id': currency.id,
            })
            request.env['res.users'].sudo().create({
                'partner_id': partner.id,
                'login': post.get('name'),
                'password': post.get('password'),
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'groups_id': groups_id_name,
            })
        else:
            groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]
            partner = request.env['res.partner'].sudo().create({
                'name': post.get('name'),
                'email': post.get('email')
            })
            request.env['res.users'].sudo().create({
                'partner_id': partner.id,
                'login': post.get('name'),
                'password': post.get('password'),
                'groups_id': groups_id_name,
            })
        return http.local_redirect('/web/login')

