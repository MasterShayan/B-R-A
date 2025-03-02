import telebot
import subprocess
import platform
import os

# Place your bot token here
BOT_TOKEN = "YOUR_BOT_TOKEN"
# Place your bot admin ID here
ADMIN_USER_ID = 1111

# Create bot instance
bot = telebot.TeleBot(BOT_TOKEN)

# Define current working directory globally and initialize with script's current directory
current_working_directory = os.getcwd()

# --- Command Management ---

@bot.message_handler(commands=['start'])
def start_command(message):
    """
    /start command handler.
    Sends this message when the bot starts and displays system information.
    """
    user_id = str(message.from_user.id)
    if user_id == str(ADMIN_USER_ID):
        system_info = get_system_info()  # Get system information
        welcome_message = f"Hello Admin!\n\nThe bot is ready to receive commands.\n\n**System Information:**\n{system_info}\n\nFrom now on, any command you send will be executed in the system terminal."
        bot.reply_to(message, welcome_message)
        bot.reply_to(message, "Made by MasterShayan")
    else:
        bot.reply_to(message, "You do not have permission to use this bot.")
        bot.reply_to(message, "Made by MasterShayan")

def get_system_info():
    """
    Get operating system and user information.
    """
    system_name = platform.system()
    username = os.getlogin()
    python_version = platform.python_version()

    info = f"**Operating System:** {system_name}\n"
    info += f"**Username:** {username}\n"
    info += f"**Current Path:** {current_working_directory}\n"  # Display current working directory
    info += f"**Python Version:** {python_version}"
    return info

@bot.message_handler(func=lambda message: str(message.from_user.id) == str(ADMIN_USER_ID))
def admin_command_handler(message):
    """
    Text message handler for admin (command execution).
    Only admin with specified user ID can use this handler.
    """
    global current_working_directory  # Access global variable
    command = message.text

    if command.startswith("cd "):  # Check if command is cd
        target_directory = command[3:].strip()  # Extract target path from cd command
        try:
            os.chdir(target_directory)  # Change script's working directory
            current_working_directory = os.getcwd()  # Update global variable with new working directory
            output = f"Working directory changed to `{current_working_directory}`."
        except Exception as e:
            output = f"Error changing directory: {e}"
    else:  # If command is not cd, execute command normally
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=current_working_directory)  # Use current working directory
            stdout, stderr = process.communicate()
            output = stdout.decode('utf-8') + stderr.decode('utf-8')
            if not output:
                output = "Command executed successfully and had no output."
        except Exception as e:
            output = f"Error executing command: {e}"

    bot.reply_to(message, f"**Command:** `{command}`\n\n**Output:**\n\n`{output}`", parse_mode="Markdown")
    bot.reply_to(message, "Made by MasterShayan")

@bot.message_handler(func=lambda message: True)
def unauthorized_user_handler(message):
    """
    Unauthorized user message handler.
    If a user other than the admin sends a message, this handler responds.
    """
    if str(message.from_user.id) != str(ADMIN_USER_ID):  # Check user ID to avoid responding to admin
        bot.reply_to(message, "You do not have permission to use this bot.")
        bot.reply_to(message, "Made by MasterShayan")

# --- Main Execution Function ---
if __name__ == '__main__':
    print("Bot is running and waiting for admin commands...")
    bot.polling(none_stop=True)
    #Made by MasterShayan
    #MasterShayan
    #Shayan
