# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 00:41:48 2025

@author: HP
"""

from fastapi import FastAPI, HTTPException
from SPARQLWrapper import SPARQLWrapper, JSON


app = FastAPI()

GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/screening_ontology"

@app.get("/")
def root():
    return {"message": "REST API for the Neonatal Screening Knowledge Graph"}


@app.get("/newborn/{newborn_id}")
def get_newborns(newborn_id: str):
    query = f"""
    PREFIX odc: <http://example.org/ontology/depistage#>
    PREFIX odp: <http://example.org/property/depistage#>
    PREFIX odr: <http://example.org/resource/depistage#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT  ?firstName ?lastName ?sex ?birthDate ?birthTime ?birthPlace 
            ?keyData ?birthWeight ?headCircumference ?armCircumference ?birthLength ?gestationalAge ?numberOfFetuses ?fetalDistress ?jaundice ?cyanosis ?riskProfile ?score ?criterion
            ?parent ?parentFirstName ?parentLastName ?parentPhone ?parentEthnicity ?parentEmail ?parentTemporaryAddress ?parentPermanentAddress ?parentHemoglobinopathyStatus
            ?screeningProcess ?biologicalResult ?code ?description ?interpretation ?status ?commentInt ?recommendation ?label ?comment
    WHERE {{
        odr:{newborn_id} a odc:Newborn ;
                    odp:firstName ?firstName ;
                    odp:lastName ?lastName;
                    odp:sex ?sex ;
                    odp:birthDate ?birthDate ;
                    odp:birthTime ?birthTime ;
                    odp:birthPlace ?birthPlace ;
                    odp:hasKeyData ?keyData ;
                    odp:hasParentHistory ?parent .
                    
        OPTIONAL {{ ?keyData odp:birthWeight ?birthWeight .}}
        OPTIONAL {{ ?keyData odp:headCircumference ?headCircumference .}}
        OPTIONAL {{ ?keyData odp:armCircumference ?armCircumference .}}
        OPTIONAL {{ ?keyData odp:birthLength ?birthLength .}}
        OPTIONAL {{ ?keyData odp:gestationalAge ?gestationalAge .}}
        OPTIONAL {{ ?keyData odp:numberOfFetuses ?numberOfFetuses .}}
        OPTIONAL {{ ?keyData odp:fetalDistress ?fetalDistress .}}
        OPTIONAL {{ ?keyData odp:jaundice ?jaundice .}}
        OPTIONAL {{ ?keyData odp:cyanosis ?cyanosis .}}
        OPTIONAL {{ ?keyData odp:generates ?riskProfile .}}
        OPTIONAL {{ ?riskProfile odp:score ?score .}}
        OPTIONAL {{ ?riskProfile odp:criterion ?criterion .}}
        
        OPTIONAL {{ ?parent odp:firstName ?parentFirstName . }}
        OPTIONAL {{ ?parent odp:lastName ?parentLastName . }}
        OPTIONAL {{ ?parent odp:phone ?parentPhone . }}
        OPTIONAL {{ ?parent odp:ethnicity ?parentEthnicity . }}
        OPTIONAL {{ ?parent odp:email ?parentEmail . }}
        OPTIONAL {{ ?parent odp:temporaryAddress ?parentTemporaryAddress . }}
        OPTIONAL {{ ?parent odp:permanentAddress ?parentPermanentAddress . }}
        OPTIONAL {{ ?parent odp:hemoglobinopathyStatus ?parentHemoglobinopathyStatus . }}
        
        OPTIONAL {{ ?sample odp:isCollectedFrom odr:{newborn_id} .}}
        OPTIONAL {{ ?screeningProcess odp:performedOn ?sample .}}
        OPTIONAL {{ ?screeningProcess odp:produces ?biologicalResult .}}
        OPTIONAL {{ ?biologicalResult odp:code ?code .}}
        OPTIONAL {{ ?biologicalResult odp:description ?description .}}
        OPTIONAL {{ ?biologicalResult odp:require ?interpretation .}}
        OPTIONAL {{ ?interpretation odp:status ?status .}}
        OPTIONAL {{ ?interpretation odp:comment ?commentInt .}}
        OPTIONAL {{ ?screeningProcess odp:leadsTo ?recommendation .}}
        OPTIONAL {{ ?recommendation rdfs:label ?label .}}
        OPTIONAL {{ ?recommendation rdfs:comment ?comment .}}
        
    }}
    """
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()
        newborns = [
            {
                "firstName": result["firstName"]["value"],
                "lastName": result["lastName"]["value"],
                "sex": result["sex"]["value"],
                "birthDate": result["birthDate"]["value"],
                "birthTime": result["birthTime"]["value"],
                "birthPlace": result["birthPlace"]["value"],
                "keyData": 
                    {
                        "id": result["keyData"]["value"],
                        "birthWeight": result["birthWeight"]["value"],
                        "headCircumference": result["headCircumference"]["value"],
                        "armCircumference": result["armCircumference"]["value"],
                        "birthLength": result["birthLength"]["value"],
                        "gestationalAge": result["gestationalAge"]["value"],
                        "numberOfFetuses": result["numberOfFetuses"]["value"],
                        "fetalDistress": result["fetalDistress"]["value"],
                        "jaundice": result["jaundice"]["value"],
                        "cyanosis": result["cyanosis"]["value"],
                        "riskProfile": 
                            {
                                "id": result["riskProfile"]["value"],
                                "score": result["score"]["value"],
                                "criterion": result["criterion"]["value"]
                            }
                    },
                "parent": 
                    {
                        "id": result["parent"]["value"],
                        "firstName": result["parentFirstName"]["value"],
                        "lastName": result["parentLastName"]["value"],
                        "phone": result["parentPhone"]["value"],
                        "ethnicity": result["parentEthnicity"]["value"],
                        "email": result["parentEmail"]["value"],
                        "temporaryAddress": result["parentTemporaryAddress"]["value"],
                        "permanentAddress": result["parentPermanentAddress"]["value"],
                        "hemoglobinopathyStatus": result["parentHemoglobinopathyStatus"]["value"]
                    },
                "screeningProcess": 
                    {
                        "id": result["screeningProcess"]["value"],
                        "biologicalResult" : 
                            { 
                                "id": result["biologicalResult"]["value"],
                                "description": result["description"]["value"],
                                "interpretation": 
                                    { 
                                        "id" : result["interpretation"]["value"],
                                        "status" : result["status"]["value"],
                                        "commentInt" : result["commentInt"]["value"]
                                    }
                             },
                        "recommendation" : 
                            { 
                                "id": result["recommendation"]["value"],
                                "label": result["label"]["value"],
                                "comment": result["comment"]["value"]
                             }
                     }
            }
            for result in results["results"]["bindings"]
        ]
        return {newborn_id: newborns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

