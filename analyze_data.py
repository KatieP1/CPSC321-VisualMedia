def menu(cn):

    while True:
        print("1. Find top k highest rated shows across seasons (with ties)")
        print("2. Find shows that have won above average number of awards")
        print("3. Find actors who have appeared in the most genres")
        print("4. Find actors who have appeared in the most TV show episodes for a specific genre")
        print("5. Return to main menu\n")

        choice = input("What information would you like to add (1-5): ")
        print("\n")

        match choice:
            case "1":
                rank_films(cn)
            case "2":
                above_avg_awards(cn)
            case "3":
                actors_most_appear_genre(cn)
            case "4":
                actors_most_ep_with_genre(cn)
            case "5":
                return

def rank_films(cn):
    top_k = int(input("Enter the number of highest rated shows you wish to be returned: "))
    print("\n")

    q = ("SELECT show_title, ROUND((ROUND(AVG(review_score/review_max), 4) * 100), 2) AS avg_score "
         "FROM review JOIN season_review USING (reviewer_name) "
         "GROUP BY show_title "
         "ORDER BY avg_score DESC, show_title ASC "
         "FETCH FIRST %s ROWS WITH TIES;")
    
    print(f"Top {top_k} highest acclaimed shows: ")
    with cn.cursor() as rs:
        rs.execute(q, (top_k,))

        for row in rs:
            print(f"\t{row[0]}: {row[1]}%")
    
    print("\n")
    userInput = input("Press enter to continue: ")
    print("\n")

def above_avg_awards(cn):
    
    q = ("SELECT COUNT(*) AS total_ct, show_title "
         "FROM season_award "
         "GROUP BY show_title "
         "HAVING COUNT(*) > (SELECT AVG(avg_total.total_awards) " \
                             "FROM (SELECT COUNT(*) AS total_awards " \
                                    "FROM season_award " \
                                    "GROUP BY show_title) avg_total) "
         "ORDER BY total_ct DESC;")
    
    print("Shows that have won awards more than the average number of times a show has won an award")
    print("Note: only counting shows that have already won awards")
    print("\n")
    with cn.cursor() as rs:
        rs.execute(q)

        for row in rs:
            print(f"\t{row[1]} has won {row[0]} awards")
    
    print("\n")
    userInput = input("Press enter to continue: ")
    print("\n")
    
def actors_most_appear_genre(cn):
    
    q = ("WITH actor_genre_ct AS (" \
            "SELECT stage_name, COUNT(DISTINCT(genre)) AS distinct_genre " \
            "FROM actor_episode JOIN tv_show USING (show_title) " \
            "GROUP BY stage_name), "
        "max_genre AS (" \
            "SELECT MAX(distinct_genre) AS max_distinct_genre " \
            "FROM actor_genre_ct) "
        "SELECT a.stage_name, a.distinct_genre "
        "FROM actor_genre_ct a JOIN max_genre m ON (a.distinct_genre = m.max_distinct_genre);")
    
    print("Actors who have appeared in most number of genres: ")

    with cn.cursor() as rs:
        rs.execute(q)

        for row in rs:
            print(f"\t{row[0]}: {row[1]} genres")
    
    print("\n")
    userInput = input("Press enter to continue: ")
    print("\n")
            
def actors_most_ep_with_genre(cn):

    q = ("SELECT ROW_NUMBER() OVER (ORDER BY genre_name), genre_name FROM genre;")

    print("All genres: ")
    with cn.cursor() as rs:
        rs.execute(q)

        for row in rs:
            print(f"\t{row[0]}. {row[1]}")
    
    print("\n")
    genre_name = input("Enter the genre name (see list above) to find the actor who has appeared in the most TV shows with the genre: ")
    print("\n")

    q = ("SELECT * FROM genre WHERE genre_name = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (genre_name,))

        if not rs.fetchone():
            print(f"{genre_name} is not a genre in the database.")
            print("\n")
            return
    
    q = ("WITH num_shows AS (" \
            "SELECT stage_name, COUNT(DISTINCT(show_title)) AS distinct_shows " \
            "FROM actor_episode JOIN tv_show USING (show_title) " \
            "WHERE genre = %s "
            "GROUP BY stage_name), "
        "max_shows AS (" \
            "SELECT MAX(distinct_shows) AS max_distinct_shows " \
            "FROM num_shows) "
        "SELECT n.stage_name, n.distinct_shows "
        "FROM num_shows n JOIN max_shows m ON (n.distinct_shows = m.max_distinct_shows);")
    
    print(f"Actor(s) who has appeared in the most shows with the genre {genre_name}:")
    with cn.cursor() as rs:
        rs.execute(q, (genre_name,))

        for row in rs:
            print(f"\t{row[0]} has appeared in {row[1]} with the genre {genre_name}")
    
    print("\n")
    userInput = input("Press enter to continue: ")
    print("\n")
