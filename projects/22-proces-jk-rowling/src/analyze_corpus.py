#!/usr/bin/env python3
"""
Pipeline d'analyse textuelle des livres Harry Potter
Extrait et analyse diverses statistiques sur le corpus
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
import PyPDF2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
# Get the script's directory and build paths relative to project root
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BOOKS_DIR = PROJECT_ROOT / "../../context/books"
OUTPUT_DIR = PROJECT_ROOT / "output"
DATA_DIR = PROJECT_ROOT / "data"

# Créer les répertoires nécessaires
OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Informations sur les livres (pages approximatives)
BOOK_INFO = {
    "harry-potter-1-lecole-des-sorciers.pdf": {"title": "L'École des Sorciers", "pages": 320},
    "harry-potter-2-la-chambre-des-secrets.pdf": {"title": "La Chambre des Secrets", "pages": 360},
    "harry-potter-3-le-prisonnier-dazkaban.pdf": {"title": "Le Prisonnier d'Azkaban", "pages": 420},
    "harry-potter-4-la-coupe-de-feu.pdf": {"title": "La Coupe de Feu", "pages": 656},
    "harry-potter-5-lordre-du-phoenix.pdf": {"title": "L'Ordre du Phénix", "pages": 980},
    "harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf": {"title": "Le Prince de Sang-Mêlé", "pages": 640},
    "harry-potter-7-les-reliques-de-la-mort.pdf": {"title": "Les Reliques de la Mort", "pages": 800}
}


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrait le texte d'un PDF"""
    print(f"📖 Extraction de {pdf_path.name}...")
    text = ""
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                try:
                    text += page.extract_text() + "\n"
                except Exception as e:
                    print(f"⚠️  Erreur page: {e}")
                    continue
    except Exception as e:
        print(f"❌ Erreur lecture {pdf_path.name}: {e}")
        return ""
    
    return text


def count_pattern(text: str, pattern: str, case_sensitive: bool = False) -> int:
    """Compte les occurrences d'un pattern dans le texte"""
    flags = 0 if case_sensitive else re.IGNORECASE
    matches = re.findall(pattern, text, flags)
    return len(matches)


def count_scar_touches(text: str) -> int:
    """Compte les fois où Harry touche sa cicatrice"""
    patterns = [
        r'cicatrice.*?(?:brûl|douleur|fait mal|élançait|picotait)',
        r'(?:douleur|brûlure).*?cicatrice',
        r'porta.*?main.*?cicatrice',
        r'toucha.*?cicatrice',
        r'front.*?(?:brûlait|douleur|élançait)',
        r'cicatrice.*?(?:pulsait|battait)'
    ]
    
    total = 0
    for pattern in patterns:
        total += count_pattern(text, pattern)
    
    return total


def count_hermione_mais(text: str) -> int:
    """Compte les fois où Hermione dit 'Mais'"""
    # Recherche Hermione suivie de dialogue contenant "Mais"
    patterns = [
        r'Hermione.*?[«"][^»"]{0,200}\bMais\b[^»"]{0,200}[»"]',
        r'[«"].*?\bMais\b.*?[»"].*?dit Hermione',
        r'— Mais.*?(?:dit|déclara|répondit|s\'écria) Hermione'
    ]
    
    total = 0
    for pattern in patterns:
        total += count_pattern(text, pattern)
    
    return total


def count_dumbledore_interventions(text: str) -> int:
    """Compte les interventions arbitraires de Dumbledore"""
    patterns = [
        r'Dumbledore.*?(?:décida|changea|modifia|annonça)',
        r'(?:exception|règle).*?Dumbledore',
        r'Dumbledore.*?(?:points|coupe)',
        r'Dumbledore.*?(?:dit|déclara|annonça).*?(?:cependant|toutefois|néanmoins)'
    ]
    
    total = 0
    for pattern in patterns:
        total += count_pattern(text, pattern)
    
    return total


