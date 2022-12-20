from aiogram.utils import executor
from game import *


@dp.message_handler(commands='start')
async def Test(message: types.Message):
    await message.answer("Добро пожаловать в ArenaGame! Давайте начнем играть",
                         reply_markup=kb_start)
    Delete()


@dp.message_handler(Text("Закончить игру"), state=FSMGame.game)
async def Exit(message: types.Message, state: FSMContext):
    await state.finish()
    CloseSession(str(message.from_user.id))
    await message.answer("Вы успешно вышли из игры!")
    await message.answer("Добро пожаловать в ArenaGame! Давайте начнем играть",
                         reply_markup=kb_start)

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)