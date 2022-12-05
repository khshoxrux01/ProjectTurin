import telebot
import buttons
from telebot import types
import json
import datetime
import data_base
import emoji
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn 


bot = telebot.TeleBot('5879404580:AAFzn7o_uW5lq90b7-9pnW_hESZpXA5M0QY')


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    text = 'Hi, How are you doing?\nAre you admin or user❔'
    
    bot.send_message(user_id, text, reply_markup=buttons.start_buttons())
    
    bot.register_next_step_handler(message, user_definer)
    
def user_definer(message):
    user_id = message.from_user.id
    admin_id = 268465740
    
    if message.text == 'Admin🤝':
        if user_id == admin_id:
            bot.send_message(user_id, 'Welcome to the part of administration!\nWhat do you want to know❓', reply_markup=buttons.all_users_button())
            
            bot.register_next_step_handler(message, show_users)
            
        else:
            bot.send_message(user_id, 'You are not a admin\nWho are you❔', reply_markup=buttons.start_buttons())
            
            bot.register_next_step_handler(message, user_definer)
            
    elif message.text == 'User👋🏽':
        checker = data_base.check_user(user_id)
        
        if not checker:
            bot.send_message(user_id, 'Please, send your name🙆‍♂️:', reply_markup=types.ReplyKeyboardRemove())
            
            bot.register_next_step_handler(message, get_user_name)
            
        else:
            bot.send_message(user_id, 'Send your JSON file from tg to see some statistics📁', reply_markup=types.ReplyKeyboardRemove())
            
            bot.register_next_step_handler(message, handle_docs_photo)
            
    else:
        bot.reply_to(message, 'Not defined❌')
        bot.send_message(user_id, 'Are you admin or user❓', reply_markup=buttons.start_buttons())
        bot.register_next_step_handler(message, user_definer)
         
def show_users(message):
    user_id = message.from_user.id
    if message.text == 'Show me all users📝':
        all_users = [i[0] for i in data_base.showing_users()] 
        
        bot.send_message(user_id, 'Here is all users below↙️\n'+'\n'.join(all_users), reply_markup=buttons.all_users_button())
        
        bot.register_next_step_handler(message, show_users)
      
    elif message.text == 'Back to main page🔙':
        bot.send_message(user_id, 'Who are you❓', reply_markup=buttons.start_buttons())
        
        bot.register_next_step_handler(message, user_definer)
          
    else:
        bot.reply_to(message, 'Not defined❌')
        bot.send_message(user_id, 'What do you want to know❔', reply_markup=buttons.all_users_button())
        bot.register_next_step_handler(message, show_users)
        
def get_user_name(message):
    user_id = message.from_user.id
    name = message.text
    
    bot.send_message(user_id, 'Please, send your phone number📱', reply_markup=buttons.contact_button())
    
    bot.register_next_step_handler(message, get_user_contact, name)
    
def get_user_contact(message, name):
    user_id = message.from_user.id
    
    if message.contact or (message.text.startswith('+998') and len(message.text) == 13):
        user_number = message.contact or message.text
        
        data_base.add_user_to_base(user_id, name, str(user_number))
        
        bot.send_message(user_id, 'You are registered successfully✅\nNow,you can send your JSON file from tg to see some analyzes📂', reply_markup=types.ReplyKeyboardRemove())
        
        bot.register_next_step_handler(message, handle_docs_photo)
        
    else:
        bot.reply_to(user_id, 'Wrong format❌')
        bot.send_message(user_id, 'Please enter your phone number in format +998*********⬇️')
        bot.register_next_step_handler(message, get_user_contact, name)
    
