def convert_sql_to_kb(dataset):
    import pytholog as pl
    kb = []
    for data in dataset:
        likes_drink = f"likes_drink({data[1].lower()}, {data[2].lower()})"
        likes_taste = f"likes_taste({data[1].lower()}, {data[3].lower()})"
        taste_combines = f"taste_combines({data[2].lower()}, {data[3].lower()})"

        likes_color = f"likes_color({data[1].lower()}, {data[4].lower()})"
        likes_music = f"likes_music({data[1].lower()}, {data[5].lower()})"
        art_combines = f"art_combines({data[2].lower()}, {data[3].lower()})"

        kb.append(likes_drink)
        kb.append(likes_taste)
        kb.append(taste_combines)

        kb.append(likes_color)
        kb.append(likes_music)
        kb.append(art_combines)

    taste_to_like = f"taste_to_like(X, Z) :- likes_drink(X, Y), taste_combines(Y, Z)"
    drink_to_like = f"drink_to_like(X, Z) :- likes_taste(X, Y), taste_combines(Y, Z)"
    color_to_like = f"color_to_like(X, Z) :- likes_music(X, Y), art_combines(Y, Z)"
    music_to_like = f"music_to_like(X, Z) :- likes_color(X, Y), art_combines(Y, Z)"

    kb.append(taste_to_like)
    kb.append(drink_to_like)
    kb.append(color_to_like)
    kb.append(music_to_like)

    new_kb = pl.KnowledgeBase("interests")
    new_kb(kb)
    return new_kb

def taste_combines(kb, taste):
    import pytholog as pl
    return kb.query(pl.Expr(f"taste_combines({taste}, What)"))

def art_combines(kb, art):
    import pytholog as pl
    return kb.query(pl.Expr(f"taste_combines({art}, What)"))