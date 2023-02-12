{% if questions %}
{{ time }}

{% for question in questions %}{{ question.text }}
{% for answer in question.answers %}{{ answer.id }}. {{ answer.text }}
{% endfor %}
{% endfor %}{% endif %}