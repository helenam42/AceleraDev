from pytz import timezone
from math import fabs
from datetime import datetime

records = [
    {'source': '48-996355555', 'destination': '48-666666666',
     'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097',
     'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097',
     'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788',
     'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788',
     'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099',
     'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697',
     'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099',
     'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697',
     'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097',
     'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564627800, 'start': 1564626000}
]


def classify_by_phone_number(records):

    lista = len(records)
    taxavard = 0.09
    taxafixa = 0.36

    for i in range(lista):

        ##############################################################
        # Conversão de timestamp para duração (em minutos) da chamada
        ##############################################################

        start = records[i]['start']
        end = records[i]['end']

        # converter o timestamp para uma data e hora em um timezone específico

        startnew = datetime.fromtimestamp(start, tz =
                                          timezone("America/Sao_Paulo"))
        endnew = datetime.fromtimestamp(end, tz =
                                        timezone("America/Sao_Paulo"))

        # separar horas, minutos e segundos

        hstart = int(startnew.strftime("%H"))
        mstart = int(startnew.strftime("%M"))
        start = int(startnew.strftime("%S"))
        hend = int(endnew.strftime("%H"))
        mend = int(endnew.strftime("%M"))
        send = int(endnew.strftime("%S"))

        # calculo da quantidade de minutos

        # caso onde a chamada começa em um dia e termina em outro

        if ((hend > fabs((hstart - 12))) and (fabs((hstart - hend)) <= 12)
                and (hend < hstart)) or (fabs((hstart - hend)) >= 12):

            mintotal = (hend + fabs((hstart - 24)))*60 + fabs(mend - mstart)

        # caso onde a chamada começa e termina no mesmo dia

        else:
            minstart = hstart*60 + mstart
            minend = hend*60 + mend
            mintotal = fabs(minend - minstart)

        # quando os segundos não resultam em um minuto inteiro

        if send < 10 or start < 10:
            mintotal = mintotal - 1
        else:
            mintotal = mintotal

        ###################
        # Calculo da taxa
        ###################

        # Começou e terminou de dia
        if (hstart >= 6 and hstart < 22) and (hend >= 6 and hend < 22):
            total = (mintotal * taxavard) + (taxafixa)

        # Começou e terminou de noite
        elif (hstart < 6 or hstart >= 22) and (hend < 6 or hend >= 22):
            total = taxafixa

        # Começou de noite e terminou de dia
        elif (hstart < 6 or hstart >= 22) and (hend >= 6 or hend < 22):
            # horas de noite
            totalhn = (int(fabs(6 - hstart)))
            totalm = (((fabs((int(fabs(hstart - hend))) - totalhn))*60))
            total = (totalm * taxavard) + (taxafixa)

        # Começou de dia e terminou de noite
        elif (hstart >= 6 or hstart < 22) and (hend > 6 or hend <= 22):
            # horas de noite
            totalhn = (int(fabs(22 - hstart)))
            totalm = (fabs(((int(fabs(hstart - hend))) - totalhn))*60)
            total = (totalm * taxavard) + (taxafixa)

        var = True

        #####################################
        # Salvar em uma lista de dicionários
        #####################################

        total = round(total, ndigits=2)
        source = records[i]['source']

        # salva o primeiro número
        if i == 0:
            tarifa = []
            tarifa.append({'source': source, 'total': total})

        # salva o restante dos números

        else:

            tamanho = len(tarifa)

        # comparação do número de origem atual com todos os
        # outros de forma a somar as taxas de números repetidos

            for j in range(tamanho):
                if tarifa[j]['source'] == source:
                    taxanterior = float(tarifa[j]['total'])
                    total = total + taxanterior
                    total = round(total, ndigits=2)
                    tarifa.remove(tarifa[j])
                    tarifa.append({'source': source, 'total': total})
                    var = False
                    break
            if var and i != 0:
                tarifa.append({'source': source, 'total': total})

        # montagem final da lista

    listacompleta = sorted(tarifa, key=lambda k: k['total'], reverse=True)
    # listacompleta = '\n'.join([str(i) for i in sorted_list])

    return listacompleta


(listacompleta) = classify_by_phone_number(records)
