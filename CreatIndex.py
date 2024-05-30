# -*- coding: utf-8 -*-


# jieba.load_userdict('./userdict/2000000-dict.txt')



class IndexModule:

    postings_lists = {}

    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        f = open(config['DEFAULT']['stop_words_path'], encoding = config['DEFAULT']['stop_words_encoding'])
        words = f.read()
        self.stop_words = set(words.split('\n'))
    

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        
    def clean_list(self, seg_list):
        cleaned_dict = {}
        n = 0
        for i in seg_list:
            i = i.strip().lower()
            if i != '' and not self.is_number(i) and i not in self.stop_words:
                n = n + 1
                if i in cleaned_dict:
                    cleaned_dict[i] = cleaned_dict[i] + 1
                else:
                    cleaned_dict[i] = 1
        return n, cleaned_dict
    
    
    def write_postings_and_knowledge_to_db(self, db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        c.execute('''DROP TABLE IF EXISTS postings''')
        c.execute('''CREATE TABLE postings
                     (term TEXT PRIMARY KEY, df INTEGER, docs TEXT)''')

        c.execute('''DROP TABLE IF EXISTS knowledge''')
        c.execute('''CREATE TABLE knowledge
                     (id INTEGER PRIMARY KEY, question TEXT, answer TEXT)''')

        for key, value in self.postings_lists.items():
            doc_list = '\n'.join(map(str,value[1]))
            t = (key, value[0], doc_list)
            c.execute("INSERT INTO postings VALUES (?, ?, ?)", t)
        
        conn.commit()

        for i,question in self.files.items():
            answer ='标准问“'+ question +'”的答案'
            t = (i, question, answer)
            c.execute("INSERT INTO knowledge VALUES (?, ?, ?)", t)
        
        conn.commit()
        conn.close()
    
     
   


if __name__ == "__main__":
    im = IndexModule('./config.ini', "uft-8")
    im.construct_postings_lists()
