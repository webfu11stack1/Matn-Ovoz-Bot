from aiogram import Bot, Dispatcher, types
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup,ReplyKeyboardRemove
from gtts import gTTS
import os
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging


# Bot tokenini bu o'zgaruvchiga kiritasiz
logging.basicConfig(level=logging.INFO)

bot_token = ""
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def on_start(message: types.Message,state:FSMContext):
    matn=ReplyKeyboardMarkup(
        keyboard=[
            ["✍️Matn kiritish"]
        ],resize_keyboard=True
    )
    await message.answer("Assalomu alaykum! ✍️Men matnni ovozga 🗣 aylantiruvchi botman. \nMatn kiritish uchun pastdagi tugmani bosing⬇️",reply_markup=matn)
    await state.set_state("til")

@dp.message_handler(text="✍️Matn kiritish", state="*")
async def matnn(message: types.Message, state: FSMContext):
    await message.answer("✍️Matn kiritishingiz mumkin")
    await state.set_state("matn")


@dp.message_handler(state="matn")
async def convert_to_speech(message: types.Message, state: FSMContext):
    global inp
    inp = message.text
    til = ReplyKeyboardMarkup(
        keyboard=[
            ["ru", "en"],
            ["✍️Matn kiritish"]
        ], resize_keyboard=True
    )
    await message.answer("⬇️Kerakli tilni tanlang⬇️", reply_markup=til)
    await state.set_state("ovoz")


@dp.message_handler(state="*")
async def ovoz(message: types.Message, state: FSMContext):
    voite = message.text
    if voite == "✍️Matn kiritish":
        await matnn(message, state)
    else:
        voice = gTTS(text=inp, lang=voite, slow=False)
        voice.save("output.mp3")

        with open("output.mp3", "rb") as audio:
            await bot.send_audio(message.chat.id, audio, caption="Matningizni audiosi")

        os.remove("output.mp3")  



if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
