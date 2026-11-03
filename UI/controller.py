import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._grafoCreato = False

    def fillDD(self):
        years = self._model.getAllYears()
        for year in years:
            self._view._ddAnno1.options.append(ft.dropdown.Option(year))
            self._view._ddAnno2.options.append(ft.dropdown.Option(year))

        self._view.update_page()

    def handleCreaGrafo(self,e):
        anno1 = self._view._ddAnno1.value
        anno2 = self._view._ddAnno2.value

        if anno1 is None or anno2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Selezionare un valore dal menu."))

            self._view.update_page()
            return



        if anno1 > anno2:
            self._view.txt_result.controls.append(
                ft.Text("L'anno iniziale deve essere minore o uguale a quello finale."))
            return

        self._model.buildGraph(anno1, anno2)
        self._model.buildGraph(self._view._ddAnno1.value, self._view._ddAnno2.value)
        nNodi, nArchi = self._model.getGraphDetails()
        self._grafoCreato = True

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato.", color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"Nodi: {nNodi}, Archi: {nArchi}"))
        self._view.update_page()

    def handleDettagli(self, e):
        if not self._grafoCreato:
            self._view.txt_result.controls.append(
                ft.Text("Creare prima il grafo."))
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore:", color="green"))
        best3 = self._model.getTop3Archi()
        for arco in best3:
            self._view.txt_result.controls.append(
                ft.Text(f"{arco[0].constructorRef} --> {arco[1].constructorRef} ({arco[2]} piloti condivisi)"))

        num = self._model.getNumCompConn()
        self._view.txt_result.controls.append(ft.Text(f"il grafo ha {num} componenti connesse", color="green"))

        largest = self._model.getMaxCompConn()
        self._view.txt_result.controls.append(ft.Text(f"componente più grande ({len(largest)} nodi): ", color="green"))
        for nodo in largest:
            self._view.txt_result.controls.append(ft.Text(nodo))


        largestOrdinata = self._model.getMaxCompConnOrdinata()
        self._view.txt_result.controls.append(ft.Text("Componente connessa in ordine descrescente:", color="green"))
        for nodo in largestOrdinata:
            self._view.txt_result.controls.append(ft.Text(f"{nodo[0]} (grado = {nodo[1]})"))

        self._view.update_page()

    def handleCerca(self, e):
        if not self._grafoCreato:
            self._view.txt_result.controls.append(
                ft.Text("Creare prima il grafo."))
            return

        kTxt = self._view._txtInK.value

        if kTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore."))
            self._view.update_page()
            return

        try:
            k = int(kTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore intero."))
            self._view.update_page()
            return

        if k < 1 :
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore tra 1 e 100."))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        bestSet, bestVal, (minNodo, minAnno), (maxNodo, maxAnno) = self._model.getBestSet(k)

        if bestSet == None:
            self._view.txt_result.controls.append(ft.Text("non è stato possibile travare un set per quel valore di k", color="green"))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text("Best set composto da:", color="green"))
        for nodo in bestSet:
            self._view.txt_result.controls.append(ft.Text(f"{nodo}"))

        self._view.txt_result.controls.append(ft.Text(f"Lo scarto minimo di età e {bestVal} giorni"))
        self._view.txt_result.controls.append(ft.Text(f"il costruttore con veterano più giovane è {maxNodo}, anno {maxAnno}"))
        self._view.txt_result.controls.append(ft.Text(f"il costruttore con veterano più anziano è {minNodo}, anno {minAnno}"))
        self._view.update_page()

