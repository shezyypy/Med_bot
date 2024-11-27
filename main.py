import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message, CallbackQuery

from tech.auth_data import token
from tech import keyboard as kb
from tech.classes import TemperatureStates
from tech.graf import plot_temperature, load_data, save_data


bot = Bot(token)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Доброй пожаловать! Я твой новый помощник во время болезней. С радостью буду отслеживать "
                         "твою температуру и составлять график. Спасибо за доверие!", reply_markup=kb.main)


@dp.message(Command("temp"))
@dp.message(F.text == 'Дневник температуры')
async def send_welcome(message: Message, state: FSMContext):
    await state.set_state(TemperatureStates.waiting_for_temperature)
    await message.answer("Введите температуру (например, 37.5)")


@dp.message(TemperatureStates.waiting_for_temperature)
async def add_temperature(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    try:
        temp_value = float(message.text.strip())
        now = datetime.now()
        date_time_str = now.strftime('%d.%m.%Y %H:%M')

        data = load_data()
        if user_id not in data:
            data[user_id] = []
        data[user_id].append(f"{temp_value} {date_time_str}")
        save_data(data)
        await message.answer("Температура добавлена!")

        image = plot_temperature(data[user_id])
        if image:
            await message.answer_photo(photo=BufferedInputFile(image.getvalue(), filename='temperature_chart.png'))
        else:
            await message.reply("Не удалось построить график.")
        await state.clear()

    except ValueError as e:
        await message.reply(f"Ошибка: {e}. Введите числовое значение температуры.")
    except Exception as e:
        await message.reply(f"Произошла другая ошибка: {e}")


@dp.message(Command('faq'))
@dp.message(F.text == 'F.A.Q.')
async def faq(message: Message):
    text = (
        "Мне приятно, что вы интересуетесь часто задаваемыми вопросами\\. "
        "Желаю приятного чтения моей [статьи](https://telegra\\.ph/FAQ\\-\\-\\-CHasto\\-zadavaemye\\-voprosy\\-11"
        "\\-26\\-2)\\!"
    )

    await message.answer(text, parse_mode="MarkdownV2")

@dp.message(Command('diseases'))
@dp.message(F.text == 'Распространенные заболевания')
async def diseases(message: Message):
    await message.answer_photo(photo='https://cdnstatic.rg.ru/uploads/images/136/29/41'
                                     '/Paralich_koma_bolnica_bolezn_suprugi_Depositphotos_1000.jpg',
                               caption="Сейчас я расскажу тебе о 10-ти популярных заболеваниях."
                                       " Нажимай кнопки ниже и развивай свой кругозор!", reply_markup=kb.diseases)


@dp.callback_query(F.data == 'back')
async def back(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(photo='https://cdnstatic.rg.ru/uploads/images/136/29/41'
                                            '/Paralich_koma_bolnica_bolezn_suprugi_Depositphotos_1000.jpg',
                                        caption="Сейчас я расскажу тебе о 10-ти популярных заболеваниях."
                                            " Нажимай кнопки ниже и развивай свой кругозор!",
                                        reply_markup=kb.diseases)


@dp.callback_query(F.data == 'influenza')
async def influenza(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo='https://i2.wp.com/lopezdoriga.com/wp-content/uploads/2019/03/virus.jpg?fit=1000%2C563&ssl=1',
        caption=(
            "• <b>Симптомы</b>: Высокая температура, кашель, ломота в теле, головная боль, усталость.\n \n"
            "• <b>Профилактика</b>: Вакцинация, регулярное мытье рук, избегание контакта с больными,"
            " укрепление иммунной системы.\n \n"
            "• <b>Причина</b>: Вирусная инфекция, вызываемая вирусами гриппа A и B."
        ),
        parse_mode="HTML",
        reply_markup=kb.back
    )


@dp.callback_query(F.data == 'covid')
async def covid(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo='https://samtfoms.ru/storage/0_618903187de31111691867_1f65a57c.jpg',
        caption=(
            "• <b>Симптомы</b>: Кашель, одышка, лихорадка, потеря вкуса или обоняния, усталость."
            " Может протекать бессимптомно.\n \n"
            "• <b>Профилактика</b>: Вакцинация, ношение масок в общественных местах, соблюдение социальной дистанции,"
            " регулярное мытье рук, избегание больших скоплений людей.\n \n"
            "• <b>Причина</b>: Вирусная инфекция, вызываемая вирусом SARS-CoV-2."
        ),
        parse_mode="HTML",
        reply_markup=kb.back
    )


@dp.callback_query(F.data == 'allergy')
async def allergy(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo='https://chitazdrav.ru/sites/default/files/news_foto/%D0%B0%D0%BB%D0%BB%D0%B5%D1%80%D0%B3%D0%B8%D1%8F_0.jpg',
        caption=(
            "• <b>Симптомы</b>: Зуд, отек, высыпания, затрудненное дыхание, насморк."
            " Симптомы варьируются в зависимости от аллергена. Может протекать бессимптомно.\n \n"
            "• <b>Профилактика</b>: Избегание контакта с аллергенами, использование антигистаминов,"
            " регулярные консультации с аллергологом.\n \n"
            "• <b>Причина</b>: Гиперчувствительность иммунной системы к определенным веществам (аллергенам)."
        ),
        parse_mode="HTML",
        reply_markup=kb.back
    )


@dp.callback_query(F.data == 'diabetes')
async def diabetes(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo='https://avatars.mds.yandex.net/i?id=dc52a9a9ce131310c370dfb64cafcab9828f85da-5251742-images-thumbs&n=13',
        caption=(
            "• <b>Симптомы</b>: Частое мочеиспускание, сильная жажда, усталость, медленное заживление ран,"
            " неясное зрение. Может протекать бессимптомно.\n \n"
            "• <b>Профилактика</b>: Здоровое питание, регулярные физические нагрузки, контроль веса,"
            " регулярные медицинские осмотры.\n \n"
            "• <b>Причина</b>: Нарушение выработки или действия инсулина, приводящее к повышению уровня сахара в крови."
            " Различают диабет 1 и 2 типа."
        ),
        parse_mode="HTML",
        reply_markup=kb.back
    )


@dp.callback_query(F.data == 'hypertension')
async def hypertension(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo='https://avatars.mds.yandex.net/i?id=50fefb71e71a0ac8c25a3728901b4da993163763-4987817-images-thumbs&n=13',
        caption=(
            "• <b>Симптомы</b>: Часто бессимптомна, но может вызывать головные боли, одышку, носовые кровотечения.\n \n"
            "• <b>Профилактика</b>: Контроль артериального давления, здоровое питание, физическая активность,"
            " отказ от курения и алкоголя.\n \n"
            "• <b>Причина</b>: Повышенное артериальное давление, причины могут быть различны:"
            " генетическая предрасположенность, неправильный образ жизни, заболевания почек и другие."
        ),
        parse_mode="HTML",
        reply_markup=kb.back
    )


@dp.callback_query(F.data == 'heart_attack')
async def heart_attack(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo='https://stomatologspb.ru/wp-content/uploads'
              '/%D0%91%D0%BE%D0%BB%D1%8C-%D0%B2-%D1%81%D0%B5%D1%80%D0%B4%D1%86%D0%B5-scaled.jpg',
        caption=(
            "• <b>Симптомы</b>: Боль в груди, одышка, потливость, тошнота, боль в руках, спине или челюсти."
            " Симптомы могут варьироваться.\n \n"
            "• <b>Профилактика</b>: Здоровое питание, физическая активность,"
            " контроль уровня холестерина и артериального давления, отказ от курения.\n \n"
            "• <b>Причина</b>: Нарушение кровоснабжения сердечной мышцы, чаще всего из-за тромба,"
            " блокирующего коронарную артерию."
        ),
        parse_mode="HTML",
        reply_markup=kb.back
    )


@dp.callback_query(F.data == 'stroke')
async def stroke(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo='https://avatars.mds.yandex.net/i?id=e9c8ff6e5d0efa7b5ef86ac0e3a54474_l-9221923-images-thumbs&n=13',
        caption=(
            "• <b>Симптомы</b>: Внезапная слабость или онемение одной стороны тела, затруднение речи,"
            " проблемы с координации. Симптомы могут варьироваться.\n \n"
            "• <b>Профилактика</b>: Контроль артериального давления, здоровый образ жизни,"
            " регулярные медицинские осмотры, отказ от курения.\n \n"
            "• <b>Причина</b>: Нарушение кровоснабжения головного мозга,"
            " чаще всего из-за закупорки или разрыва кровеносного сосуда."
        ),
        parse_mode="HTML",
        reply_markup=kb.back
    )


@dp.callback_query(F.data == 'asthma')
async def asthma(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo='https://www.mckolomen.ru/local/templates/main/img/rzvaucybf44n1fikfxauelyjcsk1c84f.jpg',
        caption=(
            "• <b>Симптомы</b>: Затрудненное дыхание, свистящее дыхание, кашель, особенно ночью или рано утром.\n \n"
            "• <b>Профилактика</b>: Избегание триггеров (аллергенов, дыма, физических нагрузок)"
            " использование ингаляторов, регулярные медицинские осмотры.\n \n"
            "• <b>Причина</b>: Хроническое воспалительное заболевание дыхательных путей, вызывающее сужение бронхов."
        ),
        parse_mode="HTML",
        reply_markup=kb.back
    )


@dp.callback_query(F.data == 'obesity')
async def obesity(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo='https://static.mk.ru/upload/entities/2023/06/13/13/articles/facebookPicture/fa/af/a5/5b/aa4c0b1f4f7012436007456546db293d.jpg',
        caption=(
            "• <b>Симптомы</b>: Увеличение веса, проблемы с дыханием, усталость, боли в суставах.\n \n"
            "• <b>Профилактика</b>: Сбалансированное питание, регулярные физические нагрузки,"
            " контроль порций и уровня стресса.\n \n"
            "• <b>Причина</b>: Избыточное накопление жировой ткани в организме,"
            " вызванное дисбалансом между потреблением и расходом энергии."
        ),
        parse_mode="HTML",
        reply_markup=kb.back
    )


@dp.callback_query(F.data == 'depression')
async def depression(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer_photo(
        photo='https://static.mk.ru/upload/entities/2024/02/10/13/articles/facebookPicture/64/dd/1e/a3/e599f3207124e8610fd2f83816d16b05.jpg',
        caption=(
            "• <b>Симптомы</b>: Постоянное чувство грусти, утрата интереса к жизни, изменения в аппетите и сне,"
            " проблемы с концентрацией. Симптомы могут варьироваться.\n \n"
            "• <b>Профилактика</b>: Физическая активность, поддержание социальных связей, релаксация,"
            " обращение за профессиональной помощью при необходимости.\n \n"
            "• <b>Причина</b>: Сложное заболевание с многочисленными факторами риска,"
            " включая генетическую предрасположенность, стресс, социальные факторы и биохимические нарушения в мозге."
        ),
        parse_mode="HTML",
        reply_markup=kb.back
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("я все")
