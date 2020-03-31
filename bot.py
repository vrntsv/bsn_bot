#!/home/dmitriy/help_on_road/venv/bin/python
import telebot
from telebot import types
import cherrypy
import telebot_calendar
from telebot_calendar import CallbackData
from telebot.types import ReplyKeyboardRemove, CallbackQuery

import datetime
import graph
import config
import util
import config_markups as conf_mark
import config_text as conf_txt
import inline_conf

WEBHOOK_HOST = '195.69.187.63'
WEBHOOK_PORT = 88  # 443, 80, 88 или 8443 (порт должен быть открыт!)В
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.BOT_TOKEN)

calendar_1 = CallbackData("calendar_1", "action", "year", "month", "day")

bot = telebot.TeleBot(config.BOT_TOKEN)
# message_text_handler(message)
menu_list = ['📊 Отчеты', '💰 Взыскания ', '✍🏻 Управление проектами', '💳 Пополнить баланс',
             '🎁 Получить бонус', '⁉ Задать вопрос', '📊 Мои отчеты', '💰 Мои взыскания']

ADD_TEMPLATE = {}
CHANGE_TEMPLATE = {}

def create_new_template_dict(id_user):
    ADD_TEMPLATE[id_user] = {}
    ADD_TEMPLATE[id_user]['id'] = id_user
    ADD_TEMPLATE[id_user]['weekdays'] = []
    ADD_TEMPLATE[id_user]['status_weekdays'] = []
    ADD_TEMPLATE[id_user]['time'] = []
    ADD_TEMPLATE[id_user]['time_to_answer'] = []
    ADD_TEMPLATE[id_user]['text'] = []
    ADD_TEMPLATE[id_user]['project'] = []
    ADD_TEMPLATE[id_user]['inline_temp'] = []
    ADD_TEMPLATE[id_user]['change_project'] = []

def create_change_template_dict(id_user, project_data):
    CHANGE_TEMPLATE[id_user]['project_data'] = project_data



@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: CallbackQuery):
    """
    Обработка inline callback запросов
    :param call:
    :return:
    """


    # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
    print('11111')
    print(call.data)
    name, action, year, month, day = call.data.split(calendar_1.sep)
    # Processing the calendar. Get either the date or None if the buttons are of a different type
    date = telebot_calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    print(date)
    full_data = util.get_data_for_statistic(ADD_TEMPLATE[call.from_user.id]['project'], selected_day=date)
    if ADD_TEMPLATE[call.from_user.id]['change_project'] == 'liniar':
        graph.line_chart(full_data[1], 'За {}'.format(date.strftime('%d.%m.%Y')), full_data[0], str(call.from_user.id) + 'liniar',
                         ['Статистика по проекту {}'.format(ADD_TEMPLATE[call.from_user.id]['project']), 'Время', 'Доход'])
    elif ADD_TEMPLATE[call.from_user.id]['change_project'] == 'bar':
        graph.bar_chart(full_data[1], 'За {}'.format(date.strftime('%d.%m.%Y')), full_data[0],
                         str(call.from_user.id) + 'liniar',
                         ['Статистика по проекту {}'.format(ADD_TEMPLATE[call.from_user.id]['project']), 'Время',
                          'Доход'])
    # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
    if action == "DAY":
        bot.send_photo(
            chat_id=call.from_user.id,
            photo=str(call.from_user.id) + 'liniar.pnh',
            reply_markup=ReplyKeyboardRemove(),
        )
        print(f"{calendar_1}: Day: {date.strftime('%d.%m.%Y')}")
    elif action == "CANCEL":
        bot.send_message(
            chat_id=call.from_user.id,
            text="Выберите время",
            reply_markup=conf_mark.graph_markup(ADD_TEMPLATE[call.from_user.id]['change_project'],
                                                ADD_TEMPLATE[call.from_user.id]['project']),
        )
        print(f"{calendar_1}: Cancellation")


@bot.message_handler(commands=['start'])
def start(message):
    if util.check_admin_in_db(message.from_user.id):
        bot.send_message(message.from_user.id, conf_txt.restart_txt, parse_mode='HTML', reply_markup=conf_mark.admin())
    elif util.check_employees_in_db(message.from_user.id):
        bot.send_message(message.from_user.id, conf_txt.welcome_txt, parse_mode='HTML', reply_markup=conf_mark.start())
    else:
        print('New user can be add in db: ', message.from_user.id)
        util.add_user_in_db(message.from_user.id)
        bot.send_message(message.from_user.id, conf_txt.welcome_txt, parse_mode='HTML', reply_markup=conf_mark.start())

# @bot.message_handler(commands=['reset'])
# def reset_msg(message):
#     util.execute('DELETE * FROM ')

