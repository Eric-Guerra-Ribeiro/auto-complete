from tkinter import *
from src.trie import trieBuilder
from src.levenshtein import filter_by_levenshtein, dict_filter_by_levenshtein
from src.fst import get_american_en_fst, fst_prefix_query

N_RESULTS = 10


def interface():
      trie = trieBuilder()
      fst = get_american_en_fst()
      window = Tk()
      window.title('Autocomplete CTC-34')
      window.geometry('100x100')
      window.attributes('-zoomed', True)

      def fst_query(query):
            return ' '.join(map(str, fst_prefix_query(query, fst)[:N_RESULTS]))

      def trie_query(query):
            return ' '.join(map(str, trie.query(query)[:N_RESULTS]))

      def lev_query(query):
            return ' '.join(map(str, dict_filter_by_levenshtein(query)[:N_RESULTS]))

      def lev_trie_query(query):
            candidates = trie.query(query)
            return ' '.join(map(str, filter_by_levenshtein(query, candidates)[:N_RESULTS]))
      
      def execute(query):
            if (fst_check.get() == 1) and (lev_check.get() == 0):
                  l.config(text=fst_query(query))
            elif (trie_check.get() == 1) and (lev_check.get() == 0):
                  l.config(text=trie_query(query))
            elif (fst_check.get() == 0) and (trie_check.get() == 0) and (lev_check.get() == 1):
                  l.config(text=lev_query(query))
            elif (fst_check.get() == 1) and (lev_check.get() == 1):
                  l.config(text='Lev + FST')
            elif (trie_check.get() == 1) and (lev_check.get() == 1):
                  l.config(text=lev_trie_query(query))
            else:
                  l.config(text='')
            window.after(1, execute, text.get(1.0,END).strip())


      def unmark_fst():
            if trie_check.get():
                  fst_check.set(0)

      def unmark_trie():
            if fst_check.get():
                  trie_check.set(0)

      fst_check = IntVar()
      trie_check = IntVar()
      lev_check = IntVar()
      c1 = Checkbutton(window, text='FST',variable=fst_check, onvalue=1, offvalue=0, command=unmark_trie)
      c1.pack()
      c2 = Checkbutton(window, text='Trie',variable=trie_check, onvalue=1, offvalue=0, command=unmark_fst)
      c2.pack()
      c3 = Checkbutton(window, text='Levenshtein',variable=lev_check, onvalue=1, offvalue=0)
      c3.pack()
      text = Text(window, width=100, height=8)
      text.pack()


      l = Label(window, bg='white', width=100, height=5)
      l.pack()

      window.after(1, execute, text.get(1.0,END).strip())
      window.update()

      window.mainloop()