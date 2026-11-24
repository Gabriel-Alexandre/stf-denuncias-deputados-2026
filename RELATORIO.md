# O STF apressou o caso do van Hattem? (relatório, rodada 1, 24/11/2026)

## A pergunta

Canais de direita dizem que o STF está apressando a denúncia contra o deputado Marcel van Hattem (Novo-RS), que é senador eleito, por um discurso na tribuna da Câmara em 14/08/2024 contra o delegado da PF Fábio Shor. A Revista Oeste chamou isso de *"fantasma do impeachment"*. O próprio deputado disse que *"pode se tornar o primeiro deputado brasileiro a ser processado e virar réu no STF por uso da tribuna"* (Gazeta do Povo, 19/11/2026).

São 2 perguntas com resposta no dado: **(1) o caso dele andou mais rápido que o dos outros deputados denunciados por fala?** e **(2) ele seria o primeiro deputado réu por falar dentro da Câmara?**

## O método

1. Juntar os casos de deputado federal denunciado pela PGR por crime contra a honra (calúnia, difamação, injúria) por uma fala, de 2020 a 2026, achados na imprensa e conferidos no portal de processos e na jurisprudência do STF (`dados/casos.csv`, uma captura por data em `dados/capturas/`).
2. Medir, em dias corridos, o tempo da denúncia à decisão de receber (ou não) e, nos casos pendentes, da denúncia a hoje.
3. Validar por outro caminho: as datas do STF relidas do texto das páginas oficiais, sem passar pela planilha (`ferramentas/validacao_independente.py`: **12 de 12** batem).

⚠️ **O limite:** o STF não publica uma lista de denúncias contra parlamentares por fala. Os 7 casos são os que a busca achou em 24/11/2026; a lista não é completa. Dois processos (Nikolas e o "ladrão" do Gilvan) não tiveram o número achado, e as datas deles vêm da imprensa.

## O que o dado mostra

| Deputado | Onde falou | Denúncia | Decisão | Dias da denúncia à decisão |
|---|---|---|---|---:|
| Gilvan da Federal (PL-ES), contra o comandante do Exército | sessão plenária da Câmara e redes | 18/12/2025 | recebida em 20/03/2026, unanimidade (Pet 15178, relator Moraes) | **92** |
| **Marcel van Hattem (Novo-RS)** | tribuna da Câmara | 28/04/2026 | julgamento virtual de 20/11/2026; Dino e Moraes votaram por receber; **Zanin pediu destaque** e o caso vai à sessão presencial, sem data | **206 até começar o julgamento** (pendente) |
| Gustavo Gayer (PL-GO) | post no X | 12/02/2025 | recebida em 28/04/2026, 4 a 0 (Inq 4974, relator Dino) | **440** |
| Gilvan da Federal, "ladrão" | evento sobre armamento | 04/10/2024 | sem decisão pública achada (relator Fux) | **781 até hoje** |
| Nikolas Ferreira (PL-MG) | evento na sede da ONU | 26/07/2024 | sem decisão pública achada (relator Fux) | **851 até hoje** |
| Otoni de Paula (MDB-RJ) | lives | 14/07/2020 | recebida em 29/06/2023, unanimidade (Pet 9007, plenário, relator Nunes Marques) | **1.080** |
| Gilvan da Federal, morte de Lula | sessão de comissão da Câmara | não achada | recebida em 18/08/2026, unanimidade (relatora Cármen Lúcia) | 497 do fato à decisão |

**1. O caso dele foi rápido, mas não o mais rápido.** Até o julgamento começar, foram **206 dias** desde a denúncia. Entre os casos que chegaram a julgamento com a data da denúncia conhecida, só o do Gilvan contra o general foi mais rápido: **85 dias** até começar o julgamento, 2,4 vezes menos. O do Gayer levou 440 dias, o do Otoni, 1.080. E 2 denúncias de 2024, contra o Nikolas e o Gilvan, estão sem decisão pública há mais de 2 anos. Do discurso até hoje, o caso dele soma **832 dias**: os 20 meses entre o inquérito e a denúncia foram da PF e da PGR, não do STF.

**2. Ele não seria o primeiro deputado réu por falar dentro da Câmara.** Em 2026 a 1ª Turma já recebeu 2 denúncias contra o Gilvan da Federal por falas dentro da Câmara: o discurso em sessão plenária de novembro de 2025 contra o comandante do Exército (março de 2026) e a fala na Comissão de Segurança Pública de 08/04/2025 (agosto de 2026). Nos 2 casos o STF afastou a imunidade parlamentar. A denúncia contra o van Hattem também cita publicações nas redes sociais, além do discurso.

**3. Toda denúncia desse tipo que chegou a julgamento foi aceita.** Nos casos achados, **4 de 4** foram recebidas, todas por unanimidade.

## O que fica de fora da conta

- **A motivação dos ministros.** O tempo e o placar se medem; a intenção não, e o relatório não afirma intenção.
- **O conflito de interesse que a imprensa aponta:** o delegado Fábio Shor trabalha no gabinete do ministro Alexandre de Moraes desde março de 2026 (Gazeta do Povo e Revista Oeste), e Moraes votou para receber a denúncia. É um fato com 2 fontes; o que ele significa é opinião.
- **O mérito:** receber a denúncia não é condenação.

## A resposta curta

O dado não mostra pressa fora do comum: o caso dele levou 206 dias da denúncia ao julgamento, mais que o do Gilvan (85) e menos que o do Gayer (440) e o do Otoni (1.080). Ele também não seria o primeiro deputado réu por falar na Câmara, porque o Gilvan virou réu 2 vezes em 2026 por isso. O que o dado mostra é outra coisa: nos 4 casos que chegaram a julgamento, o STF aceitou a denúncia, sempre por unanimidade.