@bot.message_handler(content_types=['text'])
def message_text_handler(message):
    if message.text == 'РОП Администратор':
        util.change_status(message.from_user.id, admin=True)
        bot.send_message(message.from_user.id, conf_txt.start_admin, reply_markup=conf_mark.admin(), parse_mode='HTML',
                         disable_web_page_preview=True)
    elif message.text == 'Сотрудник':
        msg = bot.send_message(message.from_user.id, 'Укажите код компании или нажмите далее ⤵', parse_mode='HTML',
                               reply_markup=conf_mark.register(), disable_web_page_preview=True)
        bot.register_next_step_handler(msg, register_just_user)
    elif message.text == '📊 Отчеты':
        # выдаем инлайн меню проекты | сотрудники все происходит внутри одного сообщения с инлайн кнопками. старые
        # удаляем, новые присылаем после отправки картинок
        pass
    elif message.text == '💰 Взыскания':
        all_employees = util.get_recovery_for_employees(message.from_user.id)
        if all_employees:
            bot.send_message(message.from_user.id, 'Выберите сотрудника ⤵', parse_mode='HTML',
                             reply_markup=conf_mark.recovery_menu(all_employees))
        else:
            bot.send_message(message.from_user.id, 'У вас еще нет сотрудников. Вы можете их добавить в разделе '
                                                   '"✍🏻 Управление проектами" ', parse_mode='HTML',
                             reply_markup=conf_mark.recovery_menu(all_employees))
        # инлайн кнопки, где выбор сотрудника. потом показывает карточку и моно увеличить долг, уменьшить. удалить
    elif message.text == '✍🏻 Управление проектами':
        # инлайн сообщения с созданием проекта и редактирование/удаление существующих
        bot.send_message(message.from_user.id, 'Выберите проект или создайте новый ⤵', parse_mode='HTML',
                         reply_markup=conf_mark.project_menu(message.from_user.id))
    elif message.text == '💳 Пополнить баланс':
        pass
    elif message.text == '🎁 Получить бонус':
        pass
    elif message.text == '⁉ Задать вопрос':
        pass
    print(message.chat.id, ": ", message.text)


