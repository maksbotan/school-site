    <div class="about_block">
        <h3>О гимназии</h3>
        <ul>
        {% for node in mininav -%}
            <li><a href="{% if node.rel == '1' %}{{ prefix }}{% endif %}{{ node.link }}">{{ node.title }}</a></li>
        {% endfor -%}
        </ul>
    </div>
