from aiogram.fsm.state import State, StatesGroup



class Pars(StatesGroup):
    vk_soob = State()



class Auth(StatesGroup):
    token = State()
    auth = State()