# Регистрация обычного пользователя с кодом компании или без
def register_just_user(message):
    if message.text == '⌛ Указать позже':
        bot.send_message(message.from_user.id, conf_txt.start_employee_no_code, parse_mode='HTML',
                         reply_markup=conf_mark.employee())
    else:
        code_company = message.text
        if not code_company.isdigit():
            msg = bot.send_message(message.from_user.id, 'Укажите код компании цифрами или нажмите далее ⤵',
                                   parse_mode='HTML', reply_markup=conf_mark.register(), disable_web_page_preview=True)
            bot.register_next_step_handler(msg, register_just_user)
        else:
            k = util.check_code_company(code_company)
            if not k:
                msg = bot.send_message(message.from_user.id, 'Компании с указанным кодом не существует. '
                                                             'Проверьте корректность данных и введите их снова ⤵',
                                       parse_mode='HTML',
                                       reply_markup=conf_mark.register())
                bot.register_next_step_handler(msg, register_just_user)
            else:
                # к сообщению прикрепляем инлайн кнопки с двуя действиями ( да / нет) , после да. эдитим текст
                # с сообщением conf_txt.start_employee и присылаем  reply_markup=conf_mark.employee()
                bot.send_message(message.from_user.id, 'Ваша компания {}, верно?'.format(k['name']))


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.recovery_menu_))
def recovery_menu(call):
    to_id_proj_card = None
    if call.data[len(inline_conf.recovery_menu_):] == 'back':
        all_employees = util.get_recovery_for_employees(call.from_user.id)
        bot.edit_message_text('Выберите сотрудника ⤵', call.from_user.id,
                              call.message.message_id, reply_markup=conf_mark.recovery_menu(all_employees))
        return
    elif call.data[len(call.data)-len('_to_user_card_'):] == '_to_user_card_':
        id_employees = call.data[len(inline_conf.recovery_menu_):-len('_to_user_card_')]
        to_id_proj_card = util.get_employees_by_id(id_employees)['id_company']
    else:
        id_employees = call.data[len(inline_conf.recovery_menu_):]
    employees = util.get_employees_by_id(id_employees)
    # ВРЕМЕННО
    print('To id proj card: ', to_id_proj_card)
    history_fine = '📅 17.03.2020 <b>Штраф 50 ₽</b>\n' \
                   '📅 15.03.2020 <b>Штраф 50 ₽</b>\n' \
                   '📅 14.03.2020 <b>Штраф 70 ₽</b>\n' \
                   '📅 11.03.2020 <b>Штраф 1800 ₽</b>\n\n' \
                   'и так максимум до 5 записей'
    txt = 'Карточка: {}\nКомпания: {}\nШтрафы: <b>{} ₽</b>\n\n' \
          '{}'.format(employees['full_name'], employees['name_company'], employees['fine'], history_fine)
    bot.edit_message_text(txt, call.from_user.id, call.message.message_id, parse_mode='HTML',
                          reply_markup=conf_mark.empl_card(id_employees, to_id_proj_card) )


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.project_))
def project_menu(call):
    print('Call data', call.data)
    if call.data[len(inline_conf.project_):] == 'back':
        print('to back')
        bot.edit_message_text('Выберите проект или создайте новый ⤵', call.from_user.id,
                              call.message.message_id, reply_markup=conf_mark.project_menu(call.from_user.id))
        return
    elif call.data[len(inline_conf.project_):] == 'new_project':
        print('Создание нового проекта: ', call.from_user.id)
        msg = bot.edit_message_text('Введите название вашего проекта ⤵', call.from_user.id, call.message.message_id,
                                    parse_mode='HTML')
        bot.register_next_step_handler(msg, create_new_company)
        return
    elif call.data[len(call.data)-len('_conf_delete'):] == '_conf_delete':
        id_company = call.data[len(inline_conf.project_):-len('_conf_delete')]
        print('Confirm delete', id_company)
        util.delete_company(id_company)
        msg = bot.edit_message_text('Проект удален', call.from_user.id, call.message.message_id,
                                    parse_mode='HTML')
        bot.send_message(call.from_user.id, 'Выберите проект или создайте новый ⤵', parse_mode='HTML',
                         reply_markup=conf_mark.project_menu(call.from_user.id))
        return
    elif call.data[len(call.data)-len('delete'):] == 'delete':
        print('Try delelete deal')
        id_company = call.data[len(inline_conf.project_):-len('delete')]
        company = util.get_company_by_id(id_company)
        bot.edit_message_text('Вы действительно хотите удалить проект <code>{}</code>'
                              ''.format(company['name_company'].upper()), call.from_user.id, call.message.message_id,
                                    parse_mode='HTML', reply_markup=conf_mark.confirm_delete(id_company))

        return
    elif call.data[len(call.data)-len('_list_empl_from_proj_'):] == '_list_empl_from_proj_':
        print('EMPL LIST')
        id_company = call.data[len(inline_conf.project_):-len('_list_empl_from_proj_')]
        company = util.get_company_by_id(id_company)
        all_empl = util.get_employees(call.from_user.id)
        print(all_empl)
        bot.edit_message_text('Сотрудники: <code>{}</code>'
                              ''.format(company['name_company']), call.from_user.id, call.message.message_id,
                              parse_mode='HTML', reply_markup=conf_mark.recovery_menu(all_empl, to_proj_card=id_company))
        return
    elif call.data[len(call.data)-len('_fine_proj_'):] == '_fine_proj_':
        # cмотрим историю штрафов
        pass
        return
    elif call.data[len(call.data)-len('_graphics_proj_'):] == '_graphics_proj_':
        # Запускаем фунцию отправки графиков
        pass
        return
    elif call.data[len(call.data)-len('_cancel_delete'):] == '_cancel_delete':
        print('Cancel delete')
        id_company = call.data[len(inline_conf.project_):-len('_cancel_delete')]
    elif call.data[len(call.data)-len('_to_card_proj_'):] == '_to_card_proj_':
        print('To card project')
        id_company = call.data[len(inline_conf.project_):-len('_to_card_proj_')]
    else:
        print('Couse request')
        id_company = call.data[len(inline_conf.project_):]

    project = util.get_company_by_id(id_company)
    print('PROJECT ', project)
    count_employees = util.get_count_empl_by_id_company(id_company)
    txt = '🆔 {}\n\n' \
          'Название: <u>{}</u>' \
          '\n👨‍💼 Cотрудников: <b>{} </b>' \
          '\n💵 за 24 часа: <b>{} ₽</b>' \
          '\n💰 за все время <b>{} ₽</b>' \
          ''.format(project['id'], project['name_company'], count_employees, '2000', '50000')
    bot.edit_message_text(txt, call.from_user.id, call.message.message_id, parse_mode='HTML',
                          reply_markup=conf_mark.project_card(id_company, call.from_user.id))



def confirm_delete(message, company):
    proj_name = str(company['name_company']).upper()
    # print('User: ', message.text, '   name: ', proj_name)
    if message.text == proj_name:
        g = util.delete_company(company['id'])
        print('G: ', g)
        if g:
            bot.send_message(message.from_user.id, 'Компания успешно удалена. Пользователи <code>{}</code> '
                                               'ждут новой работы'.format(g), parse_mode='HTML')
        else:
            bot.send_message(message.from_user.id, 'Компания успешно удалена.', parse_mode='HTML')

        bot.send_message(message.from_user.id, 'Выберите проект или создайте новый ⤵', parse_mode='HTML',
                         reply_markup=conf_mark.project_menu(message.from_user.id))
    else:
        bot.send_message(message.from_user.id, 'Название введено некорректно!', parse_mode='HTML')
        bot.send_message(message.from_user.id, 'Выберите проект или создайте новый ⤵', parse_mode='HTML',
                                          reply_markup=conf_mark.project_menu(message.from_user.id))


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.add_empl_to_project_))
def add_empl_to_project(call):
    id_company = call.data[len(inline_conf.add_empl_to_project_):]
    print('1 id company', id_company)
    # line = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # line.row('Отмена')
    # Правки
    # Добавить кнопку отмены ввода
    msg = bot.edit_message_text('Введите id одного или нескольких пользователей, через запятую напр(111, 222, 333) ⤵',
                          call.from_user.id, call.message.message_id, parse_mode='HTML')

    bot.register_next_step_handler(msg, add_employerr_in_project, id_company)


