def command_parser(message):
    content = " ".join(message.split(" ")[1::])
    content = list(map(str.strip, content.split(",")))
    return content
    