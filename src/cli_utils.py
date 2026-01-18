"""Utilidades para CLI com Rich."""

import logging

from rich.console import Console
from rich.logging import RichHandler
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.theme import Theme

# Tema customizado
custom_theme = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "red bold",
        "success": "green bold",
    }
)

# Console global com tema
console = Console(theme=custom_theme)


# Configurar logging com Rich
def setup_logging(level: str = "INFO"):
    """Configura logging com Rich handler."""
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=console,
                rich_tracebacks=True,
                show_path=False,
            )
        ],
    )
    return logging.getLogger("rich")


# Funções auxiliares
def print_header(title: str, subtitle: str = ""):
    """Exibe um cabeçalho bonito."""
    console.print()
    console.rule(f"[bold cyan]{title}[/bold cyan]")
    if subtitle:
        console.print(f"[dim]{subtitle}[/dim]", justify="center")
    console.print()


def print_success(message: str):
    """Exibe mensagem de sucesso."""
    console.print(f"[success]✓[/success] {message}")


def print_error(message: str):
    """Exibe mensagem de erro."""
    console.print(f"[error]✗[/error] {message}")


def print_warning(message: str):
    """Exibe mensagem de aviso."""
    console.print(f"[warning]⚠[/warning] {message}")


def print_info(message: str):
    """Exibe mensagem informativa."""
    console.print(f"[info](i)[/info] {message}")


def print_markdown(content: str):
    """Renderiza e exibe markdown no terminal."""
    md = Markdown(content)
    console.print(md)


def print_panel(content: str, title: str = "", style: str = "cyan"):
    """Exibe conteúdo em um painel."""
    panel = Panel(content, title=title, border_style=style)
    console.print(panel)


def create_table(title: str, columns: list[str]) -> Table:
    """Cria uma tabela formatada."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    for col in columns:
        table.add_column(col)
    return table


def progress_spinner(description: str = "Processando..."):
    """Cria um spinner de progresso."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    )


# Exemplo de uso
if __name__ == "__main__":
    # Setup logging
    logger = setup_logging()

    # Exemplos
    print_header("Exemplos de CLI com Rich", "Demonstração de funcionalidades")

    print_success("Operação concluída com sucesso!")
    print_error("Erro ao processar arquivo")
    print_warning("Atenção: Esta ação é irreversível")
    print_info("Processando 150 documentos...")

    console.print()

    # Markdown
    print_markdown("""
# Título Principal

Este é um exemplo de **markdown** renderizado no terminal!

- Item 1
- Item 2
- Item 3

```python
def hello():
    print("Hello, World!")
```
    """)

    # Painel
    print_panel(
        "Este é um conteúdo importante\nque merece destaque!", title="Importante", style="yellow"
    )

    # Tabela
    table = create_table("Documentos Processados", ["ID", "Nome", "Status"])
    table.add_row("1", "doc1.pdf", "[green]✓ Sucesso[/green]")
    table.add_row("2", "doc2.pdf", "[yellow]⚠ Pendente[/yellow]")
    table.add_row("3", "doc3.pdf", "[red]✗ Erro[/red]")
    console.print(table)

    # Logs
    logger.info("Este é um log informativo")
    logger.warning("Este é um log de aviso")
    logger.error("Este é um log de erro")
