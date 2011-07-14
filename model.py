#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Todo(Base):
	__tablename__ = 'todo'
	
	id = Column(Integer, primary_key=True)
	topic = Column(String(255), nullable=False)
	create_at = Column(Date, default=datetime.utcnow)
	status = Column(Boolean(), default=False)
	
	def __init__(self, *args, **kwargs):
		super(Todo, self).__init__(*args, **kwargs)
		
	def __repr__(self):
		return "<Todo '%s'>" % self.topic

engine = create_engine('sqlite:///database/todo.sqlite', echo=True)
Base.metadata.create_all(engine)