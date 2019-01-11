from abc import ABC
from util import ngrams
from collections import defaultdict
from time import strftime
from time import time
from os import rename, listdir

import os
import sys

BASEPATH = '/home/nlp/Desktop/Ngram/'

class Ngram(ABC):
    def __init__(self,N,path,wordtype):
        self.N = N
        self.path = path
        self.wordtype = wordtype

    def ngrams(self):
        pass
    #빈도수 반환
    def freq(self,*word):
        pass
    #음절/어절 확률 반환
    def prob(self,*word):
        pass
    #빈도 카운트
    def freqs(self,n,order='desc'):
        pass
    #상위 n개의 확률 반환
    def probs(self,n,order='desc'):
        pass
    
    def make_freq(self):
        pass
    
    def make_prob(self):
        pass

    def out(self):
        pass
    
    def make(self,ngramstr,makeline):
        file = open(self.path,'r',encoding='utf-8')
        fileindex = 0
        filecount = 0
        fw = open(BASEPATH+ngramstr+'/'+self.wordtype+'%d.txt' % fileindex,'w',encoding='utf-8')
        #print(len(file.readlines()))
        #if self.N != 1:
        for line in ngrams(file,self.N,word=self.wordtype):
            #temp = line.replace('\n','').split('\t')
            for i in line:
                templine = makeline(i)
                fw.write(templine+'\n')
                filecount += 1

                if filecount % 1000 == 0:
                    fw.flush()

                if filecount >= 20000000:
                    #print(filecount)
                    fileindex += 1
                    fw.close()
                    fw = open(BASEPATH+ngramstr+'/'+self.wordtype+'%d.txt' % fileindex,'w',encoding='utf-8')
                    filecount = 0

        fw.close()
        file.close()
    
    def make_freq_out(self,path,makeline):
        #prevgram = defaultdict(int)
        currentgram = defaultdict(int)
        with open(path,'r',encoding='utf-8') as f:
            for line in f:
                #print(line)
                temp = line.replace('\n','').replace('\t',',')#.split('\t')
                # templine = makeline(temp)
                # templine = templine.replace('\t',',')
                # print(temp)
                # print(templine)
                #prevgram[templine] += 1
                #if self.N != 1:
                #    currentgram[templine+',{}'.format(temp[self.N-1])] += 1
                #else:
                currentgram[temp] += 1
        
        pathresult = path.replace('.txt','')
        with open(pathresult+'freq.txt','w',encoding='utf-8') as f:
            for key, value in currentgram.items():
                #temp = key.replace('\n','').replace('\t',',')
                #temp = temp.split
                #templine = makeline(temp)
                #if self.N != 1:
                    #f.write(key+',{},{}\n'.format(prevgram[temp[0]],value))
                #else:
                f.write(('\t{}\t'+ key+'\n').format(value))

    def mergeBig(self,path):
        if os.path.exists('output.txt'):
            result2 = open('output.txt','r',encoding='utf-8')
        
        file = open(path,'r',encoding='utf-8')

        # prevgram = defaultdict(int)
        currentgram = defaultdict(int)

        # file1flag = defaultdict(int)
        # file2flag = defaultdict(int)
        
        # if self.N != 1:
        for line in file:
            temp = line.replace('\n','').split('\t')
            currentgram[temp[2]] += int(temp[1])

            #if temp[0] not in file1flag.keys():
            #    file1flag[temp[0]] += 1
            #    prevgram[temp[0]] += int(temp[2])
                
        result = open('output2.txt','w',encoding='utf-8')
        if os.path.exists('output.txt'):
            for line in result2:
                # print(line)
                # print(line)
                temp = line.replace('\n','').split('\t')

                #if temp[0] not in file2flag.keys():
                #    file2flag[temp[0]] += 1
                #    prevgram[temp[0]] += int(temp[2])
                # print(temp)
                if temp[2] in currentgram.keys():
                    currentgram[temp[2]] += int(temp[1])
                    result.write(('\t{}\t'+ temp[2]+'\n').format( currentgram[temp[2]]))
                    # result.write(temp[0]+','+temp[1]+',{},{}\n'.format(prevgram[temp[0]],currentgram[temp[0]+','+temp[1]]))
                    del currentgram[temp[2]]
                
                else:
                    result.write(('\t{}\t'+ temp[2]+'\n').format(temp[1]))
            
            for key, value in currentgram.items():
                #temp = key.split('')
                result.write(('\t{}\t'+ key+'\n').format(value))

            result2.close()
        else:
            for key, value in currentgram.items():
                #temp = key.split(',')
                result.write(('\t{}\t'+ key+'\n').format(value))

            
        result.close()
        file.close()
        files = listdir('.')

        for name in files:
            if name == 'output2.txt':
                rename(name,'output.txt')

                

            
    
            # if self.N != 1:
            #     for key, value in currentgram.items():
            #         temp = key.split(',')
            #         result.write(key+',{},{}\n'.format(prevgram[temp[0]],value))
            # else:
            #     for key, value in currentgram.items():
            #         result.write(key+',{}\n'.format(value))
            
            # result.close()

        
       
    def merge(self,path):
        if os.path.exists('output.txt'):
            result = open('output.txt','r',encoding='utf-8')
        
        file = open(path,'r',encoding='utf-8')

        prevgram = defaultdict(int)
        currentgram = defaultdict(int)

        file1flag = defaultdict(int)
        file2flag = defaultdict(int)
        
        if self.N != 1:
            if os.path.exists('output.txt'):
                for line in result:
                    temp = line.replace('\n','').split(',')
                    currentgram[temp[0]+','+temp[1]] += int(temp[3])

                    if temp[0] not in file1flag.keys():
                        file1flag[temp[0]] += 1
                        prevgram[temp[0]] += int(temp[2])
            
            for line in file:
                temp = line.replace('\n','').split(',')
                currentgram[temp[0]+','+temp[1]] += int(temp[3])

                if temp[0] not in file2flag.keys():
                    file2flag[temp[0]] += 1
                    prevgram[temp[0]] += int(temp[2])
            
        else:
            if os.path.exists('output.txt'):
                for line in result:
                    temp = line.replace('\n','').split(',')
                    currentgram[temp[0]] += int(temp[1])

            for line in file:
                temp = line.replace('\n','').split(',')
                # print(temp)
                currentgram[temp[0]] += int(temp[1])
        
        if os.path.exists('output.txt'):
            result.close()
        file.close()

        result = open('output.txt','w',encoding='utf-8')
        if self.N != 1:
            for key, value in currentgram.items():
                temp = key.split(',')
                result.write(key+',{},{}\n'.format(prevgram[temp[0]],value))
        else:
            for key, value in currentgram.items():
                result.write(key+',{}\n'.format(value))
        result.close()

