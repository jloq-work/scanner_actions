# Scanner — Actions françaises

Scanner simple et robuste d’actions françaises construit en Python.

L’objectif du projet est **pédagogique et pratique** :

* montrer une architecture propre de pipeline data / calculs / signaux
* proposer un scanner simple, explicable et testable
* rester compatible avec des données **gratuites** (Yahoo Finance)

Ce projet **ne constitue pas un conseil en investissement**.

---

## Idée générale

Le scanner cherche à détecter des **situations de transition** :

> Actions françaises qui ont été **en baisse ou en range à moyen terme**,
> mais qui montrent une **reprise récente** accompagnée d’une **accélération des volumes**.

C’est typiquement le type de configuration exploitable sur les actions côtées en Service de réglement différé (SRD) :

* timing court / moyen terme
* besoin de liquidité
* importance du volume

---

## Architecture du projet

```text
src/
├── data/
│   ├── loaders.py        # Chargement des données (via Yahoo Finance)
│   ├── symbols.py        # Liste des symboles des actions françaises
│   └── resample.py       # Daily → Weekly
│
├── features/
│   ├── returns.py        # Rendements glissants
│   └── volume.py         # Moyennes et ratios de volume
│
├── signals/
│   ├── trend.py          # Classification de la tendance
│   └── momentum.py       # Momentum court terme
│
├── scanner/
│   └── run.py            # Orchestration complète du scanner
│
└── tests/
    ├── data/
    ├── features/
    ├── signals/
    └── scanner/
```

### Séparation claire des responsabilités

* **data/** : accès aux données et transformations temporelles
* **features/** : calculs numériques (retours, volumes)
* **signals/** : logique métier (trend, momentum)
* **scanner/** : règles finales de sélection

Cette séparation permet :

* des tests unitaires ciblés
* des tests d’intégration robustes
* une évolution facile des règles

---

## Données utilisées

* **Source** : Yahoo Finance (via `yfinance`)
* **Fréquence principale** : Daily
* **Historique** : 3 ans
* **Univers** : Actions françaises (exemples)

Les données sont **nettoyées et typées explicitement** afin d’éviter les erreurs liées aux types (`str` / `float`).

---

## Statistiques calculées

### Rendements glissants

Calculés sur le prix de clôture (`close`) :

* `ret_5`   → momentum très court terme (5j)
* `ret_21`  → ~1 mois (21j)
* `ret_63`  → ~3 mois (63j)

Formule :

```text
ret_n = close / close.shift(n) - 1
```

---

### Volumes

* Moyennes glissantes de volume
* Ratio de volume court / long terme

Par défaut :

* court terme : 5 jours
* long terme : 20 jours

```text
vol_ratio = mean(volume, 5) / mean(volume, 20)
```

Les volumes sont systématiquement convertis en numérique (`pd.to_numeric`).

---

## Signaux métier

### Trend (tendance moyen terme)

Classification basée sur les rendements :

* **down**   : tendance baissière
* **stable** : absence de direction claire (range)

Le scanner actions **ne retient que** :

```text
down ou stable
```

Objectif : éviter les titres déjà très haussiers.

---

### Momentum (reprise court terme)

Signal booléen simple :

```text
momentum = ret_5 > 0
```

Indique une reprise récente.

---

### Volume (confirmation)

Filtre final :

```text
vol_ratio_5_20 >= seuil
```

Par défaut :

```text
seuil = 1.15
```

La reprise doit être **accompagnée de volumes**.

---

## Tests

Le projet contient :

* **tests unitaires**

  * features (returns, volume)
  * signaux (trend, momentum)

* **tests d’intégration**

  * scanner complet (`scan_symbol`)
  * données et signaux factices

Les tests :

* n’utilisent **aucun appel réseau**
* sont déterministes
* valident l’orchestration globale

---

## Exécution (lancer deux fois à l'initialisation)

```bash
python -m src.scanner.run
```

Sortie typique :

```text
symbol   trend    ret_5   ret_21   ret_63   volume_ratio
AIR.PA   down     0.032  -0.081   -0.120     1.34
```

Ou :

```text
No SRD opportunities detected.
```

Ce comportement est **normal** : le scanner vise des configurations rares.

---

## Avertissement

Ce projet est fourni à des fins **éducatives**.
Il ne constitue **en aucun cas** :

* un conseil en investissement
* une recommandation d’achat ou de vente

L’utilisation en conditions réelles se fait **sous la seule responsabilité de l’utilisateur**.


