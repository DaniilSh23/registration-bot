from pyrogram import filters


async def func_start_calculate_filter(_, __, query):
    """Фильтр первого шага калькулятора. Выбор ИП или ООО"""
    return query.data == 'start_calc'


async def func_cancel_calc_filter(_, __, query):
    """Фильтр отмены и выхода из калькулятора"""
    return query.data == 'cancel_calc'


async def func_ind_pred_tax_system_filter(_, __, query):
    """Фильтр выбора системы налогооблажения для ИП."""
    return query.data == 'ind_pred_form'


async def func_ask_patent_numbers_filter(_, __, query):
    """Фильтр для выбора количества патентов"""
    split_data = query.data.split()
    if len(split_data) == 2:
        return split_data[0] == 'is_pat'


async def func_plus_patent_filter(_, __, query):
    """Фильтр для кнопки плюс патента."""
    return query.data == 'plus_patent'


async def func_minus_patent_filter(_, __, query):
    """Фильтр для кнопки минус патент"""
    return query.data == 'minus_patent'


async def func_move_to_business_filter(_, __, query):
    """Фильтр для кнопки перехода к шагу подтв. осуществ. деятельности"""
    return query.data == 'move_to_bsns'


async def func_without_mix_tax_systm_filter(_, __, query):
    """Фильтр для кнопок налогообложения без микса с патентом."""
    split_data = query.data.split()
    if len(split_data) == 2:
        return split_data[0] == 'do_bsns'


async def func_ooo_tax_system_filter(_, __, query):
    """Фильтр хэндлера выбора системы налогообложения для ООО."""
    return query.data == 'ooo_form'


async def func_choice_employees_number_filter(_, __, query):
    """Фильтр для хэндлера выбора количества сотрудников"""
    return query.data == 'bsns_rnng'


async def func_plus_employee_filter(_, __, query):
    """Фильтр для хэндлера + сотрудник"""
    split_data = query.data.split()
    if len(split_data) == 2:
        return split_data[0] == 'pls_empl'


async def func_minus_employee_filter(_, __, query):
    """Фильтр для хэндлера - сотрудник"""
    split_data = query.data.split()
    if len(split_data) == 2:
        return split_data[0] == 'mns_empl'


async def func_source_docs_fst_step_filter(_, __, query):
    """
    Фильтр для нажатия на кнопку следующий шаг, после выбора кол-ва сотрудников.
    Она ведёт к первому шагу выбора первичных документов.
    """
    return query.data == 'to_source_docs'


async def func_write_source_docs_and_ask_control_it_filter(_, __, query):
    """Фильтр для хэндлера записи кол-ва перв.док-ов и запроса тов.учёта"""
    split_data = query.data.split()
    if len(split_data) == 2:
        return split_data[0] == 'source_docs'


async def func_input_numb_docs_for_prod_acc_filter(_, __, query):
    """Фильтр для хэндлера запроса кол-ва док-в для товарного учёта"""
    return query.data == 'need_prod_acc'


async def func_minus_prod_doc_filter(_, __, query):
    """Фильтр для хэндлера минус документа товарного учёта"""
    split_data = query.data.split()
    if len(split_data) == 2:
        return split_data[0] == 'mns_prod_doc'


async def func_plus_prod_doc_filter(_, __, query):
    """Фильтр для хэндлера плюс документ товарного учёта"""
    split_data = query.data.split()
    if len(split_data) == 2:
        return split_data[0] == 'pls_prod_doc'


async def func_need_product_reporting_filter(_, __, query):
    """
    Фильтр для хэндлера узнающего нужно ли клиенту ведение учёта и отчётности по товарам требующим маркировку.
    Я уже хз как это всё дело обзывать правильно.
    """
    return query.data == 'to_need_prod_report'


async def func_show_buh_result_filter(_, __, query):
    """Фильтр перед хэндлером отображения выбранных клиентом опций бух.сопровождения."""
    split_data = query.data.split()
    if len(split_data) == 2:
        return split_data[0] == 'show_reslt'
    else:
        return split_data[0] == 'not_need_prod_acc'


async def func_calculate_cost_filter(_, __, query):
    """Фильтр на кнопку расчитать стоимость бух. сопровождения."""
    return query.data == 'calc_cost'


async def func_need_prod_accounting_filter(_, __, query):   # TODO: похоже, надо переименовать
    """Фильтр для записи необходимости контроля перв. док-в и запрос необх. ведения тов. учёта"""
    split_data = query.data.split()
    if len(split_data) == 2:
        return split_data[0] == 'nd_control_scr_dcs'


async def func_work_on_mp_filter(_, __, query):
    """Фильтр для выбора маркептлейсов на которых работает клиент"""
    return query.data == 'work_on_mp'


async def func_change_mp_choice_filter(_, __, query):
    """Фильтр обработки нажатий кнопки по выбору конкретных маркетплейсов"""
    if len(query.data.split()) == 3:
        return query.data.split()[0] == 'marketplace'


async def func_need_prod_accounting_after_mp_filter(_, __, query):
    """Фильтр для перехода к запросу необходимости товарного учёта, после выбора МП."""
    return query.data == 'move_to_choice_need_prod_accounting' or query.data == 'not_work_on_mp'


start_calculate_filter = filters.create(func_start_calculate_filter)
cancel_calc_filter = filters.create(func_cancel_calc_filter)
ind_pred_tax_system_filter = filters.create(func_ind_pred_tax_system_filter)
ask_patent_numbers_filter = filters.create(func_ask_patent_numbers_filter)
plus_patent_filter = filters.create(func_plus_patent_filter)
minus_patent_filter = filters.create(func_minus_patent_filter)
move_to_business_filter = filters.create(func_move_to_business_filter)
without_mix_tax_systm_filter = filters.create(func_without_mix_tax_systm_filter)
ooo_tax_system_filter = filters.create(func_ooo_tax_system_filter)
choice_employees_number_filter = filters.create(func_choice_employees_number_filter)
plus_employee_filter = filters.create(func_plus_employee_filter)
minus_employee_filter = filters.create(func_minus_employee_filter)
source_docs_fst_step_filter = filters.create(func_source_docs_fst_step_filter)
write_source_docs_and_ask_control_it_filter = filters.create(func_write_source_docs_and_ask_control_it_filter)
input_numb_docs_for_prod_acc_filter = filters.create(func_input_numb_docs_for_prod_acc_filter)
minus_prod_doc_filter = filters.create(func_minus_prod_doc_filter)
plus_prod_doc_filter = filters.create(func_plus_prod_doc_filter)
need_product_reporting_filter = filters.create(func_need_product_reporting_filter)
show_buh_result_filter = filters.create(func_show_buh_result_filter)
calculate_cost_filter = filters.create(func_calculate_cost_filter)
need_prod_accounting_filter = filters.create(func_need_prod_accounting_filter)  # TODO: похоже, надо переименовать
work_on_mp_filter = filters.create(func_work_on_mp_filter)
change_mp_choice_filter = filters.create(func_change_mp_choice_filter)
need_prod_accounting_after_mp_filter = filters.create(func_need_prod_accounting_after_mp_filter)
