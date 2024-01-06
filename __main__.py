from telegram import (
    Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, ConversationHandler,
    CallbackQueryHandler, CallbackContext, Defaults
)
from telegram.constants import ParseMode

from typing import Sequence
from datetime import time, timezone, timedelta

from database.logic import UserService, ProductService
from database.core import get_engine, get_sessionmaker
from database.models import Product
from settings import Bot, Database


ARTICULE = 0


def get_buttons_product(size: int, data: Sequence[Product]) -> InlineKeyboardMarkup:
    """Generate inline buttons for list product

    Args:
        size (int): count products in row
        data (Sequence[Product]): List products for inline button

    Returns:
        InlineKeyboardMarkup: Inline Markup
    """
    data, result, count = data[::-1], [[]], 0
    while data:
        product = data.pop()
        result[-1].append(InlineKeyboardButton(product.name, callback_data=product.article))
        count += 1
        if count % size == 0: result.append([])
    return InlineKeyboardMarkup(result)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ARTICULE:
    context.bot_data['user_service'].create(update.effective_user.id)
    await context.bot.send_message(
        reply_to_message_id=update.message.message_id,
        chat_id=update.effective_chat.id,
        text='Бот предназначен для отслеживания товара и напоминании о его существовании\nОтправьте арктикул товара',
        reply_markup=ReplyKeyboardMarkup(
            [['Отмена']], one_time_keyboard=True, input_field_placeholder='Артикул товара:', resize_keyboard=True
        ),
    )
    return ARTICULE


async def callback_three_days(context: CallbackContext):
    w: Product = context.bot_data['product_service'].update(context.job.user_id, context.job.data['article'])
    await context.bot.send_photo(chat_id=context.job.chat_id, photo=context.job.data['image_product'])
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=f'Бренд: {w.brand}😎\nКоличество отзывов: {w.feedbacks}👥\nОтзывы пользователей: {w.rating_feedbacks}🌌\
            \nРейтинг: {w.rating}⭐️\nНазвание: {w.name}🙊\nСтарая Цена: {context.job.data["previous_price"]}💸\nНовая цена: {w.price}💵',
    )


async def article_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ARTICULE:
    w: Product = context.bot_data['product_service'].create(update.effective_user.id, update.message.text)
    context.job_queue.run_daily(
        callback=callback_three_days,
        time=time(22, 18, 30), days=(2, 4, 2, 4, 2, 4, 2),
        data={
            'article': update.message.text,
            'previous_price': w.price,
            'image_product': w.url_image,
        },
        user_id=update.effective_user.id,
        chat_id=update.effective_chat.id,
    )
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=w.url_image)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Бренд: {w.brand}😎\nКоличество отзывов: {w.feedbacks}👥\nОтзывы пользователей: {w.rating_feedbacks}🌌\nРейтинг: {w.rating}⭐️\nНазвание: {w.name}🙊\nЦена: {w.price}💸',
        reply_markup=ReplyKeyboardMarkup(
            [['Отмена']], one_time_keyboard=True, input_field_placeholder='Артикул товара:', resize_keyboard=True
        ),
    )
    return ARTICULE

async def restart_articule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> ARTICULE:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Отправьте артикул товара',
        reply_to_message_id=update.message.id,
        reply_markup=ReplyKeyboardMarkup(
            [['Отмена']], one_time_keyboard=True, input_field_placeholder='Артикул товара:', resize_keyboard=True
        ),
    )
    return ARTICULE
        
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Вы отменили ввод артикулов, чтобы возобновить нажмите Продолжить\nЧтобы посмотреть каталог нажмите Каталог',
        reply_to_message_id=update.message.id,
        reply_markup=ReplyKeyboardMarkup(
            [['Продолжить'], ['Каталог']], one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return ConversationHandler.END


async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_markup = get_buttons_product(
        4, context.bot_data['product_service'].get_all(update.effective_user.id)
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Выберите товар который хотитеть посмотреть по графику(график составлен за один месяц)',
        reply_markup=reply_markup
    )
    

async def callback_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    w: Product = context.bot_data['product_service'].get(update.effective_user.id, update.callback_query.data)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=w.url_image)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Бренд: {w.brand}😎\nКоличество отзывов: {w.feedbacks}👥\nОтзывы пользователей: {w.rating_feedbacks}🌌\nРейтинг: {w.rating}⭐️\nНазвание: {w.name}🙊\nЦена: {w.price}💸',
        reply_markup=ReplyKeyboardMarkup([['Отправить артикулы']], one_time_keyboard=True, resize_keyboard=True)
    )


if __name__ == '__main__':
    default = Defaults(ParseMode.HTML, tzinfo=timezone(timedelta(hours=5), name='UZ'))
    application = ApplicationBuilder().token(Bot.token).defaults(default).build()
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('articule', restart_articule),
            MessageHandler(filters.Text(['Продолжить', 'Отправить артикулы']), restart_articule)
        ],
        states={
            ARTICULE: [MessageHandler(filters.Regex('\d{9}|\d{8}'), article_product)]
        },
        fallbacks=[MessageHandler(filters.Text(['Отмена']), cancel)]
    )
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Text(['Каталог']), catalog))
    application.add_handler(CallbackQueryHandler(callback_product))
    engine = get_engine(Database.full_url)
    session = get_sessionmaker(engine)()
    application.bot_data['user_service'] = UserService(session)
    application.bot_data['product_service'] = ProductService(session)
    application.run_polling()
