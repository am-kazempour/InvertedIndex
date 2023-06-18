from math import log
import os
import re
import json
cls = lambda: os.system("cls")

def InvertedIndex(text):
    temp_indexter = {}
    clean_text = re.sub(r'[^\w\s]','',text)
    clean_text = clean_text.lower()
    terms = clean_text.split(" ")

    for term in terms:
        term = term.strip()
        if term not in temp_indexter.keys():
            temp_indexter[term] = 1
        else:
            temp_indexter[term] += 1
    
    return temp_indexter
    
def show_db(db,num):
    cls()
    print("-"*25 + "-"*12*num)
    print("|         Term          |" ,end="")
    
    for i in range(num):
        print("Document{:^3}|".format(i+1) , end = "")
    print()
    print("-"*25 + "-"*12*num)
    for term in db.keys():
        temp = "|{:^23}|".format(term)
        for i in range(num):
            temp += "{:^11}|".format(db[term][i])
        print(temp)
        print("-"*25 + "-"*12*num)

def save_db(db,num):
    with open("index.txt","w") as f:
        for term in db.keys():
            temp = term + ":"
            for i in range(num):
                temp += str(db[term][i])+","
            temp = temp[:-1]
            f.write(temp + "\n")

def search(db,num,query):
    query = query.lower()
    query = query.split(" ")
    for i in range(len(query)):
        query[i] = query[i].strip()
    
    point = [0 for i in range(num)]
    for i in range(len(point)):
        for term in query:
            if term in db.keys():
                if db[term][i] == 1:
                    point[i] += 1
                elif db[term][i] >= 1:
                    point[i] += 1 + log(10,db[term][i])
    
    for k,i in enumerate(query):
        if i not in ["not","and","or"]:
            if i in db.keys():
                query[k] = db[i]
            else:
                query = [0 for i in range(num)]

    for k,i in enumerate(query):
        if type(i) == str and i == "not":
            for p,j in enumerate(query[k+1]):
                if j>0:
                    query[k+1][p] = 0
                else:
                    query[k+1][p] = 1
    
    temp = query
    query = []

    for i in range(len(temp)):
        if type(temp[i]) == list or temp[i] != "not":
            query.append(temp[i])
    result = query[0]
    i = 1
    while i < len(query):
        if type(query[i]) == str:
            i += 1
            if query[i-1] == "and":
                for j in range(len(result)):
                    result[j] = result[j] and query[i][j]
            elif query[i-1] == "or":
                for j in range(len(result)):
                    result[j] = result[j] or query[i][j]
        i += 1
    
    for k,i in enumerate(result):
        if i > 0:
            print("Document",k+1)
            print("point:",point[k])
            print("-"*20)

def PositionalIndex(texts,db):
    positional = {}
    for i in range(len(texts)):
        texts[i] = re.sub(r'[^\w\s]','',texts[i])
        texts[i] = texts[i].lower()
        texts[i] = texts[i].split(" ")
    
    for term in db.keys():
        if term not in positional.keys():
            positional[term] = {}
        
        for k,i in enumerate(db[term]):
            temp = []
            if i>0:
                for p,j in enumerate(texts[k]):
                    if j == term:
                        temp.append(p)
            positional[term][k] = temp
    
    # with open("index.json","w") as f:
    #     f.write(json.dumps(positional))
    
    return positional
    
def positional_search(positional,query):
    query = query.lower()
    query = query.split(" ")
    num = int(query[1][1:])
    w_1 = positional[query[0]]
    w_2 = positional[query[2]]
    for k,i in enumerate(w_1.keys()):
        if i + num in w_2[k]:
            print("Document",k+1)

def main():
    db = {}
    file_list = os.listdir("dataBase")
    list_text = []
    for k,file in enumerate(file_list):
        with open("dataBase/"+file , encoding="utf8") as f:
            text = f.read()
            terms = InvertedIndex(text)
            list_text.append(text)
            for term in terms.keys():
                if term not in db.keys():
                    db[term] = [0 for i in range(len(file_list))]
                db[term][k] = terms[term]
    
    cls()
    print("-"*50)
    print("|{:-^48}|".format(" wellcome "))
    print("-"*50)
    print("\n\n")
    print("    -1)Show Inverted index")
    print("    -2)Show Inverted index")
    print("    -3)Show Inverted index")
    print("    -4)Show Inverted index")
    key = input("choose key(1-3):")
    cls()
    if key == "1":
        show_db(db,len(file_list))
    elif key == "2":
        save_db(db,len(file_list))
        print("Saved.")
    elif key == "3":
        query = input("Enter your query: ")
        search(db,len(file_list),query)
    elif key == "4":
        positional = PositionalIndex(list_text,db)
        query = input("Enter your query: ")
        positional_search(positional,query)


    # show_db(db,len(file_list))
    #save_db(db,len(file_list))
    #search(db,len(file_list),"programming to api")
main()