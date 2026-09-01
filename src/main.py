import csv
import os

def obter_caminho(nome_arquivo):
    dir_script = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_script)
    
    caminhos_possiveis = [
        os.path.join(dir_raiz, 'dados', nome_arquivo),
        os.path.join(dir_raiz, nome_arquivo),
        os.path.join(dir_script, 'dados', nome_arquivo),
        os.path.join(dir_script, nome_arquivo),
        os.path.join('dados', nome_arquivo),
        nome_arquivo
    ]
    
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            return caminho
            
    return os.path.join(dir_raiz, 'dados', nome_arquivo)

def carregar_dados():
    caminho_cursos = obter_caminho('cursos.csv')
    caminho_progresso = obter_caminho('progresso.csv')
    
    with open(caminho_cursos, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        cursos = {
            linha['id_curso']: {
                'nome': linha['nome'],
                'categoria': linha['categoria']
            }
            for linha in reader
        }

    registros_brutos = []
    with open(caminho_progresso, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for linha in reader:
            item = (
                linha['id_registro'],
                linha['estudante'],
                linha['id_curso'],
                int(linha['modulos_concluidos']),
                int(linha['percentual_conclusao']),
                float(linha['nota'])
            )
            registros_brutos.append(item)
            
    return cursos, registros_brutos

def remover_duplicidades(registros):
    return list(set(registros))

def analisar_progresso_medio(registros, cursos):
    agrupado = {}
    for reg in registros:
        id_c = reg[2]
        perc = reg[4]
        if id_c not in agrupado:
            agrupado[id_c] = []
        agrupado[id_c].append(perc)
        
    medias = {
        cursos[id_c]['nome']: sum(percs) / len(percs)
        for id_c, percs in agrupado.items()
    }
    
    return sorted(medias.items(), key=lambda x: x[1], reverse=True)

def obter_estudantes_destaque(registros, limite=80):
    destaques = [
        (reg[1], reg[2], reg[4], reg[5])
        for reg in registros
        if reg[4] >= limite
    ]
    return sorted(destaques, key=lambda x: x[2], reverse=True)

def comparar_estudantes_cursos(registros, cursos, id_c1='C01', id_c2='C02'):
    estudantes_c1 = {reg[1] for reg in registros if reg[2] == id_c1}
    estudantes_c2 = {reg[1] for reg in registros if reg[2] == id_c2}
    
    comum = estudantes_c1 & estudantes_c2
    apenas_c1 = estudantes_c1 - estudantes_c2
    apenas_c2 = estudantes_c2 - estudantes_c1
    total_unico = estudantes_c1 | estudantes_c2
    
    nome_c1 = cursos[id_c1]['nome']
    nome_c2 = cursos[id_c2]['nome']
    
    return {
        'curso1': nome_c1,
        'curso2': nome_c2,
        'comum': comum,
        'apenas_c1': apenas_c1,
        'apenas_c2': apenas_c2,
        'total_unico': total_unico
    }

def formatar_relatorio(destaques):
    return [
        f"{est} | Curso {cid} | Conclusão: {perc}% | Nota: {nota}"
        for est, cid, perc, nota in destaques
    ]

def exibir_resultados(cursos, brutos, unicos, ranking, destaques, comparacao):
    print("=" * 60)
    print("      ANALISE DE PROGRESSO EM CURSOS ONLINE (TED 01)")
    print("=" * 60)
    print(f"Total de registros lidos: {len(brutos)}")
    print(f"Registros apos remocao de duplicatas: {len(unicos)}")
    print(f"Duplicatas removidas: {len(brutos) - len(unicos)}")
    print("-" * 60)
    
    print("\n1. CURSOS COM MAIOR PROGRESSO MEDIO:")
    print(f"{'Posicao':<10}{'Curso':<25}{'Progresso Medio':<15}")
    print("-" * 50)
    for pos, (nome_curso, media) in enumerate(ranking, 1):
        print(f"{pos:<10}{nome_curso:<25}{media:.2f}%")
        
    print("\n2. ESTUDANTES COM CONCLUSAO ELEVADA (>= 80%):")
    print(f"Total de estudantes em destaque: {len(destaques)}")
    print(f"{'Estudante':<18}{'Curso ID':<12}{'Conclusao':<12}{'Nota':<10}")
    print("-" * 50)
    for est, cid, perc, nota in destaques[:10]:
        print(f"{est:<18}{cid:<12}{perc}%        {nota:.1f}")
    if len(destaques) > 10:
        print(f"... e mais {len(destaques) - 10} estudantes.")
        
    print("\n3. COMPARACAO DE ESTUDANTES ENTRE CURSOS:")
    print(f"Curso 1: {comparacao['curso1']}")
    print(f"Curso 2: {comparacao['curso2']}")
    print("-" * 50)
    print(f"Estudantes matriculados em ambos: {len(comparacao['comum'])}")
    print(f"Estudantes exclusivos do {comparacao['curso1']}: {len(comparacao['apenas_c1'])}")
    print(f"Estudantes exclusivos do {comparacao['curso2']}: {len(comparacao['apenas_c2'])}")
    print(f"Total de estudantes unicos nos dois cursos: {len(comparacao['total_unico'])}")
    print("=" * 60)

def main():
    cursos, brutos = carregar_dados()
    unicos = remover_duplicidades(brutos)
    
    ranking = analisar_progresso_medio(unicos, cursos)
    destaques = obter_estudantes_destaque(unicos, 80)
    comparacao = comparar_estudantes_cursos(unicos, cursos, 'C01', 'C02')
    
    exibir_resultados(cursos, brutos, unicos, ranking, destaques, comparacao)

if __name__ == '__main__':
    main()