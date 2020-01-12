To use this service follow the following steps:
1. Creat a bot on Telegram and check for the option for including the bot in groups.
   To do that search for the official "BotFather" on telegram and use the following commands:
   
   to creat a new bot:
   ```
   /newbot
   ```
   to check for group status:
   ```
   /setjoingroups
   ```
   and then select the desired bot
   
2. Creat a public channel and add the bot to the said channel. Proceed to promotethe bot to an
   administrator.

3. Creat a file with the name **token**, in it the API of the bot should be copied.
4. Creat a file with the name **handle**, copy to it the Telegram bot handle.
5. Creat a file with the name **proxy** and copy to it the adress of your proxy server for Telegram.
(files in point 3 and 4 should be in the same directory as **gcn_tele.py**)

6. To run use the command:
```
python3 gcn_tele.py
```

