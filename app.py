from flask import Flask, render_template, request, flash, redirect, url_for, abort

app = Flask(__name__)
app.secret_key = "dev-secret-key"

# ------------------ Дані (демо) ------------------
# У static/img/posters/ поклади відповідні файли:
# interstellar.jpg, dark_knight.jpg, parasite.jpg, inception.jpg,
# grand_budapest.jpg, whiplash.jpg, spirited_away.jpg, get_out.jpg

MOVIES = [
    {
        "id": 1,
        "title": "Interstellar",
        "year": 2014,
        "genre": "Sci-Fi",
        "rating": 8.6,
        "duration": 169,
        "director": "Christopher Nolan",
        "poster": "img/posters/interstellar.jpg",
        "desc": "Команда дослідників вирушає крізь космічний портал у пошуках нового дому для людства."
    },
    {
        "id": 2,
        "title": "The Dark Knight",
        "year": 2008,
        "genre": "Action",
        "rating": 9.0,
        "duration": 152,
        "director": "Christopher Nolan",
        "poster": "img/posters/dark_knight.jpg",
        "desc": "Бетмен протистоїть Джокеру, який руйнує межі між добром і хаосом."
    },
    {
        "id": 3,
        "title": "Parasite",
        "year": 2019,
        "genre": "Drama",
        "rating": 8.5,
        "duration": 132,
        "director": "Bong Joon-ho",
        "poster": "img/posters/parasite.jpg",
        "desc": "Дві сім’ї з різних соціальних світів несподівано переплітають свої долі."
    },
    {
        "id": 4,
        "title": "Inception",
        "year": 2010,
        "genre": "Sci-Fi",
        "rating": 8.8,
        "duration": 148,
        "director": "Christopher Nolan",
        "poster": "img/posters/inception.jpg",
        "desc": "Команда проникає в сни, щоб викрасти або підмінити ідею у свідомості людини."
    },
    {
        "id": 5,
        "title": "The Grand Budapest Hotel",
        "year": 2014,
        "genre": "Comedy",
        "rating": 8.1,
        "duration": 99,
        "director": "Wes Anderson",
        "poster": "img/posters/grand_budapest.jpg",
        "desc": "Пригоди легендарного консьєржа і його протеже в Європі міжвоєнного періоду."
    },
    {
        "id": 6,
        "title": "Whiplash",
        "year": 2014,
        "genre": "Drama",
        "rating": 8.5,
        "duration": 106,
        "director": "Damien Chazelle",
        "poster": "img/posters/whiplash.jpg",
        "desc": "Молодий барабанщик і жорсткий викладач: ціна досконалості та амбіцій."
    },
    {
        "id": 7,
        "title": "Spirited Away",
        "year": 2001,
        "genre": "Animation",
        "rating": 8.6,
        "duration": 125,
        "director": "Hayao Miyazaki",
        "poster": "img/posters/spirited_away.jpg",
        "desc": "Дівчинка потрапляє у світ духів і шукає шлях додому, рятуючи батьків."
    },
    {
        "id": 8,
        "title": "Get Out",
        "year": 2017,
        "genre": "Horror",
        "rating": 7.8,
        "duration": 104,
        "director": "Jordan Peele",
        "poster": "img/posters/get_out.jpg",
        "desc": "Знайомство з батьками дівчини перетворюється на тривожну пастку."
    },
]

def get_movie(movie_id: int):
    for m in MOVIES:
        if m["id"] == movie_id:
            return m
    return None

def get_genres():
    return sorted(set(m["genre"] for m in MOVIES))

@app.route("/")
def index():
    top = sorted(MOVIES, key=lambda x: x["rating"], reverse=True)[:3]
    return render_template("index.html", title="Головна", top=top)

@app.route("/about")
def about():
    return render_template("about.html", title="Про сайт")

@app.route("/movies")
def movies():
    q = request.args.get("q", "").strip().lower()
    genre = request.args.get("genre", "").strip()
    sort = request.args.get("sort", "rating_desc").strip()

    filtered = MOVIES

    if genre:
        filtered = [m for m in filtered if m["genre"] == genre]

    if q:
        filtered = [
            m for m in filtered
            if q in m["title"].lower()
            or q in m["director"].lower()
            or q in m["desc"].lower()
        ]

    if sort == "rating_desc":
        filtered = sorted(filtered, key=lambda x: x["rating"], reverse=True)
    elif sort == "rating_asc":
        filtered = sorted(filtered, key=lambda x: x["rating"])
    elif sort == "year_desc":
        filtered = sorted(filtered, key=lambda x: x["year"], reverse=True)
    elif sort == "year_asc":
        filtered = sorted(filtered, key=lambda x: x["year"])
    elif sort == "title_asc":
        filtered = sorted(filtered, key=lambda x: x["title"].lower())

    return render_template(
        "movies.html",
        title="Фільми",
        movies=filtered,
        q=q,
        genre=genre,
        genres=get_genres(),
        sort=sort
    )

@app.route("/movies/<int:movie_id>")
def movie_detail(movie_id):
    movie = get_movie(movie_id)
    if not movie:
        abort(404)
    return render_template("movie_detail.html", title=movie["title"], movie=movie)

@app.route("/genres")
def genres():
    genres_list = get_genres()
    counts = {g: 0 for g in genres_list}
    for m in MOVIES:
        counts[m["genre"]] += 1
    return render_template("genres.html", title="Жанри", genres=genres_list, counts=counts)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Заповни всі поля.", "error")
        else:
            flash("Дякуємо! Повідомлення надіслано (демо).", "success")
            return redirect(url_for("contact"))

    return render_template("contact.html", title="Контакти")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", title="Сторінку не знайдено"), 404

if __name__ == "__main__":
    app.run(debug=True)
