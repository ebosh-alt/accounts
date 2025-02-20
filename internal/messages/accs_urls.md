{% for acc in accs %}
*Категория:* `{{acc.category}}`
*Подкатегория:* `{{acc.subcategory}}`
*Название:* `{{acc.name}}`
*Описание:* `{{acc.description}}`
*Стоимость без гаранта:* `{{acc.price_no}} USDT`
*Стоимость с гарантом:* `{{acc.price_yes}} USDT`
[Купить]({{acc.link}})

{% endfor %}