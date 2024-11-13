from flask import Flask, render_template, request, flash, redirect, url_for
from server import models as db
from server.forms import forms
import time
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__,template_folder="templates")
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRETKEY")

@app.route('/')
def home():
    return render_template("main.html")

@app.route('/crud', methods=['GET','POST'])
def read():
    
    crudData = db.getAll()
    print(crudData)
    return render_template('create.html', data=crudData, showForm=False)


@app.route('/crud/create', methods=['GET', 'POST'])
def create():

    createForm = forms.CreateForm()
    
    if createForm.validate_on_submit():
        
        context = createForm.content.data
        flash(f'SUCCESSFULLY CREATED')

        db.insert(context)
        
        return redirect(url_for('create'))

    return render_template("/forms/createForm.html", form=createForm, showForm=True)

@app.route('/crud/update/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    context = db.getByID(id)[0]

    updateForm = forms.UpdateForm()
        
    if updateForm.validate_on_submit():
        
        updatedContext = updateForm.updateContent.data
        print(updatedContext)

        results = db.update(id, updatedContext)
        if results == 0:
            return redirect(url_for('read'))
        else:
            print('error update!')
            
    else:
        updateForm.updateContent.data = context
        
    return render_template("/forms/updateForm.html", form=updateForm, showForm=True)

@app.route('/crud/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    
    results = db.delete(id)
    
    if results == 0:
        return redirect(url_for('read'))
    else:
        print('error delete')
    

@app.errorhandler(500)
def error(e):
    return render_template('404.html')



if __name__ == "__main__":
    app.run(debug=True)

