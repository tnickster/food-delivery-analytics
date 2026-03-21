{{
    config(
        materialized='table'
    )
}}

SELECT
    courier_name,
    vehicle_type,
    COUNT(delivery_id) AS total_deliveries,
    AVG(delivery_time_minutes) AS avg_delivery_time,
    SUM(tip_amount) AS total_tips,
    AVG(distance_km) AS avg_distance
FROM 
    {{ ref('fct_deliveries') }}
GROUP BY
    courier_name, vehicle_type
ORDER BY
    total_deliveries DESC 
