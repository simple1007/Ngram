def ngrams(text, n, word='word'):
    #result = []
    for line in text:
        line = line.replace('\'','').replace('\n','').replace('"','').replace('.','').replace(' ','_').replace(',','')
        if word == 'word':
            templine = line.split(' ')
        else:
            templine = list(line)
        
        templine.insert(0, 'SS')
        templine.append('SE')
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

def main():
    with open('C:/Users/nlp/Desktop/nlplab/Ngram-new/KCC150_Korean_sentences_UTF8.txt','r',encoding='utf-8') as f:
        text = f.readlines()
    for i in ngrams(text,2):
        print(i)
    #    print(i)
    
    print(len(text))

if  __name__ == "__main__":
    main()
