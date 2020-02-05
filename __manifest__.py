{
	'name' : 'Society Managment',
	'version' : '1.1',
	'summary' : 'Manage Society as your requrment',
	'type' : 'application',
	'depends': ['web_dashboard','portal'],
	'data' : [
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/society_managment.xml',
		'views/member.xml',
		'reports.xml',
	],
	'demo' : [
		'demo/demo.xml',
	],
	'application' : True
}