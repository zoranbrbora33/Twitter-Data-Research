-- Creates quarterly views for our data
CREATE VIEW "twitter_redshift_db"."tara_s3_to_redshift_database_schema"."travelers_and_blogers_view" AS
SELECT
    grad,
    city,
    country,
    SUM(january + february + march) AS q1,
    SUM(april + may + june) AS q2,
    SUM(july + august + september) AS q3,
    SUM(october + november + december) AS q4,
    SUM(january + february + march + april + may + june + july + august + september + october + november + december) AS total_sum
FROM
    "twitter_redshift_db"."tara_s3_to_redshift_database_schema"."traveler_and_blogers"
GROUP BY
    grad, city, country;