from flask import Blueprint, g, redirect, url_for, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

from . import process

bp = Blueprint('auth', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    if g.user is None:
        return redirect(url_for('auth.login'))
    return render_template('index.html')

@bp.route('/register', methods=['POST', 'GET'])
@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        email_user = request.form['email']
        password_user = request.form['password']
        phone = request.form['phone']
        id_card_front_image = request.files['font_of_card']
        id_card_back_image = request.files['back_of_card']
        selfie_img = request.files['selfie_image']
        
        db = get_db()
        error = None
        
        try:
            db.execute("INSERT INTO user(username, phone) VALUES(?, ?)", (username, phone))
            db.commit()
        except:
            error = f"User name {username} or Phone {phone} already exists!"
        else:
            # lưu ảnh và trả về đường dẫn của ảnh(trước, sau, chân dung) là một tupple
            path_img = process.save_img(id_card_front_image, id_card_back_image, selfie_img)

            # trích xuất thông tin từ mặt trước và mặt sau căn cước
            info = process.extractInfo(path_img[0], path_img[1])
            
            # lấy id từ file extract
            id_card = list(info.keys())[0]

            try:
                print(1)
                # update id và username
                # db.execute("UPDATE user SET id=?, email=?,password=? WHERE username=?", (id_card, email_user, generate_password_hash(password_user), username))
                # db.commit()
            except:
                error = "You card is used!"
            else:
                # kiểm tra khuôn mặt có trùng với ảnh căn cước không(trả về: {'similarity':50.55,'isMatch':True})
                face_matching = process.faceMatching(path_img[0],path_img[2])
                if face_matching['isMatch']==True:
                    # insert thông tin vào bảng post
                    db.execute(
                        """
                            INSERT INTO post(
                                user_id,name,dob,sex,nationality,home,address,features,issue_date
                            ) VALUES(?,?,?,?,?,?,?,?,?)
                        """,(
                            id_card,
                            info[id_card]["name"],
                            info[id_card]["dob"],
                            info[id_card]["sex"],
                            info[id_card]["nationality"],
                            info[id_card]["home"],
                            info[id_card]["address"],
                            info[id_card]["features"],
                            info[id_card]["issue_date"]
                        )
                    )
                    db.commit()
                    process.delete()
                    
                    return redirect(url_for('auth.login'))
                else:
                    error = 'Unmatching!'
        flash(error)
    return render_template('register.html')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(username, password)
        
        db = get_db()
        error = None
        
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        
        if not user:
            error = 'Incorrect username!'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password!'
        
        if not error:
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('auth.index'))
        
        flash(error)
    return render_template('login.html')

@bp.route('/profile')
def profile():
    if g.user is None:
        return redirect(url_for('auth.login'))
    else:
        return render_template('profile.html')

@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (username,)
        ).fetchone()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))

@bp.route('/verification')
def verification():
    return render_template('verification.html')