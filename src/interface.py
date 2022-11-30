from tkinter import *
from src.trie import trieBuilder

N_RESULTS = 10

l_fst_par = ['lista', 'do', 'FST', 'par']
l_fst_impar = ['lista', 'do', 'FST', 'impar']
l_lev = ['lista', 'do', 'Lev']

def interface():
      trie = trieBuilder()
      window = Tk()
      window.title('Autocomplete CTC-34')
      window.geometry('100x100')
      window.attributes('-zoomed', True)

      def fst_query(query):
            if len(query) %2 :
                  return ' '.join(map(str, l_fst_par[:N_RESULTS]))
            else:
                  return ' '.join(map(str, l_fst_impar[:N_RESULTS]))
      def trie_query(query):
                  return ' '.join(map(str, trie.query(query)[:N_RESULTS]))
      
      def execute(query):
            if (fst_check.get() == 1) and (trie_check.get() == 0) and (lev_check.get() == 0):
                  l.config(text=fst_query(query))
            elif (fst_check.get() == 0) and (trie_check.get() == 1) and (lev_check.get() == 0):
                  l.config(text=trie_query(query))
            elif (fst_check.get() == 0) and (trie_check.get() == 0) and (lev_check.get() == 1):
                  l.config(text='Only Lev')
            elif (fst_check.get() == 1) and (trie_check.get() == 0) and (lev_check.get() == 1):
                  l.config(text='Lev + FST')
            elif (fst_check.get() == 0) and (trie_check.get() == 1) and (lev_check.get() == 1):
                  l.config(text='Lev + Trie')
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