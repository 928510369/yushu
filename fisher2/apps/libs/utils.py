
def isbn_or_key(q):
    res="key"

    if len(q)==13 and q.isdigit():
        res="isbn"
    short_q=q.replace("-","")
    if "-" in q and len(short_q)==10 and short_q.isdigit():
        res="isbn"

    return res