def count_character_speeches(text: str) -> Dict[str, int]:
    """Compte les prises de parole de Harry, Hermione et Ron"""
    characters = {
        "Harry": [r'dit Harry', r'Harry.*?(?:répondit|déclara|s\'écria|demanda|murmura)'],
        "Hermione": [r'dit Hermione', r'Hermione.*?(?:répondit|déclara|s\'écria|demanda|murmura)'],
        "Ron": [r'dit Ron', r'Ron.*?(?:répondit|déclara|s\'écria|demanda|murmura)']
    }
    
    counts = {}
    for char, patterns in characters.items():
        total = 0
        for pattern in patterns:
            total += count_pattern(text, pattern)
        counts[char] = total
    
    return counts


def count_snape_mysterious(text: str) -> int:
    """Compte les moments où Rogue est mystérieux ou sombre"""
    patterns = [
        r'Rogue.*?(?:sombre|mystérieux|inquiétant|menaçant)',
        r'(?:regard|voix|ton).*?(?:de )?Rogue.*?(?:froid|glacial|menaçant)',
        r'Rogue.*?(?:ricana|sourit.*?(?:méchamment|cruellement))',
        r'Severus.*?(?:sombre|mystérieux|inquiétant)',
        r'professeur.*?Rogue.*?(?:apparut|surgit)'
    ]
    
    total = 0
    for pattern in patterns:
        total += count_pattern(text, pattern)
    
    return total


def count_questionable_acts(text: str) -> int:
    """Compte les actes moralement/légalement répréhensibles"""
    patterns = [
        r'(?:mensonge|mentir|menti)',
        r'(?:voler|vol|volé|dérobé)',
        r'(?:enfreindre|enfreint|violer|violé).*?(?:règle|loi|règlement)',
        r'(?:sortir|sorti).*?(?:après|sans).*?(?:autorisation|permission)',
        r'(?:attaquer|attaqué|attaque)',
        r'(?:interdiction|interdit)',
        r'(?:combat|bataille|duel)(?!.*?(?:officiel|autorisé))',
        r'(?:forêt interdite)',
        r'(?:cape d\'invisibilité).*?(?:utiliser|utilisa)',
        r'(?:section interdite)'
    ]
    
    total = 0
    for pattern in patterns:
        total += count_pattern(text, pattern)
    
    # Note: Ce chiffre sera approximatif car il faut le contexte pour déterminer
    # si l'acte est vraiment répréhensible
    return total


def analyze_book(pdf_path: Path, book_info: Dict) -> Dict:
    """Analyse complète d'un livre"""
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        return None
    
    # Extraction des statistiques
    stats = {
        "title": book_info["title"],
        "filename": pdf_path.name,
        "pages": book_info["pages"],
        "scar_touches": count_scar_touches(text),
        "hermione_mais": count_hermione_mais(text),
        "dumbledore_interventions": count_dumbledore_interventions(text),
        "snape_mysterious": count_snape_mysterious(text),
        "questionable_acts": count_questionable_acts(text),
        "text_length": len(text)
    }
    
    # Prises de parole
    speeches = count_character_speeches(text)
    stats.update(speeches)
    
    # Statistiques normalisées par 100 pages
    stats["scar_per_100p"] = (stats["scar_touches"] / stats["pages"]) * 100
    stats["mais_per_100p"] = (stats["hermione_mais"] / stats["pages"]) * 100
    stats["dumbledore_per_100p"] = (stats["dumbledore_interventions"] / stats["pages"]) * 100
    stats["snape_per_100p"] = (stats["snape_mysterious"] / stats["pages"]) * 100
    stats["acts_per_100p"] = (stats["questionable_acts"] / stats["pages"]) * 100
    
    return stats


