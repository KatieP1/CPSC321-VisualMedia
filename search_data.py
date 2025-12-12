def menu(cn):

    while True:
        print("1. Search TV show information")
        print("2. Search TV shows an actor has been in")
        print("3. Search TV shows a director has directed")
        print("4. Search awards that a TV show has won")
        print("5. Search for reviews in a show")
        print("6. Return to main menu\n")

        choice = input("What information would you like to add (1-6): ")
        print("\n")

        match choice:
            case "1":
                show_info(cn)
            case "2":
                num_shows_actor(cn)
            case "3":
                num_shows_director(cn)
            case "4":
                search_awards(cn)
            case "5":
                search_reviews(cn)
            case "6":
                return

def show_info(cn):
    user_show = input("Enter which show you would like to see the information of: ")
    print("\n")

    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (user_show,))

        if not rs.fetchone():
            print("This TV show does not exist.")
            print("\n")
            return
    
    q = ("SELECT tv.show_title, tv.release_year, tv.currently_running, tv.genre, COUNT(*) "
         "FROM tv_show tv JOIN show_season USING (show_title) "
         "WHERE show_title = %s "
         "GROUP BY tv.show_title, tv.release_year, tv.currently_running, tv.genre;")
    
    with cn.cursor() as rs:
        rs.execute(q, (user_show,))

        for row in rs:
            print(f"TV Show Name: {row[0]}")
            print(f"Release Year: {row[1]}")
            print(f"Currently Running: {row[2]}")
            print(f"Genre: {row[3]}")
            print(f"Number of seasons: {row[4]}")
            max_season = row[4]
    
    print("\n")

    while True:
        season_select = input(f"Enter a season number to view episodes or press enter to exit. {user_show} has {max_season} season(s): ")
        print("\n")

        if season_select == "":
            break
        else:
            season_select = int(season_select)
        
        if season_select > max_season:
            print(f"There is no season {season_select} in {user_show}.")
            print("\n")
            continue
        
        q = ("SELECT ep_num, ep_name, ep_length FROM show_episode WHERE show_title = %s AND season_num = %s ORDER BY ep_num ASC;")
        with cn.cursor() as rs:
            rs.execute(q, (user_show, season_select))

            if not rs.fetchone():
                print(f"There are no episodes in season {season_select} of {user_show}.")
                print("\n")
                continue
        
        with cn.cursor() as rs:
            rs.execute(q, (user_show, season_select))

            for row in rs:
                print(f"Episode {row[0]}")
                print(f"Episode Name: {row[1]}")
                print(f"Episode Length: {row[2]}")
                print("\n")
        
        print("\n")
        userInput = input("Press enter to continue: ")
        print("\n")

