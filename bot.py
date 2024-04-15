import django
import os
from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'proj2.settings'
django.setup()
from telegram.ext import *
from base.models import *
from django.contrib.auth import authenticate

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update



API_KEY = "6613116760:AAE9O2mKKqEnb59Ur8UeXvZNb2RTJndCojo"
print('BOT STARTED!')

import logging


import random
import array

def create_strong_password():
    # maximum length of password needed
    # this can be changed to suit your password length
    MAX_LEN = 12
    
    # declare arrays of the character that we need in out password
    # Represented as chars to enable easy string concatenation
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', ' ', '~', '>',
            '*', '(', ')', '<']
    
    # combines all the character arrays above to form one array
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    
    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)
    
    # combine the character randomly selected above
    # at this stage, the password contains only 4 characters but
    # we want a 12-character password
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    
                                            
    # now that we are sure we have at least one character from each
    # set of characters, we fill the rest of
    # the password length by selecting randomly from the combined
    # list of character above.
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
    
        # convert temporary password into array and shuffle to
        # prevent it from having a consistent pattern
        # where the beginning of the password is predictable
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)
    
    # traverse the temporary password array and append the chars
    # to form the password
    password = ""
    for x in temp_pass_list:
            password = password + x

    return password
         
LOGIN, EMAILPASSWORD, SUCCESS_LOGGED, ADDUSER, CHECKPOINT,EDITUSER, SUCCEEDADDUSER, CHECKUSEREXIST, SUCCEEDEDITUSER, MAINMENU, REMOVEUSER, ADDONEMONTH, PRINTALLUSERS, GUESTMAINMENU = range(14)




    
def login(update, context):
    print('login --->')
    reply_keyboard = [["admin", 'apri cancello']]

    update.message.reply_text(
        'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
        ),
    )
    return EMAILPASSWORD

def emailpassword(update, context):
    print('email_password --->')
    print(str(update.message.text).lower())
    if ((str(update.message.text).lower() != 'admin') & (str(update.message.text).lower() != 'apri cancello') ):
        reply_keyboard = [["admin", 'apri cancello']]
        update.message.reply_text(
        'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
        ),
    )
        return EMAILPASSWORD
    else:
        update.message.reply_text('inserisci password')

    return SUCCESS_LOGGED

def success_logged(update, context):
    print('succedd logged --->')
    emailandpassword = str(update.message.text)
    if emailandpassword.startswith("/"):
        update.message.reply_text('inserisci password')
        return SUCCESS_LOGGED
        # nome:david pass:abc123
    else:
        fname__value = ""
        password__value = ""
        try:
            # fname__value = emailandpassword.split(' pass:')[0].split('nome:')[1]
            password__value = emailandpassword
        except:
            update.message.reply_text('inserisci password')

        is_super_user = False
        # user__value = GuestUser.objects.get(password__exact=emailandpassword)
        user__value = GuestUser.objects.all()
        user__selected = None
        username_logged = ""
        for i in user__value:
            # try:
            if (i.check_password(emailandpassword)):
                is_super_user = i.is_superuser
                correct = i.check_password(emailandpassword)
                user__selected = i
                break
            else:
                correct = False
            # except:
            #     correct = False

        if correct:
            if not is_super_user:
                reply_keyboard = [["admin", 'apri cancello']]
                if user__selected.allowed_for_open_gate:
                    update.message.reply_text(
                        'true', reply_markup=ReplyKeyboardMarkup(
                            reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
                        ),
                    )
                else:
                    update.message.reply_text(
                        'false', reply_markup=ReplyKeyboardMarkup(
                            reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
                        ),
                    )
                return EMAILPASSWORD
            else:
                reply_keyboard = [["aggiungi utente", "rimuovi utente"], ["rinnova permesso", "mostra utenti", 'mostra storico aperture']]

                update.message.reply_text(f'Credenziali corrette. Decidi quale azione fare..', reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="SELECT YOUR NEXT OPERATION?"
            ),)
                return MAINMENU
        else:
            update.message.reply_text(f'Password non corretta. Inserisci quella giusta!')
            return SUCCESS_LOGGED
    # except:
    #     update.message.reply_text(f'No, Account Found.')



# Main Menu 

