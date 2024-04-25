*Магазин:* `{{shop}}`
*Название:* `{{name}}`
*Описание:* `{{description}}`
{%if price_no and price_yes%}*Стоимость без гаранта:* `{{price_no}} USDT`
*Стоимость с гарантом:* `{{price_yes}} USDT`{%endif%}{%if price%}*Стоимость:* `{{price}} USDT`{%endif%}