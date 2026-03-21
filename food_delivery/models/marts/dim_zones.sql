{{
    config(
        materialized='table'
    )
}}

SELECT
    zone_id,
    zone_name,
    city,
    region,
    full_location
FROM
    {{ ref('stg_zones') }}