# SEO Audit Tool

[English](#english) | [Português](#português)

## English

### Overview
A comprehensive SEO audit tool that analyzes websites for search engine optimization factors. Features detailed analysis of technical SEO, content optimization, and performance metrics with actionable recommendations.

### Features
- **Complete SEO Analysis**: Title tags, meta descriptions, headings, content
- **Technical SEO**: HTTPS, canonical URLs, page speed, mobile optimization
- **Content Analysis**: Word count, readability, heading structure
- **Image Optimization**: Alt text analysis and optimization recommendations
- **Performance Metrics**: Page load time, size analysis, response codes
- **SEO Scoring**: Comprehensive scoring system with detailed breakdowns
- **Real-time Audit**: Instant website analysis with visual reports

### Technologies Used
- **Python Flask**: Backend web framework
- **BeautifulSoup**: HTML parsing and analysis
- **Requests**: HTTP client for website fetching
- **Modern Frontend**: Responsive HTML/CSS/JavaScript interface

### Installation

1. Clone the repository:
```bash
git clone https://github.com/galafis/SEO-Audit-Tool.git
cd SEO-Audit-Tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python seo_audit.py
```

4. Open your browser to `http://localhost:5000`

### Usage

#### Performing an Audit
1. Enter the website URL you want to analyze
2. Click "Start SEO Audit" to begin analysis
3. Review the comprehensive report with scores and recommendations

#### Understanding Scores
- **SEO Score (0-100)**: Overall SEO optimization level
- **Performance Score (0-100)**: Page speed and technical performance

#### Analysis Sections
- **Title & Meta Analysis**: Page titles and meta descriptions
- **Content Analysis**: Content quality, headings, and structure
- **Technical Analysis**: HTTPS, load times, and technical factors

### Key Features

#### SEO Analysis
- Page title optimization (length, presence)
- Meta description analysis
- Heading structure (H1-H6) validation
- Content quality assessment
- Image alt text coverage
- Internal/external link analysis

#### Technical SEO
- HTTPS implementation check
- Canonical URL validation
- Mobile viewport configuration
- Page load time analysis
- Response code verification

#### Performance Metrics
- Page size optimization
- Load time measurement
- Content delivery analysis

### API Endpoints
- `POST /audit` - Perform SEO audit on submitted URL

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Português

### Visão Geral
Uma ferramenta abrangente de auditoria SEO que analisa websites para fatores de otimização para mecanismos de busca. Apresenta análise detalhada de SEO técnico, otimização de conteúdo e métricas de performance com recomendações acionáveis.

### Funcionalidades
- **Análise SEO Completa**: Tags de título, meta descrições, cabeçalhos, conteúdo
- **SEO Técnico**: HTTPS, URLs canônicas, velocidade da página, otimização mobile
- **Análise de Conteúdo**: Contagem de palavras, legibilidade, estrutura de cabeçalhos
- **Otimização de Imagens**: Análise de texto alt e recomendações de otimização
- **Métricas de Performance**: Tempo de carregamento, análise de tamanho, códigos de resposta
- **Pontuação SEO**: Sistema de pontuação abrangente com detalhamentos
- **Auditoria em Tempo Real**: Análise instantânea de websites com relatórios visuais

### Tecnologias Utilizadas
- **Python Flask**: Framework web backend
- **BeautifulSoup**: Parsing e análise de HTML
- **Requests**: Cliente HTTP para busca de websites
- **Frontend Moderno**: Interface responsiva HTML/CSS/JavaScript

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/galafis/SEO-Audit-Tool.git
cd SEO-Audit-Tool
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python seo_audit.py
```

4. Abra seu navegador em `http://localhost:5000`

### Uso

#### Realizando uma Auditoria
1. Digite a URL do website que deseja analisar
2. Clique em "Start SEO Audit" para iniciar a análise
3. Revise o relatório abrangente com pontuações e recomendações

#### Entendendo as Pontuações
- **Pontuação SEO (0-100)**: Nível geral de otimização SEO
- **Pontuação de Performance (0-100)**: Velocidade da página e performance técnica

#### Seções de Análise
- **Análise de Título e Meta**: Títulos de página e meta descrições
- **Análise de Conteúdo**: Qualidade do conteúdo, cabeçalhos e estrutura
- **Análise Técnica**: HTTPS, tempos de carregamento e fatores técnicos

### Funcionalidades Principais

#### Análise SEO
- Otimização de título da página (comprimento, presença)
- Análise de meta descrição
- Validação de estrutura de cabeçalhos (H1-H6)
- Avaliação de qualidade do conteúdo
- Cobertura de texto alt de imagens
- Análise de links internos/externos

#### SEO Técnico
- Verificação de implementação HTTPS
- Validação de URL canônica
- Configuração de viewport mobile
- Análise de tempo de carregamento da página
- Verificação de código de resposta

#### Métricas de Performance
- Otimização de tamanho da página
- Medição de tempo de carregamento
- Análise de entrega de conteúdo

### Endpoints da API
- `POST /audit` - Realizar auditoria SEO na URL submetida

### Contribuindo
1. Faça um fork do repositório
2. Crie uma branch de feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adicionar nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

### Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

