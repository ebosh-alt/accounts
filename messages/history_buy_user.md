{% for deal in deals %}
*id сделки:* `{{deal.id}}` 
*Название магазина:* `{{deal.shop}}`
*Название аккаунта:* `{{deal.name}}`
*Стоимость:* `{{deal.price}}`
*Описание:* `{{deal.description}}`
*Данные:* `{{deal.data}}`
*Дата покупки:* `{{deal.date}}`
{% if deal.guarantor == True %}*Покупка совершена с гарантом*
{% else %}*Покупка совершена без гаранта*{% endif %}
{% endfor %}