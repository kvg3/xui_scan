with open('ip_port.csv', 'r', encoding='UTF-8-SIG') as infile:
    content = infile.read()

with open('ip_port.csv', 'w', encoding='UTF-8') as outfile:
    outfile.write(content)  