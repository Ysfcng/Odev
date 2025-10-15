import datetime
import json 
from typing import List, Dict

BOOKS = [{"id": 1, "title": "Kitap 1","author":"asd",'due_time':datetime.date(2025, 10, 28),"borrowed_by":""}, {"id": 2,"author":"asd",'due_time': datetime.date(2025, 10, 28),"borrowed_by":"", "title": "Kitap 2"}]


def _next_book_id(books: list[dict]) -> int:
    # BUGGY KOD (düzeltin):
    # return books[-1]["id"] + 1

    # BEKLENEN:
    # - Liste boşsa 1 dön
    # - Aksi halde max id + 1
    # TODO: Burayı düzeltin
#    raise NotImplementedError
    if(len(books)<1):
        return 1
    
    return books[len(books)-1]["id"]+1

def add_book(books: list[dict], title: str, author: str) -> dict:
    newBook={
    "id":_next_book_id(books),
    "title":title,
    "author":author,
    "Avaible":True,
    "borrowed_by":"",
    "due_time":None
    }
    if(title=="" or author==""):
        return "error"    
    books.append(newBook)
    print(newBook)
    return newBook

def search_books(books: list[dict], query: str) -> list[dict]:
    """
    Başlık ya da yazarda 'query' geçenleri (case-insensitive) döndürür.
    Boş query -> boş liste.
    """
    str=""
    if(query.strip()=="" or query==None):
        return 
    query=query.lower()
    for x in books:
        if(query in x["title"].lower() or query in  x["author"].lower()):
          str+="\n"+x  
          print(x)
    return str
    # BUGGY KOD:
    # - Büyük/küçük harf duyarlı arıyor
    # - Boş query'de tüm listeyi döndürüyor
    # - None değerleri patlatabilir
    # results = [b for b in books if (query in b["title"] or query in b["author"])]

    # TODO: Hataları giderin.


def borrow_book(books: list[dict], book_id: int, username: str, days: int = 14) -> bool:
    """
    book_id'li kitabı 'username' adına 'days' günlüğüne ayırır.
    Dönüş: True (başarılı) / False (kitap zaten müsait değil ya da yok)
    """
    if(username.strip()=="" or username==None ):
        return "error"
    for x in books:
        if(x["id"]==book_id and x["borrowed_by"]==""):
            x["borrowed_by"]=username
            today=datetime.date.today()
            x["borrowed_by"]=username
            x["Avaible"]=False
            x["due_time"] = today + datetime.timedelta(days=14)
            print(x)

            return  True
     return false
    # TODO:
    # - ID eşleşen kitabı bul
    # - available True ise:
    #     available=False, borrower=username, due_date=_in_days_str(days) ayarla
    #     True dön
    # - Aksi halde False dön
   



def return_book(books: list[dict], book_id: int) -> bool:
    """
    Kitabı iade eder; bulunursa alanları sıfırlar.
    True/False döner.
    """
    # TODO: ID eşleşirse available=True, borrower=None, due_date=None
    if(book_id>len(books) or book_id<0):
        return False

    books[book_id]["borrowed_by"]=""
    books[book_id]["due_time"]=None
    books[book_id]["Avaible"]=True
    print(books[book_id])
    return True

def list_overdue(books: list[dict], today = None) -> list[dict]:
    str=""
    for x in books:
        today=datetime.date.today()
        if(x["Avaible"]==False&&x.get("due_time")<today):
            print("tarihi gecti",x["due_time"])
            str+="\n"+x
    return str
    # TODO:
    # - today yoksa bugünün tarihini kullanın (helper var: _today_str)
    # - due_date < today olan ve available=False olanları seçin



def save_to_file(books: list[dict], path: str) -> None:
    """
    books listesini path'e JSON olarak kaydeder (UTF-8).
    """

    # datetime.date nesnelerini string'e çevir (JSON bu tipleri kaydedemez)
    for b in books:
        if isinstance(b.get("due_time"), (datetime.date, datetime.datetime)):
            b["due_time"] = b["due_time"].isoformat()

    # JSON olarak kaydet
    with open(path, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

save_to_file(BOOKS,"./a.txt")



def load_from_file(path: str) -> list[dict]:
    """
    path'teki JSON içeriğini okuyup kitap listesi döndürür.
    Dosya yoksa boş liste döndürür.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Her kitap için due_time alanını tekrar datetime.date'e çevir
        for b in data:
            due = b.get("due_time")
            if isinstance(due, str):
                try:
                    b["due_time"] = datetime.date.fromisoformat(due)
                except ValueError:
                    b["due_time"] = None  # Bozuk tarih formatı varsa None yap
        books=data
        return data

    except FileNotFoundError:
        print(f"⚠️ Dosya bulunamadı: {path} — Boş liste döndürülüyor.")
        return []

    except json.JSONDecodeError as e:
        print(f"⚠️ JSON okuma hatası ({path}): {e}")
        return []

    except Exception as e:
        print(f"⚠️ Beklenmeyen hata: {e}")
        return []
load_from_file("./a.txt")
