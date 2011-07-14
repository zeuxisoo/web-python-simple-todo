#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, model, message
from bottle import debug, route, run, template, static_file, request, redirect, default_app
from sqlalchemy.orm import relation, sessionmaker

# Load session middleware
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'library'))
from beaker.middleware import SessionMiddleware

# Const variable
TITLE = "Simple Todo"
WWW_ROOT = os.path.abspath(os.path.dirname(__file__))

# ORM session
session_marker = sessionmaker(bind=model.engine)
orm_session = session_marker()

# Index
@route('/')
def index():
	todos = orm_session.query(model.Todo).order_by('-id')

	return template("index", title=TITLE, todos=todos, flush_message=message.flush_message())

# Create
@route('/new', method='POST')
def new():
	name = request.forms.get("name").decode("utf-8");
	
	if len(name) > 0:
		record = model.Todo(topic=name, status=False)
		orm_session.add(record)
		orm_session.commit()
        
		message.success(u"新增事項成功")
	else:
		message.error(u"沒有輸入項目")
        
	redirect("/")
		
# Delete
@route('/delete/:id')
def delete(id):
	todo = orm_session.query(model.Todo).filter_by(id=id).first()
	
	if todo:
		orm_session.delete(todo)
		orm_session.commit()
		
		message.success(u"刪除事項成功")
	else:
		message.error(u"找不到記錄")

	redirect("/")
	
# Finish
@route('/finish/:id')
def finish(id):
	todo = orm_session.query(model.Todo).filter_by(id=id).first()
	
	if todo:
		orm_session.query(model.Todo).filter_by(id=id).update({
			model.Todo.status: True
		})
		orm_session.commit()
		
		message.success(u"完成事項成功")
	else:
		message.error(u"找不到記錄")

	redirect("/")
	
# Unfinish
@route('/unfinish/:id')
def unfinish(id):
	todo = orm_session.query(model.Todo).filter_by(id=id).first()
	
	if todo:
		orm_session.query(model.Todo).filter_by(id=id).update({
			model.Todo.status: False
		})
		orm_session.commit()
		
		message.success(u"恢復事項成功")
	else:
		message.error(u"找不到記錄")
		
	redirect("/")
	
# Edit
@route('/edit/:id')
def edit(id):
	todo = orm_session.query(model.Todo).filter_by(id=id).first()
	
	if todo:
		return template("edit", title=TITLE, todo=todo, flush_message=message.flush_message())
	else:
		message.error(u"找不到記錄")
		redirect("/")

@route('/save', method="POST")
def save():
	id = request.forms.get("id").decode("utf-8");
	name = request.forms.get("name").decode("utf-8");

	if id is None or id == "":
		message.error(u"找不到記錄")
	elif len(name) <= 0:
		message.error(u"沒有輸入項目")
	else:
		todo = orm_session.query(model.Todo).filter_by(id=id).first()
		
		if todo:
			orm_session.query(model.Todo).filter_by(id=id).update({
				model.Todo.topic: name
			})
			orm_session.commit()

		message.success(u"編輯事項成功")

	redirect("/")

# Static file
@route('/static/:path#.+#')
def static_folder(path):
	return static_file(path, root=os.path.join(WWW_ROOT, 'static'))

# Boot
if __name__ == "__main__":
	debug(True)
	
	app = default_app()
	session_options = {
		'session.type': 'file',
		'session.cookie_expires': 300,
		'session.data_dir': './data',
		'session.auto': True
	}
	app = SessionMiddleware(app, session_options)
	run(host='localhost', port=8082, reloader=True, app=app)