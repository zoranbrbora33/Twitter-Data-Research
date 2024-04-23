--Creates table with tweets from users with more than 5000 followers
SELECT 
    t.full_text 
FROM "twitter_redshift_db"."tara_academy_redshift"."tweets" t 
INNER JOIN "twitter_redshift_db"."tara_academy_redshift"."users"  u
ON t.user_id = u.user_id 
WHERE u.followers_count > 5000 AND t.created_at LIKE '{month_pattern}';

--Creates table with tweets talking about travel from croatian travel influencers and blogers.
--Sums up replys, quotes and reposts on every tweet and shows it as engagment column 
SELECT DISTINCT
    tt.full_text,
    SUM(tt.in_retweet_cnt  + tt.in_quote_cnt + tt.in_reply_cnt) AS engagment
FROM "twitter_redshift_db"."tara_academy_redshift"."users" AS tu
INNER JOIN "twitter_redshift_db"."tara_academy_redshift"."tweets" AS tt
ON tu.user_id = tt.user_id
WHERE tu.is_croatian = True
AND tt.created_at LIKE \'{month_pattern}\'
AND tu.description LIKE '%travel%'
AND tu.followers_count > 100
AND (tt.full_text LIKE '%travel%' OR tt.full_text LIKE '%driving%' OR tt.full_text LIKE '%fly%' OR tt.full_text LIKE '%ride%' OR tt.full_text LIKE '%sail%' OR tt.full_text LIKE '%sightseeing%' OR tt.full_text LIKE '%tour%' OR tt.full_text LIKE '%trip%' OR tt.full_text LIKE '%cruising%' OR tt.full_text LIKE '%expedition%' OR tt.full_text LIKE '%touring%' OR tt.full_text LIKE '%wanderlust%' OR tt.full_text LIKE '%wandering%' OR tt.full_text LIKE '%trekking%' OR tt.full_text LIKE '%cruise%' OR tt.full_text LIKE '%sail%' OR tt.full_text LIKE '%explore%' OR tt.full_text LIKE '%sightsee%' OR tt.full_text LIKE '%abroad%' OR tt.full_text LIKE '%camping%' OR tt.full_text LIKE '%journey%' OR tt.full_text LIKE '%putovanj%'
OR tt.full_text LIKE '%obilazak%' OR tt.full_text LIKE '%posjeta%' OR tt.full_text LIKE '%krstarenje%' OR tt.full_text LIKE '%ljetovanje%' OR tt.full_text LIKE '%lutanje%'
OR tt.full_text LIKE '%odredište%' OR tt.full_text LIKE '%zimovanje%' OR tt.full_text LIKE '%logorovanje%' OR tt.full_text LIKE '%skijanje%' OR tt.full_text LIKE '%izlet%'
OR tt.full_text LIKE '%planinarenje%')
OR tu.description LIKE 'blog%'
AND tu.screen_name NOT IN ('eZadar', 'DubrovnikTB', 'FindCroatia', 'Rovinj_official', 'TheHDTravels', 'SecretDalmatia', 'LyndaMilina', 'latcroatia', 'tourguidesplit', 'Dubrovnik_',
'tourdalmatia', 'aslagency', 'Travel2Ultra', 'Croatia_Charter', 'CroatiaFerries', 'Islandoflosinj', 'LuxuryCroatia', 'ZagrebTravels')
GROUP BY tt.full_text, tu.followers_count
ORDER BY engagment DESC;

--Creates table with tweets from users excluding 
--('Perkz', 'Sandra_Ri051', 'KolindaGK', 'KarloBujan', 'knoll_doll', 'ivospigel', 'SeverMaja', 'kmacan', 'natasazecevic', 'domagojsever')
SELECT 
    t.full_text
FROM "twitter_redshift_db"."tara_academy_redshift".users u
JOIN "twitter_redshift_db"."tara_academy_redshift".tweets t
ON u.user_id = t.user_id
AND u.screen_name IN ('Perkz', 'Sandra_Ri051', 'KolindaGK', 'KarloBujan', 'knoll_doll', 'ivospigel', 'SeverMaja', 'kmacan', 'natasazecevic', 'domagojsever')
AND t.created_at LIKE \'{month_pattern}\'
ORDER BY u.followers_count DESC;