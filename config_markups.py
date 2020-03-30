from telebot import types
import inline_conf

import util


def start():
    line = types.ReplyKeyboardMarkup(resize_keyboard=True)
    line.row('РОП Администратор', 'Сотрудник')

    return line


def admin():
    line = types.ReplyKeyboardMarkup(resize_keyboard=True)

    line.row('📊 Отчеты', '💰 Взыскания ')
    line.row('✍🏻 Управление проектами', '💳 Пополнить баланс')
    line.row('🎁 Получить бонус', '⁉ Задать вопрос')

    return line


def employee():
    line = types.ReplyKeyboardMarkup(resize_keyboard=True)
    line.row('📊 Мои отчеты', '💰 Мои взыскания')

    return line


def register():
    line = types.ReplyKeyboardMarkup(resize_keyboard=True)
    line.row('⌛ Указать позже')

    return line



def clock_inline(hour, minute):
    inline_key = types.InlineKeyboardMarkup()
    minus_hour = types.InlineKeyboardButton('-', callback_data=inline_conf.change_time_minus_hour)
    plus_hour = types.InlineKeyboardButton('+', callback_data=inline_conf.change_time_plus_hour)
    hour = types.InlineKeyboardButton(hour, callback_data=inline_conf.change_time_minus_hour)
    _break = types.InlineKeyboardButton(':', callback_data='none')
    minute = types.InlineKeyboardButton(minute, callback_data=inline_conf.change_time_minus_hour)
    plus_minute = types.InlineKeyboardButton('+', callback_data=inline_conf.change_time_plus_minute)
    minus_minute = types.InlineKeyboardButton('-', callback_data=inline_conf.change_time_minus_minute)
    inline_key.row(minus_hour, hour, plus_hour)
    inline_key.row(_break)
    inline_key.row(minus_minute, minute, plus_minute)
    return inline_key


def time_to_answer_inline():
    inline_key = types.InlineKeyboardMarkup()
    for i in range(1, 8):
        hour = types.InlineKeyboardButton(str(i), callback_data=inline_conf.add_template_answer_time+str(i))
        inline_key.add(hour)
    return inline_key


def recovery_menu(user_list, to_proj_card=None):
    inline_key = types.InlineKeyboardMarkup()
    for user in user_list:
        if to_proj_card:
            inline_btn = types.InlineKeyboardButton(text=user['full_name'] + '( {} ₽ )'.format(user['fine']),
                                                    callback_data=inline_conf.recovery_menu_ + str(user['id']) +
                                                    '_to_user_card_')
        else:
            inline_btn = types.InlineKeyboardButton(text=user['name_company'] + ' — ' + user['full_name'] +
                                                     '( {} ₽ )'.format(user['fine']),
                                                callback_data=inline_conf.recovery_menu_ + str(user['id']))
        inline_key.add(inline_btn)

    if to_proj_card:
        add_recover = types.InlineKeyboardButton('✅ Добавить сотрудника',
                                                 callback_data=inline_conf.add_empl_to_project_ + str(to_proj_card))
        inline_key.add(add_recover)
        back_btn = types.InlineKeyboardButton(text='🔙 К карточке проекта',
                                              callback_data=inline_conf.project_ + str(to_proj_card))
        inline_key.add(back_btn)
    # back_btn = types.InlineKeyboardButton(text='🔙 К списку сотрудников', callback_data=inline_conf.facult + 'back')
    # inline_key.add(back_btn)

    return inline_key


