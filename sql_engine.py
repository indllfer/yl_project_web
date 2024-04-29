from flask import Flask
from data import db_session
from data.users import User
from data.administrators import Admin
from data.games import Game
from passhash import hash_password


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def show_messsage(msg):
    print(msg)


def check_login_correct(login):
    lenth, spec, busy = False, True, True
    for i in login:
        if i not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_":
            spec = False

        if len(login) >= 3:
            lenth = True

    db_sess = db_session.create_session()
    if login not in [user.login for user in db_sess.query(User).all()]:
        busy = False
        if all([lenth, spec, not busy]):
            return True
        
        else:
            show_messsage(f"Login={login} is inc besause: lenth={lenth}, spec={spec}, busy={busy}")
            return False

    else:
        show_messsage("Login={login} is busy")
        return False
        

def check_password_correct(password):
    big, small, digits, lenth, spec = False, False, False, False, False
    for i in password:
        if i.isdigit():
            digits = True
        if i.upper() == i:
            big = True
        if i.lower() == i:
            small = True
        if i in """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~""":
            spec = True
        if len(password) >= 8:
            lenth = True    

    if all([big, small, digits, lenth, spec]):
        return True
    else:
        return False

def check_cmd_amd_name_correct(cmd__adm_name):
    lenth, spec = False, False
    if len(cmd__adm_name) > 8:
        lenth = True
    for i in cmd__adm_name:
        if i in "!?/.,[]{}():;":
            spec = True
    if all([lenth, not spec]):
        return True
    else:
        show_messsage(f"Name={cmd__adm_name} is inc because: lenth={lenth}, not spec={not spec}")
        return False
        
def check_cmd_staff_correct(id):
    return True


def player_registration(login, password, cmd_name, cmd_info, cmd_staff, achievements=bytes("", "utf8")):
    user = User()
    if check_login_correct(login):
        user.login = login
    else: 
        show_messsage("Логин некорректен")
        return False
    
    if check_password_correct(password):
        user.password = hash_password(password)
    else: 
        show_messsage("Пароль некорректен")
        return False

    if check_cmd_amd_name_correct(cmd_name):
        user.cmd_name = cmd_name
    else: 
        show_messsage("Имя команды некорректен")
        return False

    user.cmd_info = cmd_info

    if check_cmd_staff_correct(id):
        user.cmd_staff = cmd_staff
    else:
        show_messsage("Cостав команды некорректен") 
        return False

    user.achievements = achievements
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()
    return True


def player_authorization(login, password):
    db_sess = db_session.create_session()
    sp = [user.login for user in db_sess.query(User).all()]
    if login in sp:
        ind = sp.index(login)
        user = db_sess.query(User).filter(User.id == ind + 1).first()
        if hash_password(password) == str(user.password):
            return True
        else:
            show_messsage("Неверный пароль")
            return False
    else:
        show_messsage("Неверный логин")
        return False
    

def admin_registration(login, password, amd_name, amd_info):
    admin = Admin()
    if check_login_correct(login): admin.login = login
    else: 
        show_messsage("Логин некорректен")
        return False
    
    if check_password_correct(password): admin.password = hash_password(password)
    else: 
        show_messsage("Пароль некорректен")
        return False

    if check_cmd_amd_name_correct(amd_name): admin.amd_name = amd_name
    else: 
        show_messsage("Имя админа некорректен")
        return False

    admin.amd_info = amd_info
    db_sess = db_session.create_session()
    db_sess.add(admin)
    db_sess.commit()
    return True


def admin_authorization(login, password):
    db_sess = db_session.create_session()
    sp = [admin.login for admin in db_sess.query(Admin).all()]
    if login in sp:
        ind = sp.index(login)
        admin = db_sess.query(Admin).filter(Admin.id == ind + 1).first()
        if hash_password(password) == str(admin.password):
            return True
        else:
            show_messsage("Неверный пароль")
            return False
    else:
        show_messsage("Неверный логин")
        return False


def end_of_session():
    db_sess = db_session.create_session()
    db_sess.commit()


def main():
    db_session.global_init("db/invexgame.db")
    app.run()


if __name__ == '__main__':
    main()