class Unigram(Ngram):
    def __init__(self,path,wordtype):
        Ngram.__init__(self,1,path,wordtype)
        #self.wordtype = 'sentence'
        #self.path = path
        #self.bigram = {}
        self.unigram = defaultdict(int)
        #self.word = defaultdict(int)
    
    def freq(self, *word):
        return self.unigram[word[0]]

    def prob(self,*word):
        return self.unigram[word[0]] / sum(self.unigram.values())
     
    def probs(self,n,order='desc'):
        self.uniprob = {}
        for key, value in self.unigram.items():
              self.uniprob[key] = value/sum(self.unigram.values())
        # for key, value in self.bigram:    
    
    def make_freq(self):
        with open(self.path,'r',encoding='utf-8') as f:
            text = f.readlines()
    
        for line_list in ngrams(text,self.N):
            for line in line_list:
                self.unigram[line[0]] += 1        

    def make(self):
        makeline = lambda l : l[0]
        super(Unigram,self).make('uni',makeline)
    
    def make_freq_out(self,path):
        makeline = lambda l : l[0]
        super(Unigram,self).make_freq_out(path,makeline)

class Bigram(Ngram):
    def __init__(self,path,wordtype):
        Ngram.__init__(self,2,path,wordtype)
        #self.wordtype = 'sentence'
        #self.path = path
        #self.bigram = {}
        self.bigram = defaultdict(int)
        self.word = defaultdict(int)
    
    def freq(self, *word):
        return self.bigram[(word[0], word[1])]

    def prob(self,*word):
        return self.bigram[(word[0], word[1])] / self.word[(word[0])] * 100

    def probs(self,n,order='desc'):
        self.biprob = {}
        for key, value in self.bigram.items():
              self.biprob[key] = value/self.word[key[0]]
        # for key, value in self.bigram:    
    def make_freq(self):
        with open(self.path,'r',encoding='utf-8') as f:
            text = f.readlines()
    
        for line_list in ngrams(text,self.N):
            for line in line_list:
                self.word[line[0]] += 1
                self.bigram[(line[0], line[1])] += 1 

    def make(self):
        makeline = lambda l : l[0] + '\t' + l[1]
        super(Bigram,self).make('bi',makeline)

    def make_freq_out(self,path):
        makeline = lambda l : l[0]
        super(Bigram,self).make_freq_out(path,makeline)

