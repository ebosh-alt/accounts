*Магазин:* `{{shop}}`
*Название:* `{{name}}`
*Описание:* `{{description}}`
{%if count%}*Количество аккаунтов:* `{{count}}`{%endif%}
{%if price_no and price_yes%}*Стоимость без гаранта:* `{{price_no}} USDT`
*Стоимость с гарантом:* `{{price_yes}} USDT`{%endif%}{%if price%}*Стоимость:* `{{price}} USDT`{%endif%}

*Выбрано аккаунтов:* `{{choice_count}}`