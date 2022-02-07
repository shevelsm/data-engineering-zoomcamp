--Q3 jan15
SELECT
	COUNT(tpep_pickup_datetime)
FROM
	"de-zoomcamp"."yellow_taxi_trips"
WHERE
	CAST(tpep_pickup_datetime AS DATE) = '2021-01-15'
LIMIT 100;
-- 53024

--Q4 largest tip
SELECT 
	CAST(tpep_pickup_datetime AS DATE) AS DAY, 
	MAX(tip_amount) AS max_tips
FROM
	"de-zoomcamp"."yellow_taxi_trips"
GROUP BY
	CAST(tpep_pickup_datetime AS DATE)
ORDER BY
	max_tips DESC
LIMIT 1;
-- jan20 1140.44

--Q5 from cent park
SELECT 
	tz."Zone",
	COUNT(*) AS cnt 
FROM
	"de-zoomcamp"."yellow_taxi_trips" ytt,
	"de-zoomcamp"."taxi_zones" tz
WHERE
	ytt."DOLocationID" = tz."LocationID"
	AND ytt."PULocationID" = (SELECT "LocationID" FROM "de-zoomcamp".taxi_zones WHERE "Zone" = 'Central Park')
	AND CAST(ytt.tpep_pickup_datetime AS DATE) = '2021-01-14'
GROUP BY 
	tz."Zone"
ORDER BY cnt DESC;


SELECT
	--	"PULocationID",
	COALESCE(tz."Zone", 'Unknown'),
	--	"DOLocationID",
	COALESCE(tz2."Zone", 'Unknown'),
	AVG(total_amount) AS avg_amount
FROM
	"de-zoomcamp"."yellow_taxi_trips" ytt,
	"de-zoomcamp"."taxi_zones" tz,
	"de-zoomcamp"."taxi_zones" tz2
WHERE 
		ytt."PULocationID" = tz."LocationID"
	AND ytt."DOLocationID" = tz2."LocationID"
GROUP BY 
	tz."Zone",
	tz2."Zone"
ORDER BY
	avg_amount DESC
LIMIT 2;
--Alphabet City	Unknown	2292.4
--Union Sq	Canarsie	262.85200000000003
