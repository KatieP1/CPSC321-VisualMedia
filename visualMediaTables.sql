DROP TABLE IF EXISTS director_episode;
DROP TABLE IF EXISTS director;
DROP TABLE IF EXISTS season_review;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS season_award;
DROP TABLE IF EXISTS award_show;
DROP TABLE IF EXISTS actor_episode;
DROP TABLE IF EXISTS actor;
DROP TABLE IF EXISTS show_episode;
DROP TABLE IF EXISTS show_season;
DROP TABLE IF EXISTS tv_show;
DROP TABLE IF EXISTS genre;

CREATE TABLE genre (
    PRIMARY KEY (genre_name),
    genre_name VARCHAR NOT NULL,
    genre_description VARCHAR NOT NULL
);

CREATE TABLE tv_show (
    PRIMARY KEY(show_title),
    show_title VARCHAR NOT NULL,
    release_year NUMERIC(4, 0) NOT NULL,
    currently_running BOOLEAN NOT NULL,
    genre VARCHAR NOT NULL,
    FOREIGN KEY (genre) REFERENCES genre (genre_name)
);

CREATE TABLE show_season (
    PRIMARY KEY (show_title, season_num),
    show_title VARCHAR NOT NULL,
    season_num INT NOT NULL,
    release_year NUMERIC (4) NOT NULL,
    FOREIGN KEY (show_title) REFERENCES tv_show(show_title)
);

CREATE TABLE show_episode (
    PRIMARY KEY (show_title, season_num, ep_num),
    show_title VARCHAR NOT NULL,
    season_num INT NOT NULL,
    ep_num INT NOT NULL,
    ep_name VARCHAR NOT NULL,
    ep_length NUMERIC NOT NULL,
    FOREIGN KEY (show_title, season_num) REFERENCES show_season (show_title, season_num)
);

CREATE TABLE actor (
    PRIMARY KEY (stage_name),
    stage_name VARCHAR NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL
);

CREATE TABLE actor_episode (
    PRIMARY KEY (stage_name, show_title, season_num, ep_num),
    stage_name VARCHAR NOT NULL,
    show_title VARCHAR NOT NULL,
    season_num INT NOT NULL,
    ep_num INT NOT NULL,
    FOREIGN KEY (show_title, season_num, ep_num) REFERENCES show_episode(show_title, season_num, ep_num),
    FOREIGN KEY (stage_name) REFERENCES actor(stage_name)
);


CREATE TABLE award_show (
    PRIMARY KEY (award_show_name, award_name),
    award_show_name VARCHAR NOT NULL,
    award_name VARCHAR NOT NULL
);

CREATE TABLE season_award (
    PRIMARY KEY (award_show_name, award_name, show_title, season_num),
    award_show_name VARCHAR NOT NULL,
    award_name VARCHAR NOT NULL,
    show_title VARCHAR NOT NULL,
    season_num INT NOT NULL,
    FOREIGN KEY (award_show_name, award_name) REFERENCES award_show (award_show_name, award_name),
    FOREIGN KEY (show_title, season_num) REFERENCES show_season (show_title, season_num)
);

CREATE TABLE review (
    PRIMARY KEY (reviewer_name),
    reviewer_name VARCHAR NOT NULL, -- ex: rotten tomatoes, IMDb, etc
    review_metric VARCHAR NOT NULL, -- ex: tomatoes, stars, or no metric.
    review_max INT NOT NULL -- ex: max rotten tomatoes score is 100
);

CREATE TABLE season_review (
    PRIMARY KEY (reviewer_name, show_title, season_num),
    reviewer_name VARCHAR NOT NULL,
    show_title VARCHAR NOT NULL,
    season_num INT NOT NULL,
    review_score NUMERIC NOT NULL,
    FOREIGN KEY (reviewer_name) REFERENCES review(reviewer_name),
    FOREIGN KEY (show_title, season_num) REFERENCES show_season(show_title, season_num)
);

CREATE TABLE director (
    PRIMARY KEY (stage_name),
    stage_name VARCHAR NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL
);

CREATE TABLE director_episode (
    PRIMARY KEY (show_title, season_num, ep_num, stage_name), -- an episode can have more than 1 director
    show_title VARCHAR NOT NULL,
    season_num INT NOT NULL,
    ep_num INT NOT NULL,
    stage_name VARCHAR NOT NULL,
    FOREIGN KEY (show_title, season_num, ep_num) REFERENCES show_episode(show_title, season_num, ep_num),
    FOREIGN KEY (stage_name) REFERENCES director(stage_name)
);

\copy genre (genre_name, genre_description) FROM '/Users/KatiePark/Desktop/CPSC321-VisualMedia/input_data/genre.csv' CSV HEADER;
\copy tv_show (show_title,release_year,currently_running, genre) FROM '/Users/KatiePark/Desktop/CPSC321-VisualMedia/input_data/tv_show.csv' CSV HEADER;
\copy show_season (show_title,season_num,release_year) FROM '/Users/KatiePark/Desktop/CPSC321-VisualMedia/input_data/show_season.csv' CSV HEADER;
\copy show_episode (show_title,season_num,ep_num,ep_name,ep_length) FROM '/Users/KatiePark/Desktop/CPSC321-VisualMedia/input_data/show_episode.csv' CSV HEADER;
\copy actor (stage_name, first_name, last_name) FROM '/Users/KatiePark/Desktop/CPSC321-VisualMedia/input_data/actor.csv' CSV HEADER;
\copy actor_episode (stage_name,show_title,season_num,ep_num) FROM '/Users/KatiePark/Desktop/CPSC321-VisualMedia/input_data/actor_episode.csv' CSV HEADER;
\copy award_show (award_show_name,award_name) FROM '/Users/KatiePark/Desktop/CPSC321-VisualMedia/input_data/award_show.csv' CSV HEADER;
\copy season_award (award_show_name, award_name, show_title, season_num) FROM '/Users/KatiePark/Desktop/CPSC321-VisualMedia/input_data/season_award.csv' CSV HEADER;
\copy review (reviewer_name,review_metric,review_max) FROM '/Users/KatiePark/Desktop/CPSC321-VisualMedia/input_data/review.csv' CSV HEADER;
\copy season_review (reviewer_name,show_title,season_num,review_score) FROM '/Users/KatiePark/Desktop/CPSC321-VisualMedia/input_data/season_review.csv' CSV HEADER;
\copy director (stage_name, first_name, last_name) FROM '/Users/KatiePark/Desktop/CPSC321-VisualMedia/input_data/director.csv' CSV HEADER;
\copy director_episode (show_title, season_num, ep_num, stage_name) FROM '/Users/KatiePark/Desktop/CPSC321-VisualMedia/input_data/director_episode.csv' CSV HEADER;