class Trigram(Ngram):
    def __init__(self,path,wordtype):
        Ngram.__init__(self,3,path,wordtype)
        #self.wordtype = 'sentence'
        #self.path = path
        #self.bigram = {}
        self.trigram = defaultdict(int)
        self.bigram = defaultdict(int)
        #self.word = defaultdict(int)
    
    def freq(self, *word):
        return self.trigram[(word[0], word[1], word[2])]

    def prob(self,*word):
        return self.trigram[(word[0], word[1],word[2])] / self.bigram[(word[0], word[1])] * 100
     
    def probs(self,n,order='desc'):
        self.triprob = {}
        for key, value in self.trigram.items():
              self.triprob[key] = value/self.bigram[(key[0], key[1])]
        # for key, value in self.bigram:
    
    def make_freq(self):
        with open(self.path,'r',encoding='utf-8') as f:
            text = f.readlines()
    
        for line_list in ngrams(text,self.N):
            for line in line_list:
                self.bigram[(line[0], line[1])] += 1
                self.trigram[(line[0], line[1], line[2])] += 1

    def make(self):
        makeline = lambda l : l[0] + '\t' + l[1] + '\t' + l[2]
        super(Trigram,self).make('tri',makeline)
    
    def make_freq_out(self,path):
        makeline = lambda l : l[0]+'\t'+l[1]
        super(Trigram,self).make_freq_out(path,makeline)

class Fourgram(Ngram):
    def __init__(self,path,wordtype):
        Ngram.__init__(self,4,path,wordtype)
        #self.wordtype = 'sentence'
        #self.path = path
        #self.bigram = {}
        self.fourgram = defaultdict(int)
        self.trigram = defaultdict(int)
        #self.word = defaultdict(int)
    
    def freq(self, *word):
        return self.fourgram[(word[0], word[1], word[2],word[3])]

    def prob(self,*word):
        return self.fourgram[(word[0], word[1],word[2],word[3])] / self.trigram[(word[0], word[1],word[2])] * 100
     
    def probs(self,n,order='desc'):
        self.fourprob = {}
        for key, value in self.fourgram.items():
              self.fourprob[key] = value/self.trigram[(key[0], key[1],key[2])]
        # for key, value in self.bigram:
    
    def make_freq(self):
        with open(self.path,'r',encoding='utf-8') as f:
            text = f.readlines()
    
        for line_list in ngrams(text,self.N):
            for line in line_list:
                self.trigram[(line[0], line[1],line[2])] += 1
                self.fourgram[(line[0], line[1], line[2],line[3])] += 1
    
    def make(self):
        makeline = lambda l : l[0] + '\t' + l[1] + '\t' + l[2] + '\t' + l[3]
        super(Fourgram,self).make('four',makeline)
    
    def make_freq_out(self,path):
        makeline = lambda l : l[0] + '\t' + l[1] + '\t' + l[2]
        super(Fourgram,self).make_freq_out(path,makeline)

