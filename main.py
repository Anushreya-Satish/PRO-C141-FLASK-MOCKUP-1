from flask import Flask, jsonify, request
import pandas as pd

articles_data = pd.read_csv('articles.csv')
all_articles = articles_data[['url' , 'title' , 'text' , 'lang' , 'total_events']]
liked_articles = []
not_liked_articles = []

app = Flask(__name__)

def assign_val():
    m_data = {
        "url": all_articles.iloc[0,0],
        "title": all_articles.iloc[0,1],
        "text": all_articles.iloc[0,2] or "N/A",
        "lang": all_articles.iloc[0,3],
        "total_events": all_articles.iloc[0,4]
    }
    return m_data

# API to display first article
@app.route("/get-article")
def get_article():
  articles_data = assign_val()
  return jsonify ({
    "data" : articles_data,
    "status" : "success",
  })

# API to move the article into liked articles list
@app.route("/liked-article",methods = ["POST"])
def liked_article():
  global all_articles
  articles_data = assign_val()
  liked_articles.append(articles_data)
  all_articles.drop([0], inplace =True)
  all_articles = all_articles.reset_index(drop=True)
  return jsonify({"status":"success"})
@app.route("/liked")
def liked ():
  global liked_articles
  return jsonify({"data":liked_articles, "status":"success"})

# # API to move the article into not liked articles list
@app.route("/unliked-article", methods=["POST"])
def unliked_article():
  global all_articles
  articles_data = assign_val()
  not_liked_articles.append(articles_data)
  all_articles.drop([0], inplace =True)
  all_articles = all_articles.reset_index(drop=True)
  return jsonify({"status":"success"})
@app.route("/unliked")
def unliked ():
  global not_liked_articles
  return jsonify({"data":not_liked_articles, "status":"success"})

# run the application
if __name__ == "__main__":
    app.run()