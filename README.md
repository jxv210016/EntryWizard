# EntryWizard

This Discord bot is designed to automate entries into Underdog Fantasy competitions through Discord commands.

## Features

- Automatically detects Underdog Fantasy links in Discord messages.
- Logs into Underdog Fantasy using credentials provided via environment variables.
- Performs actions on the website based on the links detected.
- Uses Selenium for web automation to interact with the Underdog Fantasy website.
- Responds to success or failure of actions in specified Discord channels.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have a `macOS` machine with Python 3.x installed.
- You have installed the `discord.py` library.
- You have installed the `selenium` library and Chrome WebDriver.

## Configurations
Set up environment variables to secure sensitive information:

Persistent

For Bash users, add to ~/.bash_profile:
echo 'export DISCORD_BOT_TOKEN="your-discord-bot-token"' >> ~/.bash_profile
echo 'export UNDERDOG_EMAIL="your-email"' >> ~/.bash_profile
echo 'export UNDERDOG_PASSWORD="your-password"' >> ~/.bash_profile
source ~/.bash_profile

For Zsh users, add to ~/.zshrc:
echo 'export DISCORD_BOT_TOKEN="your-discord-bot-token"' >> ~/.zshrc
echo 'export UNDERDOG_EMAIL="your-email"' >> ~/.zshrc
echo 'export UNDERDOG_PASSWORD="your-password"' >> ~/.zshrc
source ~/.zshrc

## Running the Bot
Run the bot with: python bot.py