# Instruction about how to use Text Definer bot 📝
---
### 1️⃣Installation of libraries
* #### You should in install all libraries below to use all functionality of this bot❗️
      import telebot
      from telebot import types
      import json
      import datetime
      import emoji
      import matplotlib
      matplotlib.use('Agg')
      import matplotlib.pyplot as plt
      import seaborn 
      import sqlite3
---
*  ### ***You can use your ```Terminal/Command Line``` and write there command below⬇️***
      ```pip install pyTelegramBotApi emoji mathplotlib seaborn sqlite --update```
### 2️⃣API token from BotFather
* ##### In order to personalize this bot you should get API token from the [BotFather](https://t.me/BotFather) bot and paste it below⬇️
      bot = telebot.TeleBot('HERE')
---
### 3️⃣Bot activation
#### You can use ```Start``` button or command ```/start``` to activate this bot
![](./Images/photo_2022-12-04%2021.12.01.jpeg)
---
### 4️⃣After activating the bot you will see two buttons 
#### 1.User👋🏽
#### 2.Admin🤝
![](./Images/photo_2022-12-04%2021.12.04.jpeg)
#### ***When you will press on of this buttons above, bot will check you by your telegram id and tranfer you to the next step❗️***
---
### 5️⃣Admin part
* #### In order to personalize this bot and become and admin you should do the following⬇️

  ##### 1. You should find `start_messages()` function
  ##### 2. In this function you should change the value of `admin_id` variable to your telegram id
  ##### 3. To identify your telegram id you can use [tg_id definer bot](https://t.me/show_my_id_bot)
* #### After that when you will press `Admin🤝` button, you will see another `Show me all users📝` button, which will show you all users who use this bot
![](./Images/photo_2022-12-04%2021.44.16.jpeg)
![](./Images/photo_2022-12-04%2021.44.18.jpeg)
---
### 6️⃣User part
* #### If you pressed `User👋🏽` button, first of all, you should pass registration process 
##### 1. You should send your name
![](./Images/photo_2022-12-04%2021.54.30.jpegg)
##### 2. You should send your phone number by typing or using `Send my phone number📞` button
![](./Images/photo_2022-12-04%2021.54.26.jpeg)
---
### 7️⃣Preparing JSON file to analyze the data
* #### ***In order to analyze data of your telegram, you should export the data from the telegram chat which you want to look throw❗️***
* #### After getting JSON file you should send this file to the bot, this bot will save this file and you can start analyze your data
![](./Images/photo_2022-12-04%2022.04.25.jpeg)
---
### 8️⃣Data analyzing part📂
* ### Firstly, you will see 4 following buttons⬇️
    #### 1.`Top used word🔝`
    #### 2.`Most active user🤖`
    #### 3.`Top emojies👀`
    #### 4.`Words in time frame⏰`
![](./Images/photo_2022-12-04%2022.17.52.jpeg)

* ### If you will press `Top used word🔝` button, you will see the top used word with the value of used times in the entire time frame and the graph showing top 10 used words
![](./Images/photo_2022-12-04%2022.23.55.jpeg)

* ### If you will press `Most active user🤖` button, you will see the most active user with the quantity of his sessions for whole time frame
![](./Images/photo_2022-12-04%2022.28.46.jpeg)

* ### If you will press `Top emojies👀` button, you will see the most used emojies for the all period of time and pie chart showing top 7 used emojies
![](./Images/photo_2022-12-04%2022.28.20.jpeg)

* ### If you will press `Words in time frame⏰` button, you will see other 4 following buttons⬇️
#### 1.`Weeks🗓️`
#### 2.`Months📆`
#### 3.`Weekdays📅`
![](./Images/photo_2022-12-04%2022.48.12.jpeg)

### ***1)To see how many messages were sent for 1, 2, 3 and specific week frame, you should press `Weeks🗓️` button, after which you will see new buttons bellow***
#### 1. `1️⃣ week`
#### 2. `2️⃣ weeks`
#### 3. `3️⃣ weeks`
#### 4. `Specific week frame⏱️`
![](./Images/photo_2022-12-04%2022.48.15.jpeg)
  * #### By pressing first three buttons, you will get the number of messages for 1, 2, 3 weeks, but if you want to get the quantity of messages for specific number of week you should enter the number of weeks
![](./Images/photo_2022-12-04%2022.53.22.jpeg)

### ***2)To see how many messages users sent for each month, you should press `Months📆` button, after that you will see buttons of each month bellow***
![](./Images/photo_2022-12-04%2022.58.46.jpeg)
   * #### You will get the number of messages user sent in each month by pressing the these buttons above⬆️
### ***3) To see how many messages users sent in each day of the week, you should press `Weekdays📅` button, after this you will see weekdays buttons bellow***
![](./Images/photo_2022-12-04%2023.09.22.jpeg)
   * #### You will get the number of messages were sent by users if you will press these buttons above⬆️
---
### ***❗️You can easily use `'Back🔙'` button anytime to comeback to the previous stage ❗️***
---





