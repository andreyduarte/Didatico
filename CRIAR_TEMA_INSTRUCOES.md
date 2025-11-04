# Instruções para Criar Tema de Apresentação

## Objetivo
Criar um tema visual único e criativo para o sistema de apresentações, inspirado em um PDF existente. Cada tema deve ter seus próprios layouts exclusivos que reflitam sua identidade visual.

## Estrutura de Temas

### Localização
```
app/templates/themes/
├── default/
│   ├── hero.html
│   ├── two_cols.html
│   ├── split.html
│   ├── gallery.html
│   └── quote.html
├── behaviorist/
│   └── ...
└── [novo-tema]/
    └── ...
```

### CSS do Tema
```
app/static/css/
├── default.css
├── behaviorist.css
└── [novo-tema].css
```

## Filosofia de Design

**Cada tema é único**: Não há layouts "padrão". Cada tema deve criar seus próprios layouts que reflitam sua identidade visual e o estilo do PDF de referência.

**Liberdade criativa**: Invente layouts que façam sentido para o tema. Um tema minimalista pode ter 3 layouts simples, enquanto um tema editorial pode ter 10 layouts complexos.

## Variáveis do Sistema

O sistema fornece estas variáveis para os templates:

### Para layouts de texto
- `{{ title }}` - Título principal
- `{{ text }}` - Conteúdo de texto (use `| safe` para HTML)
- `{{ quote }}` - Citação

### Para layouts de imagem
- `{{ image }}` - URL de uma imagem
- `{{ images }}` - Lista de URLs de imagens

### Uso
```html
<!-- Texto simples -->
<h1>{{ title }}</h1>

<!-- HTML seguro -->
<div>{{ text | safe }}</div>

<!-- Condicional -->
{% if image %}
  <img src="{{ image }}" />
{% endif %}

<!-- Loop -->
{% for url in images %}
  <img src="{{ url }}" />
{% endfor %}
```

## Processo de Criação

### Passo 1: Análise do PDF
Identifique no PDF de referência:
1. **Paleta de cores** (primária, secundária, acentos)
2. **Tipografia** (fontes, tamanhos, pesos)
3. **Espaçamentos** (margens, padding, gaps)
4. **Elementos visuais** (bordas, sombras, gradientes)
5. **Layout patterns** (alinhamentos, proporções)

### Passo 2: Criar Diretório do Tema
```bash
mkdir app/templates/themes/[nome-tema]
mkdir app/static/css/
```

### Passo 3: Criar Layouts Únicos

**Analise o PDF e crie layouts que façam sentido**:

1. **Identifique padrões visuais** no PDF
   - Como os títulos são apresentados?
   - Como imagens e texto se relacionam?
   - Há elementos decorativos únicos?
   - Qual é a hierarquia visual?

2. **Invente nomes descritivos** para seus layouts
   - ❌ Evite: `hero.html`, `two_cols.html`
   - ✅ Prefira: `cover.html`, `statement.html`, `showcase.html`

3. **Crie quantos layouts forem necessários**
   - Mínimo: 3-4 layouts
   - Ideal: 5-8 layouts
   - Cada um com propósito claro

**Exemplos de layouts criativos**:
- `magazine-cover.html` - Capa estilo revista
- `side-note.html` - Texto com nota lateral
- `big-number.html` - Estatística destacada
- `timeline.html` - Linha do tempo
- `comparison.html` - Antes/depois
- `testimonial.html` - Depoimento com foto
- `chapter.html` - Abertura de capítulo
- `full-bleed.html` - Imagem sangrada

**Checklist**:
- [ ] Layouts refletem identidade do PDF
- [ ] Nomes descritivos e únicos
- [ ] Classes CSS prefixadas com tema
- [ ] Variáveis Jinja2 corretas
- [ ] Testado com/sem imagens

### Passo 4: Criar CSS do Tema
Arquivo: `app/static/css/[nome-tema].css`

