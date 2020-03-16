import json
import album_structure
# Импортируем необходимые модули для работы с сервером
from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

# Пишем сначала GET-запрос:

@route("/albums/<artist>")
def finder(artist):
	# Применяем функцию find() из модуля album_structure
	music_list_of_artist = album_structure.find(artist)
	if not music_list_of_artist:
		message = "Альбомов артиста {} нет в базе данных".format(artist)
		# Выводим ошибку
		result = HTTPError(404, message)
	else:
		# Если артист есть в БД, то создаём список его альбомов
		# Итерироваться будем с помощью генераторов, т.к. они меньше нагружают модуль
		names_of_albums = [album.album for album in music_list_of_artist]
		result = "Список альбомов {}: ".format(artist)
		result = "<br>".join(names_of_albums)

	return result

# Как было показано ранее в примере создаём класс-сохранялку данных
# Для простоты помещаем в перемнную имя будущего файла
def saver(art):
	file = "{}-{}.json".format(art[1], art[3])
# Открываем на запись файл и делаем копию данных нашего артиста(art)
	with open(file, "w") as fu:
		json.dump(art, fu)
	return file

# Создаём пост запрос, поместив "POST" в метод
@route("/albums", method = "POST")
def artist():
	# Как было показано в примере используем request с атрибутом
	# forms который поддерживает метод get для получения параметров:		
	art = [request.forms.get("year"),
		   request.forms.get("artist"),
		   request.forms.ger("genre"),
		   request.forms.get("album")]
	# Далее сохраняем файл и выводим его имя:
	save_file = saver(art)
	print("Данные сохранены в:"," ",save_file )
	return "Данные сохранены"

if __name__ == "__main__":
	run(host = "localhost", prot = 8080, debug = True)

		