from vote import Coingecko
import threading




if __name__ == "__main__":
    Coingecko = Coingecko(
        token_id=28256, # enter coin id (this one is paradox coin LMFAO)
        vote_type='negative', # replace negative with positive if you want to positivly vote a coin
        proxy='' # Enter rotating proxy here
    ) 
    for i in range(int(input("Threads: "))):
        threading.Thread(target=Coingecko.vote).start()
