"""Interface en ligne de commande : sentiment --version, predict, serve."""

import sys

import click

from sentiment_app import __version__
from sentiment_app.predict import ModeleIntrouvable, charger_modele, predire


@click.group()
@click.version_option(__version__, prog_name="sentiment-app", message="%(prog)s %(version)s")
def main():
    """Analyse de sentiment d'avis en français."""


@main.command()
@click.argument("texte")
def predict(texte: str):
    """Affiche l'étiquette et le score pour un avis."""
    try:
        modele = charger_modele()
    except ModeleIntrouvable as erreur:
        click.echo(f"Erreur : {erreur}", err=True)
        sys.exit(1)
    resultat = predire(texte, modele)
    click.echo(f"{resultat['label']} {resultat['score']}")


@main.command()
@click.option("--host", default="127.0.0.1", show_default=True)
@click.option("--port", default=8000, type=int, show_default=True)
def serve(host: str, port: int):
    """Lance l'API FastAPI avec uvicorn."""
    import uvicorn

    uvicorn.run("api.main:app", host=host, port=port)
