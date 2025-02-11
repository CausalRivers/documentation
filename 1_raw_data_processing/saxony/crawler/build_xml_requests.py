import re


def build_soap_envelope(pegel, start, end, resolution):
    """Takes a specific pegel id, a start date and an end date
    and builds an xml package to request W and Q data.
    for api information:
    https://www.umwelt.sachsen.de/umwelt/infosysteme/lhwz/download/Schnittstellenbeschreibung_Spurwertabfrage.pdf

    Args:
        pegel (int): number of a measurement station
        start (str): startdate YYYY-MM-DD
        end (str): enddate YYYY-MM-DD
        resolution (str): resolution str: Ziel ... 15 minutes;
                                          Ziel-TW-1H ... 1 hour;
                                          Ziel-MW-1T ... 1 day
    """
    envelope = "<soapenv:Envelope xmlns:spur=\"http://spurwerte.webservice.hwims.t_\
systems_mms.com/\" xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\">\
<soapenv:Header/>\
<soapenv:Body>\
<spur:liefereWerteZuSpuren2>\
<spurIdentifikator>"

    envelope += f"<messstationKennziffer>{pegel}</messstationKennziffer>"

    envelope += "<messstationTyp>Pegel</messstationTyp>\
<physikalischeGroesse>W</physikalischeGroesse>"

    envelope += f"<spurTyp>{resolution}</spurTyp>"

    envelope += "</spurIdentifikator>\
<spurIdentifikator>"

    envelope += f"<messstationKennziffer>{pegel}</messstationKennziffer>"

    envelope += "<messstationTyp>Pegel</messstationTyp>\
<physikalischeGroesse>Q</physikalischeGroesse>"

    envelope += f"<spurTyp>{resolution}</spurTyp>"

    envelope += "</spurIdentifikator>"

    envelope += f"<startZeitpunkt>{start}T00:00:00</startZeitpunkt>"
    envelope += f"<endeZeitpunkt>{end}T00:00:00</endeZeitpunkt>"

    envelope += "<statistischeZeitangaben>true</statistischeZeitangaben>\
</spur:liefereWerteZuSpuren2>\
</soapenv:Body>\
</soapenv:Envelope>"

    return envelope


def parse_response(response_str):
    """Takes response string and parses it into a dict.

    Args:
        response_str (str): response of the saxony soap wsdl api
    """
    if "<wert" not in response_str:
        return {"Q": []}

    response = response_str.split("<spurwerte>")[1].split("</spurwerte")[0]

    spur_matches = re.findall(
        "<spurIdentifikator>(.+?)</spurIdentifikator>", response)
    spur_values = []
    for spur in spur_matches:
        spur_values.append(response.split(spur)[1].split(
            "</spurIdentifikator>")[1].split("</spur>")[0])

    results = {}
    for measure, values in zip(spur_matches, spur_values):
        quantity = re.findall(
            "<physikalischeGroesse>(.+?)</physikalischeGroesse>", measure)[0]

        results[quantity] = []
        results[f"{quantity}_timestamp"] = []

        if "<wert>" not in values:
            continue

        measured_values = re.findall("<wert>([0-9]+\.?[0-9]*)</wert>", values)
        measured_values = [float(val) for val in measured_values]

        timestamps = re.findall("<zeitstempel>(.+?)</zeitstempel>", values)

        results[quantity] = measured_values
        results[f"{quantity}_timestamp"] = timestamps

    return results
