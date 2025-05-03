{
  mkShell,
  uv,
  python3,
}:
mkShell {
  env = {
    UV_PYTHON_PREFERENCES = "system";
  };
  shellHook = ''
    source .venv/bin/activate
  '';
  nativeBuildInputs = [
    uv
    python3
  ];
}