def add_employerr_in_project(message, id_company):
    print('2 id company', id_company)

    if message.text == 'Отмена':
        bot.edit_message_text('Введите id одного или нескольких пользователей, через запятую напр(111, 222, 333) ⤵',
                              message.from_user.id, message.message.message_id, parse_mode='HTML')
    l = message.text
    user_list = l.split(',')
    not_added = util.add_employees_in_project(id_company, user_list)
    if not_added:
        res = ''
        for j in not_added:
            res += j + ','
        bot.send_message(message.from_user.id, 'Все пользователи кроме {} были подключены к проекту. '.format(res),
                         reply_markup=conf_mark.project_card(id_company, message.from_user.id))
    else:
        bot.send_message(message.from_user.id, 'Пользователи успешно были подключены к проекту.',
                         reply_markup=conf_mark.project_card(id_company, message.from_user.id))


# @bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.recovery_menu_))
# def feedback_univ_menu(call):
#     id_project = call.data[len(inline_conf.project_):]
#     project = util.get_company_by_id(id_project)


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.new_project_))
def project_menu(call):
    pass


def create_new_company(message):
    if message.text == 'Отменить':
        bot.send_message(message.from_user.id, 'Отмена действия: "Создание проекта"', parse_mode='HTML',
                         reply_markup=conf_mark.project_menu(message.from_user.id))
        return
    print('Название проекта: ', message.text, '\nАдмин: ', message.from_user.id)
    company = util.add_new_company(message.from_user.id, message.text)
    if not company:
        print('Не уникальное имя компании')
        msg = bot.send_message(message.from_user.id, 'У вас уже есть проект с такими именем, '
                                         'введите уникальное название для вашего проекта ⤵', parse_mode='HTML')
        bot.register_next_step_handler(msg, create_new_company)
        return
    create_new_template_dict(message.from_user.id)
    ADD_TEMPLATE[message.from_user.id]['project'] = company['id']
    custom_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    inline_key = telebot.types.InlineKeyboardMarkup()
    for day in util.get_weekdays():
        ADD_TEMPLATE[message.from_user.id]['status_weekdays'].append({'id': day['id'],
                                                                       'day': day['day'],
                                                                       'status': False})
        inline_btn = telebot.types.InlineKeyboardButton(text=day['day'],
                                                        callback_data=inline_conf.day + str(day['id']))
        inline_key.add(inline_btn)
    bot.send_message(message.from_user.id, 'Выберите дни недели для рассылки', parse_mode='HTML', reply_markup=inline_key)
    custom_key.row('Готово ✅')
    bot.send_message(message.from_user.id, 'После выбора нужных пунктов нажмите на кнопку <b>Готово ✅</b>.',
                     parse_mode='HTML', reply_markup=custom_key)
    bot.register_next_step_handler(message, add_template_choose_time)
    # print('Project created')
    # bot.send_message(message.from_user.id, 'Проект: "{}" успешно создан.'.format(message.text), parse_mode='HTML')
    # txt = 'Название: <u>{}</u>\nCотрудников: <b>0 </b>\nДоход за 24 часа: <b>{} ₽</b>\nДоход за все время <b>{} ₽</b>' \
    #       ''.format(company['name_company'], '0', '2000', '50000')
    #
    # bot.send_message(message.from_user.id, txt, parse_mode='HTML',
    #                  reply_markup=conf_mark.project_card(company['id'], message.from_user.id))


def add_template_choose_day(message):
    ADD_TEMPLATE[message.from_user.id]['text'] = message.text


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.day))
def action_callback(call):
    bot.answer_callback_query(call.id)
    inline_key = telebot.types.InlineKeyboardMarkup()
    day_id_in_message = int(call.data[len(inline_conf.day):])
    for wd_user in ADD_TEMPLATE[call.from_user.id]['status_weekdays']:
        if wd_user['id'] == day_id_in_message:
            wd_user['status'] = not wd_user['status']
            if wd_user['status']:
                ADD_TEMPLATE[call.from_user.id]['weekdays'].append({'id': wd_user['id'],
                                                                     'day': wd_user['day']})
            else:
                ADD_TEMPLATE[call.from_user.id]['weekdays'].remove({'id': wd_user['id'],
                                                                     'day': wd_user['day']})
        # Редактирование поля status_work_type
        if wd_user['status']:
            text_btn = '✅' + wd_user['day']
        else:
            text_btn = wd_user['day']
        inline_btn = telebot.types.InlineKeyboardButton(text=text_btn,
                                                        callback_data=inline_conf.day + str(wd_user['id']))
        inline_key.add(inline_btn)

    bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                  reply_markup=inline_key)
    bot.clear_step_handler(call.message)
    bot.register_next_step_handler(call.message, add_template_choose_time)

