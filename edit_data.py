def menu(cn):

    while True:
        print("1. Edit the name of an episode")
        print("2. Set a TV show to be currently running/not running")
        print("3. Edit the review score of a TV show season")
        print("4. Return to main menu\n")

        choice = input("What information would you like to add (1-4): ")
        print("\n")

        match choice:
            case "1":
                edit_ep_name(cn)
            case "2":
                edit_running(cn)
            case "3":
                edit_review(cn)
            case "4":
                return

def edit_ep_name(cn):
   
    show_name = input("Enter the name of the show of the episode you wish to edit the name of: ")
    print("\n")

    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    
    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        if not rs.fetchone():
            print("This TV show does not exist")
            print("\n")
            return
    
    q = ("SELECT MAX(season_num) FROM show_season WHERE show_title = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        count = rs.fetchone()[0]
    
    season_num = int(input(f"Enter the season number of the episode you wish to edit the name of. There are {count} season(s) in {show_name}: "))
    print("\n")

    if season_num > count:
        print(f"There is no season {season_num} in {show_name}.")
        print("\n")
        return
    
    print(f"List of all episodes from {show_name} season {season_num}:")

    q = ("SELECT ep_num, ep_name FROM show_episode WHERE show_title = %s AND season_num = %s ORDER BY ep_num ASC;")
    
    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num))

        for row in rs:
            print(f"\tEpisode {row[0]}: {row[1]}")

    print("\n")

    ep_num = int(input("Enter the episode number you wish to change the name of from the list above: "))
    print("\n")

    q = ("SELECT * FROM show_episode WHERE show_title = %s AND season_num = %s AND ep_num = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num, ep_num))

        if not rs.fetchone():
            print("\n")
            print(f"Episode {ep_num} does not exist.")
            print("\n")
            return
    
    new_name = input("Enter the name you wish to change the name to: ")
    print("\n")

    q = ("UPDATE show_episode SET ep_name = %s WHERE show_title = %s AND season_num = %s AND ep_num = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (new_name, show_name, season_num, ep_num))
        cn.commit()

def edit_running(cn):
    
    show_name = input("Enter the TV show name you wish to set to running/not running: ")
    print("\n")
    
    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        if not rs.fetchone():
            print("\n")
            print(f"{show_name} does not exist.")
            print("\n")
            return
    
    q = ("SELECT currently_running FROM tv_show WHERE show_title = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        curr_run = rs.fetchone()[0]
    
    q = ("UPDATE tv_show SET currently_running = %s WHERE show_title = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (not curr_run, show_name))
        cn.commit()

    if curr_run:
        print(f"{show_name} is now set to be not running")
    else:
        print(f"{show_name} is no longer running")

    print("\n")

def edit_review(cn):
    show_name = input("Enter the name of the show of the season you wish to edit the review score of: ")
    print("\n")

    q = ("SELECT * FROM tv_show WHERE show_title = %s;")
    
    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        if not rs.fetchone():
            print("This TV show does not exist")
            print("\n")
            return
    
    q = ("SELECT MAX(season_num) FROM show_season WHERE show_title = %s;")
    
    with cn.cursor() as rs:
        rs.execute(q, (show_name,))

        count = rs.fetchone()[0]
    
    season_num = int(input(f"Enter the season number you wish to edit the review score of. There are {count} season(s) in {show_name}: "))
    print("\n")

    if season_num > count:
        print(f"There is no season {season_num} in {show_name}.")
        print("\n")
        return
    
    print(f"List of all reviewers who have reviewed season {season_num} of {show_name}:")

    q = ("SELECT ROW_NUMBER() OVER (ORDER BY reviewer_name), reviewer_name, review_score, review_metric, review_max"
        " FROM season_review JOIN review USING (reviewer_name)"
        " WHERE show_title = %s AND season_num = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num))

        for row in rs:
            print(f"\t{row[0]}. {row[1]}: {row[2]} out of {row[3]} {row[4]}")
    
    print("\n")
    change_review = input("Enter the name of the reviewer you wish to change the review of: ")

    q = ("SELECT * FROM review WHERE reviewer_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (change_review,))

        if not rs.fetchone():
            print("\n")
            print(f"{change_review} does not exist as a reviewer.")
            print("\n")
            return
        
    new_review = int(input(f"Enter the new score for season {season_num} of {show_name}: "))

    q = ("UPDATE season_review SET review_score = %s WHERE reviewer_name = %s AND show_title = %s AND season_num = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (new_review, change_review, show_name, season_num))
        cn.commit()
