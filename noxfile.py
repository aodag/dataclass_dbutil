import nox


@nox.session(reuse_venv=True)
def test(session):
    session.install("pytest")
    session.install(".")
    session.run("pytest")
