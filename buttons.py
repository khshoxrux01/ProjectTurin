from telebot import types

def start_buttons():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    user = types.KeyboardButton('User👋🏽')
    admin = types.KeyboardButton('Admin🤝')
    
    space.add(admin, user)
    
    return space

def options_buttons():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    month = types.KeyboardButton('Top used word🔝')
    day = types.KeyboardButton('Most active user🤖')
    emojies = types.KeyboardButton('Top emojies👀')
    frame = types.KeyboardButton('Words in time frame⏰')
    space.add(month, day,emojies, frame)
    
    return space

def contact_button():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    contact = types.KeyboardButton('Send my phone number📞', request_contact=True)
    
    space.add(contact)
    
    return space

def all_users_button():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    all_users = types.KeyboardButton('Show me all users📝')
    back = types.KeyboardButton('Back to main page🔙')
    
    space.add(all_users, back)
    
    return space

def frame_buttons():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    weeks = types.KeyboardButton('Weeks🗓️')
    months = types.KeyboardButton('Months📆')
    weekdays = types.KeyboardButton('Weekdays📅')
    back = types.KeyboardButton('Back🔙')
    
    space.add(weeks, weekdays, months, back)
    
    return space

def month_buttons():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    january = types.KeyboardButton('January')
    february = types.KeyboardButton('February')
    march = types.KeyboardButton('March')
    april = types.KeyboardButton('April')
    may = types.KeyboardButton('May')
    june = types.KeyboardButton('June')
    july = types.KeyboardButton('July')
    august = types.KeyboardButton('August')
    september = types.KeyboardButton('September')
    october = types.KeyboardButton('October')
    november = types.KeyboardButton('November')
    december = types.KeyboardButton('December')
    back = types.KeyboardButton('Back🔙')
    
    space.add(january, february, march, april, may, june, july, august, september, october, november, december, back)
    
    return space

def week_buttons():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    one_week = types.KeyboardButton('1️⃣ week')
    two_weeks = types.KeyboardButton('2️⃣ weeks')
    three_weeks = types.KeyboardButton('3️⃣ weeks')
    specific_week = types.KeyboardButton('Specific week frame⏱️')
    back = types.KeyboardButton('Back🔙')
    
    space.add(one_week, two_weeks, three_weeks, specific_week, back)
    
    return space

def weekdays_button():
    space = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    monday = types.KeyboardButton('1️⃣Monday')
    tuesday = types.KeyboardButton('2️⃣Tuesday')
    wednesday = types.KeyboardButton('3️⃣Wednesday')
    thursday = types.KeyboardButton('4️⃣Thursday')
    friday = types.KeyboardButton('5️⃣Friday')
    saturday = types.KeyboardButton('6️⃣Saturday')
    sunday = types.KeyboardButton('7️⃣Sunday')
    back = types.KeyboardButton('Back🔙')
    
    space.add(monday, tuesday, wednesday, thursday, friday, saturday, sunday, back)
    
    return space    
    