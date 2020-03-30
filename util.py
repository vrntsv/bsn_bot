import pymysql.cursors
import telebot
import datetime
import config_markups as conf_mark
import config_text as conf_txt
import random
import inline_conf

import config


paramstyle = "%s"
bot = telebot.TeleBot(config.BOT_TOKEN)

# bot = telebot.TeleBot(config.BOT_TOKEN[0])


def deploy_database():
    """
     Создать нужные таблицы в базе данных
    """
    pass


# # #стандартный коннект
# def connect():
#     # #     """
#     # #      Подключение к базе данных
#     # #     """
#     return pymysql.connect(
#         config.db_host,
#         config.db_user,
#         config.db_password,
#         config.db_database,
#         use_unicode=True,
#         charset=config.db_charset,
#         cursorclass=pymysql.cursors.DictCursor)


# мак
def connect():
  """
   Подключение к базе данных
  """
  return pymysql.connect(
      config.db_host,
      config.db_user,
      config.db_password,
      config.db_database,
      port='8889',
      unix_socket=config.db_unix_socket,
      use_unicode=True,
      charset=config.db_charset,
      cursorclass=pymysql.cursors.DictCursor)


def execute(sql, *args, commit=False):
    """
     Формат запроса:
     execute('<Запрос>', <передаваемые параметры>, <commit=True>)
    """
    db = connect()
    cur = db.cursor()
    try:
        cur.execute(sql % {"p": paramstyle}, args)
    except pymysql.err.InternalError as e:
        if sql.find('texts') == -1:
            print('Cannot execute mysql request: ' + str(e))
        return
    if commit:
        db.commit()
        db.close()
    else:
        ans = cur.fetchall()
        db.close()
        return ans


def check_employees_in_db(id_user):
    sql = execute('SELECT * FROM employees WHERE id=%(p)s', id_user)
    print(sql)
    if sql:
        if sql[0]:
            return True

    return False


def create_weekdays_for_db():
    return [0, 0, 0, 0, 0, 0, 0]


def check_admin_in_db(id_user):
    sql = execute('SELECT * FROM admins WHERE id=%(p)s', id_user)
    if sql:
        if sql[0]:
            return True

    return False

def get_employees_by_id(id_user):
    sql = execute('SELECT * FROM employees e  '
                   'LEFT JOIN company_list cl on cl.id=e.id_company '
                   'WHERE e.id=%(p)s', id_user)
    print(sql)
    if sql:
        return sql[0]
    return False

def check_unregistered(id_user):
    sql = execute('SELECT status FROM admins WHERE id=%(p)s', id_user)[0]
    if sql:
        return sql[0]

    return False


def add_user_in_db(id_user):
    execute('INSERT INTO employees(id) VALUE (%(p)s)', id_user, commit=True)


def change_status(id_user, admin=None, employees=None):
    # вместо id_user будем передавать словарик данных
    if admin:
        execute('INSERT INTO admins(id, promo, id_referal) VALUES(%(p)s, %(p)s, %(p)s)',
                id_user, None, None, commit=True)
        execute('DElETE FROM employees WHERE id=%(p)s', id_user, commit=True)
    elif employees:
        execute('UPDATE employees SET full_name=%(p)s, id_company=%(p)s WHERE id=%(p)s',
                None, None, id_user, commit=True)

def check_code_company(id_company):
    sql = execute('SELECT * FROM company_list WHERE id=%(p)s', id_company)
    if sql:
        return sql[0]

    return False


def get_recovery_for_employees(id_user):
    return execute('SELECT * FROM employees e '
            'LEFT JOIN company_list cl ON cl.id=e.id_company '
            'WHERE cl.id_admin=%(p)s AND e.fine > 0', id_user)


def generate_new_id_for_project(id_user, id_project):
    new_id = id_user + random.randint(100, 9999)
    execute('UPDATE company_list SET id=%(p)s WHERE id_admin=%(p)s and id=%(p)s', new_id, id_user, id_project, commit=True)
    return new_id


