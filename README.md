# Coneptual stuff

Application Contexts
current_app, g

Request contexts
request, session


# Checking app context

>>> app_ctx=app.app_context()
>>> app_ctx.push()
>>> current_app.name
'hello'
>>> app_ctx.pop()
>>> current_app.name


# Checking URL map

>>> app.url_map
Map([<Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>,
 	<Rule '/' (OPTIONS, GET, HEAD) -> hello>,
 	<Rule '/username/<user>' (OPTIONS, GET, HEAD) -> user>])	



<Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static> >>>>> This is a special route added by Flask to access static files.

OPTIONS, GET, HEAD   >>>>> These are the request methods


# IMPORTANT request hooks

before_request 
before_first_request
after_request
teardown_request


# IMPORTANT bootstrap template blocks

Available blocks
Block name	Outer Block	Purpose
doc	 	Outermost block.
html	doc	Contains the complete content of the <html> tag.
html_attribs	doc	Attributes for the HTML tag.
head	doc	Contains the complete content of the <head> tag.
body	doc	Contains the complete content of the <body> tag.
body_attribs	body	Attributes for the Body Tag.
title	head	Contains the complete content of the <title> tag.
styles	head	Contains all CSS style <link> tags inside head.
metas	head	Contains all <meta> tags inside head.
navbar	body	An empty block directly above content.
content	body	Convenience block inside the body. Put stuff here.
scripts	body	Contains all <script> tags at the end of the body.

ref # https://pythonhosted.org/Flask-Bootstrap/basic-usage.html#available-blocks

