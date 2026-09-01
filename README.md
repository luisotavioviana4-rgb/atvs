Análise de Progresso em Cursos Online (TED 01)

**Nome dos Integrantes:**
* [Luis Otávio Viana dos Santos] - [26.1.18406]
* [Divino Rafael Abade Oliveira] - [26.1.14744]

---

1. Cenário Recebido
O projeto consiste em um sistema de processamento e análise de dados sobre o engajamento e progresso de alunos em uma plataforma de cursos online. 

A aplicação realiza a leitura de dois arquivos no formato CSV (`cursos.csv` e `progresso.csv`), trata inconsistências de dados (duplicidades) e gera um relatório consolidado com relatórios sobre:
- Progresso médio percentual por curso;
- Identificação e ranking de alunos em destaque (taxa de conclusão $\ge 80\%$);
- Análise comparativa e de intersecção entre o público de diferentes cursos.

---

2. Descrição Resumida da Solução
A solução foi desenvolvida utilizando exclusivamente **Python 3** nativo, sem dependência de bibliotecas externas. 

1. **Busca e Resolução de Caminhos (`obter_caminho`):** Mapeia de forma dinâmica o local dos arquivos `.csv` garantindo que o programa execute independentemente do diretório atual de trabalho (buscando em subpastas `dados/` ou no diretório raiz do script).
2. **Carregamento e Limpeza (`carregar_dados` e `remover_duplicidades`):** Lê os arquivos CSV via `csv.DictReader`, mapeia os tipos de dados (strings, inteiros, floats) e elimina registros duplicados através da conversão para estruturas de conjuntos (*sets*).
3. **Análises (`analisar_progresso_medio`, `obter_estudantes_destaque`, `comparar_estudantes_cursos`):**
   - Agrupa os progressos percentuais por curso e calcula a média ponderada simples.
   - Filtra alunos com índice de conclusão superior a 80%.
   - Aplica teoria dos conjuntos para calcular intersecções e exclusividades de estudantes entre cursos específicos (ex: `C01` e `C02`).
4. **Relatório (`exibir_resultados`):** Exibe as métricas tratadas e organizadas no terminal.

---

3. Estruturas de Dados Utilizadas

* **Dicionários (`dict`):** 
  - Usados no carregamento de `cursos` (`id_curso` como chave) para busca em tempo constante $O(1)$.
  - Usados na função `analisar_progresso_medio` para agrupar as listas de percentuais associados a cada curso.
* **Tuplas (`tuple`):** Usadas para representar os registros individuais de progresso como estruturas imutáveis (`id_registro`, `estudante`, `id_curso`, `modulos_concluidos`, `percentual_conclusao`, `nota`). A imutabilidade é requisito obrigatório para permitir a remoção de duplicatas via `set`.
* **Conjuntos (`set`):**
  - **Remoção de Duplicatas:** O método `remover_duplicidades` converte a lista de tuplas em um `set` para eliminar duplicatas em $O(n)$.
  - **Operações de Conjunto:** Utilizados em `comparar_estudantes_cursos` aplicando operadores matemáticos de conjuntos:
    - `&` (Intersecção): Estudantes matriculados em ambos os cursos.
    - `-` (Diferença): Estudantes exclusivos de um curso.
    - `|` (União): Total de estudantes únicos somando os dois cursos.
* **Listas (`list`):** Utilizadas para armazenar a ordenação final das médias e destaques de alunos.

4. Principais Análises Realizadas

* **Tratamento de Duplicatas:** O sistema compara o total de registros lidos do arquivo com a quantidade de itens únicos mantidos após a conversão para `set`, apresentando a métrica exata de dados limpos.
* **Ranking de Progresso Médio:** Agrupamento de registros por curso, cálculo do percentual médio de conclusão e ordenação decrescente ($O(N \log N)$ pelo método `.sort()` / `sorted()`).
* **Filtragem por Desempenho:** Filtro de registros ordenados de forma decrescente pela porcentagem de conclusão para identificar alunos no topo do curso.
* **Análise de Intersecção de Alunos:** Identificação de perfil de matrículas simultâneas via operações de *Set Theory*, permitindo identificar sobreposição de audiência entre cursos selecionados.

---

5. Instruções para Executar o Programa

### Pré-requisitos
* **Python 3.6+** instalado no sistema (não requer bibliotecas de terceiros além das nativas `csv` e `os`).

### Estrutura de Pastas Esperada
Certifique-se de manter os arquivos em uma das estruturas abaixo para que o resolvedor automático de caminhos localize os dados:

```text
meu_projeto/
├── main.py (ou script_principal.py)
└── dados/
    ├── cursos.csv
    └── progresso.csv
