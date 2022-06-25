from fast_autocomplete import AutoComplete
import pickle

open_file = open( 'sample.pkl', "rb")
loaded_list = pickle.load(open_file)
open_file.close()

words = {i : {} for i in loaded_list}
autocomplete = AutoComplete(words=words)

s = input("Enter the str: ")
print(autocomplete.search(word = s, max_cost=3, size=1))