Very minimalistic telegram to discord message relayer need [discord-webhook](https://pypi.org/project/discord-webhook/) and [Telethon](https://github.com/LonamiWebs/Telethon)
```bash
pip install discord-webhook
pip install telethon
```

Fill the approriate field in config.json.  
`api_id` and `api_hash` you get from telegram  
`wait` is the amount in seconds to wait in-between check, you should set this number to around 3 to 5 minutes to prevent getting rate-limited or suspended  
`channel_ids` is a python-like list of ids to monitor, the exact same you'd get from doing `dialog.id` on a dialog object in Telethon(this mean keep the -100 for channels at the start)  
`url` is the url to the discord webhook
