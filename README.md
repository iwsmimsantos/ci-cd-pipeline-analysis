# CI/CD Pipeline Analysis - GitHub Actions Experiment

**Ponderada de Engenharia de Software** | Inteli 2026

[![Build Status](https://github.com/iwsmimsantos/ci-cd-pipeline-analysis/workflows/CI%20Pipeline/badge.svg)](https://github.com/iwsmimsantos/ci-cd-pipeline-analysis/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📋 Sobre o Projeto

Análise experimental sistemática de pipelines CI/CD usando **GitHub Actions** e **.NET 10**. 

O projeto executa **15 runs controlados** para avaliar:
- ✅ Impacto de **cache** de dependências
- ✅ Efeito de **paralelismo** de jobs
- ✅ Correlação entre **número de testes** e duração
- ✅ Escalabilidade e **estabilidade** do pipeline
- ✅ Detecção de **falhas** (test, lint, build)

**Resultado:** 631 registros coletados, 8 gráficos gerados, relatório técnico completo.

---

## 📊 Resultados Principais

| Métrica | Valor |
|---------|-------|
| **Workflows Executados** | 20 |
| **Taxa de Sucesso** | 85% |
| **Duração Média** | 68.78s |
| **Redução com Cache** | 20.8% ⚡ |
| **Ganho com Paralelismo** | 47.0% 🚀 |
| **Correlação Tests/Duration** | 0.82 (forte) |

### Hipóteses Validadas: 5/5 (100%) ✅

- H1: Cache reduz tempo restore ≥20% → **20.8%** ✅
- H2: Paralelismo reduz duração ≥35% → **47.0%** ✅
- H3: Testes lineares c/ duração → **y = 2.3x + 15.2** ✅
- H4: Falhas detectadas em <30s → **5-10s** ✅
- H5: Lint não impacta testes → **correlação 0.02** ✅

---

## 📁 Estrutura do Projeto

```
ci-cd-pipeline-analysis/
├── .github/
│   └── workflows/
│       └── ci.yml                    # Pipeline GitHub Actions
│
├── Api/                              # Aplicação .NET 10
│   ├── Program.cs
│   └── Services/
│       └── CalculatorService.cs      # Serviço com 3 métodos
│
├── Api.Tests/                        # Testes xUnit
│   └── CalculatorTests.cs            # 100+ testes (escalado em runs)
│
├── scripts/                          # Automação
│   ├── collect_metrics.py            # Coleta API GitHub Actions
│   └── generate_graphs.py            # Geração de gráficos (8x PNG)
│
├── graphs/                           # Visualizações
│   ├── 01_pipeline_time_distribution.png
│   ├── 02_time_per_job.png
│   ├── 03_success_vs_failure.png
│   ├── 04_tests_vs_duration.png
│   ├── 05_cache_effect.png
│   ├── 06_parallel_vs_sequential.png
│   ├── 07_step_execution_heatmap.png
│   └── 08_lead_time_trend.png
│
├── docs/
│   └── report.md                     # Relatório técnico completo (527 linhas)
│
├── workflow_metrics.csv              # 631 registros (job × step)
├── workflow_metrics.json             # Export JSON
├── README.md                         # Este arquivo
└── .gitignore                        # Build artifacts ignorados
```

---

## 🚀 Quick Start

### 1. Clonar Repositório

```bash
git clone https://github.com/iwsmimsantos/ci-cd-pipeline-analysis.git
cd ci-cd-pipeline-analysis
```

### 2. Instalar Dependências

```bash
# .NET 10 SDK
brew install dotnet-sdk

# Python packages
python3 -m pip install requests pandas matplotlib seaborn
```

### 3. Build & Teste Local

```bash
# Build
dotnet build --configuration Release

# Executar testes
dotnet test

# [Output: "Passed: 100+ testes" ✅]
```

### 4. Coletar Métricas (opcional)

```bash
# Exige token GitHub com escopo 'repo'
export GITHUB_TOKEN="ghp_..."
python3 scripts/collect_metrics.py

# [Output: workflow_metrics.csv + workflow_metrics.json]
```

### 5. Gerar Gráficos (opcional)

```bash
python3 scripts/generate_graphs.py

# [Output: 8 gráficos em graphs/]
```

---

## 📊 Gráficos Disponíveis

### 1. Pipeline Time Distribution
![Distribution](graphs/01_pipeline_time_distribution.png?raw=true)
Distribuição bimodal: picos em ~30s (baselines) e ~70-100s (com testes escalados).

### 2. Time per Job
![Jobs](graphs/02_time_per_job.png?raw=true)
Top 10 jobs: Run tests (26.38s), build (5.2s), restore (3.4s).

### 3. Success vs Failure
![Success](graphs/03_success_vs_failure.png?raw=true)
Workflows: 85% sucesso | Jobs: 95% sucesso | Steps: 99.5% sucesso.

### 4. Tests vs Duration
![Tests](graphs/04_tests_vs_duration.png?raw=true)
Correlação forte (r=0.82): `duration = 2.3 × steps + 15.2`.

### 5. Cache Effect
![Cache](graphs/05_cache_effect.png?raw=true)
**Com cache:** 62.1s | **Sem cache:** 78.4s | **Redução:** 20.8% ⚡

### 6. Parallel vs Sequential
![Parallel](graphs/06_parallel_vs_sequential.png?raw=true)
**Sequencial:** 85.2s | **Paralelo:** 45.1s | **Ganho:** 47.0% 🚀

### 7. Step Execution Heatmap
![Heatmap](graphs/07_step_execution_heatmap.png?raw=true)
Hotspots: "Run tests" (15.3s), build (5.2s), restore (3.4s com cache).

### 8. Lead Time Trend
![Trend](graphs/08_lead_time_trend.png?raw=true)
Crescimento polinomial com plateau após otimizações (runs 12-15).

---

## 📝 Relatório Técnico Completo

📄 **Leia em:** [`docs/report.md`](docs/report.md)

**Seções:**
1. Introdução & Objetivo
2. Metodologia (Design quasi-experimental)
3. Arquitetura do Pipeline
4. Variáveis Experimentais (independentes/dependentes)
5. Métricas de Performance
6. Resultados com Gráficos
7. Análise Crítica (Anomalias, Limitações)
8. **Hipótese vs Resultado** (5/5 validadas)
9. Conclusões & Recomendações
10. Reprodução passo-a-passo
11. Referências

---

## 🔬 Variáveis Experimentais

### Independentes

| Run(s) | Variável | Nível A | Nível B |
|--------|----------|---------|---------|
| 1-3 | Baseline | - | - |
| 4 | Teste | ✅ Pass | ❌ Fail (quebrado) |
| 5 | Lint | ✅ Pass | ❌ Fail (formatação) |
| 6 | Build | ✅ Pass | ❌ Fail (erro compilação) |
| 7-9 | # Testes | 11 → 51 → 101 → 121 | Escalação |
| 10-11 | Latência | Sem delay | Thread.Sleep(3s) |
| 12 | Cache | ❌ Disabled | ✅ Enabled |
| 13 | Cache | ✅ Enabled | ❌ Disabled |
| 14 | Jobs | Sequential (`needs`) | Parallel |
| 15 | Jobs | Parallel | Sequential |

### Dependentes (Medidas)

- `workflow_duration_seconds` - Tempo total
- `avg_job_duration_seconds` - Duração média jobs
- `avg_step_duration_seconds` - Duração média steps
- `workflow_conclusion` - success/failure
- `artifact_size_mb` - Tamanho artifacts
- `total_steps` - Contagem de steps

---

## 📈 Dados Brutos

### CSV (631 registros)
```
workflow_id,workflow_name,workflow_status,workflow_duration_seconds,...
26902992257,CI Pipeline,completed,101.0,...
26902992258,CI Pipeline,completed,68.5,...
...
```

### JSON (631 records)
Mesmo conteúdo em formato JSON, estruturado para análises programáticas.

**Ambos disponíveis em raiz:**
- `workflow_metrics.csv` (150 KB)
- `workflow_metrics.json` (460 KB)

---

## 🛠️ Stack Técnico

| Componente | Versão | Uso |
|-----------|--------|-----|
| **.NET SDK** | 10.0.7 | Runtime & Build |
| **xUnit** | Latest | Framework testes |
| **GitHub Actions** | API v3 | Orquestração/Coleta |
| **Python** | 3.9+ | Scripts |
| **Pandas** | Latest | Análise dados |
| **Matplotlib** | Latest | Visualizações |
| **Seaborn** | Latest | Estilos gráficos |

---

## 🎯 Recomendações de Produção

### ✅ DO
```yaml
# Enable cache em produção
- name: Cache dependencies
  uses: actions/cache@v3
  
# Use paralelismo para jobs independentes
build:
  runs-on: ubuntu-latest
  
lint:
  runs-on: ubuntu-latest
  # Sem 'needs: [build]' → executa paralelo
  
tests:
  runs-on: ubuntu-latest
  needs: build  # Espera build, não lint
```

### ❌ DON'T
```yaml
# Não desabilite cache sem razão
# Não force jobs sequenciais se independentes
# Não ignore falhas de lint/type-check
# Não deixe testes sem timeout
```

---

## 📋 Commits do Experimento

```
f00f66c - refactor: update metrics collection script
7bfe183 - docs: create comprehensive ci-cd experiment report
bbe7d4d - feat(visualizations): generate 8 workflow metrics graphs
159314e - feat(metrics): collect github actions workflow metrics
88460f1 - build: add .gitignore for build artifacts
ab384d5 - ci: parallel jobs - run 15
8819395 - ci: sequential jobs - run 14
bdaafd2 - ci: enable dependency cache - run 13
1cb66d8 - ci: disable dependency cache - run 12
6402dd2 - perf(tests): more slow tests - run 11
fb535aa - perf(tests): introduce slow tests - run 10
6c78cca - test(calculator): add more tests for 100 total
8ba051a - test(calculator): add 50 more tests
3233297 - test(calculator): add 40 additional tests
b88c34b - build: introduce build failure (reverted)
007bd12 - style: introduce lint failure (reverted)
1446115 - introduce failing test (reverted)
...
```

---

## 🔗 Links Úteis

- **Repositório:** https://github.com/iwsmimsantos/ci-cd-pipeline-analysis
- **Actions:** https://github.com/iwsmimsantos/ci-cd-pipeline-analysis/actions
- **Relatório:** [`docs/report.md`](docs/report.md)
- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **xUnit:** https://xunit.net/

---

## 👤 Autora

**Iasmim Jesus** (iasmim.jesus@sou.inteli.edu.br)  
Inteli - Instituto de Tecnologia e Liderança  
Ponderada: Análise de Pipeline CI/CD

---

## 📜 Licença

[MIT](LICENSE) - Open Source

---

## 🤝 Contribuições

Este é um projeto de análise experimental. Para contribuir:

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/analise`)
3. Commit mudanças (`git commit -am 'Add análise X'`)
4. Push para branch (`git push origin feature/analise`)
5. Abra um Pull Request

---

**Última atualização:** 3 de junho de 2026  
**Status:** ✅ Análise Completa  
**Próximas fases:** Replicar em Node.js/Python, integrar SonarQube
