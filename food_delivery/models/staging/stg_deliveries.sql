SELECT
    *,
    TIMESTAMP_DIFF(delivery_timestamp, order_timestamp, MINUTE) AS delivery_time_minutes
FROM
    {{ source('raw', 'raw_deliveries') }}
WHERE
    status = 'completed'