def mainmenu(update, context):
    if ((update.message.text).lower() == 'aggiungi utente'):
        reply_keyboard = [["continua"]]
        update.message.reply_text('Per aggiungere un utente, scrivi nome e cognome in questo modo.\nnome:Esempio cognome:Esempio\nSe non vuoi inserire un nuovo utente, clicca semplicemente su Continua.', reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="SELECT YOUR NEXT OPERATION?"
            ),)
        return SUCCEEDADDUSER

    # elif ((update.message.text).lower() == '/edituser'):
    #     reply_keyboard = [["continua"]]
    #     update.message.reply_text('If you want to edit a user. \nSend me the First Name of User.\nOthwise, Click on Skip to Skip this task.', reply_markup=ReplyKeyboardMarkup(
    #             reply_keyboard, one_time_keyboard=True, input_field_placeholder="SELECT YOUR NEXT OPERATION?"
    #         ),)
    #     return CHECKUSEREXIST

    elif ((update.message.text).lower() == 'rimuovi utente'):
        reply_keyboard = [["continua"]]
        update.message.reply_text("Inserisci il cognome dell'utente che vuoi rimuovere. \Se non vuoi più rimuovere un utente, clicca su Continua'\Se non vuoi più rimuovere un utente, clicca su Continua'", reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="SELECT YOUR NEXT OPERATION?"
            ),)
        return REMOVEUSER

    elif ((update.message.text).lower() == 'rinnova permesso'):
        reply_keyboard = [["continua"]]
        update.message.reply_text("Inserisci il cognome dell'utente a cui vuoi aggiungere un mese in cui potrà aprire il cancello.", reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="SELECT YOUR NEXT OPERATION?"
            ),)
        return ADDONEMONTH

    elif ((update.message.text).lower() == 'mostra utenti'):
        try:
            # nome:David cognome:Mark email:abc@abc.com
            user__value = GuestUser.objects.all()
            all_users_str = ''
            for i in user__value:
                all_users_str += f'\n{i.first_name} {i.last_name} {i.end_allowed_date}'

            update.message.reply_text(f'Ecco la lista completa degli utenti. \n{all_users_str}')

            reply_keyboard = [["admin", 'apri cancello']]

            update.message.reply_text(
                'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
                ),
            )
            return EMAILPASSWORD
            
        except:

            reply_keyboard = [["admin", 'apri cancello']]

            update.message.reply_text(
                'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
                ),
            )
            return EMAILPASSWORD

    elif ((update.message.text).lower() == 'mostra storico aperture'):
        try:
            # nome:David cognome:Mark email:abc@abc.com
            all__value = Opening.objects.all()
            all_users_str = ''
            for i in all__value:
                all_users_str += f'\nusername:{i.opened_by} opendatetime:{i.open_date}'

            update.message.reply_text(f'All Openings.\n{all_users_str}')

            reply_keyboard = [["admin", 'apri cancello']]

            update.message.reply_text(
                'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
                ),
            )
            return EMAILPASSWORD
            
        except:

            reply_keyboard = [["admin", 'apri cancello']]

            update.message.reply_text(
                'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
                ),
            )
            return EMAILPASSWORD



    # return ConversationHandler.END


def guestmainmenu(update, context):
    if ((update.message.text).lower() == 'continua'):
        reply_keyboard = [["admin", 'apri cancello']]

        update.message.reply_text(
            'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
            ),
        )
        return EMAILPASSWORD
    elif ((update.message.text).lower() == '/opengate'):
        Opening.objects.create(opened_by=update.message.from_user.username)

        reply_keyboard = [["admin", 'apri cancello']]

        update.message.reply_text(
            'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
            ),
        )
        return EMAILPASSWORD
    else:
        reply_keyboard = [["admin", 'apri cancello']]


        update.message.reply_text(f'true', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="SELECT YOUR NEXT OPERATION?"
        ),)

        return EMAILPASSWORD


def adduser(update, context):
    print('add user --->')
    reply_keyboard = [["continua"]]
    update.message.reply_text('Per aggiungere un utente, scrivi nome e cognome in questo modo:\nnome:Esempio cognome:Esempio\nSe non vuoi inserire un nuovo utente, clicca semplicemente su Continua.', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="SELECT YOUR NEXT OPERATION?"
        ),)

    return SUCCEEDADDUSER

def succeedadduser(update, context):
    print('succedd add user --->')
    emailandnames = str(update.message.text).lower()
    # nome:David cognome:Mark email:abc@abc.com
    if 'continua' in emailandnames:

        reply_keyboard = [["admin", 'apri cancello']]

        update.message.reply_text(
            'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
            ),
        )
        return EMAILPASSWORD
    else:
        fname__value = ""
        lname__value = ""
