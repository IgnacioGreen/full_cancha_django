
<div id="app">
    <h1>[[ message ]]</h1>
</div>

<script src="https://cdn.jsdelivr.net/npm/vue@3"></script>
<script>
    const app = Vue.createApp({
    delimiters: ['[[', ']]'], // Cambia los delimitadores a [[ ]]
    data() {
        return {
            message: 'Hello from Vue!',
        };
    },
});
app.mount('#app');
</script>


<!--
{% extends 'base/main.html' %}
{% block content %}

<div class="top-bar">
    <div>
        <h1>Hi {{request.user|title}}</h1>
        <h3 style="margin:0"> You have <i>{{count}}</i> task{{count|pluralize}} incomplete{{count|pluralize}}</h3>
    </div>

    {% if request.user.is_authenticated %}
    <form method="POST" action="{% url 'logout' %}">
        {% csrf_token %}
        <button class="button" type="submit">Exit</button>
    </form>
    {% else %}
    <a href="{% url 'login' %}">Log in</a>
    {% endif %}
</div>
<div id="container-search">

    <form method="GET" style="margin-top: 20px; display: flex;">
        <input type="text" name="search-text" value="{{search_value}}">
        <input type="submit" value="Search">
    </form>
    <a id="link-add" href="{% url 'create-task' %}">&#x1F7A5;</a>
</div>

<div class="container-task-items">
    {% for task in tasks %}
    <div class="container-task">
        {% if task.done %}
        <div class="title-task">
             <div class="icon-task-done"></div>
             <i><s><a href="{% url 'edit-task' task.id %}">{{task}}</a></s></i>
        </div>
        {% else %}
        <div class="title-task">
             <div class="icon-task-incomplete"></div>
             <a href="{% url 'edit-task' task.id %}">{{task}}</a>
        </div>
        <a class="link-delete" href="{% url 'delete-task' task.id %}">&#x2A2F;</a>
        {% endif %}
    </div>

    {% empty %}
    <h3>There are no items in this list</h3>
    {% endfor %}

</div>

{% endblock content %}

