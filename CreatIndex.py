# -*- coding: utf-8 -*-


# jieba.load_userdict('./userdict/2000000-dict.txt')


    
    
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
    im = IndexModule('./config.ini', "uft-888888")
    im.construct_postings_lists()