# nome:David cognome:Mark
        try:
            fname__value = emailandnames.split(' cognome:')[0].split('nome:')[1]
            lname__value = emailandnames.split(' cognome:')[1]
        except:
            update.message.reply_text('Send Full Name and Last Name in this format. \nnome:David cognome:Mark')
            return SUCCEEDADDUSER
        try:
            new_user_pass = create_strong_password()
            new_user = GuestUser.objects.create_user(first_name=fname__value, last_name=lname__value, password=new_user_pass)
            new_user.save()
            update.message.reply_text(f"Nuovo utente creato.\L'utente può accedere usando questa password:\n{new_user_pass}\nValidità accesso al cancello:\n{send_expire_date()}")

            reply_keyboard = [["admin", 'apri cancello']]

            update.message.reply_text(
                'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
                ),
            )
            return EMAILPASSWORD
        except:
            
            update.message.reply_text(f'Choose a Different Name.\nOr Provide values in this formate. \nnome:David cognome:Mark')
            return SUCCEEDADDUSER
    
def skip_adduser(update, context):
    print('skip adduser --->')
    return EDITUSER

def edituser(update, context):
    reply_keyboard = [["continua"]]
    update.message.reply_text('If you want to edit a user. \nSend me the First Name of User.\nOthwise, Click on Skip to Skip this task.', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="SELECT YOUR NEXT OPERATION?"
        ),)

    return CHECKUSEREXIST


def checkuserexist(update, context):
    print("check user exist --->")
    fname__value = str(update.message.text).lower()
    if fname__value == "continua":
        reply_keyboard = [["/start"]]
        update.message.reply_text(f'Chat Ended. Admin Logged Out.\nClick on /start to do another task.', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="SELECT YOUR NEXT OPERATION?"
        ),)
        return ConversationHandler.END
    else:
        try:
            user__value = GuestUser.objects.get(first_name__exact=fname__value)
            update.message.reply_text(f'You have selected a User: {fname__value}.\nFirst Name of User: {user__value.first_name}\nLast Name of User: {user__value.last_name}\nAllowed for Gate Open: {"yes" if user__value.allowed_for_open_gate else "no"}. \nNow, Change anything from this format to Change First Name, Last Name, Email or Permission.\n\nnome:{user__value.first_name} cognome:{user__value.last_name} afgo:{"yes" if user__value.allowed_for_open_gate else "no"}')
            return SUCCEEDEDITUSER
        except:
            update.message.reply_text(f'No! User Found. Please input First Name again!')
            return CHECKUSEREXIST


def succeededituser(update, context):
    print('succedd edit user --->')
    msg__values = str(update.message.text).lower()
    # nome:David cognome:Mark email:abc@abc.com
    # nome:Ayyan cognome:Inam afgo:yes
    fname__value = ""
    lname__value = ""
    afgo__value = ""

    try:
        afgo__value = msg__values.split('afgo:')[1]
        fname__value = msg__values.split(' cognome:')[0].split('nome:')[1]
        lname__value = msg__values.split('cognome:')[1].split(' afgo:')[0]
    except:
        update.message.reply_text(f'Please check upper instruction clearly. Your input is wrong.\nEnter the First Name again')
        return CHECKUSEREXIST
    try:
        user__obj = GuestUser.objects.get(first_name__exact = fname__value)
        user__obj.first_name = fname__value
        user__obj.last_name = lname__value
        if afgo__value == "no":
            user__obj.end_allowed_date = send_expire_date(1, (-1))
        else:
            user__obj.end_allowed_date = send_expire_date()

        user__obj.save()
    except:
        update.message.reply_text(f'No! User Found, Enter First Name again')
        return CHECKUSEREXIST
        
    reply_keyboard = [["admin", 'apri cancello']]

    update.message.reply_text(
        'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
        ),
    )
    return EMAILPASSWORD
    # except:
    #     update.message.reply_text(f'Wrong Input, Please Provide email to edit the user.')
    #     return CHECKUSEREXIST
    

    # return ConversationHandler.END
    # try:
    #     new_user_pass = create_strong_password()
    #     new_user = GuestUser.objects.create_user(first_name=fname__value, last_name=lname__value, email=email__value, password=new_user_pass)
    #     new_user.save()
    #     update.message.reply_text(f'New User has been created.\nEmail:\n{email__value}\nPassword:\n{new_user_pass}\nClick on /edituser to edit users permissions.')
    #     return EDITUSER

    # except:
    #     update.message.reply_text(f'Choose a Different Email.\nOr Provide values in this formate. \nnome:David cognome:Mark email:abc@abc.com')
    #     return SUCCEEDADDUSER
    