def empl_card(id_user, to_id_proj_card=None):
    inline_kb_full = types.InlineKeyboardMarkup(row_width=2)

    # inline_kb_full.add(types.InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
    add_recover = types.InlineKeyboardButton('➕ штраф', callback_data=inline_conf.recovery_menu_ + str(id_user))
    off_recover = types.InlineKeyboardButton('➖ штраф', callback_data=inline_conf.recovery_menu_ + str(id_user))
    see_recover = types.InlineKeyboardButton('🧾 История штрафов',
                                             callback_data=inline_conf.recovery_menu_ + str(id_user))
    inline_kb_full.row(add_recover, off_recover, see_recover)
    if to_id_proj_card:
        back_btn = types.InlineKeyboardButton(text='🔙 К списку сотрудников',
                                              callback_data=inline_conf.project_ + str(to_id_proj_card)
                                                            + '_list_empl_from_proj_')
        inline_kb_full.add(back_btn)
    elif not to_id_proj_card:
        back_btn = types.InlineKeyboardButton(text='🔙 К списку сотрудников',
                                              callback_data=inline_conf.recovery_menu_ + 'back')
        inline_kb_full.add(back_btn)

    return inline_kb_full


def project_menu(id_user):
    all_project = util.get_all_user_project(id_user)
    inline_key = types.InlineKeyboardMarkup()
    if all_project:
        # print('All project: ', all_project)
        for project in all_project:
            # print('Project ', project)
            inline_btn = types.InlineKeyboardButton(text=str(project['name_company']),
                                                    callback_data=inline_conf.project_ + str(project['id']))
            inline_key.add(inline_btn)

    new_proj = types.InlineKeyboardButton(text='🆕 Cоздать новый проект 🆕',
                                          callback_data=inline_conf.project_ + 'new_project')
    inline_key.add(new_proj)

    instr = types.InlineKeyboardButton(text='📖 Инструкция', callback_data='new_project')
    inline_key.add(instr)

    return inline_key


def empl_from_proj(id_project, all_empl):
    inline_key = types.InlineKeyboardMarkup()
    for user in all_empl:
        inline_btn = types.InlineKeyboardButton(text=user['full_name'] + '( {} ₽ )'.format(user['fine']),
                                                callback_data=inline_conf.empl_card_ + str(
                                                    user['id']) + '_to_user_card_')
        inline_key.add(inline_btn)


    back_btn = types.InlineKeyboardButton(text='🔙 В карточку компании',
                                          callback_data=inline_conf.project_ + str(id_project) + '_to_card_proj_')
    inline_key.add(back_btn)

    return inline_key


def project_card(id_project, id_admin):
    inline_kb_full = types.InlineKeyboardMarkup(row_width=2)

    off_recover = types.InlineKeyboardButton('🔁 Cотрудники',
                                             callback_data=inline_conf.project_ + str(id_project)
                                                           + '_list_empl_from_proj_')
    template = types.InlineKeyboardButton('📝 Шаблоны', callback_data=inline_conf.template_texts + str(id_project))
    project_settings = types.InlineKeyboardButton('⚙️ Настройка проекта',
                                                   callback_data=inline_conf.template_menu + str(id_project))
    statistics = types.InlineKeyboardButton('📈 Графики 1 ',
                                            callback_data=inline_conf.project_ + str(id_project) + '_graphics_proj_')
    statistics_two = types.InlineKeyboardButton('📊 Графики 2 ',
                                            callback_data=inline_conf.project_ + str(id_project) + '_graphics_proj_')
    empl_fine = types.InlineKeyboardButton('🔏 Штрафы',
                                           callback_data=inline_conf.project_ + str(id_project) + '_fine_proj_')

    # see_recover = types.InlineKeyboardButton(
    #     'Тут можем добавить все кнопки для получения статистики, графиков и прочего',
    #     callback_data=inline_conf.recovery_menu_ + str(id_project))
    inline_kb_full.row(off_recover)
    inline_kb_full.add(statistics, statistics_two)
    inline_kb_full.add(empl_fine)
    inline_kb_full.add(template)
    inline_kb_full.add(project_settings)

    back_btn = types.InlineKeyboardButton(text='🔙 Назад к списку проектов',
                                          callback_data=inline_conf.project_ + 'back')
    inline_kb_full.add(back_btn)

    return inline_kb_full


