from flask import Flask, request,redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))

    def __init__(self,title, content):
        self.title = title
        self.body = content

    def __repr__(self):
        return '<Blog %r>' % self.title



def get_blogs():
    return Blog.query.all()

@app.route("/blog")
def index():

    blog_id = request.args.get("id")
    print('BLOG_id is', blog_id)


    if blog_id:
        blog_obj = Blog.query.filter_by(id=blog_id).first()
        print(blog_obj)
   
        #return render_template('blog_dtl.html',blogs=blog_obj)
        return render_template('blog_dtl.html',blog_title=blog_obj.title,blog_content=blog_obj.body)
    else:
        return render_template('main_blog.html',blogs=get_blogs())


@app.route("/newpost", methods=['POST', 'GET'])
def add_blog():


    error_flag = False

    if request.method == 'POST':

        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']
        title_error_msg = ""
        content_error_msg = ""
        
        if not blog_title:
            title_error_msg = "Please enter a title"
            error_flag = True

        if not blog_content:
            error_flag = True
            content_error_msg = "Please enter blog content"

        if error_flag == False:
            new_blog = Blog(blog_title,blog_content)
            db.session.add(new_blog)
            db.session.commit()
        else:
            return render_template('add_blog.html',title_error_p=title_error_msg,
                content_error_p=content_error_msg,blog_title_p=blog_title,blog_content_p=blog_content)

    
    if request.method == 'GET':
        return render_template('add_blog.html')
    else:        
        return redirect ("/blog?id=" + str(new_blog.id))
       
 
if __name__ == '__main__':
    app.run()