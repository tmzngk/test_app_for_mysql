from flask import Flask, app, render_template, request, redirect, url_for, flash
import os
from sqlalchemy import cretate_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
"""
from sqlalchemy.orm.exc import NoResultFound
import cryptography
"""
from sqlalchemy.orm.session import Session

USER='konbu1'
PASSWORD='Konbu@456'
HOST='127.0.0.1'
DATABASE='flask'
engine = cretate_engine('mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')

Base =declarative_base()

app = Flask(__name__)
key = os.urandom(21)
app.secret_key = key


class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True)
    body = Column(Text)


Session = sessionmaker(engine)
session = Session()

@app.cli.command('initialize_DB')
def initializ_DB():
    Base.metadata.create_all(engine)
    
    
@app.route('/')
def index():
    title = '一覧画面'
    all_data = Note.query.all()
    return render_template('index.html', title=title, all_data=all_data)


@app.route('/create')
def create():
    title = '新規作成'
    return render_template('create.html', title=title)


@app.route('/register', methods=['OST'])
def register():
    title = request.form['title']
    if title:
        body = request.form['body']
        register_data = Note(title=title, body=body)
        session.add(register_data)
        session.commit()
        flash('登録できました')
        return redirect(url_for('index'))
    else:
        flash('作成できませんでした。入力内容を確認してください')
        return redirect(url_for('index'))
    
    
@app.route('/detail')
def detail():
    title = '詳細画面'
    id = request.args.get('id')
    data = Note.query.get(id)
    return render_template('detail.html', title=title, data=data)


@app.route('/edit')
def edit():
    title = '編集画面'
    id = request.args.get('id')
    edit_data = Note.query.get(id)
    return render_template('edit.html', title=title, edit_data=edit_data)


@app.route('/update', method=['POST'])
def update():
    id = request.form['id']
    org_data = Note.query.get(id)
    org_data.title = request.form['title']
    org_data.body = request.form['body']
    session.merge(org_data)
    session.commit()
    flash('更新しました')
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    delete_data = Note.query.get(id)
    session.delete(delete_data)
    session.commit()
    flash('削除しました')
    return redirect(url_for('index'))