# EmotionBot

![Robot Face](./512px-092-robot-face-1.svg.png)

A basic serverless [Telegram bot](https://core.telegram.org/bots) using [Google Cloud Functions](https://cloud.google.com/functions/).

Add me to groups and type `/emo` followed by a sentence you wish to be analysed for its evoked emotions. Original model from [Arpan Ghoshal's HugginFace model](https://huggingface.co/arpanghoshal/EmoRoBERTa). Contact [@incomple](https://t.me/Incomple) for feedback and suggestions.

Utilises the free tier of HuggingFace Inference API. May stop working near the end of each month if the 30k character/month quota runs out.

### Input:


```
/emo I love you

```

### Output:

```
Running inference for 'I love you' (May be slow if running from cold start); please wait...
```

```
(20823 msec) Top 5 emotions for: 'I love you' 

love: 0.9827135801315308 
joy: 0.007650577928870916 
admiration: 0.005227231420576572 
caring: 0.00080430245725438 
amusement: 0.0006339455721899867
```

This bot runs with Python 3.7 and [python-telegram-bot](https://python-telegram-bot.org/).

Adapted from Pablo Seminario's repo: <https://github.com/pabluk/serverless-telegram-bot>

See <https://seminar.io/2018/09/03/building-serverless-telegram-bot/> for more details about this bot.

## Deploy

```
gcloud beta functions deploy webhook --set-env-vars "TELEGRAM_TOKEN=000:yyy" --runtime python37 --trigger-http
```

## Testing

```
pip install -r requirements-test.txt
python test_main.py
```
