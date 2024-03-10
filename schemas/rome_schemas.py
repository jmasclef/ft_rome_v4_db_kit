from __future__ import annotations
from typing import List, Optional
from sqlmodel import Field, SQLModel
from schemas.core_schemas import OurRootModel


class CompetenceESCO(SQLModel, table=True):
    uri: str = Field(primary_key=True)
    libelle: str


class ContexteTravail(SQLModel, table=True):
    code: str = Field(primary_key=True)
    libelle: str
    categorie: str


class CategorieSavoir(SQLModel, table=True):
    code: str = Field(primary_key=True)
    libelle: str
    sousCategories: str
    savoirs: str


class SavoirBase(SQLModel):
    code: str = Field(primary_key=True)
    libelle: str
    codeOgr: str
    transitionEcologique: bool
    transitionNumerique: bool
    type: str


class Savoir(SavoirBase, table=True):
    pass


class SavoirRead(SavoirBase):
    competenceEsco: CompetenceESCO
    categorieSavoir: CategorieSavoir


class MacroCompetenceBase(SQLModel):
    code: str = Field(primary_key=True)
    libelle: str
    codeOgr: str
    transitionEcologique: bool
    transitionNumerique: bool
    type: str
    qualiteProfessionnelle: str


class MacroCompetence(MacroCompetenceBase, table=True):
    pass


class MacroCompetenceRead(MacroCompetenceBase):
    competenceEsco: CompetenceESCO


class ObjectifBase(SQLModel):
    code: str = Field(primary_key=True)
    libelle: str
    enjeu: str


class Objectif(ObjectifBase, table=True):
    pass


class ObjectifRead(ObjectifBase):
    macroCompetences: List[MacroCompetence]


class EnjeuBase(SQLModel):
    code: str = Field(primary_key=True)
    libelle: str
    domaineCompetence: str


class Enjeu(EnjeuBase, table=True):
    pass


class EnjeuRead(EnjeuBase):
    objectifs: List[Objectif]


class DomaineCompetenceBase(SQLModel):
    code: str = Field(primary_key=True)
    libelle: str


class DomaineCompetence(DomaineCompetenceBase, table=True):
    pass


class DomaineCompetenceRead(DomaineCompetenceBase):
    enjeux: List[EnjeuBase]


class ThemeBase(SQLModel):
    code: str = Field(primary_key=True)
    libelle: str
    definition: Optional[str] = None


class Theme(ThemeBase, table=True):
    pass


class ThemeRead(ThemeBase):
    metiers: Optional[List[str]] = None


class Competence(SQLModel, table=True):
    code: str = Field(primary_key=True)
    libelle: str
    codeOgr: str
    type: str


class CompetenceDetailleeBase(SQLModel):
    code: str = Field(primary_key=True)
    libelle: str
    codeOgr: str
    transitionEcologique: bool
    transitionNumerique: bool
    type: str
    riasecMineur: str
    riasecMajeur: str
    macroCompetence: str


class CompetenceDetaillee(CompetenceDetailleeBase):
    pass


class CompetenceDetailleeRead(CompetenceDetailleeBase):
    competenceEsco: CompetenceESCO


class MacroSavoirEtreProfessionnelBase(SQLModel):
    code: str = Field(primary_key=True)
    libelle: str
    codeOgr: str
    transitionEcologique: bool
    transitionNumerique: bool
    type: str
    qualiteProfessionnelle: str


class MacroSavoirEtreProfessionnel(MacroSavoirEtreProfessionnelBase, table=True):
    pass


class MacroSavoirEtreProfessionnelRead(MacroSavoirEtreProfessionnelBase):
    competenceEsco: CompetenceESCO


class DivisionNaf(SQLModel, table=True):
    code: str = Field(primary_key=True)
    libelle: str


class Formacode(SQLModel, table=True):
    code: str = Field(primary_key=True)
    libelle: str


class ContexteTravail(SQLModel, table=True):
    code: str = Field(primary_key=True)
    libelle: str


class GrandDomaineMetiersBase(SQLModel):
    code: str = Field(primary_key=True)
    libelle: str


class GrandDomaineMetiers(GrandDomaineMetiersBase, table=True):
    pass


class GrandDomaineMetiersRead(GrandDomaineMetiersBase):
    domaineProfessionnels: Optional[List[DomaineMetiers]] = None
    metiers: Optional[List[Metier]] = None


class DomaineMetiersBase(SQLModel):
    code: str = Field(primary_key=True)
    libelle: str


class DomaineMetiers(DomaineMetiersBase, table=True):
    pass


class DomaineMetiersRead(DomaineMetiersBase):
    grandDomaine: Optional[GrandDomaineMetiers] = None
    metiers: Optional[List[Metier]] = None


class AppellationBase(SQLModel):
    code: str = Field(primary_key=True)
    libelle: str
    libelleCourt: Optional[str] = None
    emploiCadre: Optional[bool] = None
    emploiReglemente: Optional[bool] = None
    transitionEcologique: Optional[bool] = None
    transitionNumerique: Optional[bool] = None
    classification: Optional[str] = None


class Appellation(AppellationBase, table=True):
    pass


class AppellationRead(AppellationBase):
    metier: Optional[Metier] = None
    appellationEsco: Optional[CompetenceESCO] = None
    competencesCles: Optional[List[Competence]] = None
    metiersProches: Optional[List[Metier]] = None
    metiersEnvisageables: Optional[List[Metier]] = None
    appellationsProches: Optional[List[Appellation]] = None
    appellationsEnvisageables: Optional[List[Appellation]] = None


class MetierBase(SQLModel):
    code: str = Field(primary_key=True)
    libelle: str
    definition: Optional[str] = None
    accesEmploi: Optional[str] = None
    riasecMajeur: Optional[str] = None
    riasecMineur: Optional[str] = None
    transitionEcologique: Optional[bool] = None
    transitionNumerique: Optional[bool] = None
    codeIsco: Optional[str] = None


class Metier(MetierBase, table=True):
    pass


class MetierRead(MetierBase):
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
    root: List[AppellationRead]


class Metiers(OurRootModel):
    root: List[MetierRead]


class Themes(OurRootModel):
    root: List[ThemeRead]


class GrandsDomaines(OurRootModel):
    root: List[GrandDomaineMetiersRead]


class DomainesMetiers(OurRootModel):
    root: List[DomaineMetiersRead]
