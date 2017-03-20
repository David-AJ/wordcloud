import numpy as np
from PIL import Image
from wordcloud.wordcloud import colormap_color_func as ccf
from wordcloud import WordCloud as wc
import codecs
import jieba
from multiprocessing import Pool,cpu_count


f = codecs.open('StopWord.txt','r','utf8')
StopWord  = f.read().split('\r\n')
f.close()
StopWord.remove(StopWord[-1])
StopWord = set(StopWord)

def cut(sentence):
		global StopWord
		if sentence!=None:
			sentence = [word for word in jieba.lcut(sentence,cut_all=False) if word not in StopWord]
			return [i for i in sentence]
		else :
			return None

def wordcont(wordlist):
	dic = {}
	for i in wordlist:
		if i == None:
			continue
		for j in i:
			if j in dic:
				dic[j] = dic[j] + 1
			else:
				dic[j] = 1
	return dic

def multicut(data):
	pool = Pool(cpu_count())
	data = pool.map(cut, data)
	pool.close()
	pool.join()
	return data

if __name__ == '__main__':
	path = raw_input('Enter path: ')
	state = input("state: ")
	word = np.load(path+'.npy')
	dic = wordcont(word)

	mask = np.array(Image.open("love.jpg"))
	w = wc(font_path='test.ttf',mask = mask,random_state=state,color_func=ccf('hsv'))
	w.generate_from_frequencies(dic)
	# a = w.to_image()
	# a.show()
	w.to_file(path+'.jpg')