# update_users

Small independent script for sessiyabot.

Check online status community members and add it to database

Please, use it in another docker container. It must be run always.

Next, description functions in PostgreSQL database to use:

+ Main function: add user online-status to database (and delete old records)

```sql
CREATE OR REPLACE FUNCTION sessiyabot.update_status(ids integer[], status integer[])
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
DECLARE
	id integer;
	ts timestamp;
	n integer :=1;
	BEGIN
		ts = date_trunc('seconds', LOCALTIMESTAMP);
		FOREACH id IN ARRAY ids
			LOOP
				execute 'INSERT INTO online (id, tstamp, status) VALUES('|| id || ','|| quote_literal(ts) || ','|| status[n] ||');';
	    		n = n+1;
	    	END LOOP;
	    DELETE FROM online WHERE tstamp < now() - interval '8 days';
		RETURN 0;
	END;
$function$;
```

+ Next: 3 views to extract data from table "online"

**Day bins**

```sql
CREATE OR REPLACE VIEW sessiyabot.day_bins
AS SELECT online.id,
    date_part('year'::text, online.tstamp) AS year,
    date_part('month'::text, online.tstamp) AS month,
    date_part('day'::text, online.tstamp) AS day,
    date_part('hour'::text, online.tstamp) AS hour,
    sum(online.status) AS minutes
   FROM online
  WHERE (LOCALTIMESTAMP - '23:00:00'::interval hour) < online.tstamp
  GROUP BY online.id, (date_part('day'::text, online.tstamp)), (date_part('hour'::text, online.tstamp)), (date_part('month'::text, online.tstamp)), (date_part('year'::text, online.tstamp))
  ORDER BY online.id, (date_part('day'::text, online.tstamp)), (date_part('hour'::text, online.tstamp));

-- Permissions

ALTER TABLE sessiyabot.day_bins OWNER TO sessiyabot;
GRANT ALL ON TABLE sessiyabot.day_bins TO sessiyabot;
```

**Yesterday bins**

```sql
CREATE OR REPLACE VIEW sessiyabot.yesterday_bins
AS SELECT online.id,
    date_part('year'::text, online.tstamp) AS year,
    date_part('month'::text, online.tstamp) AS month,
    date_part('day'::text, online.tstamp) AS day,
    date_part('hour'::text, online.tstamp) AS hour,
    sum(online.status) AS minutes
   FROM online
  WHERE date_part('day'::text, online.tstamp) = date_part('day'::text, LOCALTIMESTAMP - '1 day'::interval day)
  GROUP BY online.id, (date_part('day'::text, online.tstamp)), (date_part('hour'::text, online.tstamp)), (date_part('month'::text, online.tstamp)), (date_part('year'::text, online.tstamp))
  ORDER BY online.id, (date_part('day'::text, online.tstamp)), (date_part('hour'::text, online.tstamp));

-- Permissions

ALTER TABLE sessiyabot.yesterday_bins OWNER TO sessiyabot;
GRANT ALL ON TABLE sessiyabot.yesterday_bins TO sessiyabot;
```

**Week bins**

```sql
CREATE OR REPLACE VIEW sessiyabot.week_bins
AS SELECT online.id,
    date_part('year'::text, online.tstamp) AS year,
    date_part('month'::text, online.tstamp) AS month,
    date_part('day'::text, online.tstamp) AS day,
    sum(online.status)::double precision / 60.0::double precision AS hours
   FROM online
  WHERE date_part('day'::text, online.tstamp) <> date_part('day'::text, LOCALTIMESTAMP) AND online.tstamp > (LOCALTIMESTAMP - '7 days'::interval day)
  GROUP BY online.id, (date_part('year'::text, online.tstamp)), (date_part('month'::text, online.tstamp)), (date_part('day'::text, online.tstamp))
  ORDER BY online.id, (date_part('year'::text, online.tstamp)), (date_part('month'::text, online.tstamp)), (date_part('day'::text, online.tstamp));

-- Permissions

ALTER TABLE sessiyabot.week_bins OWNER TO sessiyabot;
GRANT ALL ON TABLE sessiyabot.week_bins TO sessiyabot;
```
