# WhatsApp News Bot

This folder sends the same AI news format as the Telegram bot, using Meta WhatsApp Cloud API.

## Important WhatsApp Limitation

WhatsApp is not the same as a Telegram channel. With the official Cloud API:

- You can send free-form text/image messages only inside an active 24-hour customer service window.
- Outside that window, WhatsApp usually requires an approved message template.
- Recipients must opt in to receive messages from your business.
- This code sends to phone numbers listed in `WHATSAPP_TO`; it does not post to a WhatsApp Channel.

For first testing, use Meta's test number and your own recipient number in the Meta Developer dashboard.

## Step 1: Create Meta App

1. Go to Meta for Developers.
2. Create an app.
3. Add the WhatsApp product.
4. Open WhatsApp > API Setup.
5. Copy:
   - Temporary access token
   - Phone number ID
   - Test recipient phone number

## Step 2: Add Environment Variables

Copy `whatsapp_bot/.env.example` values into your project `.env`:

```env
WHATSAPP_ACCESS_TOKEN=your_meta_cloud_api_access_token
WHATSAPP_PHONE_NUMBER_ID=your_whatsapp_phone_number_id
WHATSAPP_TO=60123456789
WHATSAPP_API_VERSION=v24.0
```

Use international phone format without `+`.

For multiple recipients:

```env
WHATSAPP_TO=60123456789,60198765432
```

## Step 3: Test Send Only

From the project root:

```bash
python3 whatsapp_bot/send_whatsapp.py
```

If successful, your phone should receive a test WhatsApp message.

## Step 4: Test News Flow

From the project root:

```bash
python3 whatsapp_bot/main_whatsapp.py
```

This will:

1. Fetch Bharian and Sinchew news.
2. Skip already-posted WhatsApp URLs using `whatsapp_bot/whatsapp_news.db`.
3. Extract full article content.
4. Generate Chinese and BM versions using the same AI function.
5. Send image + caption to WhatsApp when an image exists.

The WhatsApp bot has its own posted database, so it will not cause your Telegram bot to skip articles.

## Step 5: Cron

Use a separate cron entry first, so Telegram and WhatsApp can be debugged independently.

Example:

```cron
0 20 * * * cd /Users/joen/Joen/telegram-ai-news && /usr/bin/python3 whatsapp_bot/main_whatsapp.py >> whatsapp_bot/whatsapp.log 2>&1
```

Check logs:

```bash
tail -n 100 whatsapp_bot/whatsapp.log
```

## Common Errors

`(#131030) Recipient phone number not in allowed list`

Add the recipient number in Meta's WhatsApp API setup page while using test mode.

`(#10) Application does not have permission`

Your token is missing WhatsApp permissions or expired.

`Message failed outside customer care window`

The recipient has not messaged your business recently. Use an approved template to start the conversation.

`Unsupported post request`

Check `WHATSAPP_PHONE_NUMBER_ID`, not the display phone number.
