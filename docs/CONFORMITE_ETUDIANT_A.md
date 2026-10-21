# Verification du TP - Etudiant A

Verification du 21 octobre 2026, d'apres l'enonce court et le tutoriel complet
du TP DevOps 3 : Git Flow, Pull Requests et CI/CD avec GitHub Actions.

Le depot GitHub conserve le nom **shopwatch-lite**, au choix de Hossam.
Le code, les branches et les noms d'artefacts suivent le TP IntelliOps-Lite.

## Perimetre et resultat

La partie Extraction est implementee et testee. Le workflow CD est prepare sur
sa branche. Les fichiers Analyse et Notification, leurs tests, le contrat,
le workflow Python et la demonstration fournie n'ont pas ete modifies.

Le TP complet ne peut pas encore etre declare termine : il reste les revues
croisees, les fusions et les exercices qui dependent du travail de B et C.

| Etape du TP | Etat verifie |
| --- | --- |
| Exercice 1 : depot public et fichiers fournis | Presents et conformes fonctionnellement au tutoriel. |
| Exercice 1 : branche par defaut | `develop`, configuree sur GitHub. |
| Exercice 1 : collaborateurs | Invitations avec acces en ecriture envoyees a `Nouhaila04` et `gouihyamaroua-creator` ; acceptation encore necessaire. |
| Exercice 2 : CI | Job `test`, compilation, unittest, Python 3.12, declencheurs push/PR et tags `v*` conformes. |
| Exercice 2 : protections | `main` et `develop` exigent une PR, une approbation et le check `test`. Regles appliquees aussi a l'administrateur ; force push et suppression interdits. |
| Exercice 2 : essai de push direct | Refus reel `GH006` sur `develop` ; preuve jointe. Aucun commit de cet essai integre a la branche partagee. |
| Exercice 3 : Extraction | Quatre fonctions, 19 tests Extraction, quatre commits de code/tests, puis un commit de changelog. |
| Exercice 3 : PR Extraction | [PR #1](https://github.com/MASS0H/shopwatch-lite/pull/1), vers `develop`, check `test` vert avant ajout de ce bilan. Relecture de B et fusion encore necessaires. |
| Exercice 4.1 : CD | Branche `feature/cd-build`, [PR #2](https://github.com/MASS0H/shopwatch-lite/pull/2). Code conforme au bloc du tutoriel page 14. Check `test` vert ; build et deploy ignores sur une PR, comme prevu. |
| Exercice 6 : recuperation | Suppression, tests rouges, reset, reflog et revert executes dans un clone temporaire autonome. Retour sur `develop` propre ; aucun push. |

## Extraction : correspondance avec les regles

| Fonction | Regles couvertes par les tests |
| --- | --- |
| `masquer_secrets` | Six noms de parametres, casse ignoree, separateurs `=` et `:`, limites espace/`&`/`,`/`;`, plusieurs secrets, conservation du texte ordinaire. |
| `normaliser_log` | Identifiant sur cinq chiffres, timestamp avec `T` et `Z`, composant, source et environnement, type LOG, tous les niveaux, message masque, rejet de moins de cinq champs. |
| `normaliser_scan` | Quatre cles obligatoires, source TRIVY, type VULNERABILITY, date conservee, quatre niveaux en majuscules ou LOW, message exact. |
| `normaliser_pipeline` | Trois cles obligatoires, source CI, date conservee, `failed` sans distinction de casse, niveaux/types attendus, message avec le statut original. |

Chaque evenement respecte le contrat `Evenement` et commence au statut `NEW`.
La revue independante a aussi verifie les combinaisons de separateurs et de
delimiteurs, les champs manquants et la conservation des rapports d'entree.

## Verifications et preuves

Depuis la racine de la branche Extraction :

```powershell
python -m compileall -q src tests
python -m unittest -v
git diff --check
```

Resultat local : **22 tests verts**, dont 19 Extraction et 3 du contrat.
Python local : 3.14. La CI GitHub utilise Python 3.12 sur Ubuntu.

- [Execution GitHub Extraction](https://github.com/MASS0H/shopwatch-lite/actions/runs/39607681174) : job `test` reussi sur le code et le changelog.
- [Execution GitHub CD](https://github.com/MASS0H/shopwatch-lite/actions/runs/39607783955) : job `test` reussi, `build` et `deploy` ignores hors tag.
- Workflow CD valide avec `actionlint` 1.7.12 : aucun diagnostic.
- Archive ZIP construite et integrite verifiee dans une copie temporaire avec
  un fichier VERSION de test. Ce controle ne constitue pas une release ni une
  publication d'artefact sur GitHub.
- [Preuve de refus du push direct](preuves-a/protection.txt).
- [Preuve de l'exercice de recuperation](preuves-a/recuperation.txt).

Le workflow CD est dans `.github/workflows/ci.yml` de **feature/cd-build**.
Il sera visible sur `develop` apres approbation et fusion de la PR #2.
Le fichier `VERSION` et les tags n'ont pas ete crees dans le projet : ils
appartiennent a la preparation de release par C.

Aucun navigateur n'etait accessible a l'outil de capture. Les liens et preuves
textuelles ci-dessus sont disponibles ; les captures demandees dans le TP
restent a prendre dans l'interface GitHub.

## Ecart deja present dans l'historique

Avant cette verification, le commit CI `053c58f` etait deja sur `develop`,
sans PR et sans commit de fusion. La branche `feature/ci` existe encore.
La revue de l'exercice 2 n'a donc pas ete realisee selon le TP. Il y a aussi
quatre commits d'initialisation au lieu des trois montres dans le tutoriel,
avec deux commits `chore: initialisation du depot`.

Ces faits historiques sont conserves : aucune reecriture et aucun force push.
Les protections empechent maintenant de refaire une integration directe.
La PR CD fournit le workflow complet a la revue de B, mais ne remplace pas
retroactivement la PR manquante de l'exercice 2.

## Suite des actions de A, dans l'ordre du TP

1. Faire accepter les invitations. B relit la PR Extraction, laisse au moins
   un commentaire sur une ligne puis approuve. A fusionne uniquement apres
   CI verte, avec **Create a merge commit**, puis supprime la branche fusionnee.
2. Revenir sur `develop` et faire `git pull`. L'ordre de fusion des agents
   reste A, puis B, puis C. A relit la PR Notification de C quand elle existe.
3. Si la CI de B devient rouge pendant l'incident prevu, ouvrir les logs,
   relever le test en echec et creer l'Issue assignee a B avec l'extrait reel.
   Aucun incident ni Issue fictifs n'ont ete crees.
4. Pour CD, faire relire la PR #2 par B, actualiser sa branche avec `develop`
   si necessaire, attendre le check vert puis fusionner avec un commit de fusion.
5. Lorsque C prepare `release/v1.0`, A relit la PR vers `main`. C cree VERSION,
   les tags et les PR de synchronisation. Les vrais jobs build/deploy et les
   artefacts devront alors etre verifies dans Actions.
6. Apres publication de v1.0 seulement, A cree `hotfix/bearer-token` depuis
   `main`, ajoute le test ci-dessous, constate son echec puis le commite.
   B corrige le masquage ; C ouvre la PR ; A la relit apres CI verte.

Test Bearer a ajouter dans `TestExtraction` lors de l'exercice 5 :

```python
def test_bearer(self):
    self.assertEqual(masquer_secrets("Authorization: Bearer eyJ.abc-1"),
                     "Authorization: Bearer [SECRET]")
```

Ce test n'est pas encore active et le correctif Bearer n'a pas ete implemente :
le TP reserve cette correction a B. Ajouter maintenant ce test sur la branche
Extraction rendrait sa CI rouge avant l'etape hotfix.

Avant chaque push : faire `git pull` sur la branche concernee. Ne pas pousser
directement sur `main` ou `develop`, ne pas utiliser `git push --force`, et ne
pas fusionner ses propres PR sans l'approbation demandee par le TP.