def delete_text_confirm_markup(id_text):
    inline_kb_full = types.InlineKeyboardMarkup(row_width=2)
    yes_btn = types.InlineKeyboardButton(text='✅ Да',
                                          callback_data=inline_conf.template_text_delete_yes + str(id_text) )
    no_btn = types.InlineKeyboardButton(text='❌ Нет',
                                          callback_data=inline_conf.template_text_delete_no + str(id_text) )
    inline_kb_full.row(yes_btn, no_btn)
    return inline_kb_full


def get_text_markup(id_text):
    inline_kb_full = types.InlineKeyboardMarkup(row_width=2)
    delete_btn = types.InlineKeyboardButton(text='❌ Удалить шаблон',
                                          callback_data=inline_conf.template_text_delete + str(id_text) )
    change_btn = types.InlineKeyboardButton(text='✏️ Изменить шаблон',
                                          callback_data=inline_conf.template_text_change + str(id_text) )
    inline_kb_full.row(change_btn)
    inline_kb_full.row(delete_btn)
    return inline_kb_full


def add_text_markup(id_project):
    inline_kb_full = types.InlineKeyboardMarkup(row_width=2)
    add_btn = types.InlineKeyboardButton(text='➕ Добавить шаблон',
                                          callback_data=inline_conf.template_text_add + str(id_project))
    inline_kb_full.add(add_btn)
    return inline_kb_full

def template_settings(id_project):
    inline_kb_full = types.InlineKeyboardMarkup(row_width=2)
    change_text = types.InlineKeyboardButton(text='Изменить название проекта',
                                          callback_data=inline_conf.template_change_name + str(id_project) )
    change_time = types.InlineKeyboardButton(text='Изменить время отправки',
                                          callback_data=inline_conf.template_change_time + str(id_project))
    change_answer_time = types.InlineKeyboardButton(text='Изменить время ответа',
                                          callback_data=inline_conf.template_change_answer_time + str(id_project))
    change_days = types.InlineKeyboardButton(text='Изменить дни отправки',
                                          callback_data=inline_conf.template_change_day + str(id_project))

    change_id = types.InlineKeyboardButton(text='Изменить ID проекта',
                                          callback_data=inline_conf.template_change_id+ str(id_project))
    del_btn = types.InlineKeyboardButton(text='❌ Удалить проект',
                                          callback_data=inline_conf.project_ + str(id_project) + 'delete')
    back_btn = types.InlineKeyboardButton(text='🔙 Назад',
                                          callback_data=inline_conf.project_ + str(id_project))
    inline_kb_full.row(change_text, change_answer_time)
    inline_kb_full.row(change_time, change_days)
    inline_kb_full.row(change_id)
    inline_kb_full.add(del_btn)
    inline_kb_full.add(back_btn)

    return inline_kb_full


def template_texts_settings(id_project):
    inline_kb_full = types.InlineKeyboardMarkup(row_width=2)
    my_texts = types.InlineKeyboardButton(text='Мои шаблоны',
                                          callback_data=inline_conf.template_texts_get + str(id_project) )
    add_text = types.InlineKeyboardButton(text='Добавить шаблон',
                                          callback_data=inline_conf.template_text_add + str(id_project))
    back_btn = types.InlineKeyboardButton(text='🔙 Назад', callback_data=inline_conf.project_ + str(id_project))
    inline_kb_full.add(my_texts)
    inline_kb_full.add(add_text)
    inline_kb_full.add(back_btn)
    return inline_kb_full


def cancel_button():
    line = types.ReplyKeyboardMarkup(resize_keyboard=True)
    line.row('Отменить')

    return line


def confirm_delete(id_company):
    inline_kb = types.InlineKeyboardMarkup()
    confirm_delete = types.InlineKeyboardButton('✅ Подтверждаю',
                                                callback_data=inline_conf.project_ + str(id_company) + '_conf_delete')
    cancel_delete = types.InlineKeyboardButton('❌ Отменить',
                                               callback_data=inline_conf.project_ + str(id_company) + '_cancel_delete')
    inline_kb.row(confirm_delete, cancel_delete)

    return inline_kb
