from flask import Flask, render_template, request, flash, redirect, url_for
from server import models as db
from server.forms import forms

app = Flask(__name__,template_folder="templates")
app.config['SECRET_KEY'] = "secret"

@app.route('/')
def home():
    return render_template("main.html")

@app.route('/crud/create', methods=['GET', 'POST'])
def create():

    createForm = forms.CreateForm()
    
    if createForm.validate_on_submit():
        context = createForm.content.data
        print(context)
        flash(f'SUCCESSFULLY CREATED')
        return redirect(url_for('create'))
        

    return render_template("/forms/createForm.html", form=createForm)





@app.errorhandler(500)
def error(e):
    return render_template('404.html')



if __name__ == "__main__":
    app.run(debug=True)