@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    chat_id = message.chat.id
    
    try:
        str(message.document.file_name).split('.')[1] == 'json'
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = '/Users/sohruhhusanbaev/Downloads/TTPU/Turin_CS/Project/' + message.document.file_name
        with open (src, 'wb') as new_file:
            new_file.write (downloaded_file)
        
        # bot.reply_to(message, 'I saved it')
        bot.send_message(chat_id, 'What do you want to know❓', reply_markup=buttons.options_buttons())  
        
        bot.register_next_step_handler(message, new_step, src)
        
    except:
        bot.reply_to(message, 'Wrong format❌')
        bot.send_message(chat_id, 'Send your JSON file📂')
        bot.register_next_step_handler(message, handle_docs_photo)
    
@bot.message_handler(content_types=['text'])  
def new_step(message, downloaded_file):
    user_id = message.from_user.id
    
    if message.text == 'Top used word🔝':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        
        def show_messages():
            some_text = ''
            for messages in data['messages']:
                article = messages['text']
                if type(article) is list:
                    for i in article:
                        if type(i) is dict:
                            some_text += f'{i["text"].strip()} '
                        elif i:
                            some_text += f'{i.strip()} '
                elif article:    
                    some_text += f'{article.strip()} '
            return some_text
        
        def text_clear(text):
            new = ''
            for i in text:
                if i not in '!"#$&\'()*,-.:;<=>?[\\]^`{|}~\n\t':
                    new += i
            return new
        
        all_text = show_messages()
        cleaned_text = text_clear(all_text.lower())

        def counter(list_element):
            count = {}
            for element in list_element:
                num = count.get(element, 0)
                count[element] = num + 1
            sorted_values = sorted(count.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_values)
        


        list_word = cleaned_text.split()
        count_words = counter(list_word)
        number_of_most_word = list(count_words.values())[0]
        this_most_word = list(count_words.keys())[0]
        
        horizontal_direction_x = list(count_words.keys())[:7]
        vertical_direction_y = list(count_words.values())[:7]
        path = 'line_graph.png'
        plt.plot(horizontal_direction_x, vertical_direction_y)
        plt.title('Top used words for all period', fontsize=20, color='orange')
        plt.xlabel('The most used 7 words', color='red')
        plt.ylabel('Number of the words', color='blue')
        plt.savefig(path)
        plt.close()
        graph_photo = open('/Users/sohruhhusanbaev/Downloads/TTPU/Turin_CS/Project/' + path, 'rb')
            
        bot.reply_to(message, f'The most used word is {this_most_word} \n{number_of_most_word} times')
        bot.send_photo(user_id, graph_photo)
        bot.send_message(user_id, 'What do you want to know❓', reply_markup=buttons.options_buttons())
        bot.register_next_step_handler(message, new_step, downloaded_file)
        
    elif message.text == 'Most active user🤖':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        
        def show_users():
            def count_messages():
                return(len(data['messages']))
            space = ''
            for i in range(count_messages()):
                try:
                    text = str(data['messages'][i]['from'])
                except:
                    text = str(data['messages'][i]['actor'])
                space += ' '
                space += text
            return space
        
        all_users = show_users()
        
        def text_clear(text):
            import string
            for p in string.punctuation + '\n':
                if p in text:
                    text = text.replace(p, '')
            return text

        def counter(list_element):
            count = {}

            for element in list_element:
                if count.get(element, None):

                    count[element] += 1
                else:

                    count[element] = 1

            sorted_values = sorted(count.items(), key=lambda tpl: tpl[1], reverse=True)
            return dict(sorted_values)
        
        text = all_users

        text = text_clear(text.lower())

        list_users = text.split()
        whole_dict = counter(list_users) 
        max_num = max(counter(list_users).values()) # Defines the most value among other users
        whole_dict = list(whole_dict) # Transform dictionary to the list in order to define the most active user among other users
        most_active_user = whole_dict[0] # Define the most active user
        
        bot.reply_to(message, f'The most active user is {most_active_user}\n{max_num} active sessions')
        bot.send_message(user_id, 'What do you want to know❓', reply_markup=buttons.options_buttons())
        bot.register_next_step_handler(message, new_step, downloaded_file)
        
    elif message.text == 'Top emojies👀':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def emoji_counter(text):
            result_emojies = {}
            for i in text:
                if emoji.is_emoji(i):
                    number = result_emojies.get(i, 0)
                    result_emojies[i] = number + 1
            sorted_values = sorted(result_emojies.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_values)
        
        def show_messages():
            content = ''
            for messages in data['messages']:
                article = messages['text']
                if type(article) is list:
                    for i in article:
                        if type(i) is dict:
                            content += f'{i["text"].strip()} '
                        elif i:
                            content += f'{i.strip()} '
                elif article:    
                    content += f'{article.strip()} '
            return content

        all_text = show_messages()
        
        top_emojies = emoji_counter(all_text)
        
        all_emojies = ''
        for l,m in emoji_counter(all_text).items():
            all_emojies += f'{l: >3}   {m}\n'
        
        emojies_collecting = list(top_emojies.keys())[:5]
        emojies_values = list(top_emojies.values())[:5]
        
        palette_color = seaborn.color_palette('bright')
        plt.pie(emojies_values, labels = emojies_collecting, colors = palette_color, autopct='%.0f%%')  
        
        path_to_pie = 'pie_chart.png'
        
        plt.title('Top used emojies for all period', fontsize=20, color='purple')
        plt.savefig(path_to_pie)
        plt.close()
        
        pie_photo = open('/Users/sohruhhusanbaev/Downloads/TTPU/Turin_CS/Project/' + path_to_pie, 'rb')
           
        bot.reply_to(message, all_emojies)
        bot.send_photo(user_id, pie_photo)
        bot.send_message(user_id, 'What do you want to know❓', reply_markup=buttons.options_buttons())
        bot.register_next_step_handler(message, new_step, downloaded_file)
        
    elif message.text == 'Words in time frame⏰':
        bot.send_message(user_id, 'Choose the period📆', reply_markup=buttons.frame_buttons())
        
        bot.register_next_step_handler(message, frame_part, downloaded_file)
        
    else:
        bot.reply_to(message, 'Not defined❌')
        bot.send_message(user_id, 'What do you want to know❓', reply_markup=buttons.options_buttons())
        bot.register_next_step_handler(message, new_step, downloaded_file)
        
