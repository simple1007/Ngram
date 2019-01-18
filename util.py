#from konlpy.tag import Okt
import pymysql
import sys

def post(a):
    result = []
    for i in a:
        if i[1] == 'Noun':
            result.append(i[0])
    
    return result

def ngrams(text, n, word='word'):
    #result = []
    #twitter = Okt()
    for line in text:
        
        if word == 'word':
            line = line.replace('\'','').replace('\n','').replace('"','').replace('.','').replace('\t',' ').replace(',','').replace('(','').replace(')','').replace('=','').replace('  ',' ')
            line = ' '.join(line.split())
            templine = line.split(' ')
            #templine = twitter.nouns(line)
        else:
            line = line.replace('\'','').replace('\n','').replace('"','').replace('.','').replace(' ','').replace('\t','').replace(',','').replace('(','').replace(')','').replce('=','').replace('  ',' ')
            line = ' '.join(line.split())
            templine = list(line)
        
        #templine.insert(0, 'SS')
        #templine.append('SE')
        #yield enumerate(templine)
        tempresult = []
        if len(templine) < n:
            a = ['_'] * (n - len(templine))
            templine += a
        for index, tline in enumerate(templine):
            if index == len(templine) - n + 1:
                break
            tempresult.append(templine[index:index + n])
            #yield "{} {}".format(index,(index+n-1))
            
        yield tempresult   
        #result.append(tempresult)
    
    #return result

def make_db_word_list(path,word='word'):
    db = pymysql.connect('localhost','root','0000','Ngram')
    cursor = db.cursor()
    count = 0
    result = []
    
    with open(path,'r',encoding='utf-8') as f:
        #for line_list in ngrams(f,1,word=word):
            
           #for line in line_list:
        for line in f : 
            temp = line.replace('\n','').split('\t')
            # result.append((line[0],word,line[0]))
            count+=1
            sql = 'insert into wordlist (word) select \''+temp[3]+'\' from dual where not exists (select * from wordlist where word = \''+temp[3]+'\')'
            cursor.execute(sql)
            db.commit()
            #print('commit')
            #if count % 1000 == 0:
                #db.commit()
                #print(count)
            
    
    #sql = 'insert into wordlist (word, wordtype) select %s,%s from dual where not exists (select * from wordlist where word = %s)'
    #cursor.execut(sql,result)
                
    #db.commit()
    db.close()

def make_db_insert(path,word,mal,n=1):
    count = 0
    db = pymysql.connect('localhost','root','0000','Ngram')
    cursor = db.cursor()
    with open(path,'r',encoding='utf-8') as f:
        if n == 1:
            for line in f:
                temp = line.replace('\n','').split('\t')
                if not temp[3].startswith('SS') and not temp[3].endswith('SE'):
                    sql = '''insert into uni (doc1,freq,prob,wordtype,mal) select wl.id, \'{}\',\'{}\',
                    wordtype.id, mal.id from wordlist as wl, mal, wordtype where wl.word = \'{}\' and mal.mal=\'{}\' and wordtype.wordtype = \'{}\''''
                    sql = sql.format(temp[1],temp[2],temp[3],mal,word)
                    # db = pymysql.connect('localhost','root','0000','Ngram')
                    
                    cursor.execute(sql)
                    count += 1

                    # if count % 3000 == 0:
                    #     db.commit()
                    # if count == 100000:
                    #     break
                    db.commit()
            db.close()
        
        if n == 2:
            for line in f:
                temp = line.replace('\n','').split('\t')
                if not temp[3].startswith('SS') and not temp[3].endswith('SE'):
                    doc = temp[3].split(',')
                    sql = '''insert into bi (doc1,doc2,freq,prob,wordtype,mal) select wl.id, wl2.id,\'{}\',\'{}\',
                    wordtype.id, mal.id from (select id from wordlist where word=\'{}\') as wl2, wordlist as wl, mal, wordtype where wl.word = \'{}\' and mal.mal=\'{}\' and wordtype.wordtype = \'{}\''''
                    sql = sql.format(temp[1],temp[2],doc[1],doc[0],mal,word)
                    
                    #cursor = db.cursor()
                    cursor.execute(sql)
                    count += 1

                    # if count % 3000 == 0:
                    #     db.commit()
                    # if count == 100000:
                    #     break
                    db.commit()
            db.close()


def main():
    make_db_word_list(sys.argv[1])
    # with open('C:/Users/nlp/Desktop/nlplab/Ngram-new/KCC150_Korean_sentences_UTF8.txt','r',encoding='utf-8') as f:
    #     text = f.readlines()
    # for i in ngrams(text,2):
    #     print(i)
    # #    print(i)
    
    # print(len(text))

if  __name__ == "__main__":
    main()
