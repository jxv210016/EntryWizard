import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import concurrent.futures
import time
import re  # Import the regex module

# Define the Discord bot token
DISCORD_BOT_TOKEN = "your-discord-bot-token"


# Define the website URL prefix
website_url_prefix = "https://play.underdogfantasy.com"

# Define the regular expression pattern for the URL
url_pattern = re.compile(r'https://play\.underdogfantasy\.com/\S+')

# Define Discord intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Initialize the Discord bot with the defined intents
bot = commands.Bot(command_prefix="!", intents=intents)

def process_link(link, server_name, channel_name, insured):
    """
    Process the given link using Selenium, perform the necessary actions on the website.
    :param link: The website link to be processed
    :param server_name: The name of the Discord server
    :param channel_name: The name of the Discord channel
    :param insured: A boolean indicating whether insurance is to be applied
    :return: A boolean indicating the success of the operation
    """
    # Create a new Selenium driver with specific options
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the given link
        driver.get(link)
        time.sleep(5)

        # Log in to the website using stored credentials
        # NOTE: Store sensitive information securely, e.g., in environment variables
        email = "your-email"
        password = "your-password"

        # Locate and click the sign-in button, then enter login credentials
        sign_in_button_stage_1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "styles__logInButton__q5xc3"))
        )
        sign_in_button_stage_1.click()

        # Locate and fill the email and password fields, then click the sign-in button
        email_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@data-testid='email_input']"))
        )
        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@data-testid='password_input']"))
        )
        email_input.send_keys(email)
        password_input.send_keys(password)

        sign_in_button_stage_2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='sign-in-button']"))
        )
        sign_in_button_stage_2.click()
        time.sleep(3)

        # Navigate back to the given link and perform actions
        driver.get(link)
        add_picks_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'picks to entry')]"))
        )
        add_picks_button.click()

        # Locate and fill the amount input field, and apply insurance if necessary
        time.sleep(2)
        amount_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter amount']"))
        )
        amount_input.clear()
        amount_input.send_keys("50")

        if insured:
            insured_input_rect = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[3]/div/div[2]/div[2]/label[2]"))
            )
            driver.execute_script("arguments[0].click();", insured_input_rect)

        # Locate and click the submit and confirm buttons to complete the action
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='submit-entry-button']"))
        )
        driver.execute_script("arguments[0].click();", submit_button)

        time.sleep(1.5)
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='dialog-modal-confirm-button']"))
        )
        driver.execute_script("arguments[0].click();", confirm_button)
        time.sleep(5)

        return True
    except TimeoutException:
        print("Timed out while waiting for elements to load.")
        return False
    finally:
        # Close the Selenium driver
        driver.quit()


@bot.event
async def on_ready():
    # Print bot's name when it has successfully connected to Discord
    print(f"Logged in as {bot.user.name}")


@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Define channel names for processing and for no-insurance
    desired_channel_names = ["testing", "slips", "chat"]
    no_insurance_channel_name = "no-insurance-ud"

    # Use the regex search to find a URL in the message content
    match = url_pattern.search(message.content)

    # If a URL is found, process it
    if match:
        url = match.group(0)  # The full URL match
        try:
            # Determine if insurance should be applied based on the channel name
            insured = message.channel.name != no_insurance_channel_name

            # Process the link in a new thread
            future = concurrent.futures.ThreadPoolExecutor().submit(
                process_link, url.strip(), message.guild.name, message.channel.name, insured)
            success_message = future.result()

            # Send a confirmation message if the operation was successful
            if success_message:
                confirm_channel = discord.utils.get(message.guild.channels, name="confirms")
                if confirm_channel:
                    await confirm_channel.send(
                        f"Underdog Fantasy entry completed successfully in {message.guild.name} - #{message.channel.name}")
        except TimeoutException:
            print("Timed out while waiting for elements to load. Moving to the next slip...")

    # Process any other commands in the message
    await bot.process_commands(message)


# Run the bot with the given token
bot.run(DISCORD_BOT_TOKEN)