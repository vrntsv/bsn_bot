# Тексты внутриб ота
# ⤵
import util

welcome_txt = 'Добро пожаловать. Выберите тип аккаунта ⤵'

restart_txt = 'Вы вернулись в главное меню'

start_admin = 'Вы успешно зарегистрировались в системе, как руководитель. Пробный период на 7 дней был активирован.\n' \
              '<a  href="https://www.artlebedev.ru/dj/">Рекомендуем Вам ознакомиться с возможностями бота. </a> '

start_employee = '<a href="https://www.artlebedev.ru/dj/">Рекомендуем Вам ознакомиться с возможностями бота. </a>'

start_employee_no_code = 'Добро пожаловать, вы зарегистрировались без подключения к компании.' \
                         '\nУточните код компании или передайте свой, старшему руководителю.\n' \
                         '<a href="https://www.artlebedev.ru/dj/">Рекомендуем Вам ознакомиться с возможностями бота. </a>'

template_state = '<u>Текущие настройки проекта</u>\n\n🆔 {}\n<code>{}</code>\n\n' \
                 '<b>Время отправки:</b>\n<i>{}</i>\n\nДни отправки: <i>{}</i>\n\nВремя для ответа : <i>{}</i>'


def create_text_company(id_company, id_admin):
    company = util.get_company_by_id(id_company)
    count_employees = util.get_count_empl_by_id_company(id_company)
    project_card_text = '🆔 {}\n' \
                        'Название: <u>{}</u>' \
                        '\nРазмер штрафа: <b>{} </b>' \
                        '\n👨‍💼 Cотрудников: <b>{} </b>' \
                        ''.format(company['id'], company['fine'], company['name_company'],
                                  count_employees, 'http://t.me/testlyorderbot?start=' + str(company['id']))
    return project_card_text


# Текст приглашение
add_empl = 'http://t.me/benice_tools_bot?start='


def create_text_template(name, question):
    txt = 'Название: {}\nВопрос: {}'.format(name, question)

    return txt