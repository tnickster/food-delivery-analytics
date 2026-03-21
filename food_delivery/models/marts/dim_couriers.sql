{{
    config(
        materialized='table'
    )
}}

SELECT
    courier_id,
    courier_name,
    vehicle_type,
    signup_date,
    days_since_signup
FROM
    {{ ref('stg_couriers') }}