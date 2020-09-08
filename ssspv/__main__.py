import typer

app = typer.Typer()


@app.command()
def create_wallet():
    # TODO: wallet -> file
    typer.echo('Creating a wallet...')


@app.command()
def run_node(port: int = 8000):
    # TODO: RPC server
    typer.echo(f'Running server on {port}!')


app()
