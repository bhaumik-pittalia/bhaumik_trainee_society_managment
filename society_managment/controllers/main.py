from odoo import http
from odoo.http import request


class Societys(http.Controller):
    @http.route('/society/', auth='public', website=True, csrf=False)
    def index(self, **kw):
        print("\n\n\n\n")
        soc = http.request.env['society.society'].search([])
        return http.request.render('society_managment.society', {
            'societys': soc,
        })

    @http.route(['/society/create' , '/society/update/<model("society.society"):s>'], auth='public', website=True, csrf=False)
    def screate(self, s=None):
        print("\n\n\n\n")
        if s:
            s = http.request.env['society.society'].browse([s.id])
        return http.request.render('society_managment.create_society',{'s' : s}) 

    @http.route(['/society/form/', '/society/form/<int:society>'],method ='post', auth='public',website=True, csrf=False)
    def society(self, society=None, **post):
        print("\n\n\n\n",post)
        
        if post:
            if society:
                print("\n\n\n\n",post)
                print(dir(request.env))
                http.request.env['society.society'].browse([society]).write({
                    'name' : post.get('name'),
                    'registration_number' : post.get('registration_number'),
                    'address' : post.get('address'),
                    'society_type' : post.get('society_type')
                    })
            else:
                http.request.env['society.society'].create([{
                    'name' : post.get('name'),
                    'registration_number' : post.get('registration_number'),
                    'address' : post.get('address'),
                    'society_type' : post.get('society_type')
                    }])
        return http.request.redirect('/society')

    @http.route('/society/delete/<model("society.society"):society>', auth='public', website=True, csrf=False)
    def sdelete(self, society = None ):
        society.unlink()
        print("\n\n\n\n")
        return http.request.redirect('/society/') 
