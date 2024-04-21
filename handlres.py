import re
import vk_api
from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from app.database import insert_token_into_database, get_token_from_database

import app.keyboards as kb
from app.state import Pars, Auth



router = Router()


previous_inline_message_id = None

#КОМАНДА СТАРТ
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('<b>Выберите операцию:</b>', reply_markup=kb.Start, parse_mode='html')

#ПРОФИЛЬ
@router.callback_query(F.data == 'profile')
async def send_Profile(callback: CallbackQuery):
    username = callback.from_user.username
    user_id = callback.from_user.id
    await callback.message.edit_text(f'👤<b>Ваш ник-нейм: <u>{username}</u></b>'
                                     f'  \n🤖<b>Ваш цифровой ID: <u>{user_id}</u></b>',
                                     reply_markup=kb.Profile, parse_mode='html')

#ПАРСЕР
@router.callback_query(F.data == 'parser')
async def send_ParsChoosePars(callback: CallbackQuery):
    await callback.message.edit_text('<b>Выберите тип парсинга:</b>', reply_markup=kb.ChooseParsing, parse_mode='html')

@router.callback_query(StateFilter(None), F.data == 'parsSoobVk')
async def send_ParsSoobVk(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Pars.vk_soob)
    await callback.message.edit_text('<b>⚙️    <u>ПАРСЕР ВК СООБЩЕСТВА</u>    ⚙️</b>\n\n<b>Введите ссылку на сообщество ВК:</b>', reply_markup=kb.backParsChoosePars, parse_mode='html')

@router.message(Pars.vk_soob)
async def get_vk_soob_data(message: Message, state: FSMContext):

    from_user_soob_link = message.text
    if from_user_soob_link.startswith("https://vk.com/"):
        soobLink = from_user_soob_link.split("https://vk.com/")[1]
        user_id = message.from_user.id
        token = await get_token_from_database(user_id)
        if token:
            authroz = vk_api.VkApi(token=token)
            vk = authroz.get_api()
            group_id = soobLink
            get_member = vk.groups.getMembers(group_id=group_id, count=10, fields='first_name,last_name')

            member_list = []

            for member in get_member['items']:
                user_first_n = member['first_name']
                user_last_n = member['last_name']
                user_id = member['id']

                first_letter_last_name = user_last_n[0] + '.'
                member_list.append(f"<b>{user_first_n}{first_letter_last_name}</b> | https://vk.com/id{user_id}")

            # Отправляем все данные одним сообщением
            await message.answer('\n'.join(member_list), parse_mode='html', disable_web_page_preview=True)
            await state.clear()
        else:
            await message.answer("Не удалось получить токен из базы данных. Пожалуйста, убедитесь, что токен добавлен в таблицу Tokens.")
    else:
        await message.answer("Не корректный формат ссылки на сообщество ВК", reply_markup=kb.ChooseParsing)

#ИНСТРУКЦИЯ
@router.callback_query(F.data == 'instruction')
async def send_Instruction(callback: CallbackQuery):
    await callback.message.edit_text('<b>Выберите операцию:</b>', reply_markup=kb.Instruction, parse_mode='html', disable_web_page_preview=True)


@router.callback_query(F.data == 'getToken')
async def get_Token (callback: CallbackQuery):
    await callback.message.edit_text('<b>Для получение токен</b> '
                                      '\n1) Зайдите <a href=vkhost.github.io>СЮДА</a> '
                                      '\n2) Выбирите тип <i>VK Admin</i> '
                                      '\n3) Нажмите кнопку <i>РАЗРЕШИТЬ</i> '
                                      '\n4) Скопируйте ссылку сайта на которую вы были перенаправлены и скиньте ее боту! '
                                      '\n<b>ГОТОВО</b>',
                                      reply_markup=kb.GetToken, parse_mode='html', disable_web_page_preview=True)

#ЗАДАНИЯ
@router.callback_query(F.data == 'task')
async def get_Task(callback: CallbackQuery):
    await callback.message.edit_text('<b>Выберите необходимые настройки:</b>', reply_markup=kb.Task, parse_mode='html')