def skip_edituser(update, context):
    print('skil edit user --->')
    return ConversationHandler.END


def removeuser(update, context):
    print("check user exist --->")
    fname__value = str(update.message.text).lower()
    if fname__value == "continua":
        reply_keyboard = [["admin", 'apri cancello']]

        update.message.reply_text(
            'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
            ),
        )
        return EMAILPASSWORD
    else:
        try:
            user__value = GuestUser.objects.get(last_name__exact=fname__value)
            user__value.delete()
            update.message.reply_text(f'Hai selezionato: {fname__value}.\nHas Been Removed')

            reply_keyboard = [["admin", 'apri cancello']]

            update.message.reply_text(
                'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
                ),
            )
            return EMAILPASSWORD
        except:
            update.message.reply_text(f'No! User Found. Please input First Name again!')
            return REMOVEUSER



def addonemonth(update, context):
    fname__value = str(update.message.text).lower()
    if fname__value == "continua":

        reply_keyboard = [["admin", 'apri cancello']]

        update.message.reply_text(
            'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
            ),
        )
        return EMAILPASSWORD
    else:
        try:
            user__value = GuestUser.objects.get(last_name__exact=fname__value)
            user__value.end_allowed_date = send_expire_date()
            user__value.save()
            update.message.reply_text(f'Hai selezionato: {fname__value}.\nOra ha il permesso per aprire il cancello fino al: {send_expire_date()}')
  
            reply_keyboard = [["admin", 'apri cancello']]

            update.message.reply_text(
                'Benvenuto su OpenGate. Fai una scelta', reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, input_field_placeholder="GO TO LOGIN?"
                ),
            )
            return EMAILPASSWORD
        except:
            update.message.reply_text(f'No! User Found. Please input First Name again!')
            return ADDONEMONTH


# def printallusers(update, context):
#     fname__value = str(update.message.text).lower()
#     if fname__value == "continua":
#         reply_keyboard = [["/start"]]
#         update.message.reply_text(f'Chat Ended. Admin Logged Out.\nClick on /start to do another task.', reply_markup=ReplyKeyboardMarkup(
#             reply_keyboard, one_time_keyboard=True, input_field_placeholder="SELECT YOUR NEXT OPERATION?"
#         ),)
#         return ConversationHandler.END
#     else:
        
    

def cancel(update, context):
    print('cancel --->')

    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

    



# def name(update, context):
#     update.message.reply_text('What do you want to name this dog?')

#     return S_NAME

# def s_name(update, context):
#     update.message.reply_text('What do you want to name this dog?')

#     return DOG_SAVE

# def dog_save(update, context):
#     name = update.message.text
#     update.message.reply_text(f'Dog saved as {NAME} {S_NAME}')

#     return ConversationHandler.END

def main():
    updater = Updater(API_KEY, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', login)],

        states={
            LOGIN: [CommandHandler('login', login)],
            # ADDUSER: [CommandHandler('adduser', adduser)],
            EMAILPASSWORD: [MessageHandler(Filters.text, emailpassword)],
            SUCCESS_LOGGED: [MessageHandler(Filters.text, success_logged)],
            ADDUSER: [MessageHandler(Filters.text, adduser)],
            SUCCEEDADDUSER: [MessageHandler(Filters.text, succeedadduser)],
            EDITUSER: [MessageHandler(Filters.text, edituser)],
            CHECKUSEREXIST: [MessageHandler(Filters.text, checkuserexist)],
            SUCCEEDEDITUSER: [MessageHandler(Filters.text, succeededituser)],
            MAINMENU: [MessageHandler(Filters.text, mainmenu)],
            REMOVEUSER: [MessageHandler(Filters.text, removeuser)],
            ADDONEMONTH: [MessageHandler(Filters.text, addonemonth)],
            GUESTMAINMENU: [MessageHandler(Filters.text, guestmainmenu)],
            # PRINTALLUSERS: [MessageHandler(Filters.text, printallusers)],
            # EDITUSER: [CommandHandler(Filters.text, edituser), CommandHandler("skip", skip_edituser)],

            

            # S_NAME: [MessageHandler(Filters.text, s_name)],
            # DOG_SAVE: [MessageHandler(Filters.text, dog_save)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],

    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
