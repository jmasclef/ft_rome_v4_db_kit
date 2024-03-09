from __future__ import annotations
from typing import List, Optional
from schemas.core_schemas import OurRootModel, OurBaseModel


class CompetenceESCO(OurBaseModel):
    uri: str
    libelle: str


class MacroCompetence(OurBaseModel):
    code: str
    libelle: str
    codeOgr: str
    transitionEcologique: bool
    transitionNumerique: bool
    competenceEsco: CompetenceESCO
    type: str
    qualiteProfessionnelle: str


class Objectif(OurBaseModel):
    code: str
    libelle: str
    enjeu: str
    macroCompetences: List[MacroCompetence]


class Enjeu(OurBaseModel):
    code: str
    libelle: str
    domaineCompetence: str
    objectifs: List[Objectif]


class Theme(OurBaseModel):
    libelle: str
    definition: Optional[str] = None
    code: str
    metiers: Optional[List[str]] = None


class Competence(OurBaseModel):
    code: str
    libelle: str
    codeOgr: str
    type: str


class CompetenceCle(OurBaseModel):
    competence: Competence
    frequence: int


class DivisionNaf(OurBaseModel):
    code: str
    libelle: str


class Formacode(OurBaseModel):
    code: str
    libelle: str


class ContexteTravail(OurBaseModel):
    code: str
    libelle: str


class GrandDomaineMetiers(OurBaseModel):
    code: str
    libelle: str
    domaineProfessionnels: Optional[List[DomaineMetiers]] = None
    metiers: Optional[List[Metier]] = None


class DomaineMetiers(OurBaseModel):
    code: str
    libelle: str
    grandDomaine: Optional[GrandDomaineMetiers] = None
    metiers: Optional[List[Metier]] = None


class Appellation(OurBaseModel):
    code: str
    libelle: str
    libelleCourt: Optional[str] = None
    emploiCadre: Optional[bool] = None
    emploiReglemente: Optional[bool] = None
    transitionEcologique: Optional[bool] = None
    transitionNumerique: Optional[bool] = None
    classification: Optional[str] = None
    metier: Optional[Metier] = None
    appellationEsco: Optional[CompetenceESCO] = None
    competencesCles: Optional[List[CompetenceCle]] = None
    metiersProches: Optional[List[Metier]] = None
    metiersEnvisageables: Optional[List[Metier]] = None
    appellationsProches: Optional[List[Appellation]] = None
    appellationsEnvisageables: Optional[List[Appellation]] = None


class Metier(OurBaseModel):
    code: str
    libelle: str
    definition: Optional[str] = None
    accesEmploi: Optional[str] = None
    riasecMajeur: Optional[str] = None
    riasecMineur: Optional[str] = None
    transitionEcologique: Optional[bool] = None
    transitionNumerique: Optional[bool] = None
    codeIsco: Optional[str] = None
    domaineProfessionnel: Optional[DomaineMetiers] = None
    appellations: Optional[List[Appellation]] = None
    themes: Optional[List[Theme]] = None
    competencesMobilisees: Optional[List[Competence]] = None
    divisionsNaf: Optional[List[DivisionNaf]] = None
    formacodes: Optional[List[Formacode]] = None
    contextesTravail: Optional[List[ContexteTravail]] = None
    metiersProches: Optional[List[Metier]] = None
    metiersEnvisageables: Optional[List[Metier]] = None
    appellationsProches: Optional[List[Appellation]] = None
    appellationsEnvisageables: Optional[List[Appellation]] = None


class Appellations(OurRootModel):
    root: List[Appellation]


class Metiers(OurRootModel):
    root: List[Metier]


class Themes(OurRootModel):
    root: List[Theme]


class GrandsDomaines(OurRootModel):
    root: List[GrandDomaineMetiers]


class Domaines(OurRootModel):
    root: List[DomaineMetiers]
