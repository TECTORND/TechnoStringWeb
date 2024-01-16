from flask import Flask, render_template, request, flash, redirect, url_for, session

from pyrogram import Client, filters
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)


app = Flask(__name__)
app.secret_key = '987b2ed6612d69ea56c4da397333baf44b4f81b049916f5809449373c0c4ce84'  # Add a secret key for session management
app.config['SESSION_TYPE'] = 'filesystem'

def flash_messages():
    while True:
        message = yield
        yield f"data: {message}\n\n"


@app.route('/sse')
def sse():
    g = flash_messages()
    next(g)  # Initialize the generator
    while True:
        flash_message = yield
        g.send(flash_message)


def custom_flash(message):
    with app.test_request_context('/'):
        app.response_class()(message)
        app.preprocess_request()
        yield message


@app.route('/', methods=['GET', 'POST'])
def generate_string_session():
    if request.method == 'POST':
        choice = request.form['choice']
        session['library'] = choice
        if choice == 'telethon':
            return render_template('session.html', library='Telethon')
        elif choice == 'pyrogram':
            return render_template('session.html', library='Pyrogram')
        else:
            return render_template('error.html')
    return render_template('home.html')


@app.route('/generate_session', methods=['POST'])
async def generate_session():
    library = session.get('library')
    api_id = request.form['api_id']
    api_hash = request.form['api_hash']
    phone_number = request.form['phone_number']
    sendOTP = False
    otp = request.form['otp']
    if otp=='':
        if library == 'telethon':
            client = TelegramClient(StringSession(), api_id, api_hash)
        else:
            client = Client(":memory:", api_id, api_hash)
        await client.connect()
    else:
        try:
            client = TelegramClient(StringSession(), api_id, api_hash)
            await client.sign_in(phone_number, otp)
            custom_flash("Telethon session generated successfully!")
        except Exception as e:
            custom_flash(f"Error: {str(e)}")
    if sendOTP:
        return render_template('session.html', library=library, api_id=api_id, api_hash=api_hash, phone_number=phone_number, sendOTP='true')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=808880, debug=True)
