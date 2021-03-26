from datetime import datetime
import requests


# 1. Написать декоратор - логгер. Он записывает в файл дату и время
# вызова функции, имя функции, аргументы, с которыми
# вызвалась и возвращаемое значение.
# 2. Написать декоратор из п.1, но с параметром – путь к логам.
# 3. Применить написанный логгер к приложению из любого предыдущего д/з

def logger(file_name):
    def decorator(function_to_log):
        def wrapper(*args, **kwargs):
            f = open(file_name, "a")
            f.write(datetime.now().__str__())
            f.write(" " + function_to_log.__name__)
            f.write(" " + args.__str__())
            f.write(" " + kwargs.__str__())
            result = function_to_log(*args, **kwargs)
            f.write(" " + str(result))
            f.write("\n")
            f.close()
            return result

        return wrapper

    return decorator


@logger("logs.txt")
def get_average(results):
    sum = 0
    count = 0
    for result in results:
        intelligence = int(result["powerstats"]["intelligence"])
        sum += intelligence
        count += 1
    return sum / count


@logger("logs.txt")
def get_average_intelligence_from_api(name):
    response = requests.get("https://www.superheroapi.com/api.php/2619421814940190/search/{}".format(name))
    response.raise_for_status()
    results = response.json()["results"]
    return get_average(results)


@logger("logs.txt")
def get_most_intelligent_superhero(names):
    max_intelligence = 0
    max_name = None
    for name in names:
        intelligence = get_average_intelligence_from_api(name)
        if intelligence > max_intelligence:
            max_intelligence = intelligence
            max_name = name
    return max_name


print(get_most_intelligent_superhero(["Hulk", "Thanos", "Captain America"]))
