{% macro generate_ratings() %}
CASE
    WHEN user_rating >= 4.5 THEN 'Excellent'
    WHEN user_rating >= 4.0 THEN 'Good'
    WHEN user_rating >= 3.0 THEN 'Average'
    ELSE 'Bad'
END as rating_category
{% endmacro %}