**Estrutura recomendada**:
```css
/* Variáveis do tema */
:root {
  --tema-primary: #...;
  --tema-secondary: #...;
  --tema-accent: #...;
  --tema-text: #...;
  --tema-bg: #...;
  /* Adicione quantas variáveis precisar */
}

/* Base comum */
.[tema]-slide {
  /* estilos compartilhados */
}

/* Cada layout único */
.[tema]-cover-slide { /* ... */ }
.[tema]-statement-slide { /* ... */ }
.[tema]-showcase-slide { /* ... */ }
.[tema]-big-number-slide { /* ... */ }
/* etc */

/* Responsividade */
@media (max-width: 768px) {
  /* ajustes mobile */
}
```

### Passo 5: Registrar Tema no Sistema
Editar `app/models.py`:
```python
# Adicionar opção de tema
theme = db.Column(db.String(50), default="default")
# Valores possíveis: "default", "behaviorist", "[novo-tema]"
```

## Exemplo Prático

### Tema "Magazine"
Inspirado em revistas editoriais modernas.

**Análise do PDF**:
- Cores: Preto, branco, vermelho vibrante (#e63946)
- Tipografia: Serif para títulos, sans-serif para corpo
- Layout: Assimétrico, ousado, muito contraste
- Elementos: Números grandes, linhas diagonais, fotos sangradas

**Layouts criados**:
1. `cover.html` - Capa com título grande e imagem de fundo
2. `statement.html` - Frase de impacto em tela cheia
3. `feature.html` - Artigo com imagem lateral
4. `pull-quote.html` - Citação destacada com aspas grandes
5. `photo-essay.html` - Grid assimétrico de fotos
6. `chapter.html` - Número grande + título de seção

**cover.html**:
```html
<div class="magazine-cover-slide" style="background-image: url('{{ image }}')">
  <div class="magazine-cover-overlay"></div>
  <div class="magazine-cover-content">
    <span class="magazine-issue-number">01</span>
    <h1 class="magazine-cover-title">{{ title }}</h1>
    <div class="magazine-red-bar"></div>
  </div>
</div>
```

**statement.html**:
```html
<div class="magazine-statement-slide">
  <div class="magazine-statement-number">"</div>
  <h2 class="magazine-statement-text">{{ text | safe }}</h2>
  <div class="magazine-statement-line"></div>
</div>
```

**magazine.css**:
```css
:root {
  --magazine-black: #1a1a1a;
  --magazine-white: #ffffff;
  --magazine-red: #e63946;
  --magazine-gray: #f1f1f1;
}

/* Cover */
.magazine-cover-slide {
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  position: relative;
  display: flex;
  align-items: flex-end;
  padding: 4rem;
}

.magazine-cover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
}

.magazine-cover-content {
  position: relative;
  z-index: 1;
}

.magazine-issue-number {
  font-size: 1rem;
  color: var(--magazine-red);
  font-weight: 700;
  letter-spacing: 0.2em;
}

.magazine-cover-title {
  font-family: 'Playfair Display', serif;
  font-size: 5rem;
  font-weight: 900;
  color: var(--magazine-white);
  line-height: 0.9;
  margin: 1rem 0;
}

.magazine-red-bar {
  width: 100px;
  height: 6px;
  background: var(--magazine-red);
  transform: skewX(-10deg);
}

/* Statement */
.magazine-statement-slide {
  background: var(--magazine-black);
  color: var(--magazine-white);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 4rem;
  position: relative;
}

.magazine-statement-number {
  font-size: 15rem;
  font-family: 'Playfair Display', serif;
  color: var(--magazine-red);
  opacity: 0.3;
  position: absolute;
  top: -2rem;
  left: 2rem;
  line-height: 1;
}

.magazine-statement-text {
  font-family: 'Playfair Display', serif;
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.2;
  max-width: 800px;
  position: relative;
  z-index: 1;
}

.magazine-statement-line {
  width: 200px;
  height: 3px;
  background: var(--magazine-red);
  margin-top: 2rem;
  transform: skewX(-10deg);
}
```

## Diretrizes de Design

### Cores
- Use variáveis CSS para fácil manutenção
- Garanta contraste adequado (WCAG AA)
- Teste em modo claro e escuro

### Tipografia
- Tamanhos responsivos com `clamp()`
- Hierarquia clara (h1 > h2 > p)
- Line-height adequado (1.5-1.8 para texto)

### Imagens
- Sempre use `max-width: 100%`
- Border-radius consistente
- Sombras sutis para profundidade

### Responsividade
- Mobile-first approach
- Breakpoints: 576px, 768px, 992px, 1200px
- Teste em diferentes tamanhos

### Performance
- CSS minificado em produção
- Evite seletores complexos
- Use transform/opacity para animações

## Validação

### Checklist Final
- [ ] Mínimo 3-4 layouts únicos criados
- [ ] Layouts refletem identidade do PDF
- [ ] Nomes descritivos (não genéricos)
- [ ] CSS do tema criado
- [ ] Variáveis Jinja2 corretas
- [ ] Testado com conteúdo real
- [ ] Testado sem imagens
- [ ] Responsivo em mobile
- [ ] Cores acessíveis (contraste)
- [ ] Sem erros no console
- [ ] Preview nas thumbnails funciona

## Prompt para LLM

```
Crie um tema único chamado "[nome]" inspirado no PDF anexo.

**IMPORTANTE**: Não use layouts genéricos. Crie layouts exclusivos que reflitam a identidade visual do PDF.

### Passo 1: Análise Profunda
Analise o PDF e documente:
1. **Identidade visual**: Qual é o "feeling" do design?
2. **Paleta de cores**: Primária, secundária, acentos (códigos hex)
3. **Tipografia**: Fontes, tamanhos, pesos, hierarquia
4. **Padrões de layout**: Como elementos se organizam?
5. **Elementos únicos**: Decorações, formas, texturas
6. **Uso de imagens**: Posição, tratamento, proporções

### Passo 2: Inventar Layouts Únicos
Crie 5-8 layouts que façam sentido para este tema específico.

**Dê nomes descritivos** (não use hero, two_cols, etc):
- Exemplo tema Magazine: cover, statement, feature, pull-quote, photo-essay
- Exemplo tema Tech: terminal, code-block, diagram, api-card, dashboard
- Exemplo tema Vintage: postcard, typewriter, polaroid, stamp, letter

Para cada layout:
1. Nome do arquivo (ex: `cover.html`)
2. Propósito (ex: "Capa com título dramático")
3. Variáveis usadas (title, text, image, etc)
4. HTML completo com classes prefixadas
5. CSS específico

### Passo 3: CSS Completo
Crie `[nome].css` com:
- Variáveis CSS para todas as cores
- Estilos para cada layout único
- Elementos decorativos característicos
- Responsividade mobile
- Transições e animações sutis

### Passo 4: Documentação
Liste todos os layouts criados com:
- Nome do arquivo
- Quando usar
- Variáveis necessárias
- Screenshot ou descrição visual

**Lembre-se**: Cada tema deve ser único e memorável!
```

## Inspiração de Temas

### Exemplos de identidades únicas:

**Tema "Brutalist"**
- Layouts: `manifesto`, `raw-text`, `grid-chaos`, `mono-image`
- Estilo: Tipografia pesada, sem imagens, preto/branco

**Tema "Swiss"**
- Layouts: `grid-system`, `helvetica-hero`, `photo-grid`, `data-viz`
- Estilo: Grid rígido, Helvetica, cores primárias

**Tema "Vaporwave"**
- Layouts: `glitch-title`, `neon-quote`, `retro-grid`, `aesthetic`
- Estilo: Gradientes, neon, elementos 80s/90s

**Tema "Academic"**
- Layouts: `paper-title`, `theorem`, `citation`, `bibliography`, `proof`
- Estilo: Serif clássico, margens largas, numeração

**Tema "Startup"**
- Layouts: `pitch`, `metrics`, `team`, `roadmap`, `cta`
- Estilo: Gradientes modernos, sans-serif, gráficos

## Referências Técnicas

- Temas existentes: `app/templates/themes/`
- CSS: `app/static/css/`
- Engine: `app/services/layout_engine.py`
- Base pública: `app/templates/base_public.html`
