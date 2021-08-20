from django.shortcuts import render
from django.http import HttpResponse
import json
import numpy as np
from keras.models import load_model


def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, "home.html")


def render_flujograma(request, ci):
    # se obtiene el historico del estudiante
    with open('./static/utils/test.json', "r", encoding='utf8') as fileH:
        all_historicos = json.load(fileH)
        try:
            historico = all_historicos[str(ci)]
        except:
            return render(request, "home.html",
                          {'error': 'No se ha encontrado al estudiante en nuestra base de datos.'})
        fileH.close()

    # se obtiene el flujograma de las materias del estudiante
    with open('./static/utils/flujograma_carreras.json', "r", encoding='utf8') as fileF:
        all_flujogramas = json.load(fileF)
        flujograma = all_flujogramas[historico["Plan de Estudios"]]

        # asignar nombre a las materias del flujograma
        with open('./static/utils/code_to_assign.json', "r", encoding='utf8') as fileN:
            all_nombres = json.load(fileN)
            for materia in flujograma.keys():
                for codigo in all_nombres.keys():
                    if 'FGE0000' in materia:
                        flujograma[materia].append('FGE')
                        break

                    if materia == codigo:
                        flujograma[materia].append(all_nombres[codigo])
                        break
            fileN.close()

        carrera = historico["Plan de Estudios"]

        # materias BPELI (idiomas modernos)
        mat_IM = {
            'BPELI41': [
                0, 'ALEMAN I'
            ],
            'BPELI31': [
                0, 'FRANCES I'
            ],
            'BPELI42': [
                0, 'ALEMAN II'
            ],
            'BPELI32': [
                0, 'FRANCES II'
            ],
            'BPELI43': [
                0, 'ALEMÁN III'
            ],
            'BPELI33': [
                0, 'FRANCES III'
            ],
            'BPELI44': [
                0, 'ALEMAN IV'
            ],
            'BPELI34': [
                0, 'FRANCES IV'
            ],
            'BPELI45': [
                0, 'ALEMAN V'
            ],
            'BPELI35': [
                0, 'FRANCES V'
            ],
            'BPELI55': [
                0, 'ITALIANO V'
            ],
            'BPELI46': [
                0, 'ALEMAN VI'
            ],
            'BPELI36': [
                0, 'FRANCES VI'
            ],
            'BPELI56': [
                0, 'ITALIANO VI'
            ],
            'BPELI47': [
                0, 'ALEMAN VII'
            ],
            'BPELI37': [
                0, 'FRANCES VII'
            ],
            'BPELI48': [
                0, 'ALEMAN VIII'
            ],
            'BPELI38': [
                0, 'FRANCES VIII'
            ],
            'BPELI58': [
                0, 'ITALIANO VIII'
            ],
        }

        # verificar materias que cursó el estudiante
        for materiaF in flujograma.keys():
            for trimestre in historico["Historico"]:
                salto = False
                for n, materiaH in enumerate(trimestre):
                    # validacion para electivas
                    if materiaH != 1903 and 'FGE0000' in materiaF and 'FGE0000' in materiaH:
                        if materiaH.split('_')[1] == 'Good' or materiaH.split('_')[1] == 'Excellent':
                            trimestre[n] = 1903
                            flujograma[materiaF][0] = 1
                            salto = True
                            break

                    # validacion para materias regulares
                    if materiaH != 1903 and materiaF == materiaH.split('_')[0]:
                        if materiaH.split('_')[1] == 'Good' or materiaH.split('_')[1] == 'Excellent':
                            flujograma[materiaF][0] = 1
                            salto = True
                            break

                    # validacion para servicio comunitario
                    if materiaH != 1903 and materiaF == 'BPTDI01' and 'BPTDI01-1' in materiaH:
                        if materiaH.split('_')[1] == 'Good':
                            flujograma[materiaF][0] = 1
                            trimestre[n] = 1903
                            break

                    if materiaH != 1903 and materiaF == 'BPTDI01' and 'BPTDI01-2' in materiaH:
                        if materiaH.split('_')[1] == 'Good':
                            trimestre[n] = 1903
                            flujograma[materiaF][0] = 2
                            salto = True
                            break

                    # validacion idiomas modernos
                    if carrera == 'IDIOMAS MODERNOS' and materiaH != 1903 and 'BPELI' in materiaF and 'BPELI' in materiaH:
                        if materiaH.split('_')[1] == 'Good' or materiaH.split('_')[1] == 'Excellent':
                            trimestre[n] = 1903
                            flujograma[materiaF][0] = 1
                            mat_IM[materiaH.split('_')[0]][0] = 1
                            flujograma[materiaF].append(mat_IM[materiaH.split('_')[0]][1])
                            salto = True
                            break

                if salto:
                    break

    fileF.close()

    if carrera == 'IDIOMAS MODERNOS':
        return render(request, "flujograma.html",
                      {'flujograma': flujograma, 'carrera': carrera, 'ci': ci, 'materias_op': mat_IM})

    return render(request, "flujograma.html", {'flujograma': flujograma, 'carrera': carrera, 'ci': ci})


