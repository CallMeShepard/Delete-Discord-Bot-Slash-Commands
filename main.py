import time
import requests

headers = {
    "Authorization": "",
    "Content-Type": "application/json"
}

def set_bot_token():
    while True:
        bot_token = input("\nEnter your bot token: ")
        headers["Authorization"] = f"Bot {bot_token}"
        url = "https://discord.com/api/v9/gateway/bot"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            bot_info = response.json()
            break
        else:
            print("Invalid bot token.")

def set_application_id():
    while True:
        global application_id
        application_id = input("\nEnter your application ID: ")
        url = f"https://discord.com/api/v9/applications/{application_id}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            application_info = response.json()
            application_name = application_info["name"]
            print(f"The application '{application_name}' has been found.")
            break
        else:
            print("Invalid application ID.")

def get_all_commands():
    url = f"https://discord.com/api/v9/applications/{application_id}/commands"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commands = response.json()
        commands_count = len(commands)

        print(f"\nFound {commands_count} Slash Commands:")
        print("-" * 40)
        for command in commands:
            command_name = command["name"]
            command_id = command["id"]
            print(f"{command_name:<20} {command_id}")
        print("-" * 40)
    else:
        print(f"Failed to retrieve slash commands. Error code: {response.status_code}")

def delete_command(command_id_or_name):
    url = f"https://discord.com/api/v9/applications/{application_id}/commands"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commands = response.json()

        for command in commands:
            if command["id"] == command_id_or_name or command["name"] == command_id_or_name:
                delete_url = f"https://discord.com/api/v9/applications/{application_id}/commands/{command['id']}"
                delete_response = requests.delete(delete_url, headers=headers)

                if delete_response.status_code == 204:
                    print(f"Command '{command_id_or_name}' has been deleted successfully.")
                else:
                    print(f"Failed to delete command '{command_id_or_name}'. Error code: {delete_response.status_code}")
                return

        print(f"Command '{command_id_or_name}' not found.")
    else:
        print(f"Failed to retrieve slash commands. Error code: {response.status_code}")

def delete_all_commands():
    url = f"https://discord.com/api/v9/applications/{application_id}/commands"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commands = response.json()

        for command in commands:
            delete_url = f"https://discord.com/api/v9/applications/{application_id}/commands/{command['id']}"
            delete_response = requests.delete(delete_url, headers=headers)

            while delete_response.status_code == 429:
                print("Error 429: Too Many Requests. Trying again in 15 seconds...")
                time.sleep(15)
                delete_response = requests.delete(delete_url, headers=headers)

            if delete_response.status_code == 204:
                print(f"Command with ID {command['id']} has been deleted successfully.")
            else:
                print(f"Failed to delete command with ID {command['id']}. Error code: {delete_response.status_code}")
    else:
        print(f"Failed to retrieve slash commands. Error code: {response.status_code}")

set_bot_token()
set_application_id()

while True:
    command = input(
        "\nEnter a command ('getallcoms', 'delcom <command_id or command_name>', 'delallcoms', or 'exit'): "
    )

    if command == "getallcoms":
        get_all_commands()
    elif command.startswith("delcom"):
        command_parts = command.split(" ")
        if len(command_parts) == 2:
            command_id_or_name = command_parts[1]
            delete_command(command_id_or_name)
        else:
            print("Invalid command format. Please enter the command ID or name.")
    elif command == "delallcoms":
        delete_all_commands()
    elif command == "exit":
        break
    else:
        print("Invalid command. Please try again.")