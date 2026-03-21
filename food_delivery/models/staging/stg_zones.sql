SELECT  
    *,
    concat(city, '-', zone_name) AS full_location
FROM
    {{ source('raw', 'raw_zones')}}