def num_shows_actor(cn):
    actor_sn = input("Enter the stage name of the actor you are searching for: ")
    print("\n")

    q = ("SELECT * FROM actor WHERE stage_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (actor_sn,))

        if not rs.fetchone():
            print("This actor does not exist.")
            print("\n")
            return
    
    while True:
        
        q = ("SELECT ROW_NUMBER() OVER (ORDER BY show_title ASC), show_title "
             "FROM actor_episode "
             "WHERE stage_name = %s "
             "GROUP BY show_title;")
        
        print(f"List of shows {actor_sn} has been in: ")
        with cn.cursor() as rs:
            rs.execute(q, (actor_sn,))

            for row in rs:
                print(f"\t{row[0]}. {row[1]}")
        
        print("\n")
        userChoice = input(f"Enter a TV show name to see the episodes {actor_sn} has been in or press enter to exit: ")
        print("\n")

        if userChoice == "":
            break

        q = ("SELECT * "
             "FROM actor_episode JOIN show_episode USING (show_title, season_num, ep_num) "
             "WHERE show_title = %s AND stage_name = %s "
             "ORDER BY season_num ASC, ep_num ASC;")
        
        with cn.cursor() as rs:
            rs.execute(q, (userChoice, actor_sn))

            if not rs.fetchone():
                print(f"{actor_sn} is not in the TV show {userChoice}.")
                print("\n")
                userInput = input("Press enter to continue: ")
                continue

                    
        q = ("SELECT season_num, ep_num, ep_name "
             "FROM actor_episode JOIN show_episode USING (show_title, season_num, ep_num) "
             "WHERE show_title = %s AND stage_name = %s "
             "ORDER BY season_num ASC, ep_num ASC;")

        with cn.cursor() as rs:
            rs.execute(q, (userChoice, actor_sn))

            print(f"Show: {userChoice}")

            for row in rs:
                print(f"\tSeason {row[0]} Episode {row[1]}: {row[2]}")
                
        
        print("\n")
        userInput = input("Press enter to continue: ")
        print("\n")
    
def num_shows_director(cn):
    director_sn = input("Enter the stage name of the director you are searching for: ")
    print("\n")

    q = ("SELECT * FROM director WHERE stage_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (director_sn,))

        if not rs.fetchone():
            print("This director does not exist.")
            print("\n")
            return
    
    while True:
        
        q = ("SELECT ROW_NUMBER() OVER (ORDER BY show_title ASC), show_title "
             "FROM director_episode "
             "WHERE stage_name = %s "
             "GROUP BY show_title;")
        
        print(f"List of shows {director_sn} has directed: ")
        with cn.cursor() as rs:
            rs.execute(q, (director_sn,))

            for row in rs:
                print(f"\t{row[0]}. {row[1]}")
        
        print("\n")
        userChoice = input(f"Enter a TV show name to see the episodes {director_sn} has directed or press enter to exit: ")
        print("\n")
        
        if userChoice == "":
            break

        q = ("SELECT * "
             "FROM director_episode JOIN show_episode USING (show_title, season_num, ep_num) "
             "WHERE show_title = %s AND stage_name = %s "
             "ORDER BY season_num ASC, ep_num ASC;")
        
        with cn.cursor() as rs:
            rs.execute(q, (userChoice, director_sn))

            if not rs.fetchone():
                print(f"{director_sn} did not direct {userChoice}.")
                print("\n")
                userInput = input("Press enter to continue: ")
                continue
        
        q = ("SELECT season_num, ep_num, ep_name "
             "FROM director_episode JOIN show_episode USING (show_title, season_num, ep_num) "
             "WHERE show_title = %s AND stage_name = %s "
             "ORDER BY season_num ASC, ep_num ASC;")
        
        with cn.cursor() as rs:
            rs.execute(q, (userChoice, director_sn))
            print(f"Show: {userChoice}")

            for row in rs:
                print(f"\tSeason {row[0]} Episode {row[1]}: {row[2]}")
        
        print("\n")
        userInput = input("Press enter to continue: ")
        print("\n")

def search_awards(cn):
    user_show = input("Enter which show you would like to see has won awards: ")
    print("\n")

    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (user_show,))

        if not rs.fetchone():
            print(f"{user_show} TV show does not exist.")
            print("\n")
            return
    
    q = ("SELECT * FROM season_award WHERE show_title = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (user_show,))

        if not rs.fetchone():
            print(f"{user_show} has not won any awards.")
            print("\n")
            return

    while True:
        q = ("SELECT ROW_NUMBER() OVER (ORDER BY award_show_name), award_show_name FROM season_award WHERE show_title = %s GROUP BY award_show_name;")
        with cn.cursor() as rs:
            rs.execute(q, (user_show,))

            print(f"Award Shows that {user_show} has won: ")
            for row in rs:
                print(f"\t{row[0]}: {row[1]}")

        print("\n")
        user_award_show = input(f"Enter the name of the award show to view the award names {user_show} has won or press enter to exit: ")
        print("\n")
        
        if user_award_show == "":
            break

        q = ("SELECT * FROM season_award WHERE show_title = %s AND award_show_name = %s ORDER BY season_num ASC, award_name ASC;")
        with cn.cursor() as rs:
            rs.execute(q, (user_show, user_award_show))

            if not rs.fetchone():
                print(f"{user_show} has not won awards from {user_award_show}.")
                print("\n")
                continue
        
        q = ("SELECT * FROM season_award WHERE show_title = %s AND award_show_name = %s ORDER BY season_num ASC, award_name ASC;")
        with cn.cursor() as rs:
            rs.execute(q, (user_show, user_award_show))

            print(f"Awards that {user_show} has won at {user_award_show}: ")
            for row in rs:
                print(f"\tFor season {row[3]}: {row[1]}")
        
        print("\n")
        userInput = input("Press enter to return: ")
        print("\n")
                
def search_reviews(cn):
    user_show = input("Enter which show you would like to see reviews for: ")
    print("\n")

    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (user_show,))

        if not rs.fetchone():
            print("This TV show does not exist.")
            print("\n")
            return
    
    while True:
        q = ("SELECT ROW_NUMBER() OVER (ORDER BY reviewer_name), reviewer_name FROM season_review WHERE show_title = %s GROUP BY reviewer_name;")
        with cn.cursor() as rs:
            rs.execute(q, (user_show,))

            print(f"Reviewers that have reviewed {user_show}: ")
            for row in rs:
                print(f"\t{row[0]}. {row[1]}")

        print("\n")
        user_reviewer = input(f"Enter the name of the reviewer to view the review scores for {user_show} or press enter to exit: ")
        print("\n")
        
        if user_reviewer == "":
            break

        q = ("SELECT * "
             "FROM season_review JOIN review USING (reviewer_name) "
             "WHERE show_title = %s AND reviewer_name = %s "
             "ORDER BY season_num ASC;")
        with cn.cursor() as rs:
            rs.execute(q, (user_show, user_reviewer))

            if not rs.fetchone():
                print(f"{user_show} has not been reviewed by {user_reviewer}.")
                print("\n")
                continue

        q = ("SELECT season_num, review_score, review_metric, review_max "
             "FROM season_review JOIN review USING (reviewer_name) "
             "WHERE show_title = %s AND reviewer_name = %s "
             "ORDER BY season_num ASC;")
        with cn.cursor() as rs:
            rs.execute(q, (user_show, user_reviewer))

            
            print(f"Review scores for {user_show} by {user_reviewer}: ")
            for row in rs:
                print(f"\tFor season {row[0]}: {row[1]} out of {row[3]} {row[2]}")
        
        print("\n")
        userInput = input("Press enter to return: ")
        print("\n")