import socket
import os
import shutil

dirname = os.path.join(os.getcwd(), 'server_files')


def process(req):
    try:
        if req == 'pwd':
            return f"📁 Текущий каталог: {dirname}"

        elif req == 'ls':
            files = os.listdir(dirname)
            return f"📄 Файлы в каталоге: {', '.join(files)}"

        elif req.startswith('mkdir'):
            dir_name = req.split()[1]
            os.mkdir(os.path.join(dirname, dir_name))
            return f"📂 Каталог '{dir_name}' успешно создан!"

        elif req.startswith('rmdir'):
            dir_name = req.split()[1]
            shutil.rmtree(os.path.join(dirname, dir_name))
            return f"🗑️ Каталог '{dir_name}' успешно удален!"

        elif req.startswith('rm'):
            file_name = req.split()[1]
            os.remove(os.path.join(dirname, file_name))
            return f"🗑️ Файл '{file_name}' успешно удален!"

        elif req.startswith('mv'):
            old_name, new_name = req.split()[1:]
            os.rename(os.path.join(dirname, old_name), os.path.join(dirname, new_name))
            return f"🔄 Файл '{old_name}' успешно переименован в '{new_name}'!"

        elif req.startswith('clienttoserver'):
            _, file_name, content = req.split(maxsplit=2)
            file_path = os.path.join(dirname, file_name)
            with open(file_path, 'w') as f:
                f.write(content)
            return f"📥 Файл '{file_name}' создан на сервере."

        elif req.startswith('servertoclient'):
            file_name = req.split()[1]
            file_path = os.path.join(dirname, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                conn.send(file_content)
                return f"📤 Файл '{file_name}' успешно отправлен клиенту."
            else:
                return f"❌ Файл '{file_name}' не существует на сервере."

        elif req == 'exit':
            return 'exit'
    except Exception as e:
        return f'❌ Ошибка: {e}'

    return '❌ Неверный запрос'

PORT = 8080

sock = socket.socket()
sock.bind(('', PORT))
sock.listen()
print("🔊 Listening on port", PORT)

while True:
    conn, addr = sock.accept()

    request = conn.recv(1024).decode()
    print(request)

    response = process(request)
    if response == 'exit':
        conn.close()
        break
    conn.send(response.encode())

conn.close()

