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

