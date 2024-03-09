import os
import requests
from pprint import pprint
from dataclasses import dataclass
from schemas import rome_schemas


@dataclass
class FranceTravailClient:
    __authorization: str = None
    __env_client_id = 'ENV_FT_CLIENT_ID'
    __env_client_secret = 'ENV_FT_CLIENT_SECRET'

    def __proceed_rome_request__(self, func, **kwargs):
        if 'url' not in kwargs:
            raise NameError("Programming Error: 'url' parameter is missing in request call")
        else:
            url = kwargs['url']
        if 'headers' not in kwargs:
            kwargs.update({'headers': {'Authorization': self.__authorization,
                                       'Content-Type': 'application/x-www-form-urlencoded'}})

        try:
            response = func(**kwargs)
        except Exception as exc:
            raise ConnectionError(f"Exception on ROME request URL={url} EXCEPTION={exc}")

        if response.status_code == 200:
            return response
        elif response.status_code == 400:
            raise Exception(f"Request failure 400, URL={url}: Bad request, reason: {response.reason}")
        elif response.status_code == 401:
            raise Exception(f"Request failure 401, URL={url}: Unauthorized, check credentials")
        elif response.status_code == 404:
            raise Exception(f"Request failure 404, URL={url}: Not found")
        else:
            raise Exception(f"Request failure {response.status_code}: {response.content}")

    def rome_request_get(self, **kwargs):
        func = requests.get
        return self.__proceed_rome_request__(func=func, **kwargs)

    def rome_request_post(self, **kwargs):
        func = requests.post
        return self.__proceed_rome_request__(func=func, **kwargs)

    def __init__(self, client_id: str = None, client_secret: str = None, load_credentials_from_env: bool = False):
        """
        Source: https://francetravail.io/data/documentation/utilisation-api-pole-emploi/generer-access-token
        """
        if load_credentials_from_env:
            if os.environ.get(self.__env_client_id, None) is None:
                raise NameError(f"Missing variable {self.__env_client_id} in environment variables")
            else:
                client_id = os.environ.get(self.__env_client_id)
            if os.environ.get(self.__env_client_secret, None) is None:
                raise NameError(f"Missing variable {self.__env_client_secret} in environment variables")
            else:
                client_secret = os.environ.get(self.__env_client_secret)
        else:
            if client_secret is None:
                raise NameError(f"Missing variable client_id value")
            if client_secret is None:
                raise NameError(f"Missing variable client_secret value")

        url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token"
        data = {"grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                "scope": "nomenclatureRome api_rome-competencesv1 api_rome-metiersv1 api_rome-contextes-travailv1"}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}  # Mandatory for not to send Authorization
        params = {'realm': '/partenaire'}
        response = self.rome_request_post(url=url, headers=headers, params=params, data=data)
        access_token = response.json()['access_token']
        self.__authorization = f"Bearer {access_token}"

    def get_metiers(self, code: str = None):
        """
        Sources:
        https://francetravail.io/data/documentation/utilisation-api-pole-emploi/requeter-api
        https://francetravail.io/data/api/rome-4-0-metiers/documentation#/api-reference/operations/listerMetiers
        """
        if code is None:
            url = "https://api.pole-emploi.io/partenaire/rome-metiers/v1/metiers/metier"
            Schema = rome_schemas.Metiers
        else:
            url = f"https://api.pole-emploi.io/partenaire/rome-metiers/v1/metiers/metier/{code}"
            Schema = rome_schemas.Metier
        response = self.rome_request_get(url=url)
        return Schema.model_validate_json(response.text)

    def get_appellations(self, code: str = None):
        """
        Sources:
        https://francetravail.io/data/documentation/utilisation-api-pole-emploi/requeter-api
        https://francetravail.io/data/api/rome-4-0-metiers/documentation#/api-reference/operations/listerAppellations
        """
        if code is None:
            url = "https://api.pole-emploi.io/partenaire/rome-metiers/v1/metiers/appellation"
            Schema = rome_schemas.Appellations
        else:
            url = f"https://api.pole-emploi.io/partenaire/rome-metiers/v1/metiers/appellation/{code}"
            Schema = rome_schemas.Appellation

        response = self.rome_request_get(url=url)
        return Schema.model_validate_json(response.text)

    def get_themes(self, code: str = None):
        """
        Sources:
        https://francetravail.io/data/documentation/utilisation-api-pole-emploi/requeter-api
        https://francetravail.io/data/api/rome-4-0-metiers/documentation#/api-reference/operations/listerThemes
        """
        if code is None:
            url = "https://api.pole-emploi.io/partenaire/rome-metiers/v1/metiers/theme"
            Schema = rome_schemas.Themes
        else:
            url = f"https://api.pole-emploi.io/partenaire/rome-metiers/v1/metiers/theme/{code}"
            Schema = rome_schemas.Theme

        response = self.rome_request_get(url=url)
        return Schema.model_validate_json(response.text)

    def get_grands_domaines(self, code: str = None):
        """
        Sources:
        https://francetravail.io/data/documentation/utilisation-api-pole-emploi/requeter-api
        https://francetravail.io/data/api/rome-4-0-metiers/documentation#/api-reference/operations/listerGrandDomaines
        """
        if code is None:
            url = "https://api.pole-emploi.io/partenaire/rome-metiers/v1/metiers/grand-domaine"
            Schema = rome_schemas.GrandsDomaines
        else:
            url = f"https://api.pole-emploi.io/partenaire/rome-metiers/v1/metiers/grand-domaine/{code}"
            Schema = rome_schemas.GrandDomaineMetiers

        response = self.rome_request_get(url=url)
        return Schema.model_validate_json(response.text)

    def get_domaines(self, code: str = None):
        """
        Sources:
        https://francetravail.io/data/documentation/utilisation-api-pole-emploi/requeter-api
        https://francetravail.io/data/api/rome-4-0-metiers/documentation#/api-reference/operations/listerDomainesProfessionnels
        """
        if code is None:
            url = "https://api.pole-emploi.io/partenaire/rome-metiers/v1/metiers/domaine-professionnel"
            Schema = rome_schemas.Domaines
        else:
            url = f"https://api.pole-emploi.io/partenaire/rome-metiers/v1/metiers/domaine-professionnel/{code}"
            Schema = rome_schemas.DomaineMetiers

        response = self.rome_request_get(url=url)
        return Schema.model_validate_json(response.text)


if __name__ == '__main__':
    # ft_client = FranceTravailClient(
    #     client_id="PAR_testromev4asr_c0f296273b534af43bdd5d1b591b93a53d6a0405438dbae058e85d4a80450a45",
    #     client_secret="a78dc88f59c0065801a4df2a7f6c76745a989c7b8959001ee4d3bab71feba992")
    ft_client = FranceTravailClient(load_credentials_from_env=True)
    domaines= ft_client.get_domaines()
    pprint(domaines)

    domaine=ft_client.get_domaines(code='A11')
    pprint(domaine)