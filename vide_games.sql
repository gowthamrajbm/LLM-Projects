set schema 'video_games';

SELECT 
    gp.release_year,
    COUNT(DISTINCT g.id) AS game_count
FROM 
    game g
JOIN 
    game_publisher gpub ON g.id = gpub.game_id
JOIN 
    game_platform gp ON gpub.id = gp.game_publisher_id
GROUP BY 
    gp.release_year
ORDER BY 
    gp.release_year;