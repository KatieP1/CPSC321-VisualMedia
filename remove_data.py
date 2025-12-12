def menu(cn):

    while True:
        print("1. Remove a director from a TV show episode")
        print("2. Remove an actor from a TV show episode")
        print("3. Delete an episode")
        print("4. Return to main menu\n")

        choice = input("What information would you like to add (1-4): ")
        print("\n")

        match choice:
            case "1":
                remove_director(cn)
            case "2":
                remove_actor(cn)
            case "3":
                remove_episode(cn)
            case "4":
                return
            
def remove_director(cn):
    director_to_del = input("Enter the stage name of the director you wish to remove credit: ")
    print("\n")

    q = ("SELECT * FROM director WHERE stage_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (director_to_del,))

        if not rs.fetchone():
            print("This director does not exist.")
            return
    
    show_name = input("Enter the name of the show of the episode you wish to delete the director from: ")
    print("\n")

    q = ("SELECT * FROM director_episode WHERE show_title = %s AND stage_name = %s;")
    
    with cn.cursor() as rs:
        rs.execute(q, (show_name,director_to_del))

        if not rs.fetchone():
            print(f"{director_to_del} is not credited to the show {show_name}")
            print("\n")
            return
    
    season_num = int(input("Enter the season number of the episode you wish to delete the director from: "))
    ep_num = int(input("Enter the episode number of the season you wish to delete the director from: "))
    print("\n")

    q = ("SELECT * FROM director_episode WHERE show_title = %s AND season_num = %s AND ep_num = %s AND stage_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name,season_num, ep_num, director_to_del))

        if not rs.fetchone():
            print(f"{director_to_del} is not credited to season {season_num} episode {ep_num}")
            print("\n")
            return
        
    q = ("DELETE FROM director_episode WHERE show_title = %s AND season_num = %s AND ep_num = %s AND stage_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name,season_num, ep_num, director_to_del))
        cn.commit()
    
    print("\n")

def remove_actor(cn):
    actor_to_del = input("Enter the stage name of the actor you wish to remove credit: ")
    print("\n")

    q = ("SELECT * FROM actor WHERE stage_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (actor_to_del,))

        if not rs.fetchone():
            print("This actor does not exist.")
            return
    
    show_name = input("Enter the name of the show of the episode you wish to delete the actor from: ")
    print("\n")

    q = ("SELECT * FROM actor_episode WHERE show_title = %s AND stage_name = %s;")
    
    with cn.cursor() as rs:
        rs.execute(q, (show_name,actor_to_del))

        if not rs.fetchone():
            print(f"{actor_to_del} is not credited to the show {show_name}")
            print("\n")
            return
    
    season_num = int(input("Enter the season number of the episode you wish to delete the actor from: "))
    ep_num = int(input("Enter the episode number of the season you wish to delete the actor from: "))
    print("\n")

    q = ("SELECT * FROM actor_episode WHERE show_title = %s AND season_num = %s AND ep_num = %s AND stage_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name,season_num, ep_num, actor_to_del))

        if not rs.fetchone():
            print(f"{actor_to_del} is not credited to season {season_num} episode {ep_num}")
            print("\n")
            return
        
    q = ("DELETE FROM actor_episode WHERE show_title = %s AND season_num = %s AND ep_num = %s AND stage_name = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name,season_num, ep_num, actor_to_del))
        cn.commit()
    
    print("\n")

def remove_episode(cn):
    show_name = input("Enter the name of the show of the episode you wish to delete: ")
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
    
    season_num = int(input(f"Enter the season number of the episode you wish to delete. There are {count} season(s) in {show_name}: "))
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
            print(f"\tEpisode {row[0]}. {row[1]}")

    print("\n")

    ep_num = int(input("Enter the episode number you wish to delete from the list above: "))
    print("\n")

    q = ("SELECT * FROM show_episode WHERE show_title = %s AND season_num = %s AND ep_num = %s;")

    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num, ep_num))

        if rs.fetchone():
            print("\n")
            print(f"Episode {ep_num} does not exist.")
            print("\n")
            return
    
    q = ("DELETE FROM director_episode WHERE show_title = %s AND season_num = %s AND ep_num = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num, ep_num))

        cn.commit()

    q = ("DELETE FROM actor_episode WHERE show_title = %s AND season_num = %s AND ep_num = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num, ep_num))

        cn.commit()
    
    q = ("DELETE FROM show_episode WHERE show_title = %s AND season_num = %s AND ep_num = %s;")
    with cn.cursor() as rs:
        rs.execute(q, (show_name, season_num, ep_num))

        cn.commit()