def get_employees(id_user):
    return execute('SELECT * FROM employees e '
            'LEFT JOIN company_list cl ON cl.id=e.id_company '
            'WHERE cl.id_admin=%(p)s', id_user)



def get_all_user_project(id_user):
    sql = execute('SELECT * FROM company_list WHERE id_admin=%(p)s', id_user)
    if sql:
        return sql
    else:
        return False


def get_company_by_id(id_company):
    return execute('SELECT * FROM company_list WHERE id=%(p)s', id_company)[0]


def get_template_by_project_id(id_project):
    return execute('SELECT * FROM questions_template WHERE id_company=%(p)s', id_project)




def get_days_str_by_project_id(id_project):
    str = ''
    project = get_company_by_id(id_project)
    if project['monday'] == 1:
        str += 'Понедельник '
    if project['tuesday'] == 1:
        str += 'Вторник '
    if project['wednesday'] == 1:
        str += 'Среда '
    if project['thursday'] == 1:
        str += 'Четверг  '
    if project['friday'] == 1:
        str += 'Пятница '
    if project['saturday'] == 1:
        str += 'Суббота '
    if project['saturday'] == 1:
        str += 'Воскресенье '
    return str


def get_count_empl_by_id_company(id_company):
    sql = execute('SELECT COUNT(*) as count_empl FROM employees WHERE id_company=%(p)s', id_company)
    print('##### SQL #####', sql)
    if sql:
        return sql[0]['count_empl']
    else:
        return 0



def time_plus(time, timedelta):
    start = datetime.datetime(
        2000, 1, 1,
        hour=time.hour, minute=time.minute, second=time.second)
    end = start + timedelta
    return end.time()


def time_minus(time, timedelta):
    start = datetime.datetime(
        2000, 1, 1,
        hour=time.hour, minute=time.minute, second=time.second)
    end = start - timedelta
    return end.time()

def get_weekdays():
    return [{'id': 1, 'day': 'Понедельник'},
            {'id': 2, 'day': 'Вторник'},
            {'id': 3, 'day': 'Среда'},
            {'id': 4, 'day': 'Четверг'},
            {'id': 5, 'day': 'Пятница'},
            {'id': 6, 'day': 'Суббота'},
            {'id': 7, 'day': 'Воскресенье'}]



def add_new_company(id_user, name_company):
    if not execute('SELECT id FROM company_list WHERE id_admin=%(p)s AND name_company=%(p)s', id_user, name_company):
        execute('INSERT INTO company_list(id_admin, name_company) VALUES(%(p)s, %(p)s)', id_user, name_company, commit=True)
        return execute('SELECT * FROM company_list WHERE id_admin=%(p)s AND name_company=%(p)s', id_user, name_company)[0]
    else:
        return False


def create_weekdays_for_db():
    return [0, 0, 0, 0, 0, 0, 0]

def update_company(id_project,
                   time_to_send,
                   time_to_answer,
                    weekdays):
    week_list = create_weekdays_for_db()
    for day in weekdays:
        week_list[day['id']-1] = 1
    print("weekdays", week_list)

    execute('UPDATE company_list SET time_to_send=%(p)s, time_to_answer=%(p)s, monday=%(p)s, tuesday=%(p)s, wednesday=%(p)s, thursday=%(p)s, friday=%(p)s, saturday=%(p)s, sunday=%(p)s WHERE id=%(p)s',
            time_to_send, time_to_answer, week_list[0], week_list[1], week_list[2], week_list[3], week_list[4],
            week_list[5], week_list[6], id_project, commit=True)



