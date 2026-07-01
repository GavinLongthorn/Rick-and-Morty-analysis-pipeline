{{ config(materialized='table') }}

WITH base_data AS (
    SELECT 
        name,
        status,
        species,
        gender,
        (length(episode) - length(replace(episode, ',', '')) + 1) AS episode_count
    FROM {{ source('my_api_data', 'rick_morty_cast_analysis') }}
),

final_metrics AS (
    SELECT 
        bd.*,
        ROUND(bd.episode_count::numeric / 87.0, 2 AS exposure_ratio,
        bd.episode_count * 50000 AS total_voice_actor_pay
    FROM base_data bd
)

SELECT * FROM final_metrics