class Fivegram(Ngram):
    def __init__(self,path,wordtype):
        Ngram.__init__(self,5,path,wordtype)
        #self.wordtype = 'sentence'
        #self.path = path
        #self.bigram = {}
        self.fivegram = defaultdict(int)
        self.fourgram = defaultdict(int)
        #self.word = defaultdict(int)
    
    def freq(self, *word):
        return self.fivegram[(word[0], word[1], word[2],word[3],word[4])]

    def prob(self,*word):
        return self.fivegram[(word[0], word[1],word[2],word[3],word[4])] / self.fourgram[(word[0], word[1],word[2],word[3])] * 100
     
    def probs(self,n,order='desc'):
        self.fiveprob = {}
        for key, value in self.fivegram.items():
              self.fiveprob[key] = value/self.fourgram[(key[0], key[1],key[2],key[3])]
        # for key, value in self.bigram:
    
    def make_freq(self):
        with open(self.path,'r',encoding='utf-8') as f:
            text = f.readlines()
    
        for line_list in ngrams(text,3):
            for line in line_list:
                self.fourgram[(line[0], line[1],line[2],line[3])] += 1
                self.fivegram[(line[0], line[1], line[2],line[3],line[4])] += 1
    
    def make(self):
        makeline = lambda l : l[0] + '\t' + l[1] + '\t' + l[2] + '\t' + l[3] + '\t' + l[4]
        super(Fivegram,self).make('five',makeline)
    
    def make_freq_out(self,path):
        makeline = lambda l : l[0] + '\t' + l[1] + '\t' + l[2] + '\t' + l[3]
        super(Fivegram,self).make_freq_out(path,makeline)

class Sixgram(Ngram):
    def __init__(self,path,wordtype):
        Ngram.__init__(self,6,path,wordtype)
        #self.wordtype = 'sentence'
        #self.path = path
        #self.bigram = {}
        self.fivegram = defaultdict(int)
        self.sixgram = defaultdict(int)
        #self.word = defaultdict(int)
    
    def freq(self, *word):
        return self.sixgram[(word[0], word[1], word[2],word[3],word[4],word[5])]

    def prob(self,*word):
        return self.sixgram[(word[0], word[1],word[2],word[3],word[4],word[5])] / self.fivegram[(word[0], word[1],word[2],word[3],word[4])] * 100
     
    def probs(self,n,order='desc'):
        self.sixprob = {}
        for key, value in self.sixgram.items():
              self.sixprob[key] = value/self.fivegram[(key[0], key[1],key[2],key[3],key[4])]
        # for key, value in self.bigram:
    
    def make_freq(self):
        with open(self.path,'r',encoding='utf-8') as f:
            text = f.readlines()
    
        for line_list in ngrams(text,self.N):
            for line in line_list:
                self.fivegram[(line[0], line[1],line[2],line[3],line[4])] += 1
                self.sixgram[(line[0], line[1], line[2],line[3],line[4],line[5])] += 1
    
    def make(self):
        makeline = lambda l : l[0] + '\t' + l[1] + '\t' + l[2] + '\t' + l[3] + '\t' + l[4] + '\t' + l[5]
        super(Sixgram,self).make('six',makeline)

    def make_freq_out(self,path):
        makeline = lambda l : l[0] + '\t' + l[1] + '\t' + l[2] + '\t' + l[3] + '\t' + l[4]
        super(Sixgram,self).make_freq_out(path,makeline)

class Sevengram(Ngram):
    def __init__(self,path,wordtype):
        Ngram.__init__(self,7,path,wordtype)
        #self.wordtype = 'sentence'
        #self.path = path
        #self.bigram = {}
        self.sevengram = defaultdict(int)
        self.sixgram = defaultdict(int)
        #self.word = defaultdict(int)
    
    def freq(self, *word):
        return self.sevengram[(word[0], word[1], word[2],word[3],word[4],word[5],word[6])]

    def prob(self,*word):
        return self.sevengram[(word[0], word[1],word[2],word[3],word[4],word[5],word[6])] / self.sixgram[(word[0], word[1],word[2],word[3],word[4],word[5])] * 100
     
    def probs(self,n,order='desc'):
        self.sevenprob = {}
        for key, value in self.sevengram.items():
              self.sevenprob[key] = value/self.sixgram[(key[0], key[1],key[2],key[3],key[4],key[5])]
        # for key, value in self.bigram:
    
    def make_freq(self):
        with open(self.path,'r',encoding='utf-8') as f:
            text = f.readlines()
    
        for line_list in ngrams(text,self.N):
            for line in line_list:
                self.sixgram[(line[0], line[1],line[2],line[3],line[4],line[5])] += 1
                self.sevengram[(line[0], line[1], line[2],line[3],line[4],line[5],line[6])] += 1
    
    def make(self):
        makeline = lambda l : l[0] + '\t' + l[1] + '\t' + l[2] + '\t' + l[3] + '\t' + l[4] + '\t' + l[5] + '\t' + l[6]
        super(Sevengram,self).make('seven',makeline)
    
    def make_freq_out(self,path):
        makeline = lambda l : l[0] + '\t' + l[1] + '\t' + l[2] + '\t' + l[3] + '\t' + l[4] + '\t'+ l[5]
        super(Sevengram,self).make_freq_out(path,makeline)