def update_company_weekdays(id_project, weekdays):
    week_list = create_weekdays_for_db()
    for day in weekdays:
        week_list[day['id']-1] = 1
    print("weekdays", week_list)

    execute('UPDATE company_list SET monday=%(p)s, tuesday=%(p)s, wednesday=%(p)s, thursday=%(p)s, friday=%(p)s, saturday=%(p)s, sunday=%(p)s WHERE id=%(p)s',
            week_list[0], week_list[1], week_list[2], week_list[3], week_list[4],
            week_list[5], week_list[6], id_project, commit=True)


def add_template_text(id_project, text):
    execute('INSERT INTO questions_template(id_company, text) VALUES(%(p)s, %(p)s)', id_project, text, commit=True)


def update_company_time_to_send(time_to_send):
    execute('UPDATE company_list SET time_to_send=%(p)s', time_to_send, commit=True)


def update_company_name(new_name, id_project):
    execute('UPDATE company_list SET name_company=%(p)s WHERE id=%(p)s', new_name, id_project,commit=True)


def get_template_texts(id_project):
    return execute('SELECT * FROM questions_template WHERE id_company=%(p)s', id_project)


def get_template_text_by_id(id_text):
    return execute('SELECT * FROM questions_template WHERE id=%(p)s', id_text)


def delete_text_template(text_id):
    execute('DELETE FROM questions_template WHERE id=%(p)s', text_id, commit=True)


def update_company_time_to_answer(time_to_answer):
    execute('UPDATE company_list SET time_to_answer=%(p)s', time_to_answer, commit=True)


def delete_company(id_company):
    all_empl = execute('SELECT * FROM employees e '
                       'LEFT JOIN company_list cl ON cl.id=e.id_company '
                       'WHERE id_company=%(p)s', id_company)
    res = ''
    execute('UPDATE employees SET id_company=%(p)s, fine=0 WHERE id_company=%(p)s',None, id_company, commit=True)
    execute('DELETE FROM company_list WHERE id=%(p)s', id_company, commit=True)
    for user in all_empl:
        res += str(user['id']) + ','
        try:
            bot.send_message(user['id'], 'Компания {} была удалена.'.format(user['name_company']))
        except Exception as e:
            print(e)

    return res[:-2]


def update_text_template(id_text, new_text):
    execute('UPDATE questions_template SET text=%(p)s WHERE id=%(p)s', id_text, new_text, commit=True)


def add_employees_in_project(id_company, user_list, not_added=None):
    # -
    res = ''
    for data in user_list:
        res += data + ', '
    print('Start sql')
    sql = execute('SELECT id FROM employees WHERE id IN ({})'.format(res[:-2]))
    print('SQL: ', sql)
    res2 = ''
    if sql:
        for data in sql:
            print(data['id'])
            user_list.remove(str(data['id']))
            res2 += str(data['id']) + ', '

        not_added = execute('SELECT id FROM employees WHERE id IN ({}) AND id_company IS NULL'.format(res2[:-2]))

        execute('UPDATE employees SET id_company={} WHERE id IN ({}) AND id_company IS NULL'
                ''.format(id_company, res2[:-2]), commit=True)
    # print(res2)
    print(user_list)
    for data in user_list:
        print(data)
        execute('INSERT INTO employees(id, id_company) VALUES(%(p)s, %(p)s)', int(data), id_company, commit=True)


    # print('NEw user list: ', user_list)
    if not_added:
        return not_added
    else:
        return False


def check_free_trial(id_admin):
    sql = execute('SELECT * FROM admins WHERE id=%(p)s', id_admin)[0]['trial']
    if sql == 0:
        return False
    elif sql == 1:
        return True
    else:
        return False

def start_subscribe(id_admin, days=None):
    execute('INSERT INTO user_subscribe')
# def check_active_employees(id_admin):
#     sql = execute('SELECT * FROM employees e '
#             'LEFT JOIN company_list cl ON cl.id=e.id_company '
#             'WHERE cl.id_admin=%(p)s', id_admin)
#     print(sql)
#     if sql:
#         return True
#     else:
#         return False