def frame_part(message, downloaded_file):
    user_id = message.from_user.id
    
    if message.text == 'Months📆':
        bot.send_message(user_id, 'Choose the month⬇️', reply_markup=buttons.month_buttons())
        
        bot.register_next_step_handler(message, month_frame, downloaded_file)
        
    elif message.text == 'Weeks🗓️':
        bot.send_message(user_id, 'Choose the week frame⬇️', reply_markup=buttons.week_buttons())
        
        bot.register_next_step_handler(message, week_frame, downloaded_file)
        
    elif message.text == 'Weekdays📅':
        bot.send_message(user_id, 'Choose a day of the week⬇️', reply_markup=buttons.weekdays_button())
        
        bot.register_next_step_handler(message, weekdays_part, downloaded_file)
        
    elif message.text == 'Back🔙':
        bot.send_message(user_id, 'What do you want to know❓', reply_markup=buttons.options_buttons())
        
        bot.register_next_step_handler(message, new_step, downloaded_file)
        
    else:
        bot.reply_to(message, 'Not defined❌', reply_markup=buttons.frame_buttons())
        bot.send_message(user_id, 'Choose the period🗓️', reply_markup=buttons.frame_buttons())
        bot.register_next_step_handler(message, frame_part, downloaded_file)
   
def weekdays_part(message, downloaded_file):
    user_id = message.from_user.id
    
    def messages_per_weekday():
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        result = {}

        for msg in data['messages']:
            msg_date = msg['date'].split('T')[0]
            date = datetime.datetime.strptime(msg_date, '%Y-%m-%d')
            result[date.isoweekday()] = result.get(date.isoweekday(), 0) + 1

        result = dict(sorted(result.items(), key=lambda x: x[0]))
        result = {day_names[i - 1]: result[i] for i in result}
        return result   
    
    weekdays = messages_per_weekday()
    
    if message.text == '1️⃣Monday':
        bot.reply_to(message, f'There are {weekdays["Monday"]} messages for Mondays')
        bot.send_message(user_id, 'Choose a day of the week⤵️', reply_markup=buttons.weekdays_button())  
        bot.register_next_step_handler(message, weekdays_part, downloaded_file)
        
    elif message.text == '2️⃣Tuesday':
        bot.reply_to(message, f'There are {weekdays["Tuesday"]} messages for Tuesday')
        bot.send_message(user_id, 'Choose a day of the week⤵️', reply_markup=buttons.weekdays_button())  
        bot.register_next_step_handler(message, weekdays_part, downloaded_file)
        
    elif message.text == '3️⃣Wednesday':
        bot.reply_to(message, f'There are {weekdays["Wednesday"]} messages for Wednesday')
        bot.send_message(user_id, 'Choose a day of the week⤵️', reply_markup=buttons.weekdays_button())  
        bot.register_next_step_handler(message, weekdays_part, downloaded_file)
        
    elif message.text == '4️⃣Thursday':
        bot.reply_to(message, f'There are {weekdays["Thursday"]} messages for Thursday')
        bot.send_message(user_id, 'Choose a day of the week⤵️', reply_markup=buttons.weekdays_button())  
        bot.register_next_step_handler(message, weekdays_part, downloaded_file)
        
    elif message.text == '5️⃣Friday':
        bot.reply_to(message, f'There are {weekdays["Friday"]} messages for Friday')
        bot.send_message(user_id, 'Choose a day of the week⤵️', reply_markup=buttons.weekdays_button())  
        bot.register_next_step_handler(message, weekdays_part, downloaded_file)
        
    elif message.text == '6️⃣Saturday':
        bot.reply_to(message, f'There are {weekdays["Saturday"]} messages for Saturday')
        bot.send_message(user_id, 'Choose a day of the week⤵️', reply_markup=buttons.weekdays_button())  
        bot.register_next_step_handler(message, weekdays_part, downloaded_file)
    
    elif message.text == '7️⃣Sunday':
        bot.reply_to(message, f'There are {weekdays["Sunday"]} messages for Sunday')
        bot.send_message(user_id, 'Choose a day of the week⤵️', reply_markup=buttons.weekdays_button())  
        bot.register_next_step_handler(message, weekdays_part, downloaded_file)
        
    elif message.text == 'Back🔙':
        bot.send_message(user_id, 'Choose the period🗓️', reply_markup=buttons.frame_buttons())
        
        bot.register_next_step_handler(message, frame_part, downloaded_file)
        
    else:
        bot.reply_to(message, 'Not defined❌')
        bot.send_message(user_id, 'Choose a day of the week⤵️', reply_markup=buttons.weekdays_button())
        bot.register_next_step_handler(message, weekdays_part, downloaded_file)
        