def unimain(path,mode):
    unigram = Unigram(path,'blank')
    start = time()

    if mode == 'm':
        unigram.make()
    if mode == 'c':
        unigram.make_freq_out(path)
    if mode == 'me':
        unigram.mergeBig(path)

    end = time()
    spent = int(end - start)
    print('{:02d}:{:02d}:{:02d}'.format(spent // 3600, (spent % 3600 // 60), spent % 60))

def bimain(path,mode):
    unigram = Bigram(path,'blank')
    start = time()

    if mode == 'm':
        unigram.make()
    if mode == 'c':
        unigram.make_freq_out(path)
    if mode == 'me':
        unigram.mergeBig(path)

    end = time()
    spent = int(end - start)
    print('{:02d}:{:02d}:{:02d}'.format(spent // 3600, (spent % 3600 // 60), spent % 60))

def trimain(path,mode):
    unigram = Trigram(path,'blank')
    start = time()

    if mode == 'm':
        unigram.make()
    if mode == 'c':
        unigram.make_freq_out(path)
    if mode == 'me':
        unigram.mergeBig(path)

    end = time()
    spent = int(end - start)
    print('{:02d}:{:02d}:{:02d}'.format(spent // 3600, (spent % 3600 // 60), spent % 60))

def fourmain(path,mode):
    unigram = Fourgram(path,'blank')
    start = time()

    if mode == 'm':
        unigram.make()
    if mode == 'c':
        unigram.make_freq_out(path)
    if mode == 'me':
        unigram.mergeBig(path)

    end = time()
    spent = int(end - start)
    print('{:02d}:{:02d}:{:02d}'.format(spent // 3600, (spent % 3600 // 60), spent % 60))

def fivemain(path,mode):
    unigram = Fivegram(path,'blank')
    start = time()

    if mode == 'm':
        unigram.make()
    if mode == 'c':
        unigram.make_freq_out(path)
    if mode == 'me':
        unigram.mergeBig(path)

    end = time()
    spent = int(end - start)
    print('{:02d}:{:02d}:{:02d}'.format(spent // 3600, (spent % 3600 // 60), spent % 60))

def sixmain(path,mode):
    unigram = Sixgram(path,'blank')
    start = time()

    if mode == 'm':
        unigram.make()
    if mode == 'c':
        unigram.make_freq_out(path)
    if mode == 'me':
        unigram.mergeBig(path)

    end = time()
    spent = int(end - start)
    print('{:02d}:{:02d}:{:02d}'.format(spent // 3600, (spent % 3600 // 60), spent % 60))

def sevenmain(path,mode):
    unigram = Sevengram(path,'blank')
    start = time()

    if mode == 'm':
        unigram.make()
    if mode == 'c':
        unigram.make_freq_out(path)
    if mode == 'me':
        unigram.mergeBig(path)

    end = time()
    spent = int(end - start)
    print('{:02d}:{:02d}:{:02d}'.format(spent // 3600, (spent % 3600 // 60), spent % 60))

if __name__ == '__main__':
    path = sys.argv[1]
    gram = sys.argv[2]
    mode = sys.argv[3]

    if gram == '1':
        unimain(path,mode)
    elif gram == '2':
        bimain(path,mode)
    elif gram == '3':
        trimain(path,mode)
    elif gram == '4':
        fourmain(path,mode)
    elif gram == '5':
        fivemain(path,mode)
    elif gram == '6':
        sixmain(path,mode)
    elif gram == '7':
        sevenmain(path,mode)