@router.callback_query(F.data == 'accounts')
async def send_Accounts (callback: CallbackQuery):
    await callback.message.edit_text('<b>Список аккаунтов пуст:</b> ', reply_markup=kb.Accounts, parse_mode='html')


@router.callback_query(StateFilter(None), F.data == 'addAcc')
async def send_GetAccounts(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Auth.token)
    await callback.message.edit_text('Введите ссылку с токеном, полученный <a href=vkhost.github.io>ЗДЕСЬ</a>:',
                                     reply_markup=kb.AddingAccount, parse_mode='html', disable_web_page_preview=True)

@router.message(Auth.token)
async def get_token_and_auth(message: Message, state: FSMContext):
    token_text = message.text
    #получение токена из ссылки пользователя
    token_match = re.search(r'token=(.*?)&expires_in', token_text)
    if token_match:
        token = token_match.group(1)
        await state.update_data(token=token)
        user_id = message.from_user.id

        # existing_token = await get_token_from_database(user_id)
        # if existing_token:
        #     await message.delete()
        #     await message.answer("Данный аккаунт уже добавлен!")
        #     await asyncio.sleep(5)  # Ждем 5 секунд
        #     await reply_message.delete()  # Удаляем сообщение
        #     return

        insert_into_db = await insert_token_into_database(user_id, token)
        if insert_into_db:
            try:
                vk_auth = vk_api.VkApi(token=token)
                vk = vk_auth.get_api()
                user_info = vk.users.get()
                first_name = user_info[0]['first_name']
                last_name = user_info[0]['last_name']
                await message.answer(f'Аккаунт <b>{first_name}</b>  <b>{last_name}</b> успшено добавлен!', reply_markup=kb.Countinue, parse_mode='html')
                await state.clear()
            except vk_api.AuthError as e:
                await message.answer(f'Произошла ошибка при авторизации под данному токену!')
        else:
            await message.answer('Произошла ошибка при добавление данных в базу данных!')
    else:
        await message.answer("Не правильный формат ссылки!\nПопробуйте еще раз")



@router.callback_query(F.data == 'text')
async def send_message_for_Vk(callback: CallbackQuery):
    await state.set_state(Auth.login)
    await callback.message.edit_text('<b>Отправьте сообщение, которое вы хотите отправить во все беседы ВК:</b>', reply_markup=kb.GetTask, parse_mode='html')



@router.callback_query(F.data == 'rassilka')
async def send_Rassilka(callback: CallbackQuery):
    await callback.message.edit_text('<b>Выберите операцию:</b>', reply_markup=kb.Rassilka, parse_mode='html')

@router.callback_query(F.data == 'RassInLs')
async def send_RassInLs(callback: CallbackQuery):
    await callback.message.edit_text('<b>Вставьте ссылки на акканты пользователей ВК (макс кол-во: 10 ссылок):</b>', parse_mode='html')



@router.callback_query(F.data == 'backToStart')
async def back_to_start(callback: CallbackQuery):
    await callback.message.edit_text('<b>Выберите операцию:</b>', reply_markup=kb.Start, parse_mode='html')


@router.callback_query(F.data == 'backToPrfl')
async def back_to_prfl(callback: CallbackQuery):
    await send_Profile(callback)


@router.callback_query(F.data == 'backToInstruction')
async def back_to_instruction(callback: CallbackQuery):
    await send_Instruction(callback)


@router.callback_query(F.data == 'backToAcc')
async def back_to_acc(callback: CallbackQuery):
    await send_Accounts(callback)


@router.callback_query(F.data == 'backToTask')
async def back_to_task(callback: CallbackQuery):
    await get_Task(callback)


@router.callback_query(F.data == 'backToRass')
async def back_to_rass(callback: CallbackQuery):
    await send_Rassilka(callback)

@router.callback_query(F.data == 'backParsChoosePars')
async def back_to_rass(callback: CallbackQuery):
    await send_ParsChoosePars(callback)




@router.callback_query(F.data == 'InDev')
async def In_Dev(callback: CallbackQuery):
    await callback.answer('Кнопка в разработке !', show_alert=True)