def month_frame(message, downloaded_file):
    user_id = message.from_user.id
    
    if message.text == 'January':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def january_month_messages():
            def count_messages():
                return(len(data['messages']))
            counter = 0
            current_time = str(datetime.datetime.now())
            part = str(current_time[5:7])
            part = '01'
            for i in range(count_messages()):
                if str(data['messages'][i]['date']).startswith(current_time[0:5] + part):
                    counter += 1
                else:
                    pass
                
            return counter
          
        counter_january = january_month_messages()
        
        if counter_january > 0:
            bot.reply_to(message, f'There are {counter_january} messages 📩 for January')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
        else:
            bot.reply_to(message, 'There are not messages yet👀')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
 
    elif message.text == 'February':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def february_month_messages():
            def count_messages():
                return(len(data['messages']))
            counter = 0
            current_time = str(datetime.datetime.now())
            part = str(current_time[5:7])
            part = '02'
            for i in range(count_messages()):
                if str(data['messages'][i]['date']).startswith(current_time[0:5] + part):
                    counter += 1
                else:
                    pass
                
            return counter
          
        counter_february = february_month_messages()
        
        if counter_february > 0:
            bot.reply_to(message, f'There are {counter_february} messages 📩 for February')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
        else:
            bot.reply_to(message, 'There are not messages yet👀')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)

    elif message.text == 'March':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def march_month_messages():
            def count_messages():
                return(len(data['messages']))
            counter = 0
            current_time = str(datetime.datetime.now())
            part = str(current_time[5:7])
            part = '03'
            for i in range(count_messages()):
                if str(data['messages'][i]['date']).startswith(current_time[0:5] + part):
                    counter += 1
                else:
                    pass
                
            return counter
          
        counter_march = march_month_messages()
        
        if counter_march > 0:
            bot.reply_to(message, f'There are {counter_march} messages 📩 for March')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
        else:
            bot.reply_to(message, 'There are not messages yet👀')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
    
    elif message.text == 'April':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def april_month_messages():
            def count_messages():
                return(len(data['messages']))
            counter = 0
            current_time = str(datetime.datetime.now())
            part = str(current_time[5:7])
            part = '04'
            for i in range(count_messages()):
                if str(data['messages'][i]['date']).startswith(current_time[0:5] + part):
                    counter += 1
                else:
                    pass
                
            return counter
          
        counter_april = april_month_messages()
        
        if counter_april > 0:
            bot.reply_to(message, f'There are {counter_april} messages 📩 for April')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
        else:
            bot.reply_to(message, 'There are not messages yet👀')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
    
    elif message.text == 'May':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def may_month_messages():
            def count_messages():
                return(len(data['messages']))
            counter = 0
            current_time = str(datetime.datetime.now())
            part = str(current_time[5:7])
            part = '05'
            for i in range(count_messages()):
                if str(data['messages'][i]['date']).startswith(current_time[0:5] + part):
                    counter += 1
                else:
                    pass
                
            return counter
          
        counter_may = may_month_messages()
        
        if counter_may > 0:
            bot.reply_to(message, f'There are {counter_may} messages 📩 for May')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
        else:
            bot.reply_to(message, 'There are not messages yet👀')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
    
    elif message.text == 'June':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def june_month_messages():
            def count_messages():
                return(len(data['messages']))
            counter = 0
            current_time = str(datetime.datetime.now())
            part = str(current_time[5:7])
            part = '06'
            for i in range(count_messages()):
                if str(data['messages'][i]['date']).startswith(current_time[0:5] + part):
                    counter += 1
                else:
                    pass
                
            return counter
          
        counter_june = june_month_messages()
        
        if counter_june > 0:
            bot.reply_to(message, f'There are {counter_june} messages 📩 for June')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
        else:
            bot.reply_to(message, 'There are not messages yet👀')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
    
    elif message.text == 'July':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def july_month_messages():
            def count_messages():
                return(len(data['messages']))
            counter = 0
            current_time = str(datetime.datetime.now())
            part = str(current_time[5:7])
            part = '07'
            for i in range(count_messages()):
                if str(data['messages'][i]['date']).startswith(current_time[0:5] + part):
                    counter += 1
                else:
                    pass
                
            return counter
          
        counter_july = july_month_messages()
        
        if counter_july > 0:
            bot.reply_to(message, f'There are {counter_july} messages 📩 for July')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
        else:
            bot.reply_to(message, 'There are not messages yet👀')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
    
    elif message.text == 'August':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def august_month_messages():
            def count_messages():
                return(len(data['messages']))
            counter = 0
            current_time = str(datetime.datetime.now())
            part = str(current_time[5:7])
            part = '08'
            for i in range(count_messages()):
                if str(data['messages'][i]['date']).startswith(current_time[0:5] + part):
                    counter += 1
                else:
                    pass
                
            return counter
          
        counter_august = august_month_messages()
        
        if counter_august > 0:
            bot.reply_to(message, f'There are {counter_august} messages 📩 for August')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
        else:
            bot.reply_to(message, 'There are not messages yet👀')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
    
    elif message.text == 'September':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def september_month_messages():
            def count_messages():
                return(len(data['messages']))
            counter = 0
            current_time = str(datetime.datetime.now())
            part = str(current_time[5:7])
            part = '09'
            for i in range(count_messages()):
                if str(data['messages'][i]['date']).startswith(current_time[0:5] + part):
                    counter += 1
                else:
                    pass
                
            return counter
          
        counter_september = september_month_messages()
        
        if counter_september > 0:
            bot.reply_to(message, f'There are {counter_september} messages 📩 for September')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
        else:
            bot.reply_to(message, 'There are not messages yet👀')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
    
    elif message.text == 'October':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def october_month_messages():
            def count_messages():
                return(len(data['messages']))
            counter = 0
            current_time = str(datetime.datetime.now())
            part = str(current_time[5:7])
            part = '10'
            for i in range(count_messages()):
                if str(data['messages'][i]['date']).startswith(current_time[0:5] + part):
                    counter += 1
                else:
                    pass
                
            return counter
          
        counter_october = october_month_messages()
        
        if counter_october > 0:
            bot.reply_to(message, f'There are {counter_october} messages 📩 for October')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
        else:
            bot.reply_to(message, 'There are not messages yet👀')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
    
    elif message.text == 'November':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def november_month_messages():
            def count_messages():
                return(len(data['messages']))
            counter = 0
            current_time = str(datetime.datetime.now())
            part = str(current_time[5:7])
            part = '11'
            for i in range(count_messages()):
                if str(data['messages'][i]['date']).startswith(current_time[0:5] + part):
                    counter += 1
                else:
                    pass
                
            return counter
          
        counter_november = november_month_messages()
        
        if counter_november > 0:
            bot.reply_to(message, f'There are {counter_november} messages 📩 for November')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
        else:
            bot.reply_to(message, 'There are not messages yet👀')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
    
    elif message.text == 'December':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
        def december_month_messages():
            def count_messages():
                return(len(data['messages']))
            counter = 0
            current_time = str(datetime.datetime.now())
            part = str(current_time[5:7])
            part = '09'
            for i in range(count_messages()):
                if str(data['messages'][i]['date']).startswith(current_time[0:5] + part):
                    counter += 1
                else:
                    pass
                
            return counter
          
        counter_december = december_month_messages()
        
        if counter_december > 0:
            bot.reply_to(message, f'There are {counter_december} messages 📩 for December')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
        else:
            bot.reply_to(message, 'There are not messages yet👀')
            bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
            bot.register_next_step_handler(message, month_frame, downloaded_file)
            
    elif message.text == 'Back🔙':
        bot.send_message(user_id, 'Choose the period🗓️', reply_markup=buttons.frame_buttons())
        
        bot.register_next_step_handler(message, frame_part, downloaded_file)
        
    else:
        bot.reply_to(message, 'Not defined❌')
        bot.send_message(user_id, 'Choose the month📆', reply_markup=buttons.month_buttons())
        bot.register_next_step_handler(message, month_frame, downloaded_file)
    
