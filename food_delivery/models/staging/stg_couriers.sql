SELECT
    *,
    current_date() - signup_date AS days_since_signup
FROM
    {{ source('raw', 'raw_couriers') }}
WHERE
    status = 'active'