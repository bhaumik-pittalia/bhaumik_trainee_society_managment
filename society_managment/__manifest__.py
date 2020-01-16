{
	'name' : 'Society Managment',
	'version' : '1.1',
	'summary' : 'Manage Society as your requrment',
	'type' : 'application',
	'depends': ['website'],
	'data' : [
		'security/ir.model.access.csv',
		'views/society_managment.xml',
		'views/templates.xml',
		'reports.xml',
	],
	'demo' : [
		'demo/demo.xml',
	],
	'application' : True
}