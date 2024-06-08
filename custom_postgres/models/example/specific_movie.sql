-- using jinja to set a variable to be across the sql script or dbt model
{% set film_title = 'Dunkirk' %}

SELECT *
FROM {{ ref('films') }}
WHERE title = '{{ film_title }}'