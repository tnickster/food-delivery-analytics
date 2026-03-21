{{
    config(
        materialized='table'
    )
}}

SELECT 
    d.delivery_id,
    d.order_timestamp,
    d.delivery_timestamp, 
    d.delivery_time_minutes, 
    d.tip_amount, 
    d.distance_km,
    c.courier_name, 
    c.vehicle_type,
    z.zone_name,
    z.city
FROM
    {{ ref('stg_deliveries') }} AS d
    LEFT JOIN {{ ref('stg_couriers') }} AS c
    ON c.courier_id = d.courier_id
    LEFT JOIN {{ ref('stg_zones') }} AS z 
    ON z.zone_id = d.zone_id
WHERE c.courier_name IS NOT NULL
