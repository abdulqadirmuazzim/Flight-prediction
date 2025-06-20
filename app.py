from flask import Flask, render_template, request, redirect, url_for
from data import (
    route_list,
    sources,
    destinations,
    additional_info,
    airline,
    filter_routes,
)


app = Flask(__name__)


@app.route("/")
def home():
    return render_template(
        "index.html",
        sources=sources,
        destinations=destinations,
        routes=route_list,
        add_info=additional_info,
        airline=airline,
    )


@app.route("/next")
def another():
    return "<h1>This is another page!</h1>"


@app.route("/check_route")
def check_route():
    route = request.args.get(key="route")
    stops = len(route.split("→")) - 2
    return str(stops)


# remove Route

# Scraping urls
# 1. :
# https://foreteconline.com/?s=HP+PC&product_cat=0&post_type=product

# 2. :
# https://foreteconline.com/page/2/?s=HP+Printer&product_cat=0&post_type=product&v=330a840f8637

if __name__ == "__main__":
    app.run(debug=True)
