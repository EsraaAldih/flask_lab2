
from flask import Flask, jsonify, render_template, jsonify, request, redirect, url_for

# from form import ToDoForm


app = Flask(__name__)   # __main__

DATABASE_URI = "sqlite:///users.db"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

posts = [
    {"id":1,"title": "task1", "description": "lab1 flask"},

    ]



@app.route('/', methods=['POST', 'GET'])
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/todo', methods=['GET', 'POST'])
def createToDo():
    
    if posts==[]:
        last_id=0
    else:
        last_id =posts[-1].get('id')

    print(last_id)
    form = ToDoForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        post = {'id':last_id+1,
                'title': form.title.data, 
                'description': form.description.data,
                }
        posts.append(post)
        return render_template('home.html', posts=posts)

    # return render_template('todoForm.html', form=form)


@app.route('/update/<int:id>', methods=['GET', 'POST'])    
def update_Todo(id):
  form = ToDoForm()  
  if request.method == 'POST' and form.validate_on_submit():
        for post in posts:
            if id == post.get('id'):
                post.update({id:id,'title': form.title.data,'description':  form.description.data})
                return render_template('home.html', posts=posts)  
  else: 
    return render_template('todoEditForm.html',id=id,form=form)



@app.route('/delete/<int:id>', methods=['GET','POST'])    
def delete_Todo(id):
#    form = ToDoForm()  
#   for post in posts:
#     if id == post.get('id'):
#         del post
#    posts[:] = [d for d in posts if d.get('id') != id]
   return render_template('home.html', posts=posts)  


app.run(debug=True)
