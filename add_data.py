def menu(cn):

    while True:
        print("1. Add TV show")
        print("2. Add a new season to a show")
        print("3. Add a new episode to a show")
        print("4. Add a new actor")
        print("5. Credit an actor to a TV show episode")
        print("6. Add in a new award that a TV show has won")
        print("7. Add in a new review for a TV show season")
        print("8. Add a new director")
        print("9. Credit a director to a TV show episode")
        print("10. Return to main menu\n")

        choice = input("What information would you like to add (1-10): ")
        print("\n")

        match choice:
            case "1":
                add_show(cn)
            case "2":
                add_season(cn)
            case "3":
                add_ep(cn)
            case "4":
                add_actor(cn)
            case "5":
                credit_actor(cn)
            case "6":
                add_award(cn)
            case "7":
                add_review(cn)
            case "8":
                add_director(cn)
            case "9":
                credit_director(cn)
            case "10":
                return

def add_show(cn):
    new_name = input("Enter the new TV show name: ")

    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    
    with cn.cursor() as rs:
        rs.execute(q, (new_name,))

        if rs.fetchone():
            print("This TV show already exists")
            print("\n")
            return
        
    new_year = input("Enter the year the TV show was first released: ")
    new_curr_running = input("Is this show currently running? (True/False) ")
    print("\n")

    if new_curr_running.lower() == 'false':
        new_curr_running = False
    else:
        new_curr_running = True

    q = ("SELECT ROW_NUMBER() OVER (ORDER BY genre_name), genre_name FROM genre;")
    with cn.cursor() as rs:
        rs.execute(q)

        for row in rs:
            print(f"{row[0]}. {row[1]}")

    print("\n")
    new_genre = input("Enter the genre name for this show from the list of options above: ")
    print("\n")

    q = ("SELECT * FROM genre WHERE genre_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (new_genre,))

        if not rs.fetchone():
            print(f"{new_genre} is not a genre from the list above.")
            print("\n")
            return

    q = ("INSERT INTO tv_show VALUES (%s, %s, %s, %s);")

    with cn.cursor() as rs:
        rs.execute(q, (new_name, new_year, new_curr_running, new_genre))
        cn.commit()
    
def add_season(cn):
    show_name = input("Enter the name of the show you wish to add a new season to: ")
    print("\n")

    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    
    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        if not rs.fetchone():
            print("This TV show does not exist")
            print("\n")
            return
    
    new_year = input("Which year was this season released? ")
    print("\n")

    q = ("SELECT COUNT(*) FROM show_season WHERE show_title = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        count = rs.fetchone()[0]
        next_season = count + 1
    
    q = ("INSERT INTO show_season VALUES (%s, %s, %s);")

    with cn.cursor() as rs:
        rs.execute(q, (show_name, next_season, new_year))
        cn.commit()
    
    print(f"Successfully added season {next_season} to {show_name}")
    print("\n")
    
def add_ep(cn):
    show_name = input("Enter the name of the show you wish to add a new episode to: ")
    print("\n")

    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    
    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        if not rs.fetchone():
            print("This TV show does not exist")
            print("\n")
            return
    
    q = ("SELECT COUNT(*) FROM show_season WHERE show_title = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        count = rs.fetchone()[0]
    
    season_num = int(input(f"Enter the season number you wish to add a new episode to. There are {count} season(s) in {show_name}: "))
    print("\n")

    if season_num > count:
        print(f"There is no season {season_num} in {show_name}.")
        print("\n")
        return
    
    no_ep = False

    ep_name = input("Enter the new episode name: ")
    q = ("SELECT * FROM show_episode WHERE show_title = %s AND season_num = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num))

        if not rs.fetchone():
            ep_num = 1
            no_ep = True

    if not no_ep:
        q = ("SELECT MAX(ep_num) FROM show_episode WHERE show_title = %s AND season_num = %s;")

        with cn.cursor() as rs:
            rs.execute(q, (show_name, season_num))

            count = rs.fetchone()[0]
            ep_num = count + 1
    
    if ep_name == "":
        ep_name = f"Episode {ep_num}"
    
    ep_length = input("Enter the length of the episode (in minutes): ")
    print("\n")

    q = ("INSERT INTO show_episode VALUES (%s, %s, %s, %s, %s);")

    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num, ep_num, ep_name, ep_length))
        cn.commit()

def add_actor(cn):
    new_name = input("Enter the stage name of the new actor you wish to add: ")
    print("\n") 

    q = ("SELECT * FROM actor WHERE stage_name = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (new_name,))

        if rs.fetchone():
            print("This actor already exists.")
            print("\n")
            return
    
    new_fname = input("Enter the first name of the actor: ")
    new_lname = input("Enter the last name of the actor: ")

    q = ("INSERT INTO actor VALUES (%s, %s, %s);")

    with cn.cursor() as rs:
        rs.execute(q, (new_name, new_fname, new_lname))
        cn.commit()
    
def credit_actor(cn):
    actor_name = input("Enter the stage name of the actor you wish to credit: ")

    q = ("SELECT * FROM actor WHERE stage_name = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (actor_name,))

        if not rs.fetchone():
            print("This actor does not exist.")
            print("\n")
            return
    
    show_name = input("Enter the name of the show you wish to credit the actor: ")

    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    
    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        if not rs.fetchone():
            print("\n")
            print("This TV show does not exist")
            print("\n")
            return
    
    q = ("SELECT COUNT(*) FROM show_season WHERE show_title = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        count = rs.fetchone()[0]
    
    if count == 0:
        print("\n")
        print(f"{show_name} currently has no seasons. Please add a new season first.")
        print("\n")
        return
            
    season_num = int(input(f"Enter the season number of the show you wish to credit the actor in. There are {count} season(s) in {show_name}: "))
    print("\n")

    if season_num > count:
        print(f"There is no season {season_num} in {show_name}.")
        print("\n")
        return
    
    q = ("SELECT COUNT(*) FROM show_episode WHERE show_title = %s AND season_num = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num))

        if rs.fetchone()[0] == 0:
            print(f"Season {season_num} from {show_name} currently has no episodes. Please add a new episode first.")
            print("\n")
            return
    
    q = ("SELECT ep_num, ep_name FROM show_episode WHERE show_title = %s AND season_num = %s ORDER BY ep_num ASC;")

    print(f"List of episodes in season {season_num} in {show_name}")
    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num))

        for row in rs:
            print(f"\tEpisode {row[0]}: {row[1]}")
    
    print("\n")
    ep_num = int(input("Enter the episode number you wish to credit the actor to from the list above: "))
    print("\n")

    q = ("SELECT COUNT(*) FROM show_episode WHERE show_title = %s AND season_num = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num))

        count = rs.fetchone()[0]
        
        if ep_num > count:
            print(f"There is no episode {ep_num} in season {season_num} of {show_name}.")
            print("\n")
            return
        
    q = ("SELECT * FROM actor_episode WHERE stage_name = %s AND show_title = %s AND season_num = %s AND ep_num = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (actor_name, show_name, season_num, ep_num))

        if rs.fetchone():
            print(f"{actor_name} is already credited to episode {ep_num} of season {season_num} of {show_name}")
            print("\n")
            return

    q = ("INSERT INTO actor_episode VALUES (%s, %s, %s, %s);")

    with cn.cursor() as rs:
        rs.execute(q, (actor_name, show_name, season_num, ep_num))
        cn.commit()

def add_award(cn):
    
    show_name = input("Enter the name of the show you wish to add an award: ")

    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    
    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        if not rs.fetchone():
            print("\n")
            print("This TV show does not exist")
            print("\n")
            return
    
    q = ("SELECT COUNT(*) FROM show_season WHERE show_title = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        count = rs.fetchone()[0]
    
    if count == 0:
        print("\n")
        print(f"{show_name} currently has no seasons. Please add a new season first.")
        print("\n")
        return
            
    season_num = int(input(f"Enter the season number of the show you wish add an award to. There are {count} season(s) in {show_name}: "))
    print("\n")

    if season_num > count:
        print(f"There is no season {season_num} in {show_name}.")
        print("\n")
        return
    
    print(f"List of award shows: ")
    q = ("SELECT DISTINCT award_show_name FROM award_show;")
    with cn.cursor() as rs:
        rs.execute(q)

        for row in rs:
            print(f"\t{row[0]}")

    print("\n")
    award_show = input(f"Enter the full name of the award show that season {season_num} of {show_name} has been awarded from the list above: ")

    q = ("SELECT * FROM award_show WHERE award_show_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (award_show,))

        if not rs.fetchone():
            print("\n")
            print("This show does not exist.")
            print("\n")
            return
    
    q = ("SELECT ROW_NUMBER() OVER (ORDER BY award_name), award_name FROM award_show WHERE award_show_name = %s;")
    print("\n")
    print("List of awards: ")
    with cn.cursor() as rs:
        rs.execute(q, (award_show,))

        for row in rs:
            print(f"\t{row[0]}. {row[1]}")
    print("\n")

    award_name = input(f"Enter the full name of the award you wish to award season {season_num} of {show_name} from the list above: ")
    q = ("SELECT * FROM award_show WHERE award_show_name = %s AND award_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (award_show, award_name))

        if not rs.fetchone():
            print("\n")
            print("This award does not exist.")
            print("\n")
            return
    q = ("SELECT * FROM season_award WHERE award_show_name = %s AND award_name = %s AND show_title = %s AND season_num = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (award_show, award_name, show_name, season_num))

        if rs.fetchone():
            print("\n")
            print(f"Season {season_num} of {show_name} has already been awarded {award_show}'s {award_name}.")
            print("\n")
            return
    
    q = ("INSERT INTO season_award VALUES (%s, %s, %s, %s);")
    with cn.cursor() as rs:
        rs.execute(q, (award_show, award_name, show_name, season_num))
        cn.commit()

    print("\n")

def add_review(cn):
    
    show_name = input("Enter the name of the show you wish to review: ")

    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    
    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        if not rs.fetchone():
            print("\n")
            print("This TV show does not exist")
            print("\n")
            return
    
    q = ("SELECT COUNT(*) FROM show_season WHERE show_title = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        count = rs.fetchone()[0]
    
    if count == 0:
        print("\n")
        print(f"{show_name} currently has no seasons. Please add a new season first.")
        print("\n")
        return
            
    season_num = int(input(f"Enter the season number of the show you wish to review. There are {count} season(s) in {show_name}: "))
    print("\n")

    if season_num > count:
        print(f"There is no season {season_num} in {show_name}.")
        print("\n")
        return
    
    q = ("SELECT ROW_NUMBER() OVER (ORDER BY reviewer_name), reviewer_name FROM review;")

    with cn.cursor() as rs:
        rs.execute(q)

        for row in rs:
            print(f"\t{row[0]}. {row[1]}")

    print("\n")
    reviewer = input("Enter the reviewer name from the list above: ")
    print("\n")

    q = ("SELECT * FROM review WHERE reviewer_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (reviewer,))

        if not rs.fetchone():
            print("This reviewer does not exist.")
            print("\n")
            return
        
    q = ("SELECT * FROM season_review WHERE reviewer_name = %s AND show_title = %s AND season_num = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (reviewer, show_name, season_num))

        if rs.fetchone():
            print(f"A {reviewer} for {show_name} season {season_num} already exists.")
            print("\n")
            return
    
    q = ("SELECT * FROM review WHERE reviewer_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (reviewer,))

        for row in rs:
            metric = row[1]
            max_score = row[2]


    new_score = int(input(f"Please enter the review score. This score should be out of {max_score} {metric}: "))

    if new_score < 0:
        new_score = 0
    if new_score > max_score:
        new_score = max_score

    q = ("INSERT INTO season_review VALUES (%s, %s, %s, %s);")
    with cn.cursor() as rs:
        rs.execute(q, (reviewer, show_name, season_num, new_score))

        cn.commit()

def add_director(cn):
    new_name = input("Enter the stage name of the new director you wish to add: ")
    print("\n") 

    q = ("SELECT * FROM director WHERE stage_name = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (new_name,))

        if rs.fetchone():
            print("This director already exists.")
            print("\n")
            return
    
    new_fname = input("Enter the first name of the director: ")
    new_lname = input("Enter the last name of the director: ")
    print("\n")

    q = ("INSERT INTO director VALUES (%s, %s, %s);")

    with cn.cursor() as rs:
        rs.execute(q, (new_name, new_fname, new_lname))
        cn.commit()

def credit_director(cn):
    director_name = input("Enter the stage name of the director you wish to credit: ")

    q = ("SELECT * FROM director WHERE stage_name = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (director_name,))

        if not rs.fetchone():
            print("This director does not exist.")
            print("\n")
            return
    
    show_name = input("Enter the name of the show you wish to credit the director: ")

    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    
    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        if not rs.fetchone():
            print("\n")
            print("This TV show does not exist")
            print("\n")
            return
    
    q = ("SELECT COUNT(*) FROM show_season WHERE show_title = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        count = rs.fetchone()[0]
    
    if count == 0:
        print("\n")
        print(f"{show_name} currently has no seasons. Please add a new season first.")
        print("\n")
        return
            
    season_num = int(input(f"Enter the season number of the show you wish to credit the actor in. There are {count} season(s) in {show_name}: "))
    print("\n")

    if season_num > count:
        print(f"There is no season {season_num} in {show_name}.")
        print("\n")
        return
    
    q = ("SELECT COUNT(*) FROM show_episode WHERE show_title = %s AND season_num = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num))

        if rs.fetchone()[0] == 0:
            print(f"Season {season_num} from {show_name} currently has no episodes. Please add a new episode first.")
            print("\n")
            return
    
    q = ("SELECT ep_num, ep_name FROM show_episode WHERE show_title = %s AND season_num = %s ORDER BY ep_num ASC;")

    print(f"List of episodes in season {season_num} in {show_name}")
    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num))

        for row in rs:
            print(f"\tEpisode {row[0]}: {row[1]}")
    
    print("\n")
    ep_num = int(input("Enter the episode number you wish to credit the director to from the list above: "))
    print("\n")

    q = ("SELECT COUNT(*) FROM show_episode WHERE show_title = %s AND season_num = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num))

        count = rs.fetchone()[0]
        
        if ep_num > count:
            print(f"There is no episode {ep_num} in season {season_num} of {show_name}.")
            print("\n")
            return
        
    q = ("SELECT COUNT(*) FROM director_episode WHERE stage_name = %s AND show_title = %s AND season_num = %s AND ep_num = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (director_name, show_name, season_num, ep_num))

        if rs.fetchone()[0] != 0:
            print(f"{director_name} is already credited to episode {ep_num} of season {season_num} of {show_name}")
            print("\n")
            return

    q = ("INSERT INTO director_episode VALUES (%s, %s, %s, %s);")

    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num, ep_num, director_name))
        cn.commit()