def week_frame(message, downloaded_file):
    user_id = message.from_user.id
    
    if message.text == '1️⃣ week':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
            
        def weekly_messages():
            counter = 0
            current_time = datetime.datetime.now()
            last_week = str(current_time - datetime.timedelta(weeks=1)).split()
            beginning = False
            for i in data['messages']:
                if i['date'].startswith(last_week[0]) and not beginning:
                    beginning = True
                    
                if beginning:
                    counter += 1
                    
            if counter > 0:
                    return counter
                
            else:
                return 0

        messages_per_one_week = weekly_messages()
        
        bot.reply_to(message, f'There are {messages_per_one_week} messages 📩 for 1️⃣ week')
        bot.send_message(user_id, 'Choose the week frame📅', reply_markup=buttons.week_buttons())
        bot.register_next_step_handler(message ,week_frame, downloaded_file)
    
    elif message.text == '2️⃣ weeks':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
            
        def two_weekly_messages():
            counter = 0
            current_time = datetime.datetime.now()
            last_week = str(current_time - datetime.timedelta(weeks=2)).split()
            beginning = False
            for i in data['messages']:
                if i['date'].startswith(last_week[0]) and not beginning:
                    beginning = True
                    
                if beginning:
                    counter += 1
                    
            if counter > 0:
                    return counter
                
            else:
                return 0
                
        messages_per_two_weeks = two_weekly_messages()
        
        bot.reply_to(message, f'There are {messages_per_two_weeks} messages 📩 for 2️⃣ weeks')
        bot.send_message(user_id, 'Choose the week frame📅', reply_markup=buttons.week_buttons())
        bot.register_next_step_handler(message, week_frame, downloaded_file)
    
    elif message.text == '3️⃣ weeks':
        with open(str(downloaded_file), encoding='utf8') as file:
            data = json.load(file)
            
        def three_weekly_messages():
            counter = 0
            current_time = datetime.datetime.now()
            last_week = str(current_time - datetime.timedelta(days=21)).split()
            beginning = False
            for i in data['messages']:
                if i['date'].startswith(last_week[0]) and not beginning:
                    beginning = True
                    
                if beginning:
                    counter += 1
                    
            if counter > 0:
                    return counter
                
            else:
                return 0
                
        messages_per_three_weeks = three_weekly_messages()
        
        bot.reply_to(message, f'There are {messages_per_three_weeks} messages 📩 for 3️⃣ weeks')
        bot.send_message(user_id, 'Choose the week frame📅', reply_markup=buttons.week_buttons())
        bot.register_next_step_handler(message, week_frame, downloaded_file)
        
    elif message.text == 'Specific week frame⏱️':
        bot.send_message(user_id, 'Enter number of weeks', reply_markup=types.ReplyKeyboardRemove())
        
        bot.register_next_step_handler(message, specific_week_frame, downloaded_file)
        
    elif message.text == 'Back🔙':
        bot.send_message(user_id, 'Choose the period🗓️', reply_markup=buttons.frame_buttons())
        
        bot.register_next_step_handler(message, frame_part, downloaded_file)
        
    else:
        bot.reply_to(message, 'Not defined❌')
        bot.send_message(user_id, 'Choose the week frame📅', reply_markup=buttons.week_buttons())
        bot.register_next_step_handler(message, week_frame, downloaded_file)
        
def specific_week_frame(message, downloaded_file):
    user_id = message.from_user.id
    
    try:
        number_of_weeks_ago = int(message.text)
        
        def specific_week():    
            with open(str(downloaded_file), encoding='utf8') as file:
                    data = json.load(file)
                    
            now = datetime.datetime.now()
            last_n_weeks = now - datetime.timedelta(weeks=number_of_weeks_ago, hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
            counter = 0
            for i in data['messages']:
                message_date = datetime.datetime.strptime(i['date'].split('T')[0], '%Y-%m-%d')
                if message_date >= last_n_weeks:
                    counter += 1
                    
            return counter
            
            
        specific_week_frame_value = specific_week()

        bot.reply_to(message, f'There are {specific_week_frame_value} messages 📩 for {number_of_weeks_ago} weeks')
        bot.send_message(user_id, 'Choose the week frame📅', reply_markup=buttons.week_buttons())
        bot.register_next_step_handler(message, week_frame, downloaded_file)
        
    except:
        bot.reply_to(message, 'it is not a number❗️')
        bot.send_message(user_id, 'Enter the number of weeks⬇️', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, specific_week_frame, downloaded_file)
   

        


    
    
    
bot.polling()