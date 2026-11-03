import copy
from datetime import date

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.idMap = {}
        self._bestSet = []
        self._bestVal = float('inf')  # o 0 se massimizzi

        (self._minNodo, self._minAnno) = (None, None)
        (self._maxNodo, self._maxAnno) = (None, None)


    def getAllYears(self):
        return DAO.getAllYears()


    def buildGraph(self, anno1, anno2):
        self._graph.clear()
        self.idMap.clear()

        nodes = DAO.getAllNodes(anno1, anno2)
        for node in nodes:
            self.idMap[node.constructorId] = node

        self._graph.add_nodes_from(nodes)

        edges = DAO.getAllEdges(anno1, anno2)
        for edge in edges:
            u = self.idMap[edge[0]]
            v = self.idMap[edge[1]]
            self._graph.add_edge(u, v, weight=edge[2])


        constrYear = DAO.getConstrutorOldest()
        for idC, year in constrYear:
            if idC in self.idMap:
                constructor = self.idMap[idC]
                constructor.oldest_driver_dob = year



    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getTop3Archi(self):
        archi = [(u, v, d["weight"]) for u, v, d in self._graph.edges(data=True)]
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[:3]


    def getNumCompConn(self):
        return nx.number_connected_components(self._graph)


    def getMaxCompConn(self):
        components = list(nx.connected_components(self._graph))
        largest = list(max(components, key=len))
        return largest

    def getMaxCompConnOrdinata(self):
        lista = []
        largest = self.getMaxCompConn()
        for nodo in largest:
            lista.append((nodo, self._graph.degree(nodo)))

        lista.sort(key=lambda x: x[1], reverse=True)

        return lista

    def getBestSet(self, k):
        self._bestSet = []
        self._bestVal = float('inf')  # oppure 365*100

        (self._minNodo, self._minAnno) = (None, None)
        (self._maxNodo, self._maxAnno) = (None, None)

        components = list(nx.connected_components(self._graph))

        if len(components) < k:
            return None, 0, (None, None), (None, None)

        parziale = []
        self._ricorsione(components, k, parziale, 0)
        return self._bestSet, self._bestVal, (self._minNodo, self._minAnno), (self._maxNodo, self._maxAnno)

    def _ricorsione(self, components, k, parziale, idx):
        # HO SCELTO ABBASTANZA?
        if len(parziale) == k:
            val = self._valuta(parziale)
            diff = val[0]
            if diff.days < self._bestVal:
                self._bestVal = diff.days
                self._bestSet = copy.deepcopy(parziale)
                (self._minNodo, self._minAnno) = val[1]
                (self._maxNodo, self._maxAnno) = val[2]
            return

        # POSSO ANCORA SCEGLIERE?
        if idx >= len(components):
            return
        if len(components) - idx < k - len(parziale):
            return  # impossibile arrivare a k

        # PROVO OGNI NODO DI QUESTA COMPONENTE
        for nodo in components[idx]:
            parziale.append(nodo)
            self._ricorsione(components, k, parziale, idx + 1)
            parziale.pop()

        # SALTO QUESTA COMPONENTE
        self._ricorsione(components, k, parziale, idx + 1)



    def _valuta(self, parziale):
        # minYear = 0 #più vecchio
        # maxYear = date(1-1-1) #più giovane
        # for nodo in parziale:
        #     if nodo.oldest_driver_dob < minYear:
        #         minYear = nodo.oldest_driver_dob
        #
        #     if nodo.oldest_driver_dob > maxYear:
        #         maxYear = nodo.oldest_driver_dob

        nodiAnni = []
        for nodo in parziale:
            nodiAnni.append((nodo, nodo.oldest_driver_dob))

        minNodo, minAnno = min(nodiAnni, key=lambda x: x[1])
        maxNodo, maxAnno = max(nodiAnni, key=lambda x: x[1])

        return maxAnno - minAnno, (minNodo, minAnno), (maxNodo, maxAnno)

        # oppure semplicemente scegli il min nodo e poi fai nodo.oldest_driver_dob



