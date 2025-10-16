# Données d'entrée

Placez vos fichiers PDF de plans d'étage dans ce répertoire.

## Format attendu

- **Type** : PDF vectoriel (préférable) ou raster haute résolution
- **Échelle** : Échelle lisible dans le cartouche (ex: 1:150, 1:100)
- **Qualité** : Traits nets et contrastés
- **Pages** : Une page par étage ou plusieurs étages sur une même page

## Exemple

```
data/input/
├── PRIVE_Plans_THALIE_Montpellier.pdf
├── plan_rdc.pdf
└── plan_etage1.pdf
```

## Note de confidentialité

Les fichiers dont le nom commence par `PRIVE_` sont automatiquement ignorés par Git (voir `.gitignore`).

Pour des données sensibles, utilisez ce préfixe ou ajoutez les patterns au `.gitignore`.
