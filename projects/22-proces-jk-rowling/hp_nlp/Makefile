# Makefile pour le pipeline NLP Harry Potter
# Simplifie l'exécution des notebooks et l'installation

.PHONY: help setup install-spacy run clean test

# Couleurs pour l'affichage
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

help: ## Affiche cette aide
	@echo "$(GREEN)Pipeline NLP Harry Potter - Commandes disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

setup: ## Installation complète (dépendances + modèle spaCy)
	@echo "$(GREEN)🔧 Installation des dépendances...$(NC)"
	pip install -r requirements.txt
	@echo ""
	@echo "$(GREEN)📦 Téléchargement du modèle spaCy français...$(NC)"
	python -m spacy download fr_core_news_lg || python -m spacy download fr_core_news_sm
	@echo ""
	@echo "$(GREEN)✅ Installation terminée!$(NC)"

install-spacy: ## Installer uniquement le modèle spaCy
	@echo "$(GREEN)📦 Installation du modèle spaCy français (large)...$(NC)"
	python -m spacy download fr_core_news_lg || echo "$(YELLOW)⚠️  Modèle large non disponible, installation du modèle small...$(NC)" && python -m spacy download fr_core_news_sm

run: ## Exécuter tous les notebooks en séquence
	@echo "$(GREEN)🚀 Exécution du pipeline NLP complet...$(NC)"
	@echo ""
	@echo "$(YELLOW)📖 Notebook 1: Ingestion et nettoyage$(NC)"
	jupyter nbconvert --to notebook --execute notebooks/01_ingest_clean.ipynb --output 01_ingest_clean.ipynb
	@echo ""
	@echo "$(YELLOW)🧠 Notebook 2: Pipeline NLP$(NC)"
	jupyter nbconvert --to notebook --execute notebooks/02_nlp_pipeline.ipynb --output 02_nlp_pipeline.ipynb
	@echo ""
	@echo "$(YELLOW)🔍 Notebook 3: Extraction d'événements$(NC)"
	jupyter nbconvert --to notebook --execute notebooks/03_events_extraction.ipynb --output 03_events_extraction.ipynb
	@echo ""
	@echo "$(YELLOW)📊 Notebook 4: Agrégation et visualisations$(NC)"
	jupyter nbconvert --to notebook --execute notebooks/04_aggregation_viz.ipynb --output 04_aggregation_viz.ipynb
	@echo ""
	@echo "$(YELLOW)📄 Notebook 5: Rapport méthodologique$(NC)"
	jupyter nbconvert --to notebook --execute notebooks/05_methods_report.ipynb --output 05_methods_report.ipynb
	@echo ""
	@echo "$(GREEN)✅ Pipeline terminé! Résultats dans outputs/$(NC)"

run-nb1: ## Exécuter notebook 1 uniquement (ingestion)
	@echo "$(GREEN)📖 Exécution: Ingestion et nettoyage$(NC)"
	jupyter nbconvert --to notebook --execute notebooks/01_ingest_clean.ipynb --output 01_ingest_clean.ipynb

run-nb2: ## Exécuter notebook 2 uniquement (NLP)
	@echo "$(GREEN)🧠 Exécution: Pipeline NLP$(NC)"
	jupyter nbconvert --to notebook --execute notebooks/02_nlp_pipeline.ipynb --output 02_nlp_pipeline.ipynb

run-nb3: ## Exécuter notebook 3 uniquement (événements)
	@echo "$(GREEN)🔍 Exécution: Extraction d'événements$(NC)"
	jupyter nbconvert --to notebook --execute notebooks/03_events_extraction.ipynb --output 03_events_extraction.ipynb

run-nb4: ## Exécuter notebook 4 uniquement (visualisations)
	@echo "$(GREEN)📊 Exécution: Agrégation et visualisations$(NC)"
	jupyter nbconvert --to notebook --execute notebooks/04_aggregation_viz.ipynb --output 04_aggregation_viz.ipynb

run-nb5: ## Exécuter notebook 5 uniquement (rapport)
	@echo "$(GREEN)📄 Exécution: Rapport méthodologique$(NC)"
	jupyter nbconvert --to notebook --execute notebooks/05_methods_report.ipynb --output 05_methods_report.ipynb