def predecir(request, ci):
    # validaciones iniciales
    if request.method != 'POST':
        return render(request, "home.html", {'error': 'Ha ocurrido un error inesperado (0).'})

    grupo_materias = []
    hay_materias = False
    for i in range(3):
        grupo_materias.append(request.POST.getlist('materias[' + str(i) + '][]'))
        if len(request.POST.getlist('materias[' + str(i) + '][]')) != 0:
            hay_materias = True

    if not hay_materias:
        return render(request, "home.html", {'error': 'No se han introducido materias a predecir (1).'})

    # cargar el historico del estudiante
    with open('./static/utils/test.json', "r", encoding='utf8') as fileH:
        all_historicos = json.load(fileH)
        try:
            historico = all_historicos[str(ci)]["Historico"]
        except:
            return render(request, "home.html",
                          {'error': 'No se ha encontrado al estudiante en nuestra base de datos. (2)'})
        fileH.close()

    # cargar el json materia a int
    with open('./static/utils/vocab_to_int.json', "r", encoding='utf8') as fileHI:
        vocab_to_int = json.load(fileHI)
        fileHI.close()

    # crear input historico con sus respectivos indices numericos
    historico_int = np.zeros((1, 24, 7), dtype=int)
    array_1903 = [1903, 1903, 1903, 1903, 1903, 1903, 1903]

    for i in range(24):

        if i <= (len(historico) - 1):
            # arreglo 7 materias por trimestre
            cant_materias = 7 - len(historico[i])
            for j in range(cant_materias):
                historico[i].append(1903)

            # asignar indice numerico dependiendo de la materia
            for materia in range(0, len(historico[i])):
                if historico[i][materia] != 1903:
                    historico[i][materia] = vocab_to_int[historico[i][materia]]
            historico_int[0][i] = historico[i]
        else:
            historico_int[0][i] = array_1903

    print('Historico del estudiante')
    print(historico_int)

    # cargar el modelo predictivo en el sistema
    model = load_model('./static/utils/model_final.h5')

    # crear input target con 1s y 0s en sus respectivas posiciones
    for n, grupo in enumerate(grupo_materias):
        target_input = np.zeros((1, 466), dtype=int)
        target_int = []
        target_dict = {}
        target_file = open('./static/utils/only_assigns.txt')
        for line in target_file:
            target_int.append(line.split('\n')[0])
        target_file.close()

        target_int = sorted(target_int)

        for materia in target_int:
            target_dict[materia] = 0

        if (len(grupo) != 0):
            for materia in grupo:
                target_dict[materia] = 1

            for m, value in enumerate(target_dict.values()):
                target_input[0][m] = value

            print('Target del estudiante ' + str(n))
            print(target_input)

            prediccion = model.predict([historico_int, target_input])
            print(prediccion)
            grupo_materias[n].append(prediccion[0][0].item())

    # asignar nombre a las materias elegidas
    with open('./static/utils/code_to_assign.json', "r", encoding='utf8') as fileN:
        all_nombres = json.load(fileN)
        for grupo in grupo_materias:
            if (len(grupo) == 0):
                continue

            for n, materia in enumerate(grupo):
                for codigo in all_nombres.keys():

                    if (n + 1) == len(grupo):
                        break

                    if 'FGE0000' in materia:
                        grupo[n] = 'ELECTIVA'
                        break

                    if materia == codigo:
                        grupo[n] = all_nombres[codigo]
                        break
        fileN.close()

    # return render(request, "home.html")
    return render(request, "resultados.html", {'grupos': grupo_materias})


def resultados(request):
    return render(request, "resultados.html")
