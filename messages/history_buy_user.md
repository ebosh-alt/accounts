{% for deal in deals %}
    {{deal.shop}} {{deal.name}} {{deal.price}} {{deal.description}} {{deal.data}} {{deal.date}} {{deal.guarantor}}
{% endfor %}
