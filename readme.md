# Bot Kappa

A bot that is not kappa.

## Requirements

- python `3.9`
- discord.py `1.7.3`
- python-dotenv `0.20.0`

Ensure that an environment file `.env.token` exists in the root directory of the repository. This should contain your token and be formatted as follows where `[token]` is your bot's token.

```
token=[token]
```

## Running

Simply execute `main.py` in the root of the repository to run the bot.

## Modifying

Note that this bot is built with the assumption that it will only ever be used in a single server.

### Prefix

The prefix can be changed in `constants.py`.

### Token environment file

The name of the environment file holding the token as well as the environment variable name that the bot uses can both be changed in `constants.py`.

### Additional functionality

Additional cogs can be added in the `cogs` package. The name of the cog must then be added to one of the arrays in the `COGS` dictionary in `main.py`. Additional cog types can also be added and enabled or disabled in `main.py`.


## Permissions

This bot requires the following permissions.

- Manage roles
- Manage webhooks
- Send messages
- Manage messages

The corresponding permissions integer is `805316608`. The invite link will be of the following form where `[client id]` is replaced with your bot's client ID.

```
https://discord.com/api/oauth2/authorize?client_id=[client id]&permissions=805316608&scope=bot
```

## Commands

### Utilities

#### `hi`

- Essentially just a ping, bot will respond with "uwu".

### Fun

#### `mock [string]`

- Takes `[string]` and applies random upper- and lower-casing, bolding, and italicizing to produce a result that resembles spongebob mocking text.
- Deletes the message containing the command and sends the mocking version as an impersonator of the command author.

## Functionality

### Fun

#### Automatic mocking

- Randomly replies to messages with the spongebob mocking version of the original message.
- Whether automatic mocking occurs and the random interval used can be adjusted in `spongebot.py`.
