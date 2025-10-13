# 🚀 Quick Start Guide - Le Procès de J.K. Rowling

## ⚡ TL;DR

```bash
# Clone and navigate
cd projects/22-proces-jk-rowling

# Option 1: Docker (Recommended)
docker network create poudlard-network 2>/dev/null || true
docker compose -f docker-compose.snippet.yml up --build

# Option 2: Local Python
pip install -r requirements.txt
cd src && python analyze_corpus.py

# View results
ls -lh output/  # 5 PNG visualizations
ls -lh data/    # CSV and JSON data
```

## 📊 What You Get

### Data Files
- `data/statistics.csv` - Complete statistics in CSV format
- `data/statistics.json` - Complete statistics in JSON format

### Visualizations (300 DPI PNG)
1. `output/statistics_trends.png` - 4 metrics evolution
2. `output/speech_comparison.png` - Harry vs Ron vs Hermione
3. `output/questionable_acts.png` - Criminal acts per book
4. `output/normalized_statistics.png` - Stats per 100 pages
5. `output/heatmap_all_stats.png` - Overview heatmap

## 🎯 Key Statistics

| Metric | Total | Winner |
|--------|-------|--------|
| Harry's Scar | 78 | Book 7 (44) |
| Hermione "Mais" | 0 | N/A (needs work) |
| Dumbledore Interventions | 26 | Book 6 (14) |
| Most Talkative | 326 | Harry 👑 |
| Snape Mysterious | 12 | Book 5 (4) |
| Questionable Acts | 3,400 | Book 7 (893) |

## 📚 Documentation

- `README.md` - Full user guide
- `docs/rendu.md` - Complete methodology report (18 KB)
- `docs/resultats.md` - Detailed findings analysis (7.6 KB)
- `docs/prompts_used.md` - All AI prompts used (7.6 KB)
- `docs/notes.md` - Development notes and lessons (8.3 KB)

## ✅ Tests

```bash
cd tests
bash test_smoke.sh  # All 8 tests should pass ✅
```

## 🐳 Docker Commands

```bash
# Build and run
docker compose -f docker-compose.snippet.yml up --build

# Run in background
docker compose -f docker-compose.snippet.yml up -d

# View logs
docker compose -f docker-compose.snippet.yml logs -f

# Stop
docker compose -f docker-compose.snippet.yml down

# Clean up everything
docker compose -f docker-compose.snippet.yml down -v
rm -rf output/* data/*
```

## 🐍 Python Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis
cd src
python analyze_corpus.py

# Check results
ls -lh ../output/
cat ../data/statistics.csv
```

## 🔍 Troubleshooting

### Issue: "Books not found"
**Solution**: Ensure PDFs are in `../../context/books/`
```bash
ls -lh ../../context/books/*.pdf
```

### Issue: "Module not found"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Docker network error"
**Solution**: Create network manually
```bash
docker network create poudlard-network
```

### Issue: "Permission denied"
**Solution**: Make script executable
```bash
chmod +x tests/test_smoke.sh
```

## 📈 Example Output

```
⚡ LE PROCÈS DE J.K. ROWLING - Analyse Statistique
======================================================================
📖 Extraction de harry-potter-1-lecole-des-sorciers.pdf...
✅ L'École des Sorciers analysé
...
📊 RÉSUMÉ DES STATISTIQUES
======================================================================
🎯 TOTAUX SUR L'ENSEMBLE DE LA SAGA
======================================================================
Cicatrice de Harry: 78
Hermione dit 'Mais': 0
Interventions Dumbledore: 26
Rogue mystérieux: 12
Actes répréhensibles: 3400

🏆 Le plus bavard: Harry avec 326 prises de parole!
✨ ANALYSE TERMINÉE !
```

## 🎓 Next Steps

1. ✅ Run the analysis
2. 📊 Check visualizations in `output/`
3. 📈 Analyze data in `data/`
4. 📖 Read detailed findings in `docs/resultats.md`
5. 🔬 Review methodology in `docs/rendu.md`

## 🆘 Support

- Run smoke tests: `bash tests/test_smoke.sh`
- Check README: `cat README.md`
- View documentation: `ls docs/`
- Open an issue on GitHub

## ⚡ Pro Tips

1. Use Docker for consistent environment
2. Run smoke tests before analyzing
3. Check `docs/resultats.md` for insights
4. Export is automatic (CSV + JSON + PNG)
5. Regenerate anytime - it's reproducible!

---

> *"I solemnly swear that I am up to no good!"* - The Marauder's Map

**Version**: 1.0.0  
**Date**: October 13, 2025  
**Status**: Production Ready ✅