def add_template_choose_time(message):
    if message.text == 'Готово ✅' or message.text == 'Понятно👌':
        if not ADD_TEMPLATE[message.from_user.id]['weekdays']:
            bot.send_message(message.from_user.id, 'Выберите хотя бы один день!')
            bot.register_next_step_handler(message, add_template_choose_time)
        else:
            bot.delete_message(message.from_user.id, message.message_id-1)
            bot.delete_message(message.from_user.id, message.message_id-2)
            if ADD_TEMPLATE[message.from_user.id]['change_project'] == 'days':
                util.update_company_weekdays(ADD_TEMPLATE[message.from_user.id]['project'],
                                             ADD_TEMPLATE[message.from_user.id]['weekdays'])
                inline_key = types.InlineKeyboardMarkup()
                return_to_project = types.InlineKeyboardButton('Вернуться к проекту',
                                                               callback_data=inline_conf.project_ + str(
                                                                   ADD_TEMPLATE[message.from_user.id]['project']))
                inline_key.add(return_to_project)
                bot.send_message(message.from_user.id, 'Дни рассылки были изменены', reply_markup=inline_key)
                return
            ADD_TEMPLATE[message.from_user.id]['time'] = datetime.time(hour=12, minute=0)

            bot.send_message(message.from_user.id, 'Выберите время для рассылки',
                             reply_markup=conf_mark.clock_inline(
                                 hour=datetime.time.strftime(ADD_TEMPLATE[message.from_user.id]['time'],'%H'),
                                 minute=datetime.time.strftime(ADD_TEMPLATE[message.from_user.id]['time'],'%M')))
            custom_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            custom_key.add('Готово ✅')
            bot.send_message(message.from_user.id, 'Нажмите кнопку "Готово"', reply_markup=custom_key)
            bot.register_next_step_handler(message, add_tempalate_choose_emp)
    else:
        custom_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        custom_key.row('Готово ✅')
        bot.send_message(message.from_user.id, 'Нажмите кнопку "Готово"', reply_markup=custom_key)
        bot.register_next_step_handler(message, add_template_choose_time)



@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_change_name))
def template_change_name(call):
    bot.delete_message(call.from_user.id, call.message.message_id)
    msg = bot.send_message(call.from_user.id, 'Введите новое название проекта')
    bot.register_next_step_handler(msg, template_change_name_done)


def template_change_name_done(message):
    util.update_company_name(message.text, ADD_TEMPLATE[message.from_user.id]['project'])
    inline_key = types.InlineKeyboardMarkup()
    return_to_project = types.InlineKeyboardButton('Вернуться к проекту',
                                                   callback_data=inline_conf.project_ + str(
                                                       ADD_TEMPLATE[message.from_user.id]['project']))
    inline_key.add(return_to_project)
    bot.send_message(message.from_user.id, 'Название проекта было изменено', reply_markup=inline_key)
    return


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_text_change))
def change_text(call):
    create_new_template_dict(call.from_user.id)
    text_id = call.data[inline_conf.template_text_change.__len__():]
    ADD_TEMPLATE[call.from_user.id]['text'] = text_id
    bot.delete_message(call.from_user.id, call.message.message_id)
    msg = bot.send_message(call.from_user.id, 'Введите новый текст для шаблон #' + text_id )
    bot.register_next_step_handler(msg, change_text_done)


def change_text_done(message):
    util.update_text_template(ADD_TEMPLATE[message.from_user.id]['text'], message.text)
    text = message.text
    bot.delete_message(message.from_user.id, message.message_id)
    bot.send_message(message.from_user.id, '# '+ str(ADD_TEMPLATE[message.from_user.id]['text']) +' ' + text,
                                  reply_markup=conf_mark.get_text_markup(ADD_TEMPLATE[message.from_user.id]['text']))


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_text_delete))
def delete_text(call):
    create_new_template_dict(call.from_user.id)
    text_id = call.data[inline_conf.template_text_delete.__len__():]
    print('tewtwetwe', text_id)
    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, 'Вы действительно хотите удалить шаблон #'+str(text_id),
                     reply_markup=conf_mark.delete_text_confirm_markup(text_id))


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_text_delete_no))
def delete_text_cancel(call):
    text_id = call.data[inline_conf.template_text_delete_no.__len__():]
    text_data = util.get_template_text_by_id(text_id)
    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, '# '+ str(text_data['id']) +' ' + text_data['text'],
                                  reply_markup=conf_mark.get_text_markup(text_data['id']))


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_text_delete_yes))
def delete_text_confirm(call):
    print(call.data)
    text_id = call.data[inline_conf.template_text_delete_yes.__len__():]
    print(text_id)
    text_data = util.get_template_text_by_id(text_id)
    print(text_data)
    util.delete_text_template(text_id)
    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, 'Шаблон #' + str(text_data[0]['id']) + ' был удален')


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_texts))
def template_texts(call):
    id_project = call.data[inline_conf.template_texts.__len__():]
    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, 'Настройки шаблонов', reply_markup=conf_mark.template_texts_settings(id_project))


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_texts_get))
def tempalate_texts_get(call):
    bot.delete_message(call.from_user.id, call.message.message_id)
    id_project = call.data[inline_conf.template_texts_get.__len__():]
    texts = util.get_template_texts(id_project)
    print('text', texts)
    if texts.__len__() > 0:
        for text in texts:
            bot.send_message(call.from_user.id, '#' + str(text['id']) + '  '+text['text'], reply_markup=conf_mark.get_text_markup(text['id']))
    else:
        bot.send_message(call.from_user.id, 'У вас нет шаблонов', reply_markup=conf_mark.add_text_markup(id_project))


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.graph_liniar_choose_day))
def choose_day_liniar(call):
    print('graph_liniar_choose_day')
    create_new_template_dict(call.from_user.id)
    bot.delete_message(call.from_user.id, call.message.message_id)
    id_project = call.data[inline_conf.graph_liniar_choose_day.__len__():]
    ADD_TEMPLATE[call.from_user.id]['project'] = id_project
    ADD_TEMPLATE[call.from_user.id]['change_project'] = 'liniar'

    now = datetime.datetime.now()  # Get the current date
    bot.send_message(
        call.from_user.id,
        "Выберите дату",
        reply_markup=telebot_calendar.create_calendar(
            name=calendar_1.prefix,
            year=now.year,
            month=now.month,  # Specify the NAME of your calendar
        ),
    )