report: ## Générer uniquement le rapport (suppose que les données existent)
	@echo "$(GREEN)📄 Génération du rapport...$(NC)"
	jupyter nbconvert --to notebook --execute notebooks/05_methods_report.ipynb --output 05_methods_report.ipynb
	@echo "$(GREEN)✅ Rapport généré: outputs/methodology_report.html$(NC)"

open-report: ## Ouvrir le rapport HTML dans le navigateur
	@if [ -f outputs/methodology_report.html ]; then \
		xdg-open outputs/methodology_report.html 2>/dev/null || open outputs/methodology_report.html 2>/dev/null || echo "$(YELLOW)Ouvrez manuellement: outputs/methodology_report.html$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  Rapport non trouvé. Exécutez 'make report' d'abord.$(NC)"; \
	fi

jupyter: ## Lancer Jupyter Lab
	@echo "$(GREEN)🚀 Lancement de Jupyter Lab...$(NC)"
	jupyter lab

clean: ## Nettoyer les fichiers temporaires et générés
	@echo "$(GREEN)🧹 Nettoyage...$(NC)"
	rm -rf data/*.parquet
	rm -rf outputs/*
	rm -rf .ipynb_checkpoints
	rm -rf notebooks/.ipynb_checkpoints
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)✅ Nettoyage terminé$(NC)"

clean-outputs: ## Nettoyer uniquement les sorties (garder les données)
	@echo "$(GREEN)🧹 Nettoyage des outputs...$(NC)"
	rm -rf outputs/*
	@echo "$(GREEN)✅ Outputs nettoyés$(NC)"

test: ## Vérifier l'installation et les dépendances
	@echo "$(GREEN)🧪 Vérification de l'environnement...$(NC)"
	@echo ""
	@python --version || echo "$(YELLOW)⚠️  Python non trouvé$(NC)"
	@echo ""
	@python -c "import pandas; print('✅ pandas:', pandas.__version__)" || echo "$(YELLOW)⚠️  pandas non installé$(NC)"
	@python -c "import spacy; print('✅ spaCy:', spacy.__version__)" || echo "$(YELLOW)⚠️  spaCy non installé$(NC)"
	@python -c "import spacy; nlp = spacy.load('fr_core_news_lg'); print('✅ Modèle fr_core_news_lg chargé')" || \
		python -c "import spacy; nlp = spacy.load('fr_core_news_sm'); print('✅ Modèle fr_core_news_sm chargé')" || \
		echo "$(YELLOW)⚠️  Aucun modèle français trouvé$(NC)"
	@python -c "import matplotlib; print('✅ matplotlib:', matplotlib.__version__)" || echo "$(YELLOW)⚠️  matplotlib non installé$(NC)"
	@python -c "import jupyter; print('✅ jupyter installé')" || echo "$(YELLOW)⚠️  jupyter non installé$(NC)"
	@echo ""
	@echo "$(GREEN)✅ Vérification terminée$(NC)"

stats: ## Afficher les statistiques du projet
	@echo "$(GREEN)📊 Statistiques du projet$(NC)"
	@echo ""
	@echo "Notebooks:"
	@ls -lh notebooks/*.ipynb 2>/dev/null | wc -l | xargs echo "  Nombre:"
	@echo ""
	@echo "Données:"
	@if [ -d data ]; then \
		du -sh data 2>/dev/null | awk '{print "  Taille data: " $$1}'; \
		ls data/*.parquet 2>/dev/null | wc -l | xargs echo "  Fichiers parquet:"; \
	else \
		echo "  Aucune donnée générée"; \
	fi
	@echo ""
	@echo "Outputs:"
	@if [ -d outputs ]; then \
		du -sh outputs 2>/dev/null | awk '{print "  Taille outputs: " $$1}'; \
		ls outputs/* 2>/dev/null | wc -l | xargs echo "  Fichiers générés:"; \
	else \
		echo "  Aucun output généré"; \
	fi

# Par défaut, afficher l'aide
.DEFAULT_GOAL := help
