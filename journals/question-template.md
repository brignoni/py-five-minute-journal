{% if questions %}
---
{{ time }}

{% for question in questions %}### {{ question.content }}
{% for answer in question.answers %}{{ answer.id }}. {{ answer.content }}
{% endfor %}
{% endfor %}{% endif %}