@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.graph_liniar_menu))
def graph_liniar_menu(call):
    pass


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.graph_liniar))
def graph_liniar_call(call):
    data = call.data[inline_conf.graph_liniar.__len__():].split('.')
    bot.delete_message(call.from_user.id, call.message.message_id)

    if data.__len__() > 1:
        if data[1] == 'today':
            print('today')
            full_data = util.get_data_for_statistic(data[0], today=True)
            graph.line_chart(full_data[1], 'За сегодня', full_data[0], str(call.from_user.id)+'liniar', ['Статистика по проекту {}'.format(data[0]), 'Время', 'Доход'])
        elif data[1] == 'week':
            full_data = util.get_data_for_statistic(data[0], this_week=True)
            graph.line_chart(full_data[1], 'За неделю', full_data[0], str(call.from_user.id)+'liniar', ['Статистика по проекту {}'.format(data[0]), 'Время', 'Доход'])
        elif data[1] == 'month':
            full_data = util.get_data_for_statistic(data[0], this_month=True)
            graph.line_chart(full_data[1], 'За последний месяц', full_data[0], str(call.from_user.id)+'liniar', ['Статистика по проекту {}'.format(data[0]), 'Время', 'Доход'])
        elif data[1] == 'all':
            full_data = util.get_data_for_statistic(data[0])
            graph.line_chart(full_data[1], 'За всё время', full_data[0], str(call.from_user.id)+'liniar', ['Статистика по проекту {}'.format(data[0]), 'Время', 'Доход'])
        bot.send_photo(call.from_user.id,  str(call.from_user.id)+'liniar.png', reply_markup=conf_mark.graph_back_markup(data[0], str(call.from_user.id)+'liniar.png'))
        return
    else:

        bot.send_message(call.from_user.id, 'Выберите тип графика', reply_markup=conf_mark.graph_markup(inline_conf.graph_liniar, data[0]))
        return


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.graph_bar))
def graph_bar_call(call):
    data = call.data[inline_conf.graph_bar.__len__():].split('.')
    bot.delete_message(call.from_user.id, call.message.message_id)

    if data.__len__() > 1:
        print('trur')
        if data[1] == 'today':
            print(data[0], ' fafaf')
            full_data = util.get_data_for_statistic(data[0], today=True)
            print(full_data)
            graph.bar_chart(full_data[1], [1], full_data[0], str(call.from_user.id)+'bar', ['Статистика по проекту {}'.format(data[0]), 'Время', 'Доход'])
        elif data[1] == 'week':
            full_data = util.get_data_for_statistic(data[0], this_week=True)
            graph.bar_chart(full_data[1], 'За неделю', full_data[0], str(call.from_user.id)+'bar', ['Статистика по проекту {}'.format(data[0]), 'Время', 'Доход'])
        elif data[1] == 'month':
            full_data = util.get_data_for_statistic(data[0], this_month=True)
            graph.bar_chart(full_data[1], 'За последний месяц', full_data[0], str(call.from_user.id)+'bar', ['Статистика по проекту {}'.format(data[0]), 'Время', 'Доход'])
        elif data[1] == 'all':
            full_data = util.get_data_for_statistic(data[0])
            graph.bar_chart(full_data[1], 'За всё время', full_data[0], str(call.from_user.id)+'bar', ['Статистика по проекту {}'.format(data[0]), 'Время', 'Доход'])
        bot.send_photo(call.from_user.id,  str(call.from_user.id)+'bar.png', reply_markup=conf_mark.graph_back_markup(data[0], str(call.from_user.id)+'bar.png'))
        return
    else:

        bot.send_message(call.from_user.id, 'Выберите тип графика', reply_markup=conf_mark.graph_markup(inline_conf.graph_bar, data[0]))
        return


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_text_add))
def templates_text_add(call):
    create_new_template_dict(call.from_user.id)
    print('callsdlag', call.data)
    ADD_TEMPLATE[call.from_user.id]['project'] = call.data[inline_conf.template_text_add.__len__():]
    bot.delete_message(call.from_user.id, call.message.message_id)
    msg = bot.send_message(call.from_user.id, 'Введите текст шаблона')
    bot.register_next_step_handler(msg, templates_text_add_confirm)


