from commande import Commande
# from lire_feuille import lire_une_feuille
# from réorg_commandes import réorg_les_comms
# from time import time

# 统计一天的有效或无效订单（总价、个数）
def sommer_comms(tuples_comms, valide):
    comms = tuples_comms[1]
    if valide:
        return (sum(comms, start=Commande(tuples_comms[0][0], coûte=0.0, no_comm=True)), len(comms))
    return (sum(comms, start=Commande(tuples_comms[0][0])), len(comms))

# if __name__ == '__main__':
#     t0 = time()

#     CC = [lire_une_feuille(2), lire_une_feuille(3)]
#     ro = réorg_les_comms(CC)

#     ex_invalides = ro[2]
#     print(ex_invalides)
#     ex_valides = ro[3]
#     print(ex_valides)

#     rés_invs = sommer_comms(ex_invalides, ex_invalides[0][1])
#     rés_vs = sommer_comms(ex_valides, ex_valides[0][1])
#     print(f"Invalides ({rés_invs[1]}):", rés_invs[0])
#     print(f"Valides ({rés_vs[1]}):", rés_vs[0])

#     print(f"Durée: {time()-t0} s")