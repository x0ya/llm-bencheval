from search import search_web

for s in search_web("Who wrote Romeo and Juliet?"):
    print(s["title"], "|", s["url"])