def templates_text_add_confirm(message):
    id_project = ADD_TEMPLATE[message.from_user.id]['project']
    print(id_project)
    util.add_template_text(id_project, message.text)
    bot.send_message(message.from_user.id, 'Добавлен новый шаблон!', reply_markup=conf_mark.template_texts_settings(id_project))



@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.change_time))
def change_time(call):
    if call.data == inline_conf.change_time_minus_minute:
        ADD_TEMPLATE[call.from_user.id]['time'] = util.time_minus(ADD_TEMPLATE[call.from_user.id]['time'], datetime.timedelta(minutes=5))
    elif call.data == inline_conf.change_time_minus_hour:
        ADD_TEMPLATE[call.from_user.id]['time'] = util.time_minus(ADD_TEMPLATE[call.from_user.id]['time'], datetime.timedelta(hours=1))
    elif call.data == inline_conf.change_time_plus_minute:
        ADD_TEMPLATE[call.from_user.id]['time'] = util.time_plus(ADD_TEMPLATE[call.from_user.id]['time'], datetime.timedelta(minutes=5))
    elif call.data == inline_conf.change_time_plus_hour:
        ADD_TEMPLATE[call.from_user.id]['time'] = util.time_plus(ADD_TEMPLATE[call.from_user.id]['time'], datetime.timedelta(hours=1))
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id,
                     reply_markup=conf_mark.clock_inline(
                         hour=datetime.time.strftime(ADD_TEMPLATE[call.from_user.id]['time'], '%H'),
                         minute=datetime.time.strftime(ADD_TEMPLATE[call.from_user.id]['time'], '%M')))
    # custom_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    # custom_key.row('Готово ✅')
    # msg = bot.send_message(call.from_user.id, 'Нажмите кнопку "Готово"', reply_markup=custom_key)
    # bot.register_next_step_handler(msg, add_tempalate_choose_emp)


def add_tempalate_choose_emp(message):
    bot.delete_message(message.from_user.id, message.message_id-2)
    bot.delete_message(message.from_user.id, message.message_id-1)
    bot.delete_message(message.from_user.id, message.message_id)
    if ADD_TEMPLATE[message.from_user.id]['change_project'] == 'time':
        util.update_company_time_to_send(ADD_TEMPLATE[message.from_user.id]['time'])
        inline_key = types.InlineKeyboardMarkup()
        return_to_project = types.InlineKeyboardButton('Вернуться к проекту',
                                callback_data=inline_conf.project_+ str(ADD_TEMPLATE[message.from_user.id]['project']))
        inline_key.add(return_to_project)
        bot.send_message(message.from_user.id, 'Время отправки было изменено', reply_markup=inline_key)
        return
    inline_key = telebot.types.InlineKeyboardMarkup()
    bot.send_message(message.from_user.id, 'Выберите время для ответа', reply_markup=conf_mark.time_to_answer_inline())


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_change_id))
def change_id(call):
    bot.delete_message(call.from_user.id, call.message.message_id)
    id_project = call.data[inline_conf.template_change_id.__len__():]
    new_id = util.generate_new_id_for_project(call.from_user.id, id_project)
    inline_key = types.InlineKeyboardMarkup()

    back_btn = types.InlineKeyboardButton(text='🔙 К карточке проекта',
                                          callback_data=inline_conf.project_ + str(new_id))
    inline_key.add(back_btn)
    bot.send_message(call.from_user.id, 'ID вашего проекта изменен на {}'.format(new_id), reply_markup=inline_key)


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.add_template_answer_time))
def add_template_conf(call):

    print(util.get_company_by_id(ADD_TEMPLATE[call.from_user.id]['project']))
    bot.delete_message(call.from_user.id, call.message.message_id)

    if ADD_TEMPLATE[call.from_user.id]['change_project'] == 'answer_time':
        print('time_to_answer')
        ADD_TEMPLATE[call.from_user.id]['time_to_answer'] = call.data[inline_conf.add_template_answer_time.__len__():]
        ADD_TEMPLATE[call.from_user.id]['time_to_answer'] = \
        util.get_company_by_id(ADD_TEMPLATE[call.from_user.id]['project'])['time_to_send'] + \
        datetime.timedelta(hours=int(call.data[inline_conf.add_template_answer_time.__len__():]))
        print('time_to_answer', ADD_TEMPLATE)
        util.update_company_time_to_answer(ADD_TEMPLATE[call.from_user.id]['time_to_answer'])
        inline_key = types.InlineKeyboardMarkup()
        return_to_project = types.InlineKeyboardButton('Вернуться к проекту',
                                callback_data=inline_conf.project_+ str(ADD_TEMPLATE[call.from_user.id]['project']))
        inline_key.add(return_to_project)
        bot.send_message(call.from_user.id, 'Время для ответа было изменено', reply_markup=inline_key)
        return
    print(ADD_TEMPLATE[call.from_user.id])
    print('Project created')
    ADD_TEMPLATE[call.from_user.id]['time_to_answer'] = call.data[inline_conf.add_template_answer_time.__len__():]
    util.update_company(ADD_TEMPLATE[call.from_user.id]['project'], ADD_TEMPLATE[call.from_user.id]['time'],
                        ADD_TEMPLATE[call.from_user.id]['time_to_answer'], ADD_TEMPLATE[call.from_user.id]['weekdays'])
    company = util.get_company_by_id(ADD_TEMPLATE[call.from_user.id]['project'])
    bot.send_message(call.from_user.id, 'Проект: "{}" успешно создан.'.format(company['name_company']), parse_mode='HTML')
    txt = '🆔 {}\n\nНазвание: <u>{}</u>\nCотрудников: <b>0 </b>\nДоход за 24 часа: <b>{} ₽</b>\nДоход за все время <b>{} ₽</b>' \
          ''.format(company['id'], company['name_company'], '0', '2000', '50000')

    bot.send_message(call.from_user.id, txt, parse_mode='HTML',
                     reply_markup=conf_mark.project_card(company['id'], call.from_user.id))




@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_menu))
def template_menu(call):
    id_project = call.data[inline_conf.template_menu.__len__():]
    bot.delete_message(call.from_user.id, call.message.message_id)

    project = util.get_company_by_id(id_project)
    print(project)
    create_new_template_dict(call.from_user.id)

    ADD_TEMPLATE[call.from_user.id]['project'] = id_project
    text = conf_txt.template_state.format(project['name_company'],
                                          str(project['time_to_send']),
                                          util.get_days_str_by_project_id(id_project),
                                          str(project['time_to_answer']))
    bot.send_message(call.from_user.id, text, reply_markup=conf_mark.template_settings(id_project), parse_mode='html')


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_change_answer_time))
def template_change_answer_time(call):
    bot.delete_message(call.from_user.id, call.message.message_id)
    ADD_TEMPLATE[call.from_user.id]['change_project'] = 'answer_time'
    inline_key = telebot.types.InlineKeyboardMarkup()
    bot.send_message(call.from_user.id, 'Выберите время для ответа', reply_markup=conf_mark.time_to_answer_inline())


@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_change_day))
def template_change_day(call):
    ADD_TEMPLATE[call.from_user.id]['project'] = call.data[inline_conf.template_change_day.__len__():]
    ADD_TEMPLATE[call.from_user.id]['change_project'] = 'days'
    custom_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    inline_key = telebot.types.InlineKeyboardMarkup()
    for day in util.get_weekdays():
        ADD_TEMPLATE[call.from_user.id]['status_weekdays'].append({'id': day['id'],
                                                                      'day': day['day'],
                                                                      'status': False})
        inline_btn = telebot.types.InlineKeyboardButton(text=day['day'],
                                                        callback_data=inline_conf.day + str(day['id']))
        inline_key.add(inline_btn)
    bot.send_message(call.from_user.id, 'Выберите дни недели для рассылки', parse_mode='HTML',
                     reply_markup=inline_key)
    custom_key.row('Готово ✅')
    msg = bot.send_message(call.from_user.id, 'После выбора нужных пунктов нажмите на кнопку <b>Готово ✅</b>.',
                     parse_mode='HTML', reply_markup=custom_key)
    bot.register_next_step_handler(msg, add_template_choose_time)

@bot.callback_query_handler(func=lambda call: call.data.startswith(inline_conf.template_change_time))
def template_change_time(call):
    print('fsfsfsfsf')
    bot.delete_message(call.from_user.id, call.message.message_id)
    create_new_template_dict(call.from_user.id)
    ADD_TEMPLATE[call.from_user.id]['time'] = datetime.time(hour=12, minute=0)
    ADD_TEMPLATE[call.from_user.id]['change_project'] = 'time'
    ADD_TEMPLATE[call.from_user.id]['project'] = call.data[inline_conf.template_change_time.__len__():]
    bot.send_message(call.from_user.id, 'Выберите время для рассылки',
                     reply_markup=conf_mark.clock_inline(
                         hour=datetime.time.strftime(ADD_TEMPLATE[call.from_user.id]['time'], '%H'),
                         minute=datetime.time.strftime(ADD_TEMPLATE[call.from_user.id]['time'], '%M')))
    custom_key = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    custom_key.add('Готово ✅')
    msg = bot.send_message(call.from_user.id, 'Нажмите кнопку "Готово"', reply_markup=custom_key)
    bot.register_next_step_handler(msg, add_tempalate_choose_emp)

def tempalate_change_time_confirm(message):
    pass

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                'content-type' in cherrypy.request.headers and \
                cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling()

    # bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
    #           certificate=open(WEBHOOK_SSL_CERT, 'r'))
    # cherrypy.config.update({
    # 'server.socket_host': WEBHOOK_LISTEN,
    #   'server.socket_port': WEBHOOK_PORT,
    #   'server.ssl_module': 'builtin',
    #   'server.ssl_certificate': WEBHOOK_SSL_CERT,
    #   'server.ssl_private_key': WEBHOOK_SSL_PRIV
    # })
    # # Собственно, запуск!
    # cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
