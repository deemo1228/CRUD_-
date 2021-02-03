# 導入相對應的套件
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder
from flask_migrate import Migrate



# 創建了一個flask的實例
app = Flask(__name__)

'''
在Flask項目中，我們會用到很多配置（Config） 像是以下的密鑰以及資料庫
Session, Cookies以及一些第三方擴展都會用到SECRET_KEY值
這是一個比較重要的配置值，如未使用，會出現以下錯誤
the session is unavailable because no secret key was set.
Set the secret_key on the application to something unique and secret
'''
app.config.from_object('config')



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:redd00r@192.168.112.138:3306/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# db.init_app(app)
migrate = Migrate(app, db)
seeder = FlaskSeeder()
seeder.init_app(app, db)

# 定義模型(model)
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(120), unique=False, nullable=False)
    content = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return 'id=%r, title=%r,content=%r' % (self.id, self.title,self.content)



class User(db.Model):  # (多)
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    name = db.Column(db.String(80), unique=True, nullable=False)
    #  relationship
    message = db.relationship('Message', backref='user')

    def __repr__(self):
        return 'id=%r, User_name=%r' % (self.id, self.name)

class City(db.Model):  # (一)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='city')

    def __init__(self, name=None):
        self.name = name

    # 在python中，每個對象都可以用str()與repr()來轉成可顯示的字串，str()'可讀性'較高，是給開發者閱讀對象中的'有用資訊'的字串。
    # 而repr()的英文全名是representation，其產生的字串是給python的直譯器看的，這個字串會顯示'明確且教詳盡的資訊'，通常'可以讓python得知究竟這字串所代表的對象為何

    def __repr__(self):
        return 'id=%r, city_name=%r' % (self.id, self.name)

@app.route('/create', methods=["POST", "GET"])
def create():
    # 建立資料表
    db.create_all()

    return '建立資料庫並加入了eric,grace,deemo'


@app.route('/drop', methods=["POST", "GET"])
def drop():
    db.drop_all()

    return '刪除全部'


@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST":
        content = request.form['content']
        title = request.form['title']
        add_name = request.form['add_name']


        select_user = User.query.filter_by(name=add_name)  # 先取得在user當中naem='Eric'的User_id

        # 在Message()這張表單新增資料
        create_Eric_Messags = Message(user_id=select_user[0].id, title=title, content=content)
        db.session.add(create_Eric_Messags)  # 建立資料暫存
        db.session.commit()  # 傳送至資料庫
        return redirect(url_for('Index'))

    return render_template('add.html')


@app.route('/update_db', methods=["POST", "GET"])  # 小心同名子不行
def update_db():
    if request.method == "POST":
        content = request.form['content']
        title = request.form['title']
        username = request.form['name']
        select_message_user = User.query.filter_by(name=username).first()
        select_messages = Message.query.filter_by(user_id=select_message_user.id)

        #依序更改select_message內的內容
        for select_message in select_messages:
            select_message.title = title
            select_message.content = content
        db.session.commit()

        return redirect(url_for('show'))

    return render_template('update.html')





@app.route('/delete/<message_id>', methods=['GET', 'POST'])
def delete(message_id):

    # 抓取message表單中id = message_id 的第一筆資料
    message_delete = Message.query.filter_by(id=int(message_id)).first()
    # 利用 delete 的方法即可刪除單筆資料
    db.session.delete(message_delete)
    # 將之前的操作變更至資料庫中
    db.session.commit()

    return redirect(url_for('Index'))


@app.route('/show', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        content = request.form['content']
        title = request.form['title']
        add_name = request.form['add_name']

        select_user = User.query.filter_by(name=add_name)  # 先取得在user當中naem='Eric'的User_id

        # 在Message()這張表單新增資料
        create_Eric_Messags = Message(user_id=select_user[0].id, title=title, content=content)
        db.session.add(create_Eric_Messags)  # 建立資料暫存
        db.session.commit()  # 傳送至資料庫


        return render_template('show.html', Message=Message.query.all())

    return render_template('show.html', Message=Message.query.all())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form["user_name"]
        user_city = request.form["city_select"]  # 獲得使用者的id

        #這段不要加
        if user_city =="6" and user_name =="deemo" :
            return redirect(url_for('show'))
        #到這裡為止


        create_user = User(city_id=user_city,name=user_name)  # User()為要加入入的表單  # 必要條件為id(非必要),city_id(必要),name(必要)

        db.session.add(create_user)  # 建立資料暫存
        db.session.commit()  # 傳送至資料庫

        return render_template('Index.html', Message=Message.query.all())

    return render_template('register.html')



@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    if request.method == 'POST':

        res = User.query.all()
        res1 = City.query.all()

        return str(res)+"\n"+str(res1)

    return render_template('test.html')



@app.route('/dictionary', methods=["POST", "GET"])
def dictionary():
    movie = {'name': 'Saving Private Ryan',  # 電影名稱
             'year': 1998,  # 電影上映年份
             'director': 'Steven Spielberg',  # 導演
             'Writer': 'Robert Rodat',  # 編劇
             'Stars': ['Tom Hanks', 'Matt Damon', 'Tom Sizemore'],  # 明星
             'Oscar ': ['Best Director', 'Best Cinematography', 'Best Sound', 'Best Film Editing',
                        'Best Effects, Sound Effects Editing']
             # 獲得的奧斯卡獎項
             }

    return movie['Stars'][0]



@app.route('/', methods=["POST", "GET"])
def Index():
    if request.method == "POST":
        id_data = request.form['id']
        content = request.form['current_content']
        title = request.form['current_title']
        select_message = Message.query.filter_by(id=int(id_data)).first()
        select_message.title = title
        select_message.content = content
        db.session.commit()

        return render_template('Index.html', Message=Message.query.all())

    return render_template('Index.html', Message=Message.query.all())




@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        add_name = request.form["add_name"]
        title = request.form["title"]
        content = request.form["content"]
        select_user = User.query.filter_by(name=add_name)

        # 在Message()這張表單新增資料
        create_Messags = Message(user_id=select_user[0].id, title=title, content=content)
        db.session.add(create_Messags)  # 建立資料暫存
        db.session.commit()  # 傳送至資料庫

        return render_template('test.html', Message=Message.query.all())

    return render_template('test.html', Message=Message.query.all())









if __name__ == "__main__":
    # 由於在開發階段，將debug設為True
    app.run(debug=True)
