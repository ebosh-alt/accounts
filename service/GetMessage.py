from jinja2 import Environment, PackageLoader, select_autoescape


def get_mes(path: str, **kwargs):
    env = Environment(
        loader=PackageLoader(package_name='main', package_path="messages", encoding="utf-8"),
        autoescape=select_autoescape(['html', 'xml'])
    )

    if ".md" not in path:
        path = path + '.md'
    tmpl = env.get_template(path)
    return tmpl.render(kwargs)


def rounding_numbers(number: str):
    while number[-1] == "0":
        number = number[:-1]
    if number[-1] == ".":
        number = int(number[:-1])
    else:
        number = float(number)
    return number