def create_visualizations(df: pd.DataFrame):
    """Crée les visualisations des statistiques"""
    print("\n📊 Création des visualisations...")
    
    # Configuration du style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (14, 10)
    
    # 1. Évolution de la cicatrice de Harry
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('⚡ Le Procès de J.K. Rowling - Statistiques Harry Potter', fontsize=16, fontweight='bold')
    
    # Cicatrices
    axes[0, 0].plot(range(1, 8), df['scar_touches'], marker='o', linewidth=2, markersize=8, color='red')
    axes[0, 0].set_title('🔥 Harry et sa cicatrice (total)', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Livre')
    axes[0, 0].set_ylabel('Occurrences')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Hermione dit "Mais"
    axes[0, 1].plot(range(1, 8), df['hermione_mais'], marker='s', linewidth=2, markersize=8, color='purple')
    axes[0, 1].set_title('💬 Hermione dit "Mais"', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Livre')
    axes[0, 1].set_ylabel('Occurrences')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Dumbledore change tout
    axes[1, 0].plot(range(1, 8), df['dumbledore_interventions'], marker='^', linewidth=2, markersize=8, color='blue')
    axes[1, 0].set_title('🧙 Dumbledore change le cours de l\'histoire', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Livre')
    axes[1, 0].set_ylabel('Occurrences')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Rogue mystérieux
    axes[1, 1].plot(range(1, 8), df['snape_mysterious'], marker='D', linewidth=2, markersize=8, color='black')
    axes[1, 1].set_title('🖤 Rogue being Rogue', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Livre')
    axes[1, 1].set_ylabel('Occurrences')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'statistics_trends.png', dpi=300, bbox_inches='tight')
    print("✅ Graphique des tendances sauvegardé")
    
    # 2. Comparaison des prises de parole
    fig, ax = plt.subplots(figsize=(14, 8))
    x = np.arange(len(df['title']))
    width = 0.25
    
    ax.bar(x - width, df['Harry'], width, label='Harry', color='#740001')
    ax.bar(x, df['Hermione'], width, label='Hermione', color='#946B2D')
    ax.bar(x + width, df['Ron'], width, label='Ron', color='#1F1F1F')
    
    ax.set_title('🗣️ Qui est le plus bavard ? (Prises de parole par livre)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Livre', fontsize=12)
    ax.set_ylabel('Nombre de prises de parole', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(df['title'], rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'speech_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Graphique des prises de parole sauvegardé")
    
    # 3. Actes répréhensibles
    fig, ax = plt.subplots(figsize=(14, 8))
    colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(df)))
    bars = ax.bar(range(1, 8), df['questionable_acts'], color=colors)
    
    ax.set_title('⚖️ MAIS QUE FAIT LA POLICE ? (Actes répréhensibles)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Livre', fontsize=12)
    ax.set_ylabel('Nombre d\'actes', fontsize=12)
    ax.set_xticks(range(1, 8))
    ax.set_xticklabels([f"Livre {i}" for i in range(1, 8)])
    ax.grid(True, alpha=0.3, axis='y')
    
    # Annotations
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'questionable_acts.png', dpi=300, bbox_inches='tight')
    print("✅ Graphique des actes répréhensibles sauvegardé")
    
    # 4. Statistiques normalisées (par 100 pages)
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('📈 Statistiques normalisées (par 100 pages)', fontsize=16, fontweight='bold')
    
    metrics = [
        ('scar_per_100p', 'Cicatrice de Harry', 'red'),
        ('mais_per_100p', 'Hermione dit "Mais"', 'purple'),
        ('dumbledore_per_100p', 'Interventions Dumbledore', 'blue'),
        ('snape_per_100p', 'Rogue mystérieux', 'black')
    ]
    
    for idx, (metric, title, color) in enumerate(metrics):
        ax = axes[idx // 2, idx % 2]
        ax.plot(range(1, 8), df[metric], marker='o', linewidth=2, markersize=8, color=color)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlabel('Livre')
        ax.set_ylabel('Occurrences / 100 pages')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'normalized_statistics.png', dpi=300, bbox_inches='tight')
    print("✅ Graphique des statistiques normalisées sauvegardé")
    
    # 5. Heatmap de toutes les statistiques
    fig, ax = plt.subplots(figsize=(12, 10))
    
    stats_columns = ['scar_touches', 'hermione_mais', 'dumbledore_interventions', 
                     'snape_mysterious', 'questionable_acts', 'Harry', 'Hermione', 'Ron']
    heatmap_data = df[stats_columns].T
    
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', 
                xticklabels=[f"L{i}" for i in range(1, 8)],
                yticklabels=['Cicatrice Harry', 'Hermione "Mais"', 'Dumbledore', 
                            'Rogue', 'Actes répréh.', 'Paroles Harry', 'Paroles Hermione', 'Paroles Ron'],
                ax=ax, cbar_kws={'label': 'Occurrences'})
    
    ax.set_title('🔥 Heatmap complète des statistiques', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'heatmap_all_stats.png', dpi=300, bbox_inches='tight')
    print("✅ Heatmap complète sauvegardée")


def main():
    """Pipeline principal d'analyse"""
    print("=" * 70)
    print("⚡ LE PROCÈS DE J.K. ROWLING - Analyse Statistique")
    print("=" * 70)
    
    # Analyse de tous les livres
    all_stats = []
    
    for filename, info in BOOK_INFO.items():
        pdf_path = BOOKS_DIR / filename
        if pdf_path.exists():
            stats = analyze_book(pdf_path, info)
            if stats:
                all_stats.append(stats)
                print(f"✅ {info['title']} analysé")
        else:
            print(f"⚠️  {filename} introuvable à {pdf_path}")
    
    if not all_stats:
        print("\n❌ Aucun livre trouvé pour l'analyse!")
        print(f"Vérifiez que les PDFs sont dans: {BOOKS_DIR.absolute()}")
        return
    
    # Création du DataFrame
    df = pd.DataFrame(all_stats)
    
    # Sauvegarde des données brutes
    df.to_csv(DATA_DIR / 'statistics.csv', index=False)
    print(f"\n💾 Statistiques sauvegardées dans {DATA_DIR / 'statistics.csv'}")
    
    # Sauvegarde JSON
    df.to_json(DATA_DIR / 'statistics.json', orient='records', indent=2, force_ascii=False)
    print(f"💾 Statistiques JSON sauvegardées dans {DATA_DIR / 'statistics.json'}")
    
    # Affichage du résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES STATISTIQUES")
    print("=" * 70)
    print(df[['title', 'scar_touches', 'hermione_mais', 'dumbledore_interventions', 
             'snape_mysterious', 'questionable_acts']].to_string(index=False))
    
    print("\n" + "=" * 70)
    print("🗣️  PRISES DE PAROLE")
    print("=" * 70)
    print(df[['title', 'Harry', 'Hermione', 'Ron']].to_string(index=False))
    
    # Totaux
    print("\n" + "=" * 70)
    print("🎯 TOTAUX SUR L'ENSEMBLE DE LA SAGA")
    print("=" * 70)
    print(f"Cicatrice de Harry: {df['scar_touches'].sum()}")
    print(f"Hermione dit 'Mais': {df['hermione_mais'].sum()}")
    print(f"Interventions Dumbledore: {df['dumbledore_interventions'].sum()}")
    print(f"Rogue mystérieux: {df['snape_mysterious'].sum()}")
    print(f"Actes répréhensibles: {df['questionable_acts'].sum()}")
    print(f"\nPrises de parole:")
    print(f"  Harry: {df['Harry'].sum()}")
    print(f"  Hermione: {df['Hermione'].sum()}")
    print(f"  Ron: {df['Ron'].sum()}")
    
    # Gagnant bavardage
    total_speeches = {
        'Harry': df['Harry'].sum(),
        'Hermione': df['Hermione'].sum(),
        'Ron': df['Ron'].sum()
    }
    winner = max(total_speeches, key=total_speeches.get)
    print(f"\n🏆 Le plus bavard: {winner} avec {total_speeches[winner]} prises de parole!")
    
    # Créer les visualisations
    create_visualizations(df)
    
    print("\n" + "=" * 70)
    print("✨ ANALYSE TERMINÉE !")
    print("=" * 70)
    print(f"📊 Visualisations disponibles dans: {OUTPUT_DIR}")
    print(f"💾 Données brutes dans: {DATA_DIR}")


if __name__ == "__main__":
    main()
