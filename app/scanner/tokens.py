import re

commands = "configure, create, delete, copy, transfer, rename, modify, add, backup, exec"

def extract_commands(command_string):
  tokens = []
  command_list = commands.split(", ")

  pattern = fr"\b({'|'.join(command_list)})\b"
  matches = re.split(pattern, command_string, flags=re.IGNORECASE)
  for i in range(1, len(matches), 2):
      command = matches[i].rstrip()  # Remove leading whitespace
      if i + 1 < len(matches):
          command += matches[i + 1]  # Include the whitespace after the command
      tokens.append({matches[i].lower(): command})

  # if the only command is configure, check if the rest is encrypted data
  if len(tokens) == 1:
    command_ = tokens[0]
    if command_.get("configure"):
       data = command_.get("configure").split("\n")
       command_encrypted = data[1].replace("\n","").replace(" ","")
       if(command_encrypted != " " or command_encrypted != "\n"):
        return data[0] , command_encrypted       
  # if there is any other command, could be a encrypted data
  if len(tokens) == 0:
    return None, command_string.replace("\n","")
